#!/usr/bin/python3

# GPIOInt_AUX.py

import select, time, sys, os
import MySQLdb as mdb
from subprocess import call

DbServer = "localhost"
DbUser = "RaspiUser"
DbPasswd = "RaspiPwd"


# Creazione file descrittori per GPIO17 
pin_base = '/sys/class/gpio/gpio17/'
os.system("echo 17 > /sys/class/gpio/export")

# Inpostazione GPIO17 come ingresso 
os.system("echo 'in' > /sys/class/gpio/gpio17/direction")

# Inpostazione innesco evento su fronte di salita e discesa 
os.system("echo 'both' > /sys/class/gpio/gpio17/edge")

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
    # Si posiziona all inizio del file descrittore
    f.seek(0)
    state_last = f.read()
    # Copia il contenuto del file descrittore in un file di comodo
    # per evitare inneschi a ripetizione
    os.system("cp /sys/class/gpio/gpio17/value /home/Gpio17.txt")
    g = open('/home/Gpio17.txt', 'r')
    # Memorizza lo stato del pin di ingresso GPIO17
    stato_LED = g.read(1)
    g.close()
    # Verifica se si tratta dello innesco dopo 60 secondi o di uno vero
    if len(events) == 0:
       sys.stdout.write('  timeout  delta = {:8.4f} seconds\n'.format(t2 - t1))
    else:
       # Collegamento al database
       con = mdb.connect(DbServer, DbUser, DbPasswd, 'RaspiBase');  
       # Imposta lo stato del pin sulla tabella pinStus    
       print stato_LED
       cur2 = con.cursor(mdb.cursors.DictCursor)
       cur2.execute ("""UPDATE pinStatus SET pinStatus=%s , pinMod=%s WHERE pinNumber=%s""",(stato_LED, "1", "4"))
       # Chiusura connessione al database     
       con.close() 
    t1 = t2
    # Mezzo secondo di sleep
    time.sleep (0.5) 