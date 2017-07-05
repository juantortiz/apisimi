import urllib2
import base64
import pprint
import csv
import json
import sys
from dateutil.parser import parse as date_parse
from datetime import datetime, timedelta

def ListaProceso(paramURL, user, contr, fechaInicio, fechaFin):

    # FECHA PARA EL RANGO
    d_1 = str(datetime.today() - timedelta(days=1))
    d = str(datetime.today())
    dt_1 = date_parse(d_1)
    dt = date_parse(d)
    if fechaInicio == "" or fechaFin == "":
        tsStart = dt_1.strftime("%Y-%m-%d_17:00:00")
        tsEnd = dt.strftime("%Y-%m-%d_16:59:59")
    else:
        tsStart = fechaInicio
        tsEnd = fechaFin

    #print tsStart
    #print tsEnd
    # ENCABEZADO PARA BAJADA

    userPAss = user + ':' + contr
    user64 = base64.b64encode(userPAss, 'utf-8')
    headers = {'Authorization': 'Basic ' + user64, 'Accept': 'application/json'}
    baseURL = paramURL
    URL = '/rest/query/runtime/process'
    req = urllib2.Request(baseURL + URL + '?processinstancestatus=2&edt_max='
                          + tsEnd + '&edt_min=' + tsStart, None, headers)
    print(baseURL+URL+'?processinstancestatus=2&edt_max='+ tsEnd + '&edt_min=' + tsStart)

    response = urllib2.urlopen(req)
    resultado = json.loads(response.read())

    processes = resultado['processInstanceInfoList']
    results = {}
    listProccess = []
    for process in processes:
        results = {}
        try:
            results['processId'] = process['process-instance']['id']
            ProccessURL = baseURL + '/rest/history/instance/'
            req2 = urllib2.Request(ProccessURL + str(results['processId']), None, headers)
            response2 = urllib2.urlopen(req2)
            resultado2 = json.loads(response2.read())
            fecha = datetime.fromtimestamp(int(str(resultado2['end'])[:-3])).strftime('%Y-%m-%d %H:%M:%S')
            results['fecha_ultima_modificacion'] = fecha
            for variable in process['variables']:
                if variable['name'].startswith('a1dest_list_'):
                    fields = variable['value']['value'].split('|')
                    cant_field = len(fields)
                    field_0 = fields[0] if cant_field >= 1 else ""
                    field_1 = fields[1] if cant_field >= 2 else ""
                    field_2 = fields[2] if cant_field >= 3 else ""
                    field_3 = fields[3] if cant_field >= 4 else ""
                    field_4 = fields[4] if cant_field >= 5 else ""
                    field_5 = fields[5] if cant_field >= 6 else ""
                    field_6 = fields[6] if cant_field >= 7 else ""
                    field_7 = fields[7] if cant_field >= 8 else ""
                    field_8 = fields[8] if cant_field >= 9 else ""
                    field_9 = fields[9] if cant_field >= 10 else ""
                    field_10 = fields[10] if cant_field >= 11 else ""
                    field_11 = fields[11] if cant_field >= 12 else ""
                    field_12 = fields[12] if cant_field >= 13 else ""
                    field_13 = fields[13] if cant_field >= 14 else ""
                    field_14 = fields[14] if cant_field >= 15 else ""
                    field_15 = fields[15] if cant_field >= 16 else ""
                    field_16 = fields[16] if cant_field >= 17 else ""
                    field_17 = fields[17] if cant_field >= 18 else ""
                    field_18 = fields[18] if cant_field >= 19 else ""
                    field_19 = fields[19] if cant_field >= 20 else ""
                    field_20 = fields[20] if cant_field >= 21 else ""
                    field_21 = fields[21] if cant_field >= 22 else ""
                    field_22 = fields[22] if cant_field >= 23 else ""
                    field_23 = fields[23] if cant_field >= 24 else ""
                    results[variable['name']] = {'a1dest_estado_gestion': field_0,
                             'a1dest_fecha_ofic': field_1,
                             'a1dest_codigo_actividad': field_2,
                             'a1dest_id_simi': field_3,
                             'a1dest_numero_item': field_4,
                             'a1dest_numero_subitem': field_5,
                             'a1dest_desc_mercaderia': field_6,
                             'a1dest_fob_dolares': field_7,
                             'a1dest_fob_dolares_subitem': field_8,
                             'a1dest_tiene_subitem': field_9,
                             'a1dest_pais_procedencia': field_10,
                             'a1dest_nombre_pais_procedencia': field_11,
                             'a1dest_fecha_arribo_item': field_12,
                             'a1dest_cantidad_unidades_declarada': field_13,
                             'a1dest_posicion_arancelaria': field_14,
                             'a1dest_descripcion_arancelaria': field_15,
                             'a1dest_tiene_acuerdo_exp_imp': field_16,
                             'a1dest_monto_acuerdo_exp_imp': field_17,
                             'a1dest_id': field_18,
                             'a1dest_cuit_importador': field_19,
                             'a1dest_cuit_despachante': field_20,
                             'a1dest_lna': field_21,
                             'a1dest_unidad_medida_declarada': field_22,
                             'a1dest_descripcion_unidad_medida': field_23
                        }

                else:
                    results[variable['name']] = variable['value']['value']
        except:
            print "No se proceso es registro"
            continue
        listProccess.append(results)

    return listProccess


def escribirArchivos(lista, pathSalida):
    d = str(datetime.today())
    dt = date_parse(d)
    ts = dt.strftime("%Y-%m-%d_%H:%M:%S")

    djai = csv.writer(open(pathSalida + "/bajadaDjai-" + ts + ".csv", "wb"))
    a1dest = csv.writer(open(pathSalida + "/bajadaA1dest-" + ts + ".csv", "wb"))

    #DEVELOPMENT
    #djai = csv.writer(open("../content/output/bajadaDjai-" + ts + ".csv", "wb"))
    #a1dest = csv.writer(open("../content/output/bajadaA1dest-" + ts + ".csv", "wb"))
    for registro in lista:
        if registro['estado_simi'] == "APROBADA":
            estado = "A"
        else:
            estado = "O"
        djai.writerow([
            registro['djai_id_simi'],
            estado,
            registro['fecha_ultima_modificacion'],
            registro['usuario_simi'],
            registro['djai_cuit_imp'],
            registro['djai_fob_disp'],
            'SALI'
        ])
        for x in range(0, 150):
            if registro.get('a1dest_list_' + str(x)):
                a1dest.writerow([
                    registro['a1dest_list_' + str(x)]['a1dest_id'],
                    registro['a1dest_list_' + str(x)]['a1dest_id_simi'],
                    "SALI",
                    registro['a1dest_list_' + str(x)]['a1dest_cuit_importador'],
                    registro['a1dest_list_' + str(x)]['a1dest_cuit_despachante'],
                    registro['a1dest_list_' + str(x)]['a1dest_numero_item'],
                    registro['a1dest_list_' + str(x)]['a1dest_pais_procedencia'],
                    registro['a1dest_list_' + str(x)]['a1dest_numero_item'],
                    registro['a1dest_list_' + str(x)]['a1dest_numero_subitem'],
                    registro['a1dest_list_' + str(x)]['a1dest_posicion_arancelaria'],
                    registro['a1dest_list_' + str(x)]['a1dest_estado_gestion'],
                    registro['fecha_ultima_modificacion'],
                    registro['usuario_simi'],
                    registro['a1dest_list_' + str(x)]['a1dest_lna']
                ])

if len(sys.argv) == 5:
    # user, pass, url, pathSalida
    resultado = ListaProceso(sys.argv[1], sys.argv[2], sys.argv[3], "", "")

if len(sys.argv) == 7:
    # user, pass, url, pathSalida, fechaInicio, fechaFin
    resultado = ListaProceso(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[5], sys.argv[6])
