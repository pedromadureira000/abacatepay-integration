# connect ssh
```
chmod 400 ~/.ssh/zap_ass.pem
ssh -i ~/.ssh/zap_ass.pem ubuntu@<ip>
```

# Check system version
```
cat /etc/os-release
lsb_release -a
```

# Update system packages
```
sudo apt-get update && sudo apt-get -y upgrade
```

# Install Python 3 build tools
```
sudo apt install -y python3-pip python3-dev libpq-dev
```

# Install other stuff
```
sudo apt install -y make nginx curl neovim unzip
```

# Confirm GCC version:
```
gcc --version
```

# install venv pacakge(whatever version is the one the system is using)
```
sudo apt install -y python3.12-venv
```

# Install docker and postgres client
```
sudo apt install -y docker.io postgresql-client-common postgresql-client
```

# Configure git
```
git config --global user.name "PedroDev"
git config --global user.email "ph.websolucoes@gmail.com"
cd ~/.ssh
ssh-keygen -t ed25519 -C "ph.websolucoes@gmail.com"
sudo chmod  400 ~/.ssh/id_ed25519
sudo chmod  400 ~/.ssh/id_ed25519.pub
```
* Add public key in github ssh keys as Authentication key 
link: https://github.com/settings/keys
```
cat ~/.ssh/id_ed25519.pub
```

# Add SSH Key to SSH Agent: Start the SSH agent if it's not already running, then add your SSH private key to it
```
eval `ssh-agent -s` && ssh-add ~/.ssh/id_ed25519
```

# test if it's working
```
ssh -T git@github.com
```

# Clone the project
```
cd
git clone git@github.com:pedromadureira000/abacatepay-integration.git
```

# Other configs
```
nvim .bashrc
```

# Aliases to add on .bashrc
```
alias vim='nvim'
alias la='ls -A'
alias du='du -h --max-depth=1'
alias grep='grep --color=auto'
alias ..='cd ..'
alias gc='git commit -m'
alias gC='git checkout'
alias gp='git push'
alias ga='git add'
alias gs='git status'
alias gd='git diff'
alias gl='git log --graph --abbrev-commit'
alias gb='git branch'
alias journal='journalctl -e'
alias used_space='sudo du -h --max-depth=1 | sort -h'
alias cl='clear'
```

# Run Postgres and Redis container
-----------------------------------------
You must run this in the same folder where the 'docker-compose.yml' file is.

## install compose manually (last time docker-compose command didn't worked)
* To download and install the Compose CLI plugin, adding it to all users, run:
```
DOCKER_CONFIG=${DOCKER_CONFIG:-/usr/local/lib/docker}
sudo mkdir -p $DOCKER_CONFIG/cli-plugins
```
* download arm64 version (EC2 tg4) [This is the server I usually use]
```
sudo curl -SL https://github.com/docker/compose/releases/download/v2.27.0/docker-compose-linux-armv6 -o $DOCKER_CONFIG/cli-plugins/docker-compose
```

* download x86_64 version (EC2 t2) [optionally If I use t2]
```
# sudo curl -SL https://github.com/docker/compose/releases/download/v2.27.0/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose
```

* Apply executable permissions to the binary:
```
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
```
* test it
```
docker compose version
```
* finally
```
cd /home/ubuntu/gerador_de_boleto_web
sudo docker compose up -d
```

# Connect to default database and create the database that you will use
```
psql postgres://phsw:senhasegura@localhost:5432/postgres
create database boleto_db;
\q
```

# Initial project settings
```
cd /home/ubuntu/gerador_de_boleto_web
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp contrib/env-sample .env
vim .env
```

# If want to restore db
* make backup
```
docker exec -t <container_name_or_id> pg_dump -U <username> <database_name> > /path/to/backup_file.sql
sudo docker exec -t fully_featured_db pg_dump -U phsw ia_governo > ~/backup_file.sql
```
* get and send file
```
# get file
scp -i ~/.ssh/zap_ass.pem ubuntu@98.80.252.240:/home/ubuntu/backup_file.sql ~/Projects/

# send file
scp -i ~/.ssh/zap_ass.pem ~/Projects/backup_file.sql ubuntu@98.80.252.240:/home/ubuntu/
```
* restore backup
```
cat backup_file.sql | sudo docker exec -i <dockername> psql -U <user> -d <db_name>

# localy
cat ~/Projects/backup_file.sql | sudo docker exec -i lang_saas_db psql -U phsw -d boleto_db

# on server
cat ~/backup_file.sql | sudo docker exec -i lang_saas_db psql -U phsw -d boleto_db
```

# If I created a new DB
```
make create-user
```

Create systemd socket for Gunicorn
-----------------------------------------

* Create the file with:

```
sudo nvim /etc/systemd/system/gunicorn.socket
```

* Then copy this to that file

```
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

Create systemd service for Gunicorn
-----------------------------------------

* Create the file with:

```
sudo nvim /etc/systemd/system/gunicorn.service
```

* Then copy this to that file and edit the user field and working directory path

```
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/gerador_de_boleto_web
ExecStart=/home/ubuntu/gerador_de_boleto_web/.venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock settings.wsgi:application

[Install]
WantedBy=multi-user.target
```

* with 2 vCPUs
```
ExecStart=/home/ubuntu/gerador_de_boleto_web/.venv/bin/gunicorn --access-logfile - --workers 5 --bind unix:/run/gunicorn.sock settings.wsgi:application --threads 2
```

Start and enable the Gunicorn socket
-----------------------------------------
```
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
sudo systemctl status gunicorn.socket
```

Check the Gunicorn socket’s logs 
-----------------------------------------

```
sudo journalctl -u gunicorn.socket
```

Test socket activation
-----------------------------------------

It will be dead. The gunicorn.service will not be active yet since the socket has not yet received any connections

```
sudo systemctl status gunicorn  
```

If you don't receive a html, check the logs. Check your /etc/systemd/system/gunicorn.service file for problems. If you make changes to the /etc/systemd/system/gunicorn.service file, reload the daemon to reread the service definition and restart the Gunicorn process:
-----------------------------------------

```
sudo journalctl -u gunicorn
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
sudo systemctl status gunicorn
```

Configure Nginx to Proxy Pass to Gunicorn
-----------------------------------------
* Create the file

```
sudo nvim /etc/nginx/sites-available/gerador_de_boleto_web
```

* Paste the nginx configuration code, and edit the sever name with your server IP.
```
server {
        listen 80;
        # Above is the server IP
        server_name sentencemining.com;

        location = /favicon.ico { access_log off; log_not_found off; }

        location / {
                include proxy_params;
                proxy_pass http://unix:/run/gunicorn.sock;
        }

        location /static/ {
            autoindex off;
            alias /home/ubuntu/gerador_de_boleto_web/staticfiles/;
	    }

        location /media/ {
            autoindex off;
            alias /home/ubuntu/gerador_de_boleto_web/media/;
            add_header 'Access-Control-Allow-Origin' 'https://app.sentencemining.com';
            add_header 'Access-Control-Allow-Methods' 'GET, OPTIONS';
            add_header 'Access-Control-Allow-Headers' 'accept, authorization, content-type, user-agent, x-csrftoken, x-requested-with';
        }
}
```

Enable the file by linking it to the sites-enabled directory:
-----------------------------------------

```
sudo ln -s /etc/nginx/sites-available/gerador_de_boleto_web /etc/nginx/sites-enabled
```

Test for syntax errors
-----------------------------------------
test it
```
sudo nginx -t
```

Restart nginx
-----------------------------------------

```
sudo systemctl restart nginx
```

Nginx serve static file and got 403 forbidden Problem
-----------------------------------------
* add permission (first try)
```
sudo chown -R :www-data /home/ubuntu/gerador_de_boleto_web/staticfiles
sudo chown -R :www-data /home/ubuntu/gerador_de_boleto_web/media
```
* add permission (second try)
```
sudo usermod -a -G ubuntu www-data  # (adds the user "nginx" to the "ubuntu" group without removing them from their existing groups)
chmod 710 /home/ubuntu 
```

Restart nginx
-----------------------------------------

```
sudo systemctl restart nginx
sudo systemctl reload nginx
sudo systemctl status nginx
```

Install SSL and set domain (22-04)
-----------------------------------------
*OBS: Don't use UFW (You might lost SSH access 💀💀💀)*

* https://saturncloud.io/blog/recovering-ssh-access-to-amazon-ec2-instance-after-accidental-ufw-firewall-activation/
https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-22-04

## Checking stuff
* Check ubuntu version
```
lsb_release -a
```
* check ALLOWED_HOSTS on settings.py (add the domain name)
* Check server_name on nginx config file
`
sudo vim /etc/nginx/sites-available/gerador_de_boleto_web
sudo systemctl restart nginx
sudo systemctl restart gunicorn
`

## Installing Certbot 
* make sure your snapd core is up to date
```
sudo snap install core; sudo snap refresh core
```
* Make sure certbot is in the correct version
```
sudo apt remove certbot
sudo snap install --classic certbot
```

## Point the A register from your domain to ec2 instance IP

## Delete any AAAA register, because certbot will try to use it instead of A @ register

## Obtaining an SSL Certificate
* run it (with nginx plugin)
```
sudo certbot --nginx -d sentencemining.com
```

## Verifying Certbot Auto-Renewal
```
sudo systemctl status snap.certbot.renew.service
sudo certbot renew --dry-run
```

## On Cloundflare: Change domain ssl config to Full SSL encryption  (not the restric option)
