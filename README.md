> ### Overview
>

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

> ### Installation
>
> - Update network info and passwords (optional)
> - Create database and table
> - Put Python files on system

	```
	cp ./lanview_scan.py /opt/lanview2/lanview2_scan.py
	cp ./lanview_expire.py /opt/lanview2/lanview2_expire.py
	```

	These can go wherever, you just need to know where you put them to create the crontab entries.

> - Update Crontab
	Add two entries. One for the scan and one for the expiration.
	This must be done using the root users crontab so the scan runs as root (yea, yea, I know).
	If you do not run this as root the nmap scan will not get as much information.

	```
	*/10 * * * * /usr/bin/python3 /opt/lanview2/lanview2_scan.py >> /var/log/lanview2.log 2>&1
	0 0 * * * /usr/bin/python3 /opt/lanview2/lanview2_expire.py
	```

> ### Usage
> 
> - Check log
> - Browser to index.php (or whatever)
> - Buttons to view list types
