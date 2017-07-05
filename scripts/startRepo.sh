cd /var/www/html/simi/api
. .venv/bin/activate
python api/reportDjaiAndA1dest.py http://186.33.211.247:89/kie-wb-distribution-wars-6.5.0.Final-wildfly10 admin admin /u01/simi/simi_output 
DESDE=$(date +%Y-%m-%d_17:00:00 -d "yesterday" ) 
HASTA=$(date '+%Y-%m-%d_17:00:00')
python api/parseAprobadoAndSend.py /u01/simi/scripts/config.ini $DESDE $HASTA APROBADO /u01/simi/scripts/emailsprueba.csv
python api/parseAprobadoAndSend.py /u01/simi/scripts/config.ini $DESDE $HASTA CAUTELAR /u01/simi/scripts/emailsprueba.csv
