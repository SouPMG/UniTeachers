#!/usr/bin/perl -w
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use CGI;
use CGI::Session;
use XML::LibXML;
require 'functions.pl';

# Dichiarazioni variabili pagina
$page  = new CGI;
$login = getSession();
$user  = $page -> param ( 'user' );
$url   = $page -> url ( -relative => 1 ) . "?user=$user";

# Reindirizzamento a homepage se manca il parametro 'user'
if ( $user ) {
	print "Content-Type: text/html\n\n";
} else {
	print $page -> redirect("index.cgi");
}

# Preparo header e contenuto fisso della pagina
print<<ENDM;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"  xml:lang="it" lang="it">
	<head>
		<title xml:lang="en">$user on UniTeachers</title>
		
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
		<meta name="title"       content="$user on UniTeachers" />
		<meta name="description" content="Il profilo personale di $user" />
		<meta name="keywords"    content="Universita', Insegnante, Recupero, Profilo personale, Profilo utente" />
		<meta name="author"      content="Zero Productions" />
		<meta name="language"    content="italian it" />
		
		<link rel="stylesheet" type="text/css" href="../css/style.css" media="screen"/>
		<link rel="stylesheet" type="text/css" href="../css/print.css" media="print"/>
		
		<script type="text/javascript" src="../js/backtotop.js"></script>
		<script type="text/javascript" src="../js/check.js"></script>
	</head>
	
	<body>
		<!-- Parte header della pagina -->
		<div id="header">
		    <h1 id="logo" xml:lang="en">UniTeachers</h1>
		</div>
		
		<!-- Link diretto al contenuto per utenti svantaggiati -->
		<div id="accessibility">
			<a href="#content" accesskey="c">Vai al contenuto</a>
			<a href="#footer"  accesskey="a">Vai all'area personale</a>
		</div> 
		
		<!-- Barra di navigazione della pagina -->
		<div id="navbar">
		    <ul>
		        <li><a href="index.cgi"        tabindex="1"><span xml:lang="en">Home</span></a></li>
		        <li><a href="insegnanti.cgi"   tabindex="2">Insegnanti</a></li>
		        <li><a href="feedback.cgi"     tabindex="3">Valutazioni</a></li>
		        <li><a href="registration.cgi" tabindex="4">Registrazione</a></li>
		     </ul>
		</div>

		<div id="breadcrumb">
			Ti trovi in: Home &raquo; Profilo
		</div>
		
ENDM

# Contenuto della pagina
$database = '../data/database/database.xml';
$parser   = XML::LibXML -> new();
$doc      = $parser-> parse_file ( $database ) || die ( "Operazione di parsificazione fallita" );
$root     = $doc   -> getDocumentElement || die ( "Non accedo alla radice" );
$utente   = $root  -> findnodes ( "user[\@id='$user']" ) -> get_node (1);

# Dati letti dal file xml
$name     = $utente -> findnodes ( "info/name" )    -> get_node(1) -> textContent;
$surname  = $utente -> findnodes ( "info/surname" ) -> get_node(1) -> textContent;
$city     = $utente -> findnodes ( "info/city" )    -> get_node(1) -> textContent;
$country  = $utente -> findnodes ( "info/country" ) -> get_node(1) -> textContent;
$corsi    = $utente -> findnodes ( "course" );
$feedback = $utente -> findnodes ( "feedback" );

$username = $page -> url_param ( 'user' );

# Stampa del contenuto della pagina
print<<ENDF;
		<div id="content">
			<h2 class="heading">Profilo personale di $name $surname</h2>
			<div class="data half">
				<h3 class="data-heading">Informazioni personali</h3>
				<ul>
					<li><span class="info">Nome:</span>    $name</li>
					<li><span class="info">Cognome:</span> $surname</li>
					<li><span class="info">Mail:</span>    <a href="mailto:$user">$user</a></li>
					<li><span class="info">Città:</span>   $city</li>
					<li><span class="info">Paese:</span>   $country</li>
				</ul>
			</div>
ENDF

if ( $corsi ) {
	print<<ENDF;
			<div class="data half">
				<h3 class="data-heading">Materie insegnate</h3>
				<table summary="Lista delle materie insegnate da $username">
					<thead>
						<tr>
							<th id="titolo">Titolo</th>
							<th id="prezzo">Prezzo</th>
						</tr>
					</thead>
					<tbody>
ENDF

	for ( $i = 1; $i <= $corsi -> size(); $i++ ) {	
		$titolo = $corsi -> get_node ( $i ) -> findnodes ( "title" ) -> get_node(1) -> textContent;
		$prezzo = $corsi -> get_node ( $i ) -> findnodes ( "price" ) -> get_node(1) -> textContent;
		
		print "\t\t\t\t\t\t<tr>\n";
		print "\t\t\t\t\t\t\t<td headers=\"titolo\">$titolo</td>\n";
		print "\t\t\t\t\t\t\t<td headers=\"prezzo\">$prezzo €/Ora</td>\n";
		print "\t\t\t\t\t\t</tr>\n";
	}
	
	print<<ENDF;
					</tbody>
				</table>
			</div>
ENDF
} else {
	print<<ENDF;
			<div class="data half">
				<h3 class="data-heading">Gestisci Materie Insegnate</h3>
				<p>Non ha ancora inserito materie.</p>
			</div>
ENDF
}
if ( $feedback ) {
	print<<ENDF;
			<div class="data full">
				<h3 class="data-heading">Valutazioni ricevute</h3>
				<table summary="Lista delle valutazioni ricevute dagli studenti per l'insegnante $username">
					<thead>
						<tr>
							<th id="voto">Voto</th>
							<th id="commento">Commento</th>
						</tr>
					</thead>
					<tbody>
ENDF
	for ( $i = 1; $i <= $feedback -> size(); $i++ ) {	
		$voto     = $feedback -> get_node($i) -> findnodes ( "grade" ) -> get_node(1) -> textContent;
		$commento = $feedback -> get_node($i) -> findnodes ( "note" )  -> get_node(1) -> textContent; 
		print "\t\t\t\t\t\t<tr>\n";
		print "\t\t\t\t\t\t\t<td headers=\"voto\">$voto</td>\n";
		print "\t\t\t\t\t\t\t<td headers=\"commento\">$commento</td>\n";
		print "\t\t\t\t\t\t</tr>\n";
	}
	print<<ENDF;
					</tbody>
				</table>
			</div>
		</div>
ENDF
} else {
	print<<ENDF;
			<div class="data full">
				<h3 class="data-heading">Valutazioni ricevute</h3>
				<p>Non hai ancora ricevuto alcuna valutazione.</p>
			</div>
		</div>
ENDF
}

# Errore dovute al login
if ( $page -> param ( 'error' ) eq true ) {
	print "<p class='error'> Le credenziali d'accesso sono invalide</p>\n";
}

# Preaparo tabindex per footer
$tabindex = 8;

$tabTop  = $tabindex++;
$tabMap  = $tabindex++;
$tabHtml = $tabindex++;
$tabCss  = $tabindex++;

# Footer dinamico della pagina
if ( $login ) {
	print<<ENDUSR;
		<!-- Footer della pagina -->
		<div id="footer">
			<div id="userbar">
				<ul>
					<li><a href="userprofile.cgi?user=$login" tabindex="5">Profilo</a></li>
					<li><a href="edit.cgi" tabindex="6">Modifica Profilo</a></li>
					<li><a href="logout.cgi?url=$url" tabindex="7">Esci</a></li>
				</ul> 
			</div>
			<div id="valid">
ENDUSR
		if ( $url eq "sitemap.cgi" ) {
			print <<ENDUSR;
				<span id="sitemap">Mappa del sito</span>
ENDUSR
		} else {
			print <<ENDUSR;
				<a id="sitemap" href="sitemap.cgi" tabindex="$tabMap">Mappa del sito</a>
ENDUSR
		}
		print <<ENDUSR;
				<a href="http://validator.w3.org/check?uri=referer" tabindex="$tabHtml">
					<img src="http://www.w3.org/Icons/valid-xhtml10" alt="Valid XHTML 1.0 Strict" height="31" width="88" />
				</a>
				<a href="http://jigsaw.w3.org/css-validator/check/referer" tabindex="$tabCss">
					<img src="http://jigsaw.w3.org/css-validator/images/vcss" alt="Valid CSS!" height="31" width="88" />
				</a>
				<a href="#" id="gotop" tabindex="$tabTop">
					<img src="../media/arrow.png" alt="Torna su"/>
				</a>
			</div>
		</div>
	</body>
</html>
ENDUSR
	} else {
		print<<ENDFTR;
		<!-- Footer della pagina -->
		<div id="footer">
			<div class="login">
				<form method="post" action="login.cgi?url=$url"> 
					<fieldset>
						<legend> Accedi all'area riservata </legend>
						<div class="field">
							<label for="username"><span xml:lang="en">Username</span>:</label>
							<input type="text" name="username" id="username" maxlength="30" tabindex="5"/>
						</div>
						<div class="field">					
							<label for="password"><span xml:lang="en">Password:</span></label>
							<input type="password" name="password" id="password" maxlength="8" tabindex="6"/>
						</div>
						<input type="submit" value="Accedi" tabindex="7"/>
					</fieldset>
				</form>
			</div>
			<div id="valid">
ENDFTR
		if ( $url eq "sitemap.cgi" ) {
			print <<ENDFTR;
				<a class="active" id="sitemap" href="sitemap.cgi" tabindex="$tabMap">Mappa del sito</a>
ENDFTR
		} else {
			print <<ENDFTR;
				<a id="sitemap" href="sitemap.cgi" tabindex="$tabMap">Mappa del sito</a>
ENDFTR
		}
		print <<ENDFTR;
				<a href="http://validator.w3.org/check?uri=referer" tabindex="$tabHtml">
					<img src="http://www.w3.org/Icons/valid-xhtml10" alt="Valid XHTML 1.0 Strict" height="31" width="88" />
				</a>
				<a href="http://jigsaw.w3.org/css-validator/check/referer" tabindex="$tabCss">
					<img src="http://jigsaw.w3.org/css-validator/images/vcss" alt="Valid CSS!" height="31" width="88" />
				</a>
				<a href="#" id="gotop" tabindex="$tabTop">
					<img src="../media/arrow.png" alt="Torna su"/>
				</a>
			</div>
		</div>
	</body>
</html>
ENDFTR
}

exit;
