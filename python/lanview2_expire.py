import time
import pymysql
import lanview2_config as conf

def get_host_rows():
    db = pymysql.connect(host=conf.db_host,port=conf.db_port,user=conf.db_user,passwd=conf.db_pass,db=conf.db_name)
    handle = db.cursor()

    handle.execute("""SELECT id,last_seen FROM hosts""")

    return handle.fetchall()

    db.close()

def update_row(id):
    db = pymysql.connect(host=conf.db_host,port=conf.db_port,user=conf.db_user,passwd=conf.db_pass,db=conf.db_name)
    handle = db.cursor()

    try:
        handle.execute("""UPDATE hosts SET visible = 1 WHERE id = %s""", [id])
        db.commit()
    except TypeError as e:
        db.rollback()
        print(e)

    db.close()


host_rows = get_host_rows()

for row in host_rows:
    time_diff = int(time.time()) - row[1]
    
    #if(time_diff > 15780000): ### Older than 6 months
    if(time_diff > 7890000):   ### Older than 3 months
        update_row(row[0])
