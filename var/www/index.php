<?php
session_start();
//////////////////////////////
//         index.php        //
//////////////////////////////

$MySQLUsername = "RaspiUser";
$MySQLPassword = "RaspiPwd";
$MySQLHost = "localhost";
$MySQLDB = "RaspiBase";

If (($MySQLUsername == "USERNAME HERE") || ($MySQLPassword == "PASSWORD HERE")){
	print 'ERROR - Please set up the script first';
	exit();
}
# Connessione al database
$dbConnection = mysql_connect($MySQLHost, $MySQLUsername, $MySQLPassword);
mysql_select_db($MySQLDB, $dbConnection);

# Sezione CAMBIO PASSWORD
If (isset($_POST['action'])){
	If ($_POST['action'] == "setPassword"){
		$password1 = $_POST['password1'];
		$password2 = $_POST['password2'];
		If ($password1 != $password2){
			header('Location: index.php');
		}
		$password = mysql_real_escape_string($_POST['password1']);
		If (strlen($password) > 28){
			mysql_close();
			header('location: index.php');
		}
		$utente = $_SESSION['username'];
              $resetQuery = "SELECT username, salt FROM users WHERE username = '$utente';";
		$resetResult = mysql_query($resetQuery);
		If (mysql_num_rows($resetResult) < 1){
			mysql_close();
			header('location: index.php');
		}
		$resetData = mysql_fetch_array($resetResult, MYSQL_ASSOC);
		$resetHash = hash('sha256', $salt . hash('sha256', $password));
		$hash = hash('sha256', $password);
		function createSalt(){
			$string = md5(uniqid(rand(), true));
			return substr($string, 0, 8);
		}
		$salt = createSalt();
		$hash = hash('sha256', $salt . $hash);

		mysql_query("UPDATE users SET salt='$salt' WHERE username='$utente'");
		mysql_query("UPDATE users SET password='$hash' WHERE username='$utente'");
		mysql_close();
		header('location: index.php');
	}
}

# Controllo di userid e password sul database
If ((isset($_POST['username'])) && (isset($_POST['password']))){
	$username = mysql_real_escape_string($_POST['username']);
	$password = mysql_real_escape_string($_POST['password']);
	$loginQuery = "SELECT UserID, password, salt FROM users WHERE username = '$username';";
	$loginResult = mysql_query($loginQuery);
	If (mysql_num_rows($loginResult) < 1){
		mysql_close();
		header('location: index.php?error=incorrectLogin');
	}
	$loginData = mysql_fetch_array($loginResult, MYSQL_ASSOC);
	$loginHash = hash('sha256', $loginData['salt'] . hash('sha256', $password));
	If ($loginHash != $loginData['password']){
		mysql_close();
		header('location: index.php?error=incorrectLogin');
	} else {
		session_regenerate_id();
		$_SESSION['username'] = $username;
		$_SESSION['userID'] = $loginData['UserID'];
		mysql_close();
		header('location: index.php');
	}
}

# Sezione LOGIN
# Al il primo collegamento o alla scadenza della sessione 
# richiede il login inviando la pagina con userid e password
If ((!isset($_SESSION['username'])) || (!isset($_SESSION['userID']))){
	print '
	<html>
	<head>
	<title>Controllo remoto - Login</title>
	</head>
	<body>
	<table border="0" align="center">
	<form name="login" action="index.php" method="post">
	<tr>
	<td>Utente: </td><td><input type="text" name="username"></td>
	</tr>
	<tr>
	<td>Password: </td><td><input type="password" name="password"></td>
	</tr>
	<tr>
	<td colspan="2" align="center"><input type="submit" value="Log In"></td>
	</tr>
	</form>
	</table>
	</body>
	</html>
	';
	die();
}

# Sezione LOGOUT
If (isset($_GET['action'])){
	If ($_GET['action'] == "logout"){
		$_SESSION = array();
		session_destroy();
		header('Location: index.php');
	} else If ($_GET['action'] == "setPassword"){
		print '
		<form name="changePassword" action="index.php" method="post">
		<input type="hidden" name="action" value="setPassword">
		<p>Nuova Password: <input type="password" name="password1">
              <br>
              Conferma:&emsp;&emsp;&ensp;&ensp;<input type="password" name="password2">
              <br>
              &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<input type="submit" value="Esegui"></p>
		</form>
		';
	} 
} else {

# Sezione pagina HTML
# Preparazione della pagina principale con iframe emoncms
# le funzioni javascript ed i campi e i pulsanti di comando
	print '
		<html>
		<head>
		<title>Controllo Remoto</title>
		<script type="text/javascript">
             /* Funzioni javascript                           */
             /* Funzione di richiamo del programma AJ_DAC.php */
             /* Attivata dalla pressione dei pulsanti - e +   */
             function spedisciDAC(MP){
                     document.getElementById("descrizione").innerHTML = "--- Attendi ... ---";
                     server = "AJ_DAC.php?action=DAC_1" + "&MP=" + MP;
                     richiesta = new XMLHttpRequest();
                     richiesta.onreadystatechange = updateasincronoDAC;
                     richiesta.open("GET", server, true);
                     richiesta.send(null);
                     }

             /* Funzione richiamata alla ricezione della risposta dal programma AJ_DAC.php */
             function updateasincronoDAC(){
             if ((richiesta.readyState == 4) && (richiesta.status == 200))
                     {
                     esito = richiesta.responseText;
                     iparr = esito.split(","); 
                     Stato = iparr[0];
                     xVal = iparr[1];
                     document.getElementById("Dac").value  = xVal;
                     document.getElementById("descrizione").innerHTML = esito;
                     }
                }
 
             /* Funzione di richiamo del programma AJ_FF.php    */
             /* Attivata dalla pressione del pulsante Flip Flop */
             function spedisciFF(){
                     document.getElementById("descrizione").innerHTML = "--- Attendi ... ---";
                     server = "AJ_FF.php?action=FF_1";
                     richiesta = new XMLHttpRequest();
                     richiesta.onreadystatechange = updateasincronoFF;
                     richiesta.open("GET", server, true);
                     richiesta.send(null);
                     }
             /* Funzione richiamata alla ricezione della risposta dal programma AJ_FF.php */
             function updateasincronoFF(){
             if ((richiesta.readyState == 4) && (richiesta.status == 200))
                     {
                     esito = richiesta.responseText;
                     document.getElementById("descrizione").innerHTML = esito;
                     }
                }
             /* Funzione di richiamo del programma AJ_TERMO.php */
             /* Attivata dalla pressione del pulsante Cambia    */
             function spedisciTermo(Tmin,Tmax){
                     document.getElementById("descrizione").innerHTML = "--- Attendi ... ---";
                     server = "AJ_TERMO.php?action=Termo" + "&Tmin=" + Tmin + "&Tmax=" + Tmax;
                     richiesta = new XMLHttpRequest();
                     richiesta.onreadystatechange = updateasincronoTermo;
                     richiesta.open("GET", server, true);
                     richiesta.send(null);
                     }
             /* Funzione richiamata alla ricezione della risposta dal programma AJ_TERMO.php */
             function updateasincronoTermo(){
             if ((richiesta.readyState == 4) && (richiesta.status == 200))
                     {
                     esito = richiesta.responseText;
                     iparr = esito.split(","); 
                     Stato = iparr[0];
                     Tmin = iparr[1];
                     Tmax = iparr[2];
                     document.getElementById("tmin").value  = Tmin;
                     document.getElementById("tmax").value  = Tmax;
                     document.getElementById("descrizione").innerHTML = esito;
                     }
                }
             /* Funzione di richiamo del programma AJ_MESS.php */
             /* Attivata dalla pressione del pulsante Invia    */
             function spedisciMess(Mess){
                     document.getElementById("descrizione").innerHTML = "--- Attendi ... ---";
                     server = "AJ_MESS.php?action=Mess" + "&Mess=" + Mess;
                     richiesta = new XMLHttpRequest();
                     richiesta.onreadystatechange = updateasincronoMess;
                     richiesta.open("GET", server, true);
                     richiesta.send(null);
                     }
             /* Funzione richiamata alla ricezione della risposta dal programma AJ_MESS.php */
             function updateasincronoMess(){
             if ((richiesta.readyState == 4) && (richiesta.status == 200))
                     {
                     esito = richiesta.responseText;
                     iparr = esito.split(","); 
                     Stato = iparr[0];
                     document.getElementById("mess").value  = " ";
                     document.getElementById("descrizione").innerHTML = esito;
                     }
                }

		</script>
		</head>
              <!– Istruzioni per eliminare le barre di scorrimento nella pagina principale –>
              <style>
              body {
                  overflow: hidden;
                   }
              </style>
              <body scroll="no">
		<font face="verdana">
		<p style="text-align: center;">Controllo remoto</p> 
              <!– Iframe che richiama la pagina emoncms –>
              <!– il tag scrolling = no elimina la barra di scorrimento nello iframe –>
              <iframe src="http://192.168.0.43/emoncms/admin&id=1&apikey=24b0332c796a0a19031925380e4f483a" width="800" height="330" frameborder="0" scrolling="no"></iframe>
		';
              print '
              <br><br>
              <!– Testo titoli Flip Flop e Dimmer –>
              Flip-Flop &emsp;&emsp;&emsp;&emsp;&emsp; Dimmer
              <br>
              <!– Pulsante di comando Flip Flop              –>
              <!– Richiama la funzione javascript spedisciFF –>
              <input type="button" value="Flip-Flop" id="buttonFF"
                  onclick="spedisciFF();"/>
              &emsp;&emsp;&emsp;&emsp;&ensp;   
              ';
              # Query di recupero del valore corrente Dac 
              $query3 = mysql_query("SELECT xVal FROM xDac WHERE xDac = 1;");
              $tempRow = mysql_fetch_assoc($query3);
              $xVal = $tempRow['xVal'];
              print '
              <!– Pulsanti di comando DAC                                      –>
              <!– Ciascun pulsante richiama la funzione javascript spedisciDAC –>
              <!– Con parametro diverso rispettivamente M e P                  –>
              <!– Il campo che mostra il valore DAC e di sola lettura          –>
              <input type="button" value="-" id="buttonDACM"
                  onclick="spedisciDAC(\'M\');"/>
              <input type="text" name="DAC" id="Dac" value="' . $xVal . '" size="3" readonly/>
              <input type="button" value="+" id="buttonDACP"
                  onclick="spedisciDAC(\'P\');"/>
              <br><br>
              ';
              # Query di recupero dei valori min e msx del termostato  
              $query4 = mysql_query("SELECT xMin, xMax FROM xTemp WHERE xLocale = 1;");
              $tempRow = mysql_fetch_assoc($query4);
              $xMin = $tempRow['xMin'];
              $xMax = $tempRow['xMax'];
              print '
              <!– Campi e pulsante di comando Termostato                         –>
              <!– Ciascun pulsante richiama la funzione javascript spedisciTermo –>
              <!– passando come parametri i campi min e max                      –>
              Termostato
              <br>
              T-Min: <input type="text" name="Tmin" id="tmin" value="' . $xMin . '" size="3"/>
              T-Max: <input type="text" name="Tmax" id="tmax" value="' . $xMax . '" size="3"/>
              <input type="button" value="Cambia" id="buttonTermo"
                  onclick="spedisciTermo(document.getElementById(\'tmin\').value,
                                         document.getElementById(\'tmax\').value);"/>
              <br><br>
              <!– Campo e pulsante di comando Messaggio vocale                  –>
              <!– Ciascun pulsante richiama la funzione javascript spedisciMess –>
              <!– passando come parametro il messaggio da sintetizzare          –>
              Messaggio vocale
              <br>
              <input type="text" name="Mess" id="mess" value=" " size="80"/>
              <input type="button" value="Invia" id="buttonMess"
                 onclick="spedisciMess(document.getElementById(\'mess\').value);"/>
              ';
              # Chiusura connessione al database 
		mysql_close();
       print '
	<br><br>
       <!– Link alle richieste di cambio password e logou      –>
	<a href="index.php?action=setPassword">Cambia Password</a> <a href="index.php?action=logout">Log out</a>
       <!– Campo dove appare il messaggio attendi e i   –>
       <!– messaggi di ritorno dalla chiamate AJAX      –>
	<p id="descrizione"> - </p>
       </font>
	</body>
	</html>
	';
}
?>