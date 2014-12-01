#!/usr/bin/python3

# GPIOInt_FF.py

import select, time, sys, os
#import RPi.GPIO as GPIO
import MySQLdb as mdb
from subprocess import call

DbServer = "localhost"
DbUser = "RaspiUser"
DbPasswd = "RaspiPwd"

# Variabile per il controllo della esecuzione
# della transazione di blocco 
# del test sul database per il controllo termostato
# e per lo invio dei dati a emoncms (JSON)
# SI = salta le istruzioni citate
# NO = esegue tutto
#xTest = "SI"
xTest = "NO"

# Creazione file descrittori per GPIO27 
pin_base = '/sys/class/gpio/gpio27/'
os.system("echo 27 > /sys/class/gpio/export")

# Inpostazione GPIO17 come ingresso 
os.system("echo 'in' > /sys/class/gpio/gpio27/direction")

# Inpostazione innesco evento su fronte di risalita 
os.system("echo 'rising' > /sys/class/gpio/gpio27/edge")

# Registarzione richiesta di innesco evento 
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
    #print t2 - t1
    # Si posiziona all inizio del file descrittore
    f.seek(0)
    state_last = f.read()
    if len(events) == 0:
       sys.stdout.write('  timeout  delta = {:8.4f} seconds\n'.format(t2 - t1))
    else:
       # Scarta successivi inneschi entro 1 secondo
       # per limitare il fenomeno di bouncing
       if (t2-t1) > 1.0:
          print "X"
          if xTest == "NO":
             # Collegamento al database
             con = mdb.connect(DbServer, DbUser, DbPasswd, 'RaspiBase');    
             # Legge lo stato del LED Flip Flop sulla tabella pinStatus   
             cur1 = con.cursor(mdb.cursors.DictCursor)
             cur1.execute("SELECT * FROM pinStatus WHERE pinNumber = 18")
             row = cur1.fetchone()
             # Inverte lo stato del pin 
             state_LED = row ["pinStatus"]
             #print state_LED
             if state_LED == "1": 
                state_LED = "0"
             else:
                state_LED = "1"
             # Imposta lo stato del pin sulla tabella pinStus  
             cur2 = con.cursor(mdb.cursors.DictCursor)
             cur2.execute ("""UPDATE pinStatus SET pinStatus=%s, pinMod=%s, pinMess=%s WHERE pinNumber=%s""",(state_LED, 1, 0, 18))
             #print state_LED
             # Chiusura connessione al database  
             con.close() 
    t1 = t2
    # Mezzo secondo di sleep
    time.sleep (0.5) 