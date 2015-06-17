# How to setup new Ubuntu web server

This manual provide information about how to setup Ubuntu server to work as web server. I personally use **Python** language to bild my applications with **Django framework**. But you can find useful informaton for your use case, for example - you learn how to setup **Postfix to send emails** from your server to real users.


### Prepare server to work

On local Linux/Mac:
 * generate ssh key (if you don't have one): `ssh-keygen -t rsa`
 * copy key to use on server `cat ~/.ssh/id_rsa.pub`
 * connect to server via ssh `ssh username@ip-address`

On server (Ubuntu):
 * add your SSH key to your server `.ssh/known_hosts` (that you copied before)
 * disconnect from server and try connect again `ssh username@ip-address` (should not ask for password)
 * `sudo apt-get update && sudo apt-get upgrade`
 * `sudo apt-get install python-pip python-dev nginx git memcached`
 * `sudo apt-get install libjpeg-dev` - to work with images *(also possible libs `libtiff5-dev  zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk`)*

#### Install database

**Postgres**
```shell
sudo apt-get install postgresql postgresql-contrib libpq-dev

# create database for your website
sudo su - postgres
psql

# > CREATE DATABASE `myproject` DEFAULT CHARACTER SET utf8;
# > CREATE USER myprojectuser WITH PASSWORD 'password';
# > GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;
# > \q

# return to original user
exit
```

**MySQL**
```shell
sudo apt-get install mysql-server libmysqlclient-dev
sudo mysql_install_db && sudo mysql_secure_installation

# create database for your website
mysql -u root -p

# > CREATE DATABASE `myproject` DEFAULT CHARACTER SET utf8;
# > CREATE USER myprojectuser@localhost IDENTIFIED BY 'password';
# > GRANT ALL PRIVILEGES ON myproject.* TO myprojectuser@localhost;
# > FLUSH PRIVILEGES;
# > \q

# fix problem with timezone like this "Database returned an invalid value in QuerySet.dates()"
mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root -p mysql
```

You can restore your database from dump if you migrate data from old server.

#### Use virtualenv

This allow you to work with multiple projects on a single server. You can install different versions of django or other python packages on the same server. For example, project1 can work on django 1.6 and project2 can work on django 1.8.

Install python virtualenv:

```shell
sudo pip install virtualenv virtualenvwrapper
nano ~/.bashrc

# add this line to end of file:
# source /usr/local/bin/virtualenvwrapper.sh
# save and close file (Ctrl + X then Y)

# apply changes to use autocomplitions
source ~/.bashrc
```

Create new virtual environment for your website: `mkvirtualenv projectname`. To switch virtualenv to your project - type `workon projectname`.

#### Clone git repo

```shell
# setup SSH key and add this server public key to github/bitbucket
ssh-keygen -t rsa
cat ~/.ssh/id_rsa.pub
```

```shell
# clone your project to your user directory
git clone git@github.com:username/projectname.git
cd ~/projectname
pip install -r requirements.txt
pip install gunicorn
```

#### Prepare Django project to work (optional)

Edit 'local_settings.py' of your django project:
 * add database settings in `DATABASES` section
 * `STATIC_ROOT = os.path.join(BASE_DIR, "static/")`
 * be sure that your `settings.py` include `local_settings.py`

Make migrations:
```shell
chmod +x manage.py

# you don't need to run these commands if you restored database from dump
./manage.py makemigrations
./manage.py migrate
./manage.py createsuperuser
./manage.py collectstatic
```

Test django project in work. Run `./manage.py runserver 0.0.0.0:8000` and open your website `http://ip-address:8000`


### Setup gunicorn and nginx

Run website to be served via gunicorn:

```shell
cd ~/myproject
gunicorn --bind 0.0.0.0:8000 myproject.wsgi:application
```

Visit your website `http://ip-address:8000` to test it in work. After this press `Ctrl + X` to exit from gunicorn session. Then run `deactivate` to exit from project virtualenv.

Edit file `sudo nano /etc/init/gunicorn.conf` and paste this content ()replace `projectname` and `user` to correct values):
```
description "Gunicorn application server handling projectname"

start on runlevel [2345]
stop on runlevel [!2345]

respawn
setuid user
setgid www-data
chdir /home/user/projectname

exec /home/user/.virtualenvs/projectname/bin/gunicorn --workers 3 --bind unix:/home/user/projectname/projectname.sock projectname.wsgi:application
```

Start gunicorn `sudo service gunicorn start`.

#### Configure Nginx to Proxy Pass to Gunicorn


Edit file `` and add this line

Paste content to this file `sudo nano /etc/nginx/sites-available/projectname`:
```
server {
    listen 80;
    server_name server_domain_or_IP;
    # limit on upload file (up to 10 MB)
    client_max_body_size 10M;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/user/projectname;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/user/projectname/projectname.sock;
    }
}
```

Next steps:
 * save this file
 * enable this new website with command: `sudo ln -s /etc/nginx/sites-available/projectname /etc/nginx/sites-enabled`
 * test that nginx configured without errors: `sudo nginx -t`
 * restart nginx: `sudo service nginx restart`
 * visit your website


Read:
 * [How To Set Up Django with Postgres, Nginx, and Gunicorn on Ubuntu 14.04](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-14-04)
 * [How To Add and Delete Users on an Ubuntu 14.04 VPS](https://www.digitalocean.com/community/tutorials/how-to-add-and-delete-users-on-an-ubuntu-14-04-vps)


### Send email with POSTFIX

```shell
sudo apt-get update
sudo apt-get install postfix
```

Use your real hostname, for example: `mywebsite.com`

Edit lines (use your hostname): `sudo nano /etc/postfix/main.cf`

```
myhostname = mywebsite.com
virtual_alias_maps = hash:/etc/postfix/virtual
```

Add mapping for emails that you want to redirect: `sudo nano /etc/postfix/virtual`

```
info@mywebsite.com    admin office
order@mywebsite.com   admin office sales
support@mywebsite.com admin
```

And add appropriate "aliases" for recipient addresses: `sudo nano /etc/aliases`

```
# See man 5 aliases for format
postmaster:    root
admin:         admin@gmail.com
sales:         sales@gmail.com
office:        office@gmail.com
```

Compile emails database AND restart postfix:

```shell
sudo postmap /etc/postfix/virtual
sudo service postfix restart
```

Read: [How To Install and Setup Postfix on Ubuntu 14.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-setup-postfix-on-ubuntu-14-04)
