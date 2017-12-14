import requests
import MySQLdb
from requests.auth import HTTPBasicAuth


# [DB]
dbuser = 'simi'
dbpass = 'Simi.T.7102'
db = 'jbpmdb'
dbhost = '192.168.150.101'
deploymentID = 'minprod:simi:3.04'

dbJbpm = MySQLdb.connect(host=dbhost, user=dbuser, passwd=dbpass, db=db)
cursorJbpm = dbJbpm.cursor()
# query = "SELECT vil.processinstanceid FROM ProcessInstanceLog AS pil JOIN VariableInstanceLog AS vil ON vil.processinstanceid = pil.processinstanceid AND vil.variableId='djai_id_simi' WHERE pil.STATUS = 1;"
query = "SELECT pil.processinstanceid FROM ProcessInstanceLog AS pil WHERE pil.STATUS = 1";
cursorJbpm.execute(query)
process = cursorJbpm.fetchall();

for i in process:
    # url = 'http://192.168.150.101:8088/kie-wb-distribution-wars-6.5.0.Final-wildfly10/rest/runtime/minprod:simi:3.04/process/instance/'+str(i[0])+'/abort'
    url = 'http://186.33.211.247:89/kie-wb-distribution-wars-6.5.0.Final-wildfly10/rest/runtime/'+deploymentID+'/process/instance/'+str(i[0])+'/abort'
    print (requests.post(url,auth=HTTPBasicAuth('admin', 'admin')))
