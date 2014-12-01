<?php
//
//////////////////////////////
// AJ_DAC.php
//////////////////////////////

$MySQLUsername = "RaspiUser";
$MySQLPassword = "RaspiPwd";
$MySQLHost = "localhost";
$MySQLDB = "RaspiBase";

# Costanti parametriche per impostare incremento e valore minimo
# da passare al convertitore DAC
# Il primo per velocizzare il passaggio dalla minima alla massima 
# luminosita del LED e viceversa
# Il secondo in quanto sotto ad una certa tensione il LED rimane spento
$xIncr = 10;
$xDacMin = 80;

If (($MySQLUsername == "USERNAME HERE") || ($MySQLPassword == "PASSWORD HERE")){
	print 'ERROR - Please set up the script first';
	exit();
}
# Apertura della connessione al database
$dbConnection = mysql_connect($MySQLHost, $MySQLUsername, $MySQLPassword);
mysql_select_db($MySQLDB, $dbConnection);
# Estrazione dal buffer GET dei contenuti azione richiesta
# e valore del parametro MP
$action = $_GET['action'];
$MP = mysql_real_escape_string($_GET['MP']);

if ($action == "DAC_1"){
    # Lettura del valore DAC presente nalla tabella xDAC
    $query = mysql_query("SELECT xVal FROM xDac WHERE xDac = 1;");
    $dacRow = mysql_fetch_assoc($query);
    $xVal = $dacRow['xVal'];
    # Impostazione del nuovo valore tenendo conto
    # del passo di incremento e dei limiti minimo
    # e massimo da rispettare
    if ($xVal == 0) {
          $xVal = $xDacMin;           
          }
    if ($MP == "P"){
          $xVal = $xVal + $xIncr;           
          }
       else
          {
          $xVal = $xVal - $xIncr;  
          }
    if ($xVal < $xDacMin){
          $xVal = $xDacMin;           
          }
    if ($xVal > 255){
          $xVal = 255;           
          }
    # Scrittura del nuovo valore nella tabella xDac
    mysql_query("UPDATE xDac SET xVal='$xVal', xMod='1' WHERE xDac = 1;");
    # Chiusura connessione al database
    mysql_close();
    }
# Invio al browser del messaggio di ritorno 
print 'OK,' . $xVal . ',' . $MP;

?>