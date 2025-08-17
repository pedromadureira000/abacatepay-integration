# Deployment in production
## connect ssh
```
chmod 400 ~/.ssh/your_key.pem
ssh -i ~/.ssh/your_key.pem ubuntu@<ip>
```

## Check system version
```
cat /etc/os-release
lsb_release -a
```

## Update system packages
```
sudo apt-get update && sudo apt-get -y upgrade
```

## Install Python 3 build tools
```
sudo apt install -y python3-pip python3-dev libpq-dev
```

## Install other stuff
```
sudo apt install -y make nginx curl neovim unzip
```

## Confirm GCC version:
```
gcc --version
```

## install venv package (whatever version is the one the system is using)
```
sudo apt install -y python3.12-venv
```

## Install docker and postgres client
```
sudo apt install -y docker.io postgresql-client-common postgresql-client
```

## Configure git
```
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
cd ~/.ssh
ssh-keygen -t ed25519 -C "your.email@example.com"
sudo chmod 400 ~/.ssh/id_ed25519
sudo chmod 400 ~/.ssh/id_ed25519.pub
```
* Add public key in github ssh keys as Authentication key 
link: https://github.com/settings/keys
```
cat ~/.ssh/id_ed25519.pub
```

## Add SSH Key to SSH Agent: Start the SSH agent if it's not already running, then add your SSH private key to it
```
eval `ssh-agent -s` && ssh-add ~/.ssh/id_ed25519
```

## test if it's working
```
ssh -T git@github.com
```

## Clone the project
```
cd
git clone git@github.com:pedromadureira000/abacatepay-integration.git
```

## Run Postgres container
-----------------------------------------
You must run this in the same folder where the 'docker-compose.yml' file is.

### install compose manually (if `docker-compose` command doesn't work)
* To download and install the Compose CLI plugin, adding it to all users, run:
```
DOCKER_CONFIG=${DOCKER_CONFIG:-/usr/local/lib/docker}
sudo mkdir -p $DOCKER_CONFIG/cli-plugins
```
* download correct version for your server's architecture (e.g., arm64 for EC2 t4g, x86_64 for EC2 t2)
```
# For arm64
sudo curl -SL https://github.com/docker/compose/releases/download/v2.27.0/docker-compose-linux-aarch64 -o $DOCKER_CONFIG/cli-plugins/docker-compose

# For x86_64
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
cd /home/ubuntu/abacatepay-integration
sudo docker compose up -d
```

## Connect to default database and create the database that you will use
```
psql postgres://phsw:senhasegura@localhost:5432/postgres
create database abacatepay_db;
\q
```

## Initial project settings
```
cd /home/ubuntu/abacatepay-integration
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env # Assuming .env.example exists
nvim .env # Edit your environment variables
```

## Create initial user
```
make create-user
```

Create systemd service for Uvicorn
-----------------------------------------

* Create the file with:

```
sudo nvim /etc/systemd/system/abacatepay.service
```

* Then copy this to that file. This will run Uvicorn with 3 workers listening on a local port.

```
[Unit]
Description=Uvicorn instance to serve abacatepay-integration
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/abacatepay-integration
ExecStart=/home/ubuntu/abacatepay-integration/.venv/bin/uvicorn src.main:app --host 127.0.0.1 --port 8000 --workers 3

[Install]
WantedBy=multi-user.target
```

Start and enable the Uvicorn service
-----------------------------------------
```
sudo systemctl start abacatepay.service
sudo systemctl enable abacatepay.service
sudo systemctl status abacatepay.service
```

Check the Uvicorn service's logs 
-----------------------------------------
```
sudo journalctl -u abacatepay.service -f
```

If you make changes to the `/etc/systemd/system/abacatepay.service` file, reload the daemon and restart the service:
-----------------------------------------
```
sudo systemctl daemon-reload
sudo systemctl restart abacatepay.service
```

## Configure Nginx to Proxy Pass to Uvicorn

* Create the file

```
sudo nvim /etc/nginx/sites-available/abacatepay
```

* Paste the nginx configuration code, and edit the `server_name` with your server IP or domain.
```
server {
        listen 80;
        server_name your_server_ip_or_domain;

        location / {
                include proxy_params;
                proxy_pass http://127.0.0.1:8000;
        }
}
```

Enable the file by linking it to the sites-enabled directory:
-----------------------------------------

```
sudo ln -s /etc/nginx/sites-available/abacatepay /etc/nginx/sites-enabled
```

Test for syntax errors
-----------------------------------------
```
sudo nginx -t
```

Restart nginx
-----------------------------------------
```
sudo systemctl restart nginx
```

If Nginx fails to start, check its status and logs for errors.
-----------------------------------------
```
sudo systemctl status nginx
sudo journalctl -u nginx
```

Install SSL and set domain
-----------------------------------------
*OBS: Don't use UFW on cloud providers like AWS unless you configure it to allow SSH (port 22). You might lose SSH access.*

For a detailed guide on securing Nginx with Let's Encrypt, follow this tutorial:
https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-22-04

After setting up SSL, your Nginx config file will be modified by Certbot. Remember to restart the services if you make manual changes.
`
sudo nvim /etc/nginx/sites-available/abacatepay
sudo systemctl restart nginx
sudo systemctl restart abacatepay.service
`
