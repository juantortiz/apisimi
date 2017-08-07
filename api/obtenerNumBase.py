import mysql.connector
import sys

import ConfigParser

dbusername = dbpassword = dbhost = ''

def init_config(configFile):
    config = ConfigParser.ConfigParser()
    config.read(configFile)
    global dbusername
    global dbpassword
    global dbhost
    dbusername = config.get('DB','dbusername')
    dbpassword = config.get('DB','dbpassword')
    dbhost = config.get('DB','dbhost')

def get_cantidad(query,db):
    cnx = mysql.connector.connect(user=dbusername,password=dbpassword,database=db, host=dbhost )
    cursor = cnx.cursor(buffered=True)
    cursor.execute(query)
    response = cursor.fetchone()
    cursor.close()
    cnx.close()
    return response[0]


if __name__ == '__main__':
    init_config(sys.argv[1])
    query = ()
    db = sys.argv[2]
    if db == 'simidb':
        query = ("SELECT count(DISTINCT(destinacion)) FROM djais_hist;")
    elif db == 'jbpmdb':
        query = ("SELECT count(distinct (value)) FROM VariableInstanceLog where variableId = 'djai_id_simi';")
    sys.stdout.write(str(get_cantidad(query,db)))
