import mysql.connector
import sys

import ConfigParser

dbusername = dbpassword = dbhost = database = ''

def init_config(configFile):
    config = ConfigParser.ConfigParser()
    config.read(configFile)
    global dbusername
    global dbpassword
    global dbhost
    global database
    dbusername = config.get('DB','dbusername')
    dbpassword = config.get('DB','dbpassword')
    database = config.get('DB','db')
    dbhost = config.get('DB','dbhost')

def getInstanciadas():
    cnx = mysql.connector.connect(user=dbusername,password=dbpassword,database=database, host=dbhost )
    cursor = cnx.cursor(buffered=True)
    query = ("select count(*) from ProcessInstanceLog")
    cursor.execute(query)
    response = cursor.fetchone()
    cursor.close()
    cnx.close()
    return response[0]


if __name__ == '__main__':
    init_config(sys.argv[1])
    sys.stdout.write(str(getInstanciadas()))
