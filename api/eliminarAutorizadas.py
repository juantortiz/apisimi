import mysql.connector
import sys
import csv
import requests
import dateparser

import ConfigParser
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta


instance = dbhost = dbusername = dbpassword = username = password = database = base_url =  ''
counterOk = 0
counterNOK = 0
counter = 0
counterTo = 0

def init_config(configFile):
    config = ConfigParser.ConfigParser()
    config.read(configFile)
    global dbusername
    global dbpassword
    global dbhost
    global username
    global password
    global database
    global base_url
    global instance
    dbusername = config.get('DB','dbusername')
    dbpassword = config.get('DB','dbpassword')
    database = config.get('DB','db')
    dbhost = config.get('DB','dbhost')
    username = config.get('JBPM','username')
    password = config.get('JBPM','password')
    base_url = config.get('JBPM','url')
    base_url = base_url[:base_url.find(base_url.split('/')[6])]



def eliminar(simis):
    print "Abortando simi"
    for simi in simis:
        url = base_url + instance + '/process/instance/'+str(simi)+'/abort'
        r = requests.post(url,auth=HTTPBasicAuth(username, password))
        if r.status_code == 200:
            global counterOk
            counterOk = counterOk + 1
            print('La simi con proceso ' + str(simi) + ' Fue abortada exitosamente')
        else:
            global counterNOK
            counterNOK = counterNOK + 1
            print >>sys.stderr, 'ERROR \t La simi con proceso ' + str(simi) + ' No pudo ser abortada. Error: ' + str(r.status_code)



def esta_instanciada(simi):
    query = ("select pil.processInstanceId "
                "FROM ProcessInstanceLog as pil "
                "join VariableInstanceLog as vil on vil.processinstanceid = pil.processinstanceid and vil.variableId = 'djai_id_simi'"
                "where vil.value='"+simi+"' and pil.status in (0,1);")
    response = doQuery(query)
    aux = [ a[0] for a in response ]
    return aux

def simis_con_fecha(simi):
    query = ("SELECT pil.processInstanceId, vil.value FROM ProcessInstanceLog as pil "
    "join VariableInstanceLog as vil on pil.processInstanceId = vil.processInstanceId and vil.variableId ='djai_fech_env_afip' "
    "join VariableInstanceLog as vil2 on pil.processInstanceId = vil2.processInstanceId and vil2.variableId = 'djai_id_simi' "
    "where vil2.value = '"+simi+"' and pil.status in (0,1);")
    response = doQuery(query)
    simisViejas = getViejas(response)
    return simisViejas


def getViejas(simis):
    viejas = []
    fechaHoy = datetime.now()
    N = 180
    fechaPasado = fechaHoy - timedelta(days = N)
    for simi in simis:
        if simi[1] != '':
            fechaSimi = dateparser.parse(simi[1])
            if fechaSimi < fechaPasado:
                viejas.append(int(simi[0]))
    return viejas




def esta_aprobada(estado):
    return estado == 'A'

def process_file(filename):
    reader = csv.reader(open(filename),delimiter=';')
    row1 = next(reader)
    for row in reader:
        global counter
        global counterTo
        counter = counter + 1

        print "Simi: \t"+row[0],
        simis = necesitan_abortar(row)
        if len(simis) > 0:
            print "\t Necesita ser abortada"
            counterTo = counterTo + 1
            eliminar(simis)
        else:
            print "\t No necesita ser abortada",
        print

def simis_por_estado(row):
    if esta_aprobada(row[1]):
        simis = esta_instanciada(row[0])
        return simis
    else:
        simis = cambio_estado(row[0],row[1])
        return simis


def doQuery(query):
    cnx = mysql.connector.connect(user=dbusername,password=dbpassword,database=database, host=dbhost )
    cursor = cnx.cursor(buffered=True)
    cursor.execute(query)
    response = cursor.fetchall()
    cursor.close()
    cnx.close()
    return response


def cambio_estado(simi,estado):
    simis = []
    query = ("SELECT pil.processInstanceId, vil.value FROM ProcessInstanceLog as pil "
    "join VariableInstanceLog as vil on pil.processInstanceId = vil.processInstanceId and vil.variableId ='djai_estado' "
    "join VariableInstanceLog as vil2 on pil.processInstanceId = vil2.processInstanceId and vil2.variableId = 'djai_id_simi' "
    "where vil2.value = '"+simi+"' and pil.status in (0,1);")
    response = doQuery(query)
    for simi in response:
        djai_estado = simi[1]
        if estado == 'O'and djai_estado == 'O' or djai_estado == 'P' or djai_estado == 'M' or djai_estado == ' ':
            simis.append(simi[0])
        if estado == 'M'and djai_estado == 'O' or djai_estado == 'P' or djai_estado == 'M' or djai_estado == ' ':
            simis.append(simi[0])
    return simis




def necesitan_abortar(row):
    # Checkeo viejas ( 180 dias )
    simis = simis_con_fecha(row[0])
    if len(simis) > 0:
        return simis
    # Checkeo por estado
    simis = simis_por_estado(row)
    if len(simis) > 0:
        return simis
    return []

def main(filename):
    process_file(filename)

if __name__ == '__main__':
    instance = sys.argv[1]
    init_config(sys.argv[2])
    main(sys.argv[3])
    print("Hubo \t"+str(counter)+"\t Simis en la cabecera")
    print("Hubo \t"+str(counterTo)+"\t Simis para abortar")
    print("Hubo \t"+str(counterOk)+"\t Simis abortadas")
    print("Hubo \t"+str(counterNOK)+"\t Simis no pudieron ser abortadas")

