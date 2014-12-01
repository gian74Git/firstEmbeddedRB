#!/usr/bin/env python

# TempLux.py

# Import librerie
from smbus import SMBus
import math
import time
import MySQLdb as mdb
import requests 

# Definizione costanti

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

# URL di chiamata JSON ad emoncms e APIKEY di scrittura
# da reperire nella pagina Inputs nella applicazione di 
# amministrazione di emoncms
URL_EMONCMS = 'http://192.168.0.43/emoncms'
EMONCMS_API_KEY = 'e4b81181b1038f3f59ceecf7f0c90214'

#bus = SMBus(0)        # RaspberryPi modello A
bus = SMBus(1)         # RaspberryPi modello B

adc_address1 = 0x48   # Imposta indirizzo 000 ADC 

adc_channel1 = 0x40   # 
adc_channel2 = 0x41   # Imposta indirizzi canali
adc_channel3 = 0x42   # con risoluzione di 8 bit
adc_channel4 = 0x43   # 

R1 = 15000.0          # Resistenza R1 
R2 = 15000.0          # Resistenza R2
R_th0 = 10000.0       # Resistenza riferimento termistore a 25 c
R_fr0 = 70000.0       # Resistenza fotoresistore con illuminamento IL unitario 

V_IN = 3.3            # Tensione alimentazione partitori tensione
V_REF = 3.3           # Tensione riferimento misura ADC
A = 0.00335402        # Steinhart-Hart Costante A
B = 0.000256985       # Steinhart-Hart Costante B
C = 2.62013e-6        # Steinhart-Hart Costante C
D = 6.38309e-8        # Steinhart-Hart Costante D

pB = 4100.0           # Costante parametro B

K = 6.0               # Fattore dissipazione K 6mV C

Pend = 0.7            # Valore Gamma fotoresistenza

# Inizio elaborazione

if xTest == "NO":
   # Connessione al database
   con = mdb.connect(DbServer, DbUser, DbPasswd, 'RaspiBase');   
   con.commit

   # Inizio transazione MySQL per evitare confilitti su i2C
   con.begin()
   print "inizio"

   # Attivazione del blocco risorsa sul database
   # Altri programmi che usano bus i2C aspettano
   cur = con.cursor()
   cur.execute("SELECT * FROM xBus WHERE xBus = 'I2C1' for update")
   print "fine"

# Lettura canale 0 ADC - un byte esadecimale
# La prima istruzione imposta la richiesta di campionamento su ADC 0
# Si eseguino tre letture per evitare 0x80 all'accensione e per la precisone 
# incrementale del convertire
bus.write_byte(adc_address1,adc_channel1)
raw_val = bus.read_byte(adc_address1)
raw_val = bus.read_byte(adc_address1)
raw_val = bus.read_byte(adc_address1)
print "Hex ADC_0 = ",
print hex(raw_val)
# Elimina i primi due caratteri 0x dal valore letto ed eventuale L finale
# Trasforma il risultato in decimale 
hex_val = hex(raw_val)[2:].rstrip('L')
dec_val = int(hex_val,16)
print "Dec ADC_0 = ",
print dec_val

# Trasformazione in tensione del valore letto 
V = (dec_val * V_REF) / 256.0

print "Volt NTC = ",
print V

# Calcolo della resistenza 
R_th = (R1 * V) / (V_IN - V)

print "Resistenza NTC = ",
print R_th

# Calcolo dei gradi Kelvin con la formula di Steinhart-Hart 
logR = math.log(R_th / R_th0)
logR2 = logR**2
logR3 = logR**3
Stein = 1.0 / (A + B * logR + C * logR2 + D * logR3)

# Conversione in gradi Celsius e applicazione fattore di dispersione
Celsius = round(Stein - 273.15 - V**2 / (K * R_th),2)

# Stampa del risultato
print "Steinhart - Celsius = ",
print Celsius

# Calcolo dei gradi Kelvin con la formula del parametro B
RRo = (R_th / 10000.0)
logRRo = math.log(RRo)
parB = 1.0 / ((1.0 / 298.15) + (logRRo / pB))

# Conversione in gradi Celsius e applicazione fattore di dispersione
Celsius2 = round(parB - 273.15 - V**2 / (K * R_th),2)

# Stampa del risultato
print "parametro B - Celsius = ",
print Celsius2

# Lettura canale 1 ADC - un byte esadecimale
# La prima istruzione imposta la richiesta di campionamento su ADC 1
# Si eseguino tre letture per evitare 0x80 all'accensione e per la precisone 
# incrementale del convertire
bus.write_byte(adc_address1,adc_channel2)
raw_val2 = bus.read_byte(adc_address1)
print "Hex ADC_1 = ",
print hex(raw_val2)
raw_val2 = bus.read_byte(adc_address1)
raw_val2 = bus.read_byte(adc_address1)
# Elimina i primi due caratteri 0x dal valore letto ed eventuale L finale
# Trasforma il risultato in decimale 
hex_val2 = hex(raw_val2)[2:].rstrip('L')
dec_val2 = int(hex_val2,16)
print "Dec ADC_1 = ",
print dec_val2

# Trasformazione in tensione del valore letto 
V2 = (dec_val2 * V_REF) / 256.0

print "Volt LUX = ",
print V2

# Calcolo della resistenza 
R_lm = (R1 * V2) / (V_IN - V2)

# Calcolo della luminosita con 2 decimali
Lux = round((R_lm / R_fr0)**(1.0/-Pend),2)

# Stampa del risultato
print "Lux = ", 
print Lux

if xTest == "NO":
   # Ritardo per testare il funzionamento del blocco risorsa sul database
   #time.sleep (15)
   # Rilascio del blocco risorsa sul database
   con.commit()

   # Controllo se la temperatura compresa nei limiti oppure richiede
   # la accensione del riscldamento o del condizionamento
   cur1 = con.cursor(mdb.cursors.DictCursor)
   cur1.execute("SELECT * FROM xTemp WHERE xLocale = 1")
   row = cur1.fetchone()
   T_min = row ["xMin"]
   T_max = row ["xMax"]
   if Celsius <= T_min: 
      x_LEDRISC = 1
   else:
      x_LEDRISC = 0

   if Celsius >= T_max: 
      x_LEDCOND = 1
   else:
      x_LEDCOND = 0  
   cur2 = con.cursor(mdb.cursors.DictCursor)
   cur2.execute ("""UPDATE pinStatus SET pinStatus=%s , pinMod=%s WHERE pinNumber=%s""",(x_LEDRISC, "1", "24"))
   cur2.execute ("""UPDATE pinStatus SET pinStatus=%s , pinMod=%s WHERE pinNumber=%s""",(x_LEDCOND, "1", "23"))

   # Chiusura connessione al database
   con.close()       

   # Invio messaggio JSON verso emoncms con lo stato dei LED COND e RISC
   requests.post(URL_EMONCMS+"/api/post?apikey=" + EMONCMS_API_KEY +"&json={TEMP_1:"+str(Celsius)+"}")
   requests.post(URL_EMONCMS+"/api/post?apikey=" + EMONCMS_API_KEY +"&json={LUX_1:"+str(Lux)+"}")
   print (URL_EMONCMS+"/api/post?apikey=" + EMONCMS_API_KEY +"&json={LUX_1:"+str(Lux)+"}")












