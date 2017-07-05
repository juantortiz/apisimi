import mysql.connector
import sys
import csv
import requests

import ConfigParser
from requests.auth import HTTPBasicAuth

dbusername = dbpassword = username = password = database = base_url =  ''

def init_config(configFile):
	config = ConfigParser.ConfigParser()
	config.read(configFile)
	global dbusername
	global dbpassword
	global username
	global password
	global database
	global base_url
	dbusername = config.get('DB','dbusername')
	dbpassword = config.get('DB','dbpassword')
	database = config.get('DB','db')
	username = config.get('JBPM','username')
	password = config.get('JBPM','password')
	base_url = config.get('JBPM','url')


def eliminar(simis):
	for simi in simis:
		url = base_url+ 'process/instance/'+str(simi[0])+'/abort'
   		r = requests.post(url,auth=HTTPBasicAuth(username, password))
		if r.status_code == 200: 	
			print('La simi ' + str(simi[0]) + ' Fue abortada exitosamente')
		else:
			print('ERROR \t La simi ' + str(simi[0]) + ' No pudo ser abortada. Error: ' + str(r.status_code)) 


def esta_instanciada(simi):
	cnx = mysql.connector.connect(user=dbusername,password=dbpassword,database=database)
	cursor = cnx.cursor(buffered=True)
	query = ("select pil.id "
			"from ProcessInstanceLog as pil "
			"join VariableInstanceLog as vil on vil.processinstanceid = pil.processinstanceid and vil.variableId='djai_id_simi'"
			"where vil.value = '"+simi+"'and pil.status in (1,2);")
	cursor.execute(query)
	response = cursor.fetchall()
	cursor.close()
	cnx.close()
	return response

def process_file(filename):
	reader = csv.reader(open(filename),delimiter=',')
	for row in reader:
		simis = esta_instanciada(row[0])
		if len(simis) > 0:
			eliminar(simis)


def main(filename):
	process_file(filename)
	
if __name__ == '__main__':
	init_config(sys.argv[1])
	main(sys.argv[2])

