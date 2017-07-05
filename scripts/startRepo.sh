. .venv/bin/activate
python api/reportDjaiAndA1dest.py http://186.33.211.247:89/kie-wb-distribution-wars-6.5.0.Final-wildfly10 admin admin /home/rburdet/miprod/simi_output 
DESDE=$(date +%Y-%m-%d_17:00:00 -d "yesterday" ) 
HASTA=$(date '+%Y-%m-%d_17:00:00')
python api/parseAprobadoAndSend.py config.ini $DESDE $HASTA APROBADO emailsprueba.csv
python api/parseAprobadoAndSend.py config.ini $DESDE $HASTA CAUTELAR emailsprueba.csv
