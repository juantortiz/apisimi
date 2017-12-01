import re

def getRol(lsRols):
    for e in lsRols:
        if e == "director_nacional":
            return e
        if e == "director_importacion":
            return e
        # if e == "coordinador":
        if e == "supervisor":
            return e
        # if e == "Supervisor_":
        if e[0:9] == "aprobador_":
            return "aprobador"
            # return "supervisor"
    return "analista"





if __name__ == '__main__':

    fileUsers = open("/home/nachodz/Documentos/application-roles.properties", "r");
    userLns = fileUsers.readlines();
    for ln in userLns:
        if ln[0] != "#":
            ln = ln[:-1]
            lsUserRol = re.findall(r"[\w']+", ln)
            if lsUserRol[0] != "admin":
                lsUserRol = filter(lambda a: a != 'rest', lsUserRol)
                lsUserRol = filter(lambda a: a != 'all', lsUserRol)
                lsUserRol = filter(lambda a: a != 'user', lsUserRol)
                print lsUserRol
                rol = getRol(lsUserRol)
                print rol





