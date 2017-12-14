import re
import sys
import ConfigParser
import mysql.connector


def init_config(configFile):
    global dbuser, dbpass, db, dbhost
    global escale_to

    escale_to = {
        "analista": "supervisor",
        "supervisor": "coordinador",
        "coordinador": "director_importacion",
        "director_importacion":  "director_nacional",
        "director_nacional":""
    }
    config = ConfigParser.ConfigParser()
    config.read(configFile)
    dbuser = config.get('DBSIMI', 'dbusername')
    dbpass = config.get('DBSIMI', 'dbpassword')
    db = config.get('DBSIMI', 'db')
    dbhost = config.get('DBSIMI', 'dbhost')


def do_insert_simidb(query,params):
    try:
        cnx = mysql.connector.connect(user=dbuser, password=dbpass, database=db, host=dbhost)
        cursor = cnx.cursor()
        cursor.execute(query,params)
        cnx.commit()
    except Exception as exc:
        print exc
        print "Error al realizar comando contra la base"
    finally:
        cursor.close()
        cnx.close()


def get_rol(lsRols):
    if any("director_nacional" in elem for elem in lsRols):
        return "director_nacional"
    if any("director_importacion" in elem for elem in lsRols):
        return "director_importacion"
    if any("coordinador" in elem for elem in lsRols):
        return "coordinador"
    if any("supervisor_" in entry for entry in lsRols):
        return "supervisor"
    else:
        return "analista"


def get_groups_to_share(rol, lsGroups):
    analistas = ['grupo1','grupo2','grupo3','grupo4']
    aprobadores = ['supervisor_grupo1','supervisor_grupo2','supervisor_grupo3','supervisor_grupo4']
    to_share = []
    # analistas = ['Varios1', 'Varios2', 'Varios4', 'Textil', 'Automotriz']
    # aprobadores = ['aprobador_Varios1', 'aprobador_Varios2', 'aprobador_Varios3', 'aprobador_Varios4','aprobador_Textil', 'aprobador_Automotriz']

    if rol == 'analista':
        to_share = filter(lambda a: a not in lsGroups, analistas)

    if rol == 'supervisor':
        to_share = filter(lambda a: a not in lsGroups, aprobadores)

    return to_share


# /u01/simi/wildfly/wildfly/standalone/configuration/application-roles.properties
if __name__ == '__main__':
    if len(sys.argv) >= 2:
        init_config(sys.argv[1])
        fileUsers = open(sys.argv[2], "r");
        userLns = fileUsers.readlines();
        for ln in userLns:
            if ln[0] != "#":
                ln = ln[:-1]
                lsUserRol = re.findall(r"[\w']+", ln)
                if lsUserRol[0] != "admin":
                    lsUserRol = filter(lambda a: a != 'rest', lsUserRol)
                    lsUserRol = filter(lambda a: a != 'all', lsUserRol)
                    lsUserRol = filter(lambda a: a != 'user', lsUserRol)
                    user = lsUserRol.pop(0)
                    rol = get_rol(lsUserRol)
                    groups_to_share = get_groups_to_share(rol,lsUserRol)
                                                     # user,rol,groups,groups_to_share,group_to_scale
                    add_user = ("INSERT INTO user_rol (user,rol,groups,groups_to_share,group_to_scale) VALUES (%s, %s, %s, %s, %s) "
                                "ON DUPLICATE KEY UPDATE rol = VALUES(rol),groups=VALUES(groups),groups_to_share=VALUES(groups_to_share),group_to_scale = VALUES(group_to_scale)")

                    data_user = (user, rol, ','.join(lsUserRol), ','.join(groups_to_share),escale_to[rol])
                    do_insert_simidb(add_user,data_user)
    else:
        print "Falta parametro archivo de usuarios y de configuracion"