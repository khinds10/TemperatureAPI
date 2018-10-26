# TemperatureAPI
Python Flash API for displaying temperatures as color gradients

### Installation
Clone the project locally on your webserver
Create the Apache configuration to point to this project (Python Flask API)

Required Packages for Python Flash on Apache

sudo apt-get install libapache2-mod-wsgi python-dev python-pip python-pil

sudo a2enmod wsgi
sudo service apache2 restart

pip install flask

<VirtualHost *:80>
    ServerAdmin webmaster@mytempuratureapi.com
    ServerName mytempuratureapi.com
    ServerAlias mytempuratureapi.com
    DocumentRoot /var/www/temperatureapi
    ErrorLog /var/www/temperatureapi/error.log
    CustomLog /var/www/temperatureapi/access.log combined

    WSGIDaemonProcess temperatureapp user=khinds group=khinds threads=5
    WSGIProcessGroup temperatureapp
    WSGIScriptAlias / /var/www/temperatureapi/app.wsgi

    <Directory /var/www/temperatureapi>
           Require all granted
    </Directory>

</VirtualHost>

### Setup
Copy settings-shadow.py to your own version of settings.py with your own values place in

\# device API url for gathering temperatures
deviceLoggerAPI = 'http://mywebsite.net'

\# webroot for the clock wall tablet to show the current house conditions
clockTabletImageRoot = '/var/www/clocktablet/img/'

### Finished!

You can now ask for color gradients for given environment tempuratures

http://mytempuratureapi.com/?temperature=72
http://mytempuratureapi.com/multiple?temperatures=72,23,89

