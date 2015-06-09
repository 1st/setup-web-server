# How to setup new Ubuntu web server

This manual provide information about how to setup Ubuntu server to work as web server. I personally use Python language to bild my applications with Django framework. But you can find useful informaton for your use case, for example - you learn how to setup Postfix to send emails from your server to real users.


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

Read more:
 * [How To Install and Setup Postfix on Ubuntu 14.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-setup-postfix-on-ubuntu-14-04)
