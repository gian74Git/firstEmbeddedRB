#!/usr/bin/python

# LEDServer.py

# Import librerie
import time
import RPi.GPIO as GPIO
import MySQLdb as mdb
import os
import requests 
from smbus import SMBus

# Definizione costanti
DbServer = "localhost"
DbUser = "RaspiUser"
DbPasswd = "RaspiPwd"

# URL di chiamata JSON ad emoncms e APIKEY di scrittura
# da reperire nella pagina Inputs nella applicazione di 
# amministrazione di emoncms
URL_EMONCMS = 'http://192.168.0.43/emoncms'
EMONCMS_API_KEY = 'e4b81181b1038f3f59ceecf7f0c90214'

#bus = SMBus(0)        # RaspberryPi modello A
bus = SMBus(1)       # RaspberryPi modello B

adc_address1 = 0x48   # Imposta indirizzo 000 ADC 

adc_channel1 = 0x40   # Imposta indirizzi canale

X_pinNumber  = 99
X_pinStatus = 0
X_pinDirection = "zzz"
X_pinMod = 0
X_pinZero = 0


# Inizializza libreria GPIO a utilizzare la numerazione standard GPIOxx
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Ciclo di elaborazione principale
while True:
   # Connessione al database
   con = mdb.connect(DbServer, DbUser, DbPasswd, 'RaspiBase');
   # Ciclo di impostazione fissica dei livelli sui pin dei LED
   # in accordo agli stati della tabella pinStatus
   with con: 
       # Lettura di tutti i pin di uouput presenti nella tabella pinStatus
       cur1 = con.cursor(mdb.cursors.DictCursor)
       cur1.execute("SELECT * FROM pinStatus WHERE pinDir = %s", ("out"))
       rows = cur1.fetchall()
       for row in rows:
         # Per ciascun pin si salvano i dati in apposite variabili
         X_pinNumber = int(row["pinNumber"])
         X_pinStatus = row ["pinStatus"]
         X_pinMod = row["pinMod"]
         X_pinDirection = row["pinDir"]
         X_pinCms = row["pinCms"] 
         X_pinMess = row["pinMess"] 

         #print X_pinNumber
         GPIO.setup(X_pinNumber, GPIO.OUT)
         # Impostazione del livello del GPIO fisico in base
         # al valore PinStatus della tabella pinStatus
         if X_pinStatus == "1": 
            GPIO.output(X_pinNumber, True)
         else:
            GPIO.output(X_pinNumber, False)
         # Se il campo pinCms contiene un nome di Input per emoncms
         # viene inviata la richiesta JSON con il nome del corrispondente LED 
         # e lo sato del pin
         if X_pinCms is not None:
            if X_pinMod == "1":
               a=1
               requests.post(URL_EMONCMS+"/api/post?apikey=" + EMONCMS_API_KEY +"&json="+str(X_pinCms)+":"+str(X_pinStatus)+"}")
               # Se il campo pinMess vale 1 viene letta la tabella pinMsg e viene sintetizzato
               # il messaggio associato aelezionando il caso che il LED corriepondente 
               # sia stato acceso o spento
               if X_pinMess == "1":
                  cur3 = con.cursor(mdb.cursors.DictCursor)
                  cur3.execute("SELECT * FROM pinMsg WHERE pinNumber = %s", (X_pinNumber))
                  row3 = cur3.fetchone()
                  if X_pinStatus == "1": 
                     parla=row3["pinMsgON"]
                  else:
                     parla=row3["pinMsgOFF"]
                  os.system('espeak "'+ parla +  '" -v it -p 70 -s 155 > /dev/null 2> /dev/null')
         # Si azzerano i campi pinMod e pinMess sulla tabella pinStatus
         # per evitare di ripetere messaggi e inviare richieste JSON nei
         # cicli successivi del programma
         cur4 = con.cursor(mdb.cursors.DictCursor)
         cur4.execute ("""UPDATE pinStatus SET pinMod=%s, pinMess=%s WHERE pinNumber=%s""",(X_pinZero, X_pinZero, X_pinNumber))

         # print X_pinNumber, X_pinDirection, X_pinStatus, X_pinMod 
   con.commit
   # Lettura tabella xDac per verifica se vi sono cambiamenti
   cur5 = con.cursor(mdb.cursors.DictCursor)
   cur5.execute("SELECT * FROM xDac WHERE xDac = 1")
   row5 = cur5.fetchone()
   xMod = row5 ["xMod"]
   xVal = row5 ["xVal"]
   # Se impostata una variazione 
   if xMod == 1:
      # Inizio transazione MySQL per evitare conflitti su i2C
      con.begin()
      # print "inizio"
      cur6 = con.cursor()
      # Attivazione del blocco risorsa sul database
      # Altri programmi che usano bus i2C aspettano
      cur6.execute("SELECT * FROM xBus WHERE xBus = 'I2C1' for update")
      # print "fine"
      # Imposta il nuovo valore sulla uscita DAC del convertore
      # mediante chiamata i2C
      bus.write_byte_data(adc_address1,0x40,xVal)
      cur7 = con.cursor()
      cur7.execute ("UPDATE xDac SET xMod=0 WHERE xDac = 1") 
      # Invio messaggio JSON verso emoncms con il nuovo valore DAC
      requests.post(URL_EMONCMS+"/api/post?apikey=" + EMONCMS_API_KEY +"&json=DAC_1:"+str(xVal)+"}")
      # Ritardo per testare il funzionamento del blocco risorsa sul database
      #time.sleep (15)
      # Rilascio del blocco risorsa sul database
      con.commit()
   # Chiusura connessione al database
   if con:    
           con.close()        
   # Intervallo tra due cicli del programma 
   time.sleep (0.5)        



