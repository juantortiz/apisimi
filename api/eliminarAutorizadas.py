import mysql.connector
import sys
import csv
import requests

import ConfigParser
from requests.auth import HTTPBasicAuth

dbhost = dbusername = dbpassword = username = password = database = base_url =  ''
counterOk = 0
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
    dbusername = config.get('DB','dbusername')
    dbpassword = config.get('DB','dbpassword')
    database = config.get('DB','db')
    dbhost = config.get('DB','dbhost')
    username = config.get('JBPM','username')
    password = config.get('JBPM','password')
    base_url = config.get('JBPM','url')


def eliminar(simis):
    print "Abortando simi"
    for simi in simis:
        url = base_url+ 'process/instance/'+str(simi[0])+'/abort'
        r = requests.post(url,auth=HTTPBasicAuth(username, password))
        if r.status_code == 200:
            global counterOk
            counterOk = counterOk + 1
            print('La simi con proceso' + str(simi[0]) + ' Fue abortada exitosamente')
        else:
            print >>sys.stderr, 'ERROR \t La simi con proceso' + str(simi[0]) + ' No pudo ser abortada. Error: ' + str(r.status_code)



def esta_instanciada(simi):
    cnx = mysql.connector.connect(user=dbusername,password=dbpassword,database=database, host=dbhost )
    cursor = cnx.cursor(buffered=True)
    query = ("select pil.processInstanceId "
                "FROM ProcessInstanceLog as pil "
                "join VariableInstanceLog as vil on vil.processinstanceid = pil.processinstanceid and vil.variableId = 'djai_id_simi'"
                "where vil.value='"+simi+"' and pil.status in (0,1);")
    cursor.execute(query)
    response = cursor.fetchall()
    cursor.close()
    cnx.close()
    return response

def esta_aprobada(estado):
    return estado == 'A'

def process_file(filename):
    reader = csv.reader(open(filename),delimiter=';')
    row1 = next(reader)
    for row in reader:
        global counter
        counter = counter + 1
        print "Simi: \t"+row[0],
        if esta_aprobada(row[1]):
            print "Aprobada ",
            simis = esta_instanciada(row[0])
            if len(simis) > 0:
                global counterTo
                counterTo = counterTo + 1
                eliminar(simis)
        else:
            print "No aprobada",
        print



def main(filename):
    process_file(filename)

if __name__ == '__main__':
    init_config(sys.argv[1])
    main(sys.argv[2])
    print("Hubo \t"+str(counter)+"\t Simis en la cabecera")
    print("Hubo \t"+str(counterTo)+"\t Simis para abortar")
    print("Hubo \t"+str(counterOk)+"\t Simis abortadas")

