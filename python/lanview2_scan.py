import nmap
import subprocess
import time
import pymysql
from getmac import get_mac_address

import lanview2_config as conf

def get_all_macs():
    seen_macs = []

    db = pymysql.connect(host=conf.db_host,port=conf.db_port,user=conf.db_user,passwd=conf.db_pass,db=conf.db_name)
    handle = db.cursor()

    handle.execute("""SELECT mac FROM hosts""")

    for record in handle.fetchall():
        seen_macs.append(record[0])

    return seen_macs

def get_by_mac(mac):
    db = pymysql.connect(host=conf.db_host,port=conf.db_port,user=conf.db_user,passwd=conf.db_pass,db=conf.db_name)
    handle = db.cursor()

    handle.execute("""SELECT * FROM hosts WHERE mac = %s""", [mac])
    handle.fetchall()

    if handle.rowcount == 0:
        return False
    else:
        return True

    db.close()

def insert_new(db_data):
    db = pymysql.connect(host=conf.db_host,port=conf.db_port,user=conf.db_user,passwd=conf.db_pass,db=conf.db_name)
    handle = db.cursor()

    query = """
        INSERT INTO hosts (id, status, mac, ip, hostname, vendor, first_seen, last_seen) 
        VALUES (null, %s, %s, %s, %s, %s, %s, %s);
    """

    try:
        handle.execute(query, db_data)
        db.commit()
    except TypeError as e:
        db.rollback()
        print(e)

    db.close()

def update_rec(db_data):
    db = pymysql.connect(host=conf.db_host,port=conf.db_port,user=conf.db_user,passwd=conf.db_pass,db=conf.db_name)
    handle = db.cursor()

    query = """
        UPDATE hosts SET status = %s, ip = %s, hostname = %s, vendor = %s, last_seen = %s, visible = 0
        WHERE mac = %s;
    """

    try:
        handle.execute(query, db_data)
        db.commit()
    except TypeError as e:
        db.rollback()
        print(e)

    db.close()

def set_down(mac):
    db = pymysql.connect(host=conf.db_host,port=conf.db_port,user=conf.db_user,passwd=conf.db_pass,db=conf.db_name)
    handle = db.cursor()

    handle.execute("""UPDATE hosts SET status = 'down' WHERE mac = %s;""", [mac])
    db.commit()

    db.close()



def netbios_info(ip):
    netbios = subprocess.Popen(('nbtscan', '-q', ip), stdout=subprocess.PIPE)
    hostbyte = subprocess.check_output(('awk', '''{print $2}'''), stdin=netbios.stdout)
    hostname = hostbyte.decode().strip()
        
    if not hostname:
        hostname = 'unknown'

    return hostname


seen_macs = get_all_macs()
down_macs = []
up_macs = []


nm = nmap.PortScanner()
nm.scan(hosts=conf.nm_scan, arguments='-sn')

for host in nm.all_hosts():

    status = nm[host].state()
    ip = nm[host]['addresses']['ipv4']

    if nm[host]['status']['reason'] == "localhost-response":
        mac = get_mac_address(interface="ens160")
        mac = mac.upper()
        vendor = "localhost"
    else:
        mac = nm[host]['addresses']['mac']
        
        try:
            vendor = nm[host]['vendor'][mac]
        except:
            vendor = "unknown"

    hostname = nm[host].hostname()

    if not hostname:
        hostname = netbios_info(ip)

    first_seen = last_seen = int(time.time())

    up_macs.append(mac)

    if get_by_mac(mac):
        db_data = [status, ip, hostname, vendor, last_seen, mac]
        update_rec(db_data)
    else:
        db_data = [status, mac, ip, hostname, vendor, first_seen, last_seen]
        insert_new(db_data)


for address in seen_macs:
    if address not in up_macs:
        down_macs.append(address)

for down_mac in down_macs:
    set_down(down_mac)
