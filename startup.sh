cd /var/www/html/simi/api
. .venv/bin/activate
python api/api.py simi Simi.T.7102 simidb 192.168.150.101 192.168.150.101 simi Simi.T.7102 jbpmdb &
echo  > /tmp/api_simi.pid 
