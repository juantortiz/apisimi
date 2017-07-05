import csv
import sys
import os
import smtplib
import mimetypes
import mysql.connector
import ConfigParser
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from dateutil.parser import parse as date_parse
from datetime import datetime, timedelta,date


attachs = []
dbuser = dbpass = db = emailfrom = emailto = username = password = smtp = dirtosearch =  ""

def init_config(configFile,emailfile):
    config = ConfigParser.ConfigParser()
    config.read(configFile)
    global emailfrom
    global emailto
    global username
    global password
    global smtp
    global dirtosearch
    global dbuser
    global dbpass
    global db
    global dbhost
    emailfrom = config.get('SMTP','emailfrom')
    username = config.get('SMTP','username')
    password = config.get('SMTP','password')
    smtp = config.get('SMTP','smtp')
    dirtosearch = config.get('GLOBAL','dirtosearch')
    dbuser = config.get('DB','dbusername')
    dbpass = config.get('DB','dbpassword')
    db = config.get('DB','db')
    dbhost = config.get('DB','dbhost')
    emailto = get_emails(emailfile)

def get_emails(filename):
    reader = csv.reader(open(filename))
    emails = []
    for row in reader:
        emails.append(str(row[0]))
    return emails

def get_fechas(fechadesde,fechahasta):
    fechas = []
    desde = datetime.strptime(fechadesde, '%Y-%m-%d_%H:%M:%S').date()
    hasta = datetime.strptime(fechahasta, '%Y-%m-%d_%H:%M:%S').date()
    delta = hasta - desde         # timedelta
    for i in range(delta.days + 1):
        aux = desde+timedelta(days=i)
        fechas.append(aux.strftime("%Y-%m-%d_00:00:00"))
    return fechas


def attach_files(msg):
    for i in attachs:
        attach_file(msg,i)


def attach_file(msg,filetoattach):
    ctype, encoding = mimetypes.guess_type(filetoattach)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"

    maintype, subtype = ctype.split("/", 1)
    if maintype == "text":
        fp = open(filetoattach)
        # Note: we should handle calculating the charset
        attachment = MIMEText(fp.read(), _subtype=subtype)
        fp.close()
    else:
        fp = open(filetoattach, "rb")
        attachment = MIMEBase(maintype, subtype)
        attachment.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(attachment)
    newfilename = filetoattach[filetoattach.rfind('/')+1:]
    attachment.add_header("Content-Disposition", "attachment", filename=newfilename)
    msg.attach(attachment)


def send_mails(msg):
    server = smtplib.SMTP(smtp)
    server.starttls()
    server.login(username,password)
    server.sendmail(emailfrom, emailto, msg.as_string())
    server.quit()

def create_mails(dia,estado):
    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = ', '.join(emailto)
    subject = "Resumen de simis en el estado "+estado+" al dia " if (len(attachs) > 0) else "No hay simis aprobadas en el dia "
    msg["Subject"] = subject + dia[:dia.find('_')]
    msg.preamble = "Ver adjuntos"
    attach_files(msg)
    return msg




def get_archivos(fechas,dirToSearch):
    archivos = []
    for fecha in fechas:
        fecha = fecha[:fecha.find('_')]
        for i in os.listdir(dirToSearch):
            if os.path.isfile(os.path.join(dirToSearch,i)) and fecha in i:
                archivos.append((dirToSearch+'/'+i,dirToSearch+'/salidasUsuario/'+i))
    return archivos

def a_letra(estado):
    if estado == 'APROBADO':
        return 'A'
    elif estado == 'CAUTELAR':
        return 'C'
    else:
        return ''

def parse_archivos(archivos,estado):
    letraEstado = a_letra(estado)
    for archivo in archivos:
        salida = parse_archivo(archivo,letraEstado)

def write_row(archivo,row):
    archivo = archivo[:archivo.find('csv')]
    archivo = archivo + row[3] + '.csv'
    fd = open(archivo, 'a+')
    writer = csv.writer(fd, delimiter=',')
    writer.writerow([row[0]])
    fd.flush()
    if archivo not in attachs:
        attachs.append(archivo)

def esta_realmente_aprobada(simi):
    cnx = mysql.connector.connect(user=dbuser,password=dbpass, database=db, host = dbhost)
    cursor = cnx.cursor(buffered=True)
    query = ("select vil.id as estado_simi from ProcessInstanceLog as pil join VariableInstanceLog as vil on vil.processinstanceid = pil.processinstanceid and vil.variableId = 'estado_simi'"
                    "join VariableInstanceLog as vil1 on vil1.processinstanceid = pil.processinstanceid and vil1.variableId='djai_id_simi'"
                    "where vil1.value = '"+simi+"' and vil.value='APROBADA';")
    cursor.execute(query,simi)
    leg_no = cursor.fetchall()
    cursor.close()
    cnx.close()
    if len(leg_no) > 0:
        return True
    else:
        return False

def parse_archivo(archivo,estado):
    reader = csv.reader(open(archivo[0]),delimiter=',')
    for row in reader:
        if row[1] == estado:
            if esta_realmente_aprobada(row[0]):
                write_row(archivo[1],row)

if __name__ == '__main__':
    if len(sys.argv) != 6 :
        print("Argumentos incorrectos")
    else:
        init_config(sys.argv[1],sys.argv[5])
        fechadesde = sys.argv[2]
        fechahasta = sys.argv[3]
        estado = sys.argv[4]
        fechas = get_fechas(fechadesde,fechahasta)
        archivos = get_archivos(fechas,dirtosearch)
        parse_archivos(archivos,estado)
        msg = create_mails(fechas[-1],estado)
        send_mails(msg)


