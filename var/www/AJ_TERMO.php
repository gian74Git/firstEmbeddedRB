<?php
//
//////////////////////////////
// AJ_TERMO.php
//////////////////////////////

$MySQLUsername = "RaspiUser";
$MySQLPassword = "RaspiPwd";
$MySQLHost = "localhost";
$MySQLDB = "RaspiBase";

If (($MySQLUsername == "USERNAME HERE") || ($MySQLPassword == "PASSWORD HERE")){
	print 'ERROR - Please set up the script first';
	exit();
}
# Apertura della connessione al database
$dbConnection = mysql_connect($MySQLHost, $MySQLUsername, $MySQLPassword);
mysql_select_db($MySQLDB, $dbConnection);
# Estrazione dal buffer GET del contenuto azione richiesta
# e dei valori dei parametri Min e Max del Termostato
$action = $_GET['action'];
$Tmin = mysql_real_escape_string($_GET['Tmin']);
$Tmax = mysql_real_escape_string($_GET['Tmax']);
if ($action == "Termo"){
    # Scrittura dei nuovi valori nella tabella xTemp
    mysql_query("UPDATE xTemp SET xMin='$Tmin',xMax='$Tmax' WHERE xLocale=1;");
    # Chiusura connessione al database
    mysql_close();
   }
# Invio al browser del messaggio di ritorno 
print 'OK,' . $Tmin . ',' . $Tmax . ',' . $action;

?>