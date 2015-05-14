##fixed parameters
#openerp
OE_USER="odoo"
OE_HOME="/opt/$OE_USER"
OE_HOME_EXT="/opt/$OE_USER/$OE_USER-server"
#Enter version for checkout "8.0" for version 8.0, "7.0 (version 7), saas-4, saas-5 (opendays version) and "master" for trunk
OE_VERSION="8.0"
#set the superadmin password
OE_SUPERADMIN="vladimir"
OE_CONFIG="$OE_USER-server"
OE_CONFIG_debug="$OE_USER-server-d"
OE_HOST="lafamosa.yugla.com"
OE_DATABASE="lafamosa.yugla.com"

#--------------------------------------------------
# Update Server
#--------------------------------------------------
echo -e "\n---- Update Server ----"
sudo apt-get update
sudo apt-get upgrade -y
#--------------------------------------------------
# Install PostgreSQL Server
#--------------------------------------------------
echo -e "\n---- Install PostgreSQL Server ----"
sudo apt-get install postgresql -y
echo -e "\n---- PostgreSQL $PG_VERSION Settings ----"
sudo sed -i s/"#listen_addresses = 'localhost'"/"listen_addresses = '*'"/g /etc/postgresql/9.3/main/postgresql.conf
echo -e "\n---- Creating the ODOO PostgreSQL User ----"
sudo su - postgres -c "createuser -s $OE_USER" 2> /dev/null || true
#--------------------------------------------------
# Install Dependencies
#--------------------------------------------------
echo -e "\n---- Install tool packages ----"
sudo apt-get install wget subversion git bzr bzrtools python-pip -y
echo -e "\n---- Install python packages ----"
sudo apt-get install python-dateutil python-feedparser python-ldap python-libxslt1 python-lxml python-mako python-openid python-psycopg2 python-pybabel python-pychart python-pydot python-pyparsing python-reportlab python-simplejson python-tz python-vatnumber python-vobject python-webdav python-werkzeug python-xlwt python-yaml python-zsi python-docutils python-psutil python-mock python-unittest2 python-jinja2 python-pypdf python-decorator python-requests python-passlib python-pil -y
echo -e "\n---- Install python libraries ----"
sudo pip install gdata
echo -e "\n---- Install wkhtml and place on correct place for ODOO 8 ----"
sudo wget http://downloads.sourceforge.net/project/wkhtmltopdf/archive/0.12.1/wkhtmltox-0.12.1_linux-trusty-amd64.deb
sudo dpkg -i wkhtmltox-0.12.1_linux-trusty-amd64.deb
sudo cp /usr/local/bin/wkhtmltopdf /usr/bin
sudo cp /usr/local/bin/wkhtmltoimage /usr/bin
echo -e "\n---- Create ODOO system user ----"
sudo adduser --system --quiet --shell=/bin/bash --home=$OE_HOME --gecos 'ODOO' --group $OE_USER
echo -e "\n---- Create Log directory ----"
sudo mkdir /var/log/$OE_USER
sudo chown $OE_USER:$OE_USER /var/log/$OE_USER

echo -e "\n==== Installing ODOO Server ===="
sudo git clone --branch $OE_VERSION https://www.github.com/odoo/odoo $OE_HOME_EXT/

echo -e "\n---- Create custom module directory ----"
sudo su $OE_USER -c "mkdir $OE_HOME/addons/"
sudo su $OE_USER -c "mkdir $OE_HOME/addons/yelizariev_pos"
sudo su $OE_USER -c "mkdir $OE_HOME/addons/yelizariev_main"
sudo su $OE_USER -c "mkdir $OE_HOME/addons/oca_server-tools"
sudo su $OE_USER -c "mkdir $OE_HOME/addons/viktor_main"
sudo su $OE_USER -c "mkdir $OE_HOME/addons/addons-extra"

git clone https://github.com/yelizariev/pos-addons.git $OE_HOME/addons/yelizariev_pos/
git clone https://github.com/yelizariev/addons-yelizariev.git $OE_HOME/addons/yelizariev_main/
git clone https://github.com/OCA/server-tools.git $OE_HOME/addons/oca_server-tools/
git clone https://github.com/straga/odoo_addons-viktor.git $OE_HOME/addons/viktor_main/
git clone https://github.com/straga/odoo-addon_fts.git $OE_HOME/addons/addons-extra/



echo -e "\n---- Setting permissions on home folder ----"
sudo chown -R $OE_USER:$OE_USER $OE_HOME/*

echo -e "* Create server config file"
sudo cp $OE_HOME_EXT/debian/openerp-server.conf /etc/$OE_CONFIG.conf
sudo chown $OE_USER:$OE_USER /etc/$OE_CONFIG.conf
sudo chmod 640 /etc/$OE_CONFIG.conf

echo -e "* Create server config file debug"
sudo cp $OE_HOME_EXT/debian/openerp-server.conf /etc/$OE_CONFIG_debug.conf
sudo chown $OE_USER:$OE_USER /etc/$OE_CONFIG_debug.conf
sudo chmod 640 /etc/$OE_CONFIG_debug.conf
a


echo -e "* Change server config file"
sudo sed -i s/"db_user = .*"/"db_user = $OE_USER"/g /etc/$OE_CONFIG.conf
sudo sed -i s/"; admin_passwd.*"/"admin_passwd = $OE_SUPERADMIN"/g /etc/$OE_CONFIG.conf
sudo su root -c "echo 'logfile = /var/log/$OE_USER/$OE_CONFIG$1.log' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '#dbfilter = ^%h$' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'addons_path=$OE_HOME/addons/addons-extra,$OE_HOME_EXT/addons,$OE_HOME/addons/yelizariev_main,$OE_HOME/addons/yelizariev_pos,$OE_HOME/addons/oca_server-tools,$OE_HOME/addons/viktor_main' >> /etc/$OE_CONFIG.conf"

echo -e "* Change server config file for debug"
sudo sed -i s/"db_user = .*"/"db_user = $OE_USER"/g /etc/$OE_CONFIG_debug.conf
sudo sed -i s/"; admin_passwd.*"/"admin_passwd = $OE_SUPERADMIN"/g /etc/$OE_CONFIG_debug.conf
sudo su root -c "echo '#dbfilter = ^%h$' >> /etc/$OE_CONFIG_debug.conf"
sudo su root -c "echo 'addons_path=$OE_HOME/addons/addons-extra,$OE_HOME_EXT/addons,$OE_HOME/addons/yelizariev_main,$OE_HOME/addons/yelizariev_pos,$OE_HOME/addons/oca_server-tools,$OE_HOME/addons/viktor_main' >> /etc/$OE_CONFIG_debug.conf"

#echo -e "* Create startup file"
#sudo su root -c "echo '#!/bin/sh' >> $OE_HOME_EXT/start.sh"
#sudo su root -c "echo 'sudo -u $OE_USER $OE_HOME_EXT/openerp-server --config=/etc/$OE_CONFIG.conf' >> $OE_HOME_EXT/start.sh"
#sudo chmod 755 $OE_HOMEsudo su root_EXT/start.sh

#--------------------------------------------------
# Adding ODOO as a deamon (initscript)
#--------------------------------------------------
sudo service $OE_CONFIG stop
sudo rm /etc/init.d/$OE_CONFIG

echo -e "* Create init file"
echo '#!/bin/sh' >> ~/$OE_CONFIG
echo '### BEGIN INIT INFO' >> ~/$OE_CONFIG
echo '# Provides: $OE_CONFIG' >> ~/$OE_CONFIG
echo '# Required-Start: $remote_fs $syslog' >> ~/$OE_CONFIG
echo '# Required-Stop: $remote_fs $syslog' >> ~/$OE_CONFIG
echo '# Should-Start: $network' >> ~/$OE_CONFIG
echo '# Should-Stop: $network' >> ~/$OE_CONFIG
echo '# Default-Start: 2 3 4 5' >> ~/$OE_CONFIG
echo '# Default-Stop: 0 1 6' >> ~/$OE_CONFIG
echo '# Short-Description: Enterprise Business Applications' >> ~/$OE_CONFIG
echo '# Description: ODOO Business Applications' >> ~/$OE_CONFIG
echo '### END INIT INFO' >> ~/$OE_CONFIG
echo 'PATH=/bin:/sbin:/usr/bin' >> ~/$OE_CONFIG
echo "DAEMON=$OE_HOME_EXT/openerp-server" >> ~/$OE_CONFIG
echo "NAME=$OE_CONFIG" >> ~/$OE_CONFIG
echo "DESC=$OE_CONFIG" >> ~/$OE_CONFIG
echo '' >> ~/$OE_CONFIG
echo '# Specify the user name (Default: odoo).' >> ~/$OE_CONFIG
echo "USER=$OE_USER" >> ~/$OE_CONFIG
echo '' >> ~/$OE_CONFIG
echo '# Specify an alternate config file (Default: /etc/openerp-server.conf).' >> ~/$OE_CONFIG
echo "CONFIGFILE=\"/etc/$OE_CONFIG.conf\"" >> ~/$OE_CONFIG
echo '' >> ~/$OE_CONFIG
echo '# pidfile' >> ~/$OE_CONFIG
echo 'PIDFILE=/var/run/$NAME.pid' >> ~/$OE_CONFIG
echo '' >> ~/$OE_CONFIG
echo '# Additional options that are passed to the Daemon.' >> ~/$OE_CONFIG
echo 'DAEMON_OPTS="-c $CONFIGFILE"' >> ~/$OE_CONFIG
echo '[ -x $DAEMON ] || exit 0' >> ~/$OE_CONFIG
echo '[ -f $CONFIGFILE ] || exit 0' >> ~/$OE_CONFIG
echo 'checkpid() {' >> ~/$OE_CONFIG
echo '[ -f $PIDFILE ] || return 1' >> ~/$OE_CONFIG
echo 'pid=`cat $PIDFILE`' >> ~/$OE_CONFIG
echo '[ -d /proc/$pid ] && return 0' >> ~/$OE_CONFIG
echo 'return 1' >> ~/$OE_CONFIG
echo '}' >> ~/$OE_CONFIG
echo '' >> ~/$OE_CONFIG
echo 'case "${1}" in' >> ~/$OE_CONFIG
echo 'start)' >> ~/$OE_CONFIG
echo 'echo -n "Starting ${DESC}: "' >> ~/$OE_CONFIG
echo 'start-stop-daemon --start --quiet --pidfile ${PIDFILE} \' >> ~/$OE_CONFIG
echo '--chuid ${USER} --background --make-pidfile \' >> ~/$OE_CONFIG
echo '--exec ${DAEMON} -- ${DAEMON_OPTS}' >> ~/$OE_CONFIG
echo 'echo "${NAME}."' >> ~/$OE_CONFIG
echo ';;' >> ~/$OE_CONFIG
echo 'stop)' >> ~/$OE_CONFIG
echo 'echo -n "Stopping ${DESC}: "' >> ~/$OE_CONFIG
echo 'start-stop-daemon --stop --quiet --pidfile ${PIDFILE} \' >> ~/$OE_CONFIG
echo '--oknodo' >> ~/$OE_CONFIG
echo 'echo "${NAME}."' >> ~/$OE_CONFIG
echo ';;' >> ~/$OE_CONFIG
echo '' >> ~/$OE_CONFIG
echo 'restart|force-reload)' >> ~/$OE_CONFIG
echo 'echo -n "Restarting ${DESC}: "' >> ~/$OE_CONFIG
echo 'start-stop-daemon --stop --quiet --pidfile ${PIDFILE} \' >> ~/$OE_CONFIG
echo '--oknodo' >> ~/$OE_CONFIG
echo 'sleep 1' >> ~/$OE_CONFIG
echo 'start-stop-daemon --start --quiet --pidfile ${PIDFILE} \' >> ~/$OE_CONFIG
echo '--chuid ${USER} --background --make-pidfile \' >> ~/$OE_CONFIG
echo '--exec ${DAEMON} -- ${DAEMON_OPTS}' >> ~/$OE_CONFIG
echo 'echo "${NAME}."' >> ~/$OE_CONFIG
echo ';;' >> ~/$OE_CONFIG
echo '*)' >> ~/$OE_CONFIG
echo 'N=/etc/init.d/${NAME}' >> ~/$OE_CONFIG
echo 'echo "Usage: ${NAME} {start|stop|restart|force-reload}" >&2' >> ~/$OE_CONFIG
echo 'exit 1' >> ~/$OE_CONFIG
echo ';;' >> ~/$OE_CONFIG
echo '' >> ~/$OE_CONFIG
echo 'esac' >> ~/$OE_CONFIG
echo 'exit 0' >> ~/$OE_CONFIG


echo -e "* Security Init File"
sudo mv ~/$OE_CONFIG /etc/init.d/$OE_CONFIG
sudo chmod 755 /etc/init.d/$OE_CONFIG
sudo chown root: /etc/init.d/$OE_CONFIG
echo -e "* Start ODOO on Startup"
sudo update-rc.d $OE_CONFIG defaults
sudo service $OE_CONFIG start


#--------------------------------------------------
# NGINX
#--------------------------------------------------
sudo apt-get install nginx -y

echo 'server {' >> ~/$OE_CONFIG
echo '		listen 80;' >> ~/$OE_CONFIG
sudo su root -c "echo 'server_name $OE_HOST;' >> ~/$OE_CONFIG"
echo '		charset utf-8;' >> ~/$OE_CONFIG
sudo su root -c "echo '	access_log  /var/log/nginx/$OE_DATABASE.ac.log;' >> ~/$OE_CONFIG"
sudo su root -c "echo '	error_log   /var/log/nginx/$OE_DATABASE.er.log;' >> ~/$OE_CONFIG"
echo '		location / {' >> ~/$OE_CONFIG
echo '			proxy_pass         http://127.0.0.1:8069/;' >> ~/$OE_CONFIG
echo '			proxy_redirect     off;' >> ~/$OE_CONFIG
echo '			proxy_set_header   Host             $host;' >> ~/$OE_CONFIG
echo '			proxy_set_header   X-Real-IP        $remote_addr;' >> ~/$OE_CONFIG
echo '			proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;' >> ~/$OE_CONFIG
sudo su root -c "echo '		proxy_set_header   X-OpenERP-dbfilter $OE_DATABASE;' >> ~/$OE_CONFIG"
echo '			client_max_body_size       200m;' >> ~/$OE_CONFIG
echo '			#    proxy_connect_timeout      90;' >> ~/$OE_CONFIG
echo '			#    proxy_send_timeout         90;' >> ~/$OE_CONFIG
echo '			#    proxy_read_timeout         90;' >> ~/$OE_CONFIG
echo '			proxy_buffer_size          128k;' >> ~/$OE_CONFIG
echo '			proxy_buffers              16 64k;' >> ~/$OE_CONFIG
echo '			#    proxy_busy_buffers_size    64k;' >> ~/$OE_CONFIG
echo '			#    proxy_temp_file_write_size 64k;' >> ~/$OE_CONFIG
echo '		 }' >> ~/$OE_CONFIG
echo '		# Static files location' >> ~/$OE_CONFIG
echo '		#location ~* ^.+.(jpg|jpeg|gif|png|ico|css|zip|tgz|gz|rar|bz2|doc|xls|exe|pdf|ppt|txt|tar|mid|midi|wav|bmp|rtf|js)$ {' >> ~/$OE_CONFIG
echo '		#    root   /spool/www/members_ng;' >> ~/$OE_CONFIG
echo '		#}' >> ~/$OE_CONFIG
echo '	}' >> ~/$OE_CONFIG
sudo rm /etc/nginx/sites-available/$OE_CONFIG.conf
sudo mv ~/$OE_CONFIG /etc/nginx/sites-available/$OE_CONFIG.conf
sudo chmod 755 /etc/nginx/sites-available/$OE_CONFIG.conf
sudo chown root: /etc/nginx/sites-available/$OE_CONFIG.conf

sudo rm /etc/nginx/sites-enabled/$OE_CONFIG.conf 
sudo ln -s /etc/nginx/sites-available/$OE_CONFIG.conf /etc/nginx/sites-enabled/$OE_CONFIG.conf 
sudo service nginx restart
                  
               
echo "Done! The ODOO server can be started with: service $OE_CONFIG start".

