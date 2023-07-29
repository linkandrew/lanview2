> ### Overview
> This is a simple system I threw together to keep track of devices connected to my network.
> It basically just uses some Python code to scan the network using a nmap module and puts it in a database table.
> Then we use some basic PHP to create a simple interface and you just point your browser at it.
> You will be able to see all devices currently and previously connected to your network.
> This was tested with Ubuntu 20 but should work with almost any Linux distro.
> If you know anything about Linux administration this should be pretty self explainitory.

> ### Prerequisites
> 
> - Linux (Ubuntu 20) 
> - MySQL/Apache/PHP (LAMP Stack)
> - Python3
> - Python PIP (pip3)
>	- nmap (python-nmap)
>	- subprocess
>	- time
>	- pymysql (PyMySQL)
>	- getmac (getmac)

	sudo apt install apache2 mysql-server php libapache2-mod-php php-mysql python3-pip
	sudo pip3 install python-nmap PyMySQL getmac

> ### Installation
>
> - #### Put PHP files on system
>
> You can put these in the Apache document root or user page or somthing like that.
> As long as Apache can display them and the files are all in the same directory.
    
    cp ./php/index.php /var/www/html/index.php
    cp ./php/creds.php /var/www/html/creds.php
    cp ./php/nickname.php /var/www/html/nickname.php
>
> - #### Put Python files on system
>
> These can go wherever, you just need to know where you put them to create the crontab entries.

	cp ./python/lanview2_scan.py /opt/lanview2/lanview2_scan.py
	cp ./python/lanview2_expire.py /opt/lanview2/lanview2_expire.py
	cp ./python/lanview2_config.py /opt/lanview2/lanview2_config.py
>
> - #### Update config files and passwords (optional)
> 
> The config that must be changed is in the Python script config file and that is the network range to scan.
> It is in the lanview2_config file and will likley not be the same addressing that I use.
>
> Also before you run the SQL script you can change the default passwords I added to the database accounts.
> You will obviously need to update them to whatever you change them to in the config files for both Python and PHP scripts.
> I just randomly created these passwords and they are pretty short, so I would suggest doing this as it is a public reepo and all.
>
> - #### Create database and table
>
> Just run the MySQL script as the database admin/root user.

	mysql -u root -p < lanview2.sql
	(Enter Password)
    
> - #### Update crontab
>
> Add two entries. One for the scan and one for the expiration.
> This must be done using the root users crontab so the scan runs as root (yea, yea, I know).
> If you do not run this as root the nmap scan will not get as much information.
> The most frequent I woud run this is every 5 minutes since it takes a bit to run the scan.

	*/10 * * * * /usr/bin/python3 /opt/lanview2/lanview2_scan.py >> /var/log/lanview2.log 2>&1
	0 0 * * * /usr/bin/python3 /opt/lanview2/lanview2_expire.py

> ### Usage
> 
> - Check log
> - Browser to index.php (or whatever)
> - Buttons to view list types

