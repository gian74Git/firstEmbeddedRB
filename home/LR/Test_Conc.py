#!/usr/bin/python3
# Test_Conc.py
# Test concorrenza.

import time
import MySQLdb as mdb

DbServer = "localhost"
DbUser = "RaspiUser"
DbPasswd = "RaspiPwd"
       
con = mdb.connect(DbServer, DbUser, DbPasswd, 'RaspiBase');       
cur1 = con.cursor()
con.commit()
#con.begin()
print "inizio select"
cur1.execute("SELECT * FROM xBus WHERE xBus = 'I2C1' for update")
print "fine select"
time.sleep (20)

con.commit()
print "dormo"
time.sleep (5)
con.close()
