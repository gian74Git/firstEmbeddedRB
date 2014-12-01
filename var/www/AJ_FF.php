<?php
//
//////////////////////////////
// AJ_FF.php
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
$action = $_GET['action'];

if ($action == "FF_1"){
    # Lettura del valore del pin Flip Flop 
    # presente nalla tabella pinStatus
    $query = mysql_query("SELECT pinNumber, pinStatus FROM pinStatus WHERE pinNumber = 18;");
    $pinRow = mysql_fetch_assoc($query);
    $pinStatus = $pinRow['pinStatus'];
    # Inversione del valore del pin Flip Flop
    if ($pinStatus == "1"){
       $setting = "0";
       }
    else
       {
       $setting = "1";
       }
    # Scrittura del nuovo valore nella tabella pinStatus
    mysql_query("UPDATE pinStatus SET pinStatus='$setting', pinMod='1', pinMess='1' WHERE pinNumber = 18;");
    }
    # Chiusura connessione al database
    mysql_close();
# Invio al browser del messaggio di ritorno 
print '18,' . $setting . ',' . $action;

?>