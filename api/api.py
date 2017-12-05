import json
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


class ImportadorRobot(Resource):

    def get(self):
        con_simidb = mysql.connect()

        try:
            parser = reqparse.RequestParser()
            parser.add_argument('cuit', type=unicode, required=True)
            rargs = parser.parse_args()
            cuit_arg = rargs['cuit']

            con_simidb = mysql.connect()
            cursor_robot = con_simidb.cursor()

            query_importador = "SELECT " \
                                  "posicion_arancelaria, " \
                                  "fob_cantidad, " \
                                  "unidad_medida, " \
                                  "factor_lineal, " \
                                  "tope_fob, " \
                                  "cantidad, " \
                                  "cantidad_disponible, " \
                                  "unidad_declarada, " \
                                  "libre_acuerdo_cantidad " \
                               "FROM acuerdo_importado_posicion " \
                               "WHERE cuit = %s ";

            cursor_robot.execute(query_importador, cuit_arg)
            cuits_pa = cursor_robot.fetchall()
            cuit_pa_fields = cursor_robot.description
            cursor_robot.close()
            cuit_pa_list = []
            for cuit in cuits_pa:
                cuit_send = {}
                for (idx, fieldcuit) in enumerate(cuit_pa_fields):
                    if (isinstance(cuit[idx], decimal.Decimal) or isinstance(cuit[idx], datetime.datetime)):
                        cuit_send[(cuit_pa_fields[idx][0])] = str(cuit[idx])
                    else:
                        cuit_send[(cuit_pa_fields[idx][0])] = cuit[idx]
                cuit_pa_list.append(cuit_send)
            return cuit_pa_list

        except Exception as e:
            app.logger.error('ERROR: ' + str(e) + '.')
            return {'error': str(e)}

        finally:
            con_simidb.close()


class ImportadorPaOcho(Resource):

    def get(self):
        con_simidb = mysql.connect()

        try:
            parser = reqparse.RequestParser()
            parser.add_argument('cuit', type=unicode, required=True)
            rargs = parser.parse_args()
            cuit_arg = rargs['cuit']

            con_simidb = mysql.connect()
            cursor_import_ocho = con_simidb.cursor()

            query_importador = "SELECT " \
                                  "Subpartida" \
                                  ",unidad_declarada " \
                                  ",cantidad " \
                                  ",fob_dolares " \
                                  ",kilos " \
                                  ",cantidad_disponible " \
                                  ",fob_dolares_disponible " \
                               "FROM importado_por_subpartida " \
                               "WHERE cuit = %s " \
                               "ORDER BY Subpartida;";

            cursor_import_ocho.execute(query_importador, cuit_arg)
            cuits_pa = cursor_import_ocho.fetchall()
            cuit_pa_fields = cursor_import_ocho.description
            cursor_import_ocho.close()
            cuit_pa_list = []
            for cuit in cuits_pa:
                cuit_send = {}
                for (idx, fieldcuit) in enumerate(cuit_pa_fields):
                    if (isinstance(cuit[idx], decimal.Decimal) or isinstance(cuit[idx], datetime.datetime)):
                        cuit_send[(cuit_pa_fields[idx][0])] = str(cuit[idx])
                    else:
                        cuit_send[(cuit_pa_fields[idx][0])] = cuit[idx]
                cuit_pa_list.append(cuit_send)
            return cuit_pa_list

        except Exception as e:
            app.logger.error('ERROR: ' + str(e) + '.')
            return {'error': str(e)}

        finally:
            con_simidb.close()


class ImportadorPaDoce(Resource):

    def get(self):
        con_simidb = mysql.connect()

        try:
            parser = reqparse.RequestParser()
            parser.add_argument('cuit', type=unicode, required=True)
            rargs = parser.parse_args()
            cuit_arg = rargs['cuit']

            con_simidb = mysql.connect()
            cursor_import_doce = con_simidb.cursor()

            query_importador = "SELECT " \
                                  "posicion_arancelaria " \
                                  ",unidad_declarada " \
                                  ",cantidad " \
                                  ",fob_dolares " \
                                  ",kilos " \
                                  ",cantidad_disponible " \
                                  ",fob_dolares_disponible " \
                               "FROM importado_por_posicion_arancelaria  " \
                               "WHERE cuit = %s " \
                               "ORDER BY posicion_arancelaria;";

            cursor_import_doce.execute(query_importador, cuit_arg)
            cuits_pa = cursor_import_doce.fetchall()
            cuit_pa_fields = cursor_import_doce.description
            cursor_import_doce.close()
            cuit_pa_list = []
            for cuit in cuits_pa:
                cuit_send = {}
                for (idx, fieldcuit) in enumerate(cuit_pa_fields):
                    if (isinstance(cuit[idx], decimal.Decimal) or isinstance(cuit[idx], datetime.datetime)):
                        cuit_send[(cuit_pa_fields[idx][0])] = str(cuit[idx])
                    else:
                        cuit_send[(cuit_pa_fields[idx][0])] = cuit[idx]
                cuit_pa_list.append(cuit_send)
            return cuit_pa_list

        except Exception as e:
            app.logger.error('ERROR: ' + str(e) + '.')
            return {'error': str(e)}

        finally:
            con_simidb.close()


class Importador(Resource):
    def get(self):

        try:
            conn = mysql.connect()
            parser = reqparse.RequestParser()
            parser.add_argument('cuit_id', type=unicode, required=True)
            rargs = parser.parse_args()

            cuit_id = rargs['cuit_id']

            cursorImp = conn.cursor()

            queryImportador = "SELECT " \
                                "acumulado_solicitado, " \
                                "acumulado_solicitado_lna, " \
                                "acumulado_autorizado, " \
                                "acumulado_autorizado_lna, " \
                                "porcentaje_autorizado, " \
                                "porcentaje_autorizado_lna, " \
                                "acumulado_observado, " \
                                "acumulado_observado_lna, " \
                                "porcentaje_observado, " \
                                "porcentaje_observado_lna, " \
                                "total_importado_anio_anterior, " \
                                "total_importado_anio_anterior_lna, " \
                                "tiene_acuerdo_exp_imp_lna, " \
                                "monto_acuerdo_exp_imp_lna, " \
                                "importado_acum_lna_anio_anterior, " \
                                "porcentaje_indicador_anio_actual_lna , " \
                                "importado_acum_lna_anio_actual " \
                                "monto_acuerdo_exp_imp " \
                                "monto_referencia_anio_anterior " \
                                "monto_acuerdo_exp_lna " \
                            "FROM  Importadores " \
                            "WHERE id_persona = %s;";


            cursorImp.execute(queryImportador, cuit_id)
            dataImportador = cursorImp.fetchone()
            fieldsHeader = cursorImp.description
            dataJson = {}

            for (idx, fieldImp) in enumerate(dataImportador):
                if (isinstance(fieldImp, decimal.Decimal) or isinstance(fieldImp, datetime.datetime)):
                    dataJson[fieldsHeader[idx][0]] = str(fieldImp)
                else:
                    dataJson[fieldsHeader[idx][0]] = fieldImp

            cursorImp.close()
            return dataJson

        except Exception as e:
            return {'error': str(e)}
        finally:
            conn.close()


class ListaSimisPorCuit(Resource):

    def get(self):
        con_simidb = mysql.connect()

        try:
            parser = reqparse.RequestParser()
            parser.add_argument('cuit', type=unicode, required=True)
            rargs = parser.parse_args()
            cuit_arg = rargs['cuit']

            cursor_historico = con_simidb.cursor()
            query_historico = "SELECT"\
                              "     dj.destinacion,"\
                              "     dj.estado," \
                              "     dj.estado_djai," \
                              "     dj.fecha_ofic,"\
                              "     dj.fecha_caducidad,"\
                              "     dj.fecha_envio_afip,"\
                              "     dj.fecha_envio_afip_motivo_observacion,"\
                              "     dj.fob_dolares_disponible,"\
                              "     dj.fob_dolares_lna_disponible,"\
                              "     dj.fecha_anulacion,"\
                              "     dj.motivo_bloqueo,"\
                              "     dj.fecha_salidas,"\
                              "     dj.cudap," \
                              "     dj.cuit_importador," \
                              "     dj.razon_social_importador," \
                              "     dj.fob_dolares_bi34," \
                              "     imp.monto_acuerdo_exp_imp_lna,"\
                              "     imp.porcentaje_indicador_anio_actual_lna,"\
                              "     imp.tiene_acuerdo_exp_imp_lna,"\
                              "     imp.acumulado_procesado_lna,"\
                              "     imp.id_actividad,"\
                              "     imp.desc_actividad,"\
                              "     (CASE WHEN (ac.djai IS NOT NULL) THEN 'S' ELSE 'N' END) AS acuerdo_cargado,"\
                              "     (CASE WHEN (re.CUIT_CUIL IS NOT NULL) THEN 'S' ELSE 'N' END) AS tiene_acuerdo_automatico,"\
                              "     (CASE WHEN (ap.cuit IS NOT NULL) THEN 'S' ELSE 'N' END) AS tiene_rump"\
                              " FROM djais_hist AS dj"\
	                          "    JOIN Importadores AS imp ON (dj.cuit_importador = imp.id_persona)"\
	                          "    LEFT JOIN acuerdo_anexos as ac ON (dj.destinacion = ac.djai)"\
	                          "    LEFT JOIN (select ap.cuit from acuerdo_pa as ap group by ap.cuit) ap ON (dj.cuit_importador = ap.cuit)"\
	                          "    LEFT JOIN (select re.CUIT_CUIL from rump_cuits as re group by re.CUIT_CUIL) re ON (dj.cuit_importador = re.CUIT_CUIL)"\
                              " WHERE dj.cuit_importador = %s";

            cursor_historico.execute(query_historico, cuit_arg)
            cuits_pa = cursor_historico.fetchall()
            cuit_pa_fields = cursor_historico.description
            cursor_historico.close()
            cuit_pa_list = []

            for cuit in cuits_pa:
                cuit_send = {}
                for (idx, fieldcuit) in enumerate(cuit_pa_fields):
                    if (isinstance(cuit[idx], decimal.Decimal) or isinstance(cuit[idx], datetime.datetime)):
                        cuit_send["h_"+(cuit_pa_fields[idx][0])] = str(cuit[idx])
                    else:
                        cuit_send["h_"+(cuit_pa_fields[idx][0])] = cuit[idx]

                cursorSimi_Detail = con_simidb.cursor()
                query_DetailView ="SELECT a1.destinacion AS destinacion,"\
                                "         a1.estado_gestion AS estado_gestion,"\
                                "	 	  a1.numero_item AS numero_item,"\
                                "		  a1.numero_subitem AS numero_subitem,"\
                                "	      a1.descripcion_mercaderia AS descripcion_mercaderia,"\
                                "	      a1.posicion_arancelaria AS posicion_arancelaria,"\
                                "	      pr.codigo_posicion_arancelaria AS codigo_posicion_arancelaria,"\
                                "	      a1.fob_dolares AS fob_dolares,"\
                                "	      a1.fob_dolares_subitem AS fob_dolares_subitem,"\
                                "	      a1.cantidad_unidades_declarada AS cantidad_unidades_declarada,"\
                                "	      a1.pais_procedencia AS pais_procedencia,"\
                                "	      a1.pais_origen AS pais_origen,"\
                                "	      a1.descripcion_moneda_fob AS descripcion_moneda_fob,"\
                                "	      a1.fecha_embarque_item AS fecha_embarque_item,"\
                                "	      a1.fecha_arribo_item AS fecha_arribo_item,"\
                                "	      a1.fecha_ultima_modificacion AS fecha_ultima_modificacion,"\
                                "	      a1.marca_subitem AS marca_subitem,"\
                                "	      a1.modelo_subitem AS modelo_subitem,"\
                                "	      a1.descripcion_unidad_medida AS descripcion_unidad_medida,"\
                                "	      a1.unidad_estadistica AS unidad_estadistica,"\
                                "	      a1.peso_neto_kg AS peso_neto_kg,"\
                                "	      a1.precio_unitario_subitem AS precio_unitario_subitem,"\
                                "	      a1.lna AS lna"\
                                " FROM a1dest_hist a1"\
                                "      LEFT JOIN posiciones_res pr ON a1.posicion_arancelaria = CONVERT(pr.codigo_posicion_arancelaria USING utf8)"\
                                "      JOIN djais_hist dj ON dj.destinacion = a1.destinacion"\
                                " WHERE a1.destinacion = %s"\

                cursorSimi_Detail.execute(query_DetailView, cuit_send["h_destinacion"])
                simiDetails = cursorSimi_Detail.fetchall()
                fieldsDetail = cursorSimi_Detail.description
                detailList = []
                cursorSimi_Detail.close()

                for simi_Detail in simiDetails:
                    detailSimi = {}
                    for (idx_d, fieldSimiDetail) in enumerate(simi_Detail):
                        if (isinstance(fieldSimiDetail, decimal.Decimal) or isinstance(fieldSimiDetail,datetime.datetime)):
                            detailSimi['d_' + (fieldsDetail[idx_d][0])] = str(fieldSimiDetail)
                        else:
                            detailSimi['d_' + (fieldsDetail[idx_d][0])] = fieldSimiDetail
                    detailList.append(detailSimi)

                cuit_send["listSimiDetails"] = detailList
                cuit_pa_list.append(cuit_send)
            return cuit_pa_list

        except Exception as e:
            app.logger.error('ERROR: ' + str(e) + '.')
            return {'error': str(e)}

        finally:
            con_simidb.close()


class ListaSimis(Resource):

    def __init__(self):
        self.grpMap = {}
        analistas = ['Varios1','Varios2','Varios4','Textil','Automotriz']
        aprobadores = ['aprobador_Varios1','aprobador_Varios2','aprobador_Varios3','aprobador_Varios4','aprobador_Textil','aprobador_Automotriz']
        for grp in analistas:
            grupos = analistas[:]
            grupos.pop(grupos.index(grp))
            self.grpMap[grp] = grupos
            # //self.grpMap[grp].append('aprobador_'+grp)
        for grp in aprobadores:
            grupos = aprobadores[:]
            grupos.pop(grupos.index(grp))
            self.grpMap[grp] = grupos
            # self.grpMap[grp].append('supervisor')
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
                                        ",tiene_rump                          " \
                                        ",cuit_inhibido                       " \
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
                                    "*" \
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
        resultado = self.do_request(listaIdSImis)

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
        return "razon_social_importador LIKE \"%" + value + "%\""

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
            listDates = json.loads(value);
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
        listTemp = []
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

            for i in range(len(data)):
                listTemp.append(data[i][0])
            listaIdSimis["vv"] = listTemp

            return listaIdSimis

        except Exception as e:
            app.logger.error('ERROR: ' + str(e) + '.')
            return {'error': str(e)}
        finally:
            dbSimi.close()

    def do_request(self, simis):
        busqueda = ListaSimis()
        url = (urlAPITaskSearch)
        headers = {'Accept': 'application/json'}
        basic = request.authorization
        auth = HTTPBasicAuth(basic.username, basic.password)
        r = requests.get(url, params=simis, auth=auth, headers=headers)
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
api.add_resource(ImportadorPaOcho, '/ImportadorPaOcho')
api.add_resource(ImportadorPaDoce, '/ImportadorPaDoce')
api.add_resource(ImportadorRobot, '/ImportadorRobot')
api.add_resource(ListaSimisPorCuit, '/ListaSimisPorCuit')


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

