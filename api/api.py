import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_restful import reqparse
from flaskext.mysql import MySQL
from flask_cors import CORS
import sys
import MySQLdb
import re
import ConfigParser
import requests
from requests.auth import HTTPBasicAuth
import json


app = Flask(__name__)
api = Api(app)
CORS(app)
mysql = MySQL()
mysql.init_app(app)

def init_config(configFile):
    config = ConfigParser.ConfigParser()
    config.read(configFile)
    global dbuser
    global dbpass
    global db
    global dbhost
    global dirlog
    global dirusrrol
    global urlAPI
    global usrAPI
    global passAPI

    app.config['MYSQL_DATABASE_USER'] = config.get('DBSIMI', 'dbusername')
    app.config['MYSQL_DATABASE_PASSWORD'] = config.get('DBSIMI', 'dbpassword')
    app.config['MYSQL_DATABASE_DB'] = config.get('DBSIMI', 'db')
    app.config['MYSQL_DATABASE_HOST'] = config.get('DBSIMI', 'dbhost')
    dbuser = config.get('DB', 'dbusername')
    dbpass = config.get('DB', 'dbpassword')
    db = config.get('DB', 'db')
    dbhost = config.get('DB', 'dbhost')
    dirlog = config.get('GLOBAL', 'dirlog')
    dirusrrol = config.get('GLOBAL', 'dirusrrol')
    urlAPI = config.get('GLOBAL', 'urlAPIJbpm')
    usrAPI = config.get('GLOBAL', 'usrAPI')
    passAPI = config.get('GLOBAL', 'passAPI')




class Importador(Resource):
    def get(self):

        try:
            conn = mysql.connect()
            parser = reqparse.RequestParser()
            parser.add_argument('cuit_id', type=unicode, required=True)
            rargs = parser.parse_args()

            cuit_id = rargs['cuit_id']

            cursor = conn.cursor()

            query_string = "SELECT id_actividad, desc_actividad, mail, area, telefono, acumulado_solicitado, " \
                           "acumulado_solicitado_lna, " \
                           "acumulado_autorizado, porcentaje_autorizado, acumulado_autorizado_lna," \
                           "porcentaje_autorizado_lna, acumulado_observado, porcentaje_observado," \
                           "acumulado_observado_lna, porcentaje_observado_lna, acumulado_procesado_lna," \
                           "porcentaje_procesado_lna, total_importado_anio_anterior, " \
                           "total_importado_anio_anterior_lna, porcentaje_indicador_anio_actual_lna, " \
                           "monto_referencia_anio_anterior, porcentaje_indicador_anio_actual," \
                           "acumulado_fob_dolares_disponible_sali, acumulado_fob_dolares_disponible_sali_lna, " \
                           "desc_actividad, acumulado_procesado, monto_referencia_anio_anterior_lna," \
                           "monto_acuerdo_exp_imp, monto_acuerdo_exp_imp_lna " \
                           "FROM  Importadores im " \
                           "WHERE im.id_persona = %s;"

            cursor.execute(query_string, cuit_id)
            data = cursor.fetchone()

            dataJson = {
                    "imp_id_actividad": data[0],
                    "imp_estado_djai": data[1],
                    "imp_mail": data[2],
                    "imp_area": data[3],
                    "imp_telefono": data[4],
                    "imp_acumulado_solicitado": data[5],
                    "imp_acumulado_solicitado_lna": data[6],
                    "imp_acumulado_autorizado": data[7],
                    "imp_porcentaje_autorizado": data[8],
                    "imp_acumulado_autorizado_lna": data[9],
                    "imp_porcentaje_autorizado_lna": data[10],
                    "imp_acumulado_observado": data[11],
                    "imp_porcentaje_observado": data[12],
                    "imp_acumulado_observado_lna": data[13],
                    "imp_porcentaje_observado_lna": data[14],
                    "imp_acumulado_procesado_lna": data[15],
                    "imp_porcentaje_procesado_lna": data[16],
                    "imp_total_importado_anio_anterior": data[17],
                    "imp_total_importado_anio_anterior_lna": data[18],
                    "imp_porcentaje_indicador_anio_actual_lna": data[19],
                    "imp_monto_referencia_anio_anterior": data[20],
                    "imp_porcentaje_indicador_anio_actual": data[21],
                    "imp_acumulado_fob_dolares_disponible_sali": data[22],
                    "imp_acumulado_fob_dolares_disponible_sali_lna": data[23],
                    "imp_descripcion_actividad": data[24],
                    "imp_acumulado_procesado": data[25],
                    "imp_monto_referencia_anio_anterior_lna": data[26],
                    "imp_monto_acuerdo_exp_imp": data[27],
                    "imp_monto_acuerdo_exp_imp_lna": data[28]
            }

            return dataJson

        except Exception as e:
            return {'error': str(e)}
        finally:
            conn.close()

class ListaSimis(Resource):

    def __init__(self):
        self.grpMap = {}
        analistas = ['Varios1','Varios2','Varios4','Textil','Automotriz']
        aprobadores = ['aprobador_Varios1','aprobador_Varios2','aprobador_Varios3','aprobador_Varios4','aprobador_Textil','aprobador_Automotriz']
        for grp in analistas:
            grupos = analistas[:]
            grupos.pop(grupos.index(grp))
            self.grpMap[grp] = grupos
            self.grpMap[grp].append('aprobador_'+grp)
        for grp in aprobadores:
            grupos = aprobadores[:]
            grupos.pop(grupos.index(grp))
            self.grpMap[grp] = grupos
            self.grpMap[grp].append('supervisor')
        self.grpMap['supervisor'] = ['director_importacion']
        self.grpMap['director_importacion'] = ['director_nacional']
        self.grpMap['director_nacional'] = []

    def get(self):
        # DB SIMI
        parser2 = reqparse.RequestParser()
        parser2.add_argument('usuario', type=unicode, required=True)
        parser2.add_argument('p', type=unicode, required=True)

        rargs = parser2.parse_args()
        usuario = rargs['usuario']
        page = rargs['p']

        url = urlAPI + '&potentialOwner='+usuario+'&p='+page+'&s=1000'
        headers = {'Accept': 'application/json'}
        r = requests.get(url, auth=HTTPBasicAuth(usrAPI, passAPI), headers=headers)

        if r.status_code == 200:
            data = r.json()
            cant = len(data['taskSummaryList'])
            data = data['taskSummaryList']
            lSimis = ''
            for index in range(cant):
                reg = str(data[index]['id']) + ','
                lSimis = lSimis + reg
            lSimis = lSimis[:-1]
            app.logger.debug('DEB: Cant:' + str(len(lSimis.split(','))) + ' listTaskByUser: ' + str(lSimis) + '.')
        else:
            app.logger.error('ERR: ' + r.status_code + '.')

        resultado = self.fetch_simis(lSimis)
        return resultado


    def fetch_simis(self, lista):
        dataJson2 = []
        dbSimi = mysql.connect()
        # DB JBPM
        dbJbpm = MySQLdb.connect(host=dbhost, user=dbuser, passwd=dbpass, db=db)
        cursorJbpm = dbJbpm.cursor()
        try:
            lp = ''
            query_string1 = "SELECT tvi1.processinstanceid, tvi1.taskId, tvi1.value as actions_available "\
                            "FROM  TaskVariableImpl as tvi1 where tvi1.name = 'actions_available' "\
                            "and tvi1.taskId in (" + lista + ") " \
                            "order by tvi1.processinstanceid;"

            cursorJbpm.execute(query_string1)

            data1 = cursorJbpm.fetchall()

            for index0 in range(len(data1)):
                if index0 == 0:
                    reg = str(data1[index0][0])
                    lp = lp + reg
                else:
                    reg = ',' + str(data1[index0][0])
                    lp = lp + reg


            query_string3 = " SELECT vil.processInstanceId, vil.variableId, vil.value from  VariableInstanceLog  vil " \
                            "where vil.variableId in ('djai_estado', 'djai_id_simi', 'grp', 'djai_cuit_imp', " \
                            "'djai_raz_soc_imp', 'djai_fob_bi34', 'djai_fech_env_afip','estado_simi')" \
                            "and vil.processinstanceid in (" + lp + ") "\
                            "order by vil.processinstanceid, variableId;"

            cursorJbpm.execute(query_string3)
            data3 = cursorJbpm.fetchall()

            lp = ''

            for index1 in range(len(data1)):
                eleJson = {'process_instance_id': data1[index1][0],
                           'task_id': data1[index1][1],
                           'actions_available': data1[index1][2]}
                for index3 in range(len(data3)):
                    if data1[index1][0] == data3[index3][0]:
                        if data3[index3][1] == 'grp':
                            groups = self.grpMap[data3[index3][2]]
                            eleJson['escale_to'] = groups
                            eleJson[data3[index3][1]] = data3[index3][2]
                        else:
                            eleJson[data3[index3][1]] = data3[index3][2]
                    else:
                        continue

                cursorSimi = dbSimi.cursor()

                query_string2 = "SELECT porcentaje_procesado_lna, porcentaje_indicador_anio_actual_lna, "\
                                "total_importado_anio_anterior_lna "\
                                "FROM  Importadores im "\
                                "WHERE im.id_persona = %s; "

                cursorSimi.execute(query_string2, eleJson['djai_cuit_imp'])
                data2 = cursorSimi.fetchone()

                if data2 == None:
                    data2 = [0, 0, 0]

                eleJson['impor_porc_lna'] = data2[0]
                eleJson['impor_porc_actual_lna'] = data2[1]
                eleJson['impor_impor_ant_lna'] = data2[2]

                dataJson2.append(eleJson)

            # print len(dataJson2)
            return dataJson2

        except Exception as e:
            app.logger.error('ERROR: ' + str(e) + '.')
            return {'error': str(e)}

        finally:
            dbJbpm.close()
            dbSimi.close()


api.add_resource(Importador, '/Importador')
api.add_resource(ListaSimis, '/ListaSimis')

if len(sys.argv) == 2:
    # MySQL configurations
    init_config(sys.argv[1])

else:
    print "Parametros Incorrectos"
    exit()

if __name__ == '__main__':
    handler = RotatingFileHandler(dirlog + '/error.log', maxBytes=100000000, backupCount=1)
    handler.setLevel(logging.ERROR)
    app.logger.addHandler(handler)
    app.run(debug=True, host='0.0.0.0', port=8111)
