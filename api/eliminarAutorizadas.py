import mysql.connector
import sys
import csv
import requests

import ConfigParser
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta
from dateutil.parser import parse as date_parse

instance = dbhost = dbusername = dbpassword = username = password = database = base_url = ''
dbusernameSimi = dbpasswordSimi = dbhostSimi = databaseSimi = ''
counterOk = 0
counterNOK = 0
counter = 0
counterTo = 0


def init_config(configFile):
    config = ConfigParser.ConfigParser()
    config.read(configFile)

    global dbusernameSimi
    global dbpasswordSimi
    global dbhostSimi
    global databaseSimi

    global dbusername
    global dbpassword
    global dbhost
    global username
    global password
    global database
    global base_url
    global instance

    dbusername = config.get('DB', 'dbusername')
    dbpassword = config.get('DB', 'dbpassword')
    database = config.get('DB', 'db')
    dbhost = config.get('DB', 'dbhost')

    databaseSimi = config.get('DBSIMI', 'db')
    dbusernameSimi = config.get('DBSIMI', 'dbusername')
    dbpasswordSimi = config.get('DBSIMI', 'dbpassword')
    dbhostSimi = config.get('DBSIMI', 'dbhost')

    username = config.get('JBPM', 'username')
    password = config.get('JBPM', 'password')
    base_url = config.get('JBPM', 'url')
    # base_url = base_url[:base_url.find(base_url.split('/')[6])]


def eliminar(simis):
    print "Abortando simi"
    for simi in simis:
        url = base_url + instance + '/process/instance/' + str(simi) + '/abort'
        print url
        r = requests.post(url, auth=HTTPBasicAuth(username, password))
        if r.status_code == 200:
            global counterOk
            counterOk = counterOk + 1
            print('La simi con proceso ' + str(simi) + ' Fue abortada exitosamente')
        else:
            global counterNOK
            counterNOK = counterNOK + 1
            print >> sys.stderr, 'ERROR \t La simi con proceso ' + str(simi) + ' No pudo ser abortada. Error: ' + str(r.status_code)


def doQuerySimiDb(query):
    cnx = mysql.connector.connect(user=dbusernameSimi, password=dbpasswordSimi, database=databaseSimi, host=dbhostSimi)
    cursor = cnx.cursor(buffered=True)
    cursor.execute(query)
    response = cursor.fetchall()
    cursor.close()
    cnx.close()
    return response


def doQueryJBPM(query):
    cnx = mysql.connector.connect(user=dbusername, password=dbpassword, database=database, host=dbhost)
    cursor = cnx.cursor(buffered=True)
    cursor.execute(query)
    response = cursor.fetchall()
    cursor.close()
    cnx.close()
    return response


def process_simis_to_abort():
    print 'Proceso bajas'
    simisToAbort = []
    query = ("SELECT processInstanceId FROM simis_a_abortar")
    response = doQuerySimiDb(query)
    for simi in response:
        simisToAbort.append(simi[0])
    eliminar(simisToAbort)


def main():
    process_simis_to_abort()


if __name__ == '__main__':

    start_time = datetime.now()
    instance = sys.argv[1]
    init_config(sys.argv[2])

    main();
    print("Hubo \t" + str(counterOk) + "\t Simis abortadas")
    print("Hubo \t" + str(counterNOK) + "\t Simis no pudieron ser abortadas")

    elapsed_time = datetime.now() - start_time
    print(elapsed_time)