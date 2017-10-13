# import json
import datetime
import decimal
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_restful import reqparse
from flaskext.mysql import MySQL
from flask_cors import CORS
import sys
import MySQLdb
import ConfigParser
import requests
from requests.auth import HTTPBasicAuth




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
    global urlAPITask
    global urlAPITaskSearch
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
    urlAPITask = config.get('GLOBAL', 'urlAPITask')
    urlAPITaskSearch = config.get('GLOBAL', 'urlAPITaskSearch')
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

            for keyImp in dataJson.keys():
                if (isinstance(dataJson[keyImp], decimal.Decimal) or isinstance(dataJson[keyImp], datetime.datetime)):
                    dataJson[keyImp] = str(dataJson[keyImp])


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

        lSimis = self.getTask()
        resultado = self.fetch_simis(lSimis)

        return resultado

    def getTask(self):
        # DB SIMI - MySQL
        parser2 = reqparse.RequestParser()
        basic = request.authorization

        parser2.add_argument('usuario', type=unicode, required=True)
        parser2.add_argument('p', type=unicode, required=True)
        parser2.add_argument('s', type=unicode, required=True)

        rargs = parser2.parse_args()
        usuario = rargs['usuario']
        page = rargs['p']
        size = rargs['s']

        url = urlAPITask + '&p=' + page + '&s=' + size
        headers = {'Accept': 'application/json'}
        auth = HTTPBasicAuth(basic.username, basic.password)
        r = requests.get(url, auth=auth, headers=headers)

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
            app.logger.error('ERR: ' + str(r.status_code) + '.')

        return lSimis

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

            # Devuelve tabla con clave-valor (por ej : djai_estado --> 0; djai_id_simi --> 17001SIMI348320M )
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
                    if data1[index1][0] == data3[index3][0]: # Verifica que tenga el PInstanceId
                        if data3[index3][1] == 'grp':
                            groups = self.grpMap[data3[index3][2]] # Depende el grupo, se fija a quienes puede escalar.
                            eleJson['escale_to'] = groups
                            eleJson[data3[index3][1]] = data3[index3][2]
                        else:
                            eleJson[data3[index3][1]] = data3[index3][2]
                    else:
                        continue

                cursorSimi_Header = dbSimi.cursor()

                # Se unifican querys en una sola vista para traer datos, a su vez se agregan datos.
                query_HeaderView = "SELECT " \
                                        "destinacion                          "\
                                        ",estado                              "\
                                        ",fecha_ofic                          "\
                                        ",fecha_caducidad					  "\
                                        ",fecha_envio_afip                    "\
                                        ",fecha_envio_afip_motivo_observacion "\
                                        ",fob_dolares_disponible              "\
                                        ",fob_dolares_lna_disponible          "\
                                        ",fecha_anulacion                     "\
                                        ",motivo_bloqueo                      "\
                                        ",fecha_salidas                       "\
                                        ",cudap                               "\
                                        ",monto_acuerdo_exp_imp_lna           "\
                                        ",porcentaje_indicador_anio_actual_lna"\
                                        ",tiene_acuerdo_exp_imp_lna           "\
                                        ",acumulado_procesado_lna             "\
                                        ",id_actividad                        "\
                                        ",desc_actividad                      "\
                                        ",acuerdo_cargado                     "\
                                        ",tiene_acuerdo_automatico            "\
                                        ",tiene_rump                          "\
                                   "FROM simidb.simi_cabecera "\
                                   "WHERE destinacion = %s"


                cursorSimi_Header.execute(query_HeaderView, eleJson['djai_id_simi'])
                simiHeader = cursorSimi_Header.fetchone()
                fieldsHeader = cursorSimi_Header.description

                for (idx,fieldSimi) in enumerate(simiHeader):
                    if (isinstance(fieldSimi,decimal.Decimal) or isinstance(fieldSimi,datetime.datetime)):
                        eleJson['h_'+(fieldsHeader[idx][0])] = str(fieldSimi)
                    else:
                        eleJson['h_'+(fieldsHeader[idx][0])] = fieldSimi

                cursorSimi_Header.close()

                # Cargo la informacion de las posiciones arancelarias de la Simi en particular.
                # Hacer una lista de jsons con los detalles.

                query_DetailView = "SELECT " \
                                    "destinacion					" \
                                    ",estado_gestion                " \
                                    ",numero_item                   " \
                                    ",numero_subitem                " \
                                    ",descripcion_mercaderia        " \
                                    ",posicion_arancelaria          " \
                                    ",fob_dolares                   " \
                                    ",fob_dolares_subitem           " \
                                    ",cantidad_unidades_declarada   " \
                                    ",pais_procedencia              " \
                                    ",pais_origen                   " \
                                    ",descripcion_moneda_fob        " \
                                    ",fecha_embarque_item           " \
                                    ",fecha_arribo_item             " \
                                    ",fecha_ultima_modificacion     " \
                                    ",marca_subitem                 " \
                                    ",modelo_subitem                " \
                                    ",descripcion_unidad_medida     " \
                                    ",unidad_estadistica            " \
                                    ",peso_neto_kg					" \
                                    ",precio_unitario_subitem		" \
                                    ",lna                   		" \
                                   "FROM simidb.v_simi_detalle " \
                                   "WHERE destinacion = %s"

                cursorSimi_Detail = dbSimi.cursor()
                cursorSimi_Detail.execute(query_DetailView, eleJson['djai_id_simi'])
                simiDetails = cursorSimi_Detail.fetchall()
                fieldsDetail = cursorSimi_Detail.description
                detailList = []
                cursorSimi_Detail.close()

                for simi_Detail in simiDetails:
                    detailSimi = {}
                    for (idx_d, fieldSimiDetail) in enumerate(simi_Detail):
                        if (isinstance(fieldSimiDetail, decimal.Decimal) or isinstance(fieldSimiDetail, datetime.datetime)):
                            detailSimi['d_' + (fieldsDetail[idx_d][0])] = str(fieldSimiDetail)
                        else:
                            detailSimi['d_' + (fieldsDetail[idx_d][0])] = fieldSimiDetail
                    detailList.append(detailSimi)

                eleJson["listSimiDetails"] = detailList

                dataJson2.append(eleJson)
            # print dataJson2
            return dataJson2

        except Exception as e:
            app.logger.error('ERROR: ' + str(e) + '.')
            return {'error': str(e)}

        finally:
            dbJbpm.close()
            dbSimi.close()


class Query(Resource):

    def __init__(self):
        self.args = {}

    def get(self):
        self.args = request.args
        parser = reqparse.RequestParser()
        parser.add_argument('accion', type=unicode)
        parser.add_argument('simis', type=unicode)
        parser.add_argument('pa', type=unicode)
        parser.add_argument('cuit', type=unicode)
        parser.add_argument('rz', type=unicode)
        parser.add_argument('dates', type=unicode)

        rargs = parser.parse_args()
        listaIdSImis = self.listaIdSimis(rargs)

        listaTasks = params_to_string(listaIdSImis)
        resultado = self.do_request(listaTasks)

        return resultado

    def addDestinacion(self, value):
        listPa = str(value).splitlines()
        value = ','.join(unicode("\"" + e + "\"") for e in listPa)
        return "destinacion IN (" + value + ")"

    def addDjai(self,value):
        if value == ' ':
            return "estado_djai IS NULL"
        if value == 'T':
            return ""
        else:
            return "estado_djai IN (\""+value+"\")"

    def addCuit(self, value):
        return "cuit_importador IN (\"" + value + "\")"

    def addRazon(self,value):
        return "razon_social_importador IN (\"" + value + "\")"

    def addPA(self,value):
        listPa = str(value).splitlines()
        lengthPA = len(listPa[0])
        value = ','.join(unicode("\"" + e + "\"") for e in listPa)

        if lengthPA == -1:
            lengthPA = len(value)
        return "SUBSTRING(posicion_arancelaria,1,"+str(lengthPA)+") IN (" + value + ")"

    def addDates(self, value):
        field_db = {
            "dRec":"fecha_ofic",
            "dCad":"fecha_caducidad",
            "dInt":"fecha_ultima_modificacion"
        }

        clause = "";
        if value:
            # listDates = json.loads(value);
            listDates = {};
            for arg in listDates:
                    if str(arg).lower().find("ini") != -1:
                        clause += field_db[str(arg)[:4]] + " > \"" + listDates[arg] + "\" AND ";
                    if str(arg).lower().find("fin") != -1:
                        clause += field_db[str(arg)[:4]] + " < \"" + listDates[arg] + "\" AND ";
            if (clause): clause = clause[:-5];
        return clause;

    def getFilter(self, keyArg, valueArg):
        fieldsToFind = {
            'simis': self.addDestinacion,
            'accion': self.addDjai,
            'cuit': self.addCuit,
            'rz': self.addRazon,
            'pa': self.addPA,
            'dates': self.addDates
        }

        return fieldsToFind[keyArg](valueArg)

    def listaIdSimis(self, rargs):
        #DB SIMI
        dbSimi = mysql.connect()
        cursor = dbSimi.cursor()
        regs = ''
        listaIdSimis = {}
        whereClause = ""
        filterClause = ""
        try:
            query_string = "SELECT DISTINCT destinacion " \
                           "FROM v_campos_busqueda " \

            for arg in rargs:
                if rargs[arg] is not None and rargs[arg] != 'undefined':
                    filterClause = self.getFilter(arg, rargs[arg])
                    if filterClause != "":
                        if whereClause == "":
                            whereClause = "WHERE " + filterClause
                        else:
                            whereClause = whereClause + " AND " + filterClause

            query_string = query_string + whereClause

            cursor.execute(query_string)
            data = cursor.fetchall()

            for index in range(len(data)):
                reg = str(data[index][0]) + ','
                regs = regs + reg
            listaIdSimis['id_simis'] = regs[:-1]
            print listaIdSimis

            return listaIdSimis

        except Exception as e:
            app.logger.error('ERROR: ' + str(e) + '.')
            return {'error': str(e)}
        finally:
            dbSimi.close()

    def do_request(self, params):
        busqueda = ListaSimis()
        url = (urlAPITaskSearch + params)
        headers = {'Accept': 'application/json'}
        basic = request.authorization
        auth = HTTPBasicAuth(basic.username, basic.password)
        r = requests.get(url, auth=auth, headers=headers)
        data = r.json()
        print data

        if r.status_code == 200:
            data = r.json()
            cant = len(data['taskInfoList'])
            data = data['taskInfoList']
            lSimis = ''
            for index in range(cant):
                reg = str(data[index]['taskSummaries'][0]['id']) + ','
                lSimis = lSimis + reg
            lSimis = lSimis[:-1]
            app.logger.debug('DEB: Cant:' + str(len(lSimis.split(','))) + ' listTaskByUser: ' + str(lSimis) + '.')
        else:
            app.logger.error('ERR: ' + str(r.status_code) + '.')

        resultado = busqueda.fetch_simis(lSimis)

        return resultado


api.add_resource(Importador, '/Importador')
api.add_resource(ListaSimis, '/ListaSimis')
api.add_resource(Query, '/Query')


def params_to_string(params):
    query_params = ''
    for key in params.keys():
        values = params.get(key).split(',')
        for value in values:
            query_params += '&vv=' + value
    return query_params


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

