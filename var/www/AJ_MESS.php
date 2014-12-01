<?php
//
//////////////////////////////
// AJ_MESS.php
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
# Estrazione dal buffer GET dei contenuti azione richiesta
# e del contenuto del messaggio da sintetizzare
$action = $_GET['action'];
$Mess = mysql_real_escape_string($_GET['Mess']);
if ($action == "Mess"){
    # Scrittura del messaggio nella tabella xMess
    # impostazione dei flag di modifics
    mysql_query("UPDATE xMess SET xMess='$Mess', xMod=1 WHERE xMessID=1;");
    # Se il messaggio contenuto nel buffer GET e vuoto
    # imposta il record relatico al LED MESS in modo che si spento
    # altrimenti che sia acceso
    if (strlen($Mess) == 0)
       mysql_query("UPDATE pinStatus SET pinStatus='0', pinMod='1' WHERE pinNumber='25';");
    else
       mysql_query("UPDATE pinStatus SET pinStatus='1', pinMod='1', pinMess='1' WHERE pinNumber='25';");
    # Chiusura connessione al database
    mysql_close();
   }
# Invio al browser del messaggio di ritorno
print 'OK,' . $action;

?>