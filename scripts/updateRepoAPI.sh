API_HOME=/var/www/html/simi
TMP_DIR=/tmp/update_api
sudo mkdir -p /tmp/update_api
echo "=================================================="
echo "Instalando key"
echo "=================================================="
cat > /tmp/deploy_key << EOF
-----BEGIN RSA PRIVATE KEY-----
MIIEoAIBAAKCAQEAseRPPev4ia7KC56k/OWkniep0PKLy+BoA4OaTF40nh3VXCYa
/LaxfQaKpdAQAjBhTkdWc5jkyJp6S1PL812MrqqXUVmUW/WskhR+N5AQIubyHxNg
sX96xJEElXzuslAHb30P1FVYO4l2sJIwnMZQ5KfKhR/4gqldblNJSJwG1Ip44CLo
74NsWDeqS8W6VguB3reBL7NSCQOTUEtlSOyW6YZulrkPRRtjiZ/Gnlo55FU+9QdH
tLbvfwVwVw0HX2G9ECpXxfc2FTd335w1zTzuAb6Eqvdv/M2F8zSWHaKLdLwPo6E/
KmcV236OdIuMJ8M2BIgQaPR3scBJE/6AXxurEwIBIwKCAQB05n03Uex3vAEdlCNH
GpC/s6obmBK5LREm4XQGTIj6MNyqRO0pueJZeVPMDGJKlNI6wSoutO4dbNQFnXdl
aVxyx9/HvoYQi4AIOVpBxRHrDMr+enK9yM0E1FN4LYbqNJcsAbnx7vDWqspWxne3
ewH1WFHidBhV3QLiGXlM+NFJ1j5DGRtpr2KUjq/Km3FWui0LtPzKVvi0CW/vV8tA
bvshYMBgFJmKUwpxi8g/oPB94qbDNzv19R4xu7Yn7Sl9rtjJvbPZcILc7xVlWM1v
jct0tuCXHRv1WLzOj+TecbZjWuSYPBm8q/5ogly25/iaP0+zsdWLyHN2BCvVbSQ/
5TJ7AoGBANeHbQiebH72BOsuSJr0WIwe1vFlrijDay0k3YSpuMPaHU5UVDr6EbbK
TcIPc8Ac6JhBHHELllWFX0olhsvMVD87tIMHh9xqpoNwjHZ/XRHHBaF0cXUWQ6jQ
exRPEx1kN3AL5hYDqpck7ffzrQIbmBT/Xbd5ClYvEtLG0448bdp5AoGBANNLpe5A
9casp4cVsfh5jISuD+23gNAzoEyHjzwFf89XDYw1v+qlEN+jOoXrSpyCS2YmrQwc
lVXEOpaQl8TIqmB08Pq2VNVPO2SSDi2kHli1opiTWa72wAu73omztd4VJtRtSXFK
aNotyjXwGV2nAnAVG7rurfdfyIGC0sYafY7rAoGAUA26yK/fJ9e4rx/R0yeOmnHa
zrC9B9OONVbV73I9UA8vdN1+Xwxs+sArgpgGa+169rkZMU1yWkd7KisyES6i8upK
XI3Ev5VTymuh4t7ZbQDHk72JOh42Y0YfFiv/yRaYP49kFs4pa1bcC6OmqQLvWEGX
1m7JUzYOTknZjJoaLJMCgYA2VUfszuAdJRUivG+XqjoTfTdLwXjlFJbvG4s7Ud8J
bigOHHMttWq9KfkbHz8STWPYcFhiMzxX4gBv3AnE4yR/NANzqzpivJo+brMwTsX5
jcq5hPnN562539ojaLm8w5xFQKx8N7SP3+OKNmzsMkJ0l7asaUKtUyTuGlN0xPu3
CQKBgBoujmLvbbK5SsIwtOfZSFrxV3mZ/xxdJKpm5MiBMKB3XFuygWqWzPB0AWC+
rv/ebeaJ6qbvUaGhkXuTVue81mL/vvFOkrAGueW0D3Jy8nXWmh8AvQ9bggxjU8XH
j8UnPd6+1Q5Iwu0HULfizQtr3bES0fK64p8cb5AGZWLU7f7h
-----END RSA PRIVATE KEY-----
EOF
sudo mv /tmp/deploy_key $TMP_DIR/deploy_key
echo '/usr/bin/ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no $*'  > /tmp/ssh_conf
sudo mv /tmp/ssh_conf $TMP_DIR/ssh_conf
sudo chmod 755 $TMP_DIR/ssh_conf
sudo chmod 400 $TMP_DIR/deploy_key
sudo ssh-agent bash -c "ssh-add $TMP_DIR/deploy_key;export GIT_SSH=$TMP_DIR/ssh_conf ;git pull"

