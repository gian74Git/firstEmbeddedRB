#!/usr/bin/python3

# GPIOInt_MESS.py

import select, time, sys, os
import MySQLdb as mdb
import os
#from subprocess import call

DbServer = "localhost"
DbUser = "RaspiUser"
DbPasswd = "RaspiPwd"

# Creazione file descrittori per GPIO22 
os.system("echo 22 > /sys/class/gpio/export")

# Inpostazione GPIO17 come ingresso 
os.system("echo 'in' > /sys/class/gpio/gpio22/direction")

# Inpostazione innesco evento su fronte di salita
os.system("echo 'rising' > /sys/class/gpio/gpio22/edge")

# Registarzione richiesta di innesco evento 
pin_base = '/sys/class/gpio/gpio22/'
f = open(pin_base + 'value', 'r')
po = select.epoll()
po.register(f, select.POLLPRI)

# Stampa su stdout lo stato attuale del pin
state_last = f.read(1)
sys.stdout.write('Initial pin value = {}\n'.format(repr(state_last)))

# Salva il tempo attuale
t1 = time.time()

# Ciclo loop di elaborazione
while 1:
    # Attiva attesa evento Se non avviene entro 60 secondi genera un evento fasullo
    # giusto per segnalare di essere in vita
    events = po.poll(60000)
    #print events
    t2 = time.time()
    # Si posiziona all inizio del file descrittore
    f.seek(0)
    state_last = f.read()
    if len(events) == 0:
       sys.stdout.write('  timeout  delta = {:8.4f} seconds\n'.format(t2 - t1))
    else:
       # Scarta successivi inneschi entro 1 secondo
       # per limitare il fenomeno di bouncing
       if (t2-t1) > 1.0:
          # Collegamento al database
          con = mdb.connect(DbServer, DbUser, DbPasswd, 'RaspiBase');  
          # Legge il messaggio da leggere nella tabella xMess   
          cur = con.cursor(mdb.cursors.DictCursor)
          cur.execute("SELECT * FROM xMess WHERE xMessID = 1")
          row = cur.fetchone()
          parla = row["xMess"]
          print state_last
          #print parla + "a"
          #print len(parla) + 1
          # Se messaggio non vuoto lo passa a espeak per sintetizzarlo 
          if int(len(parla)) > 0:
             print 2
             os.system('espeak "'+ parla +  '" -v it -p 70 -s 155 > /dev/null 2> /dev/null')
             # Legge lo stato del LED Flip Flop sulla tabella pinStatus   
             cur1 = con.cursor(mdb.cursors.DictCursor)
             cur1.execute("SELECT * FROM pinStatus WHERE pinNumber = 25")
             row1 = cur1.fetchone()  
             state_LED = row1["pinStatus"]
             print state_LED
             # Se lo stato del pin = 1 - prima volta che viene letto il messaggio
             # porta lo stato del LED a 0 e aggiorna la tabella pinStatus
             if state_LED == "1": 
                state_LED = "0"
                #print state_LED
                cur2 = con.cursor(mdb.cursors.DictCursor)
                cur2.execute ("""UPDATE pinStatus SET pinStatus=%s , pinMod=%s WHERE pinNumber=%s""",(state_LED, "1", "25"))
          # Chiusura connessione al database  
          con.close() 
    t1 = t2
    # Mezzo secondo di sleep
    time.sleep (0.5) 