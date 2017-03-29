#!/usr/bin/perl -w
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use CGI;
use CGI::Session;
use XML::LibXML;
require 'functions.pl';

# Dichiarazioni variabili pagina
$page  = new CGI;
$login = getSession();

# Reindirizzamento a homepage se non autenticato
if ( $login ) {
	print "Content-Type: text/html\n\n";
} else {
	print $page -> redirect ( "index.cgi" );
}

# Preparo header e contenuto fisso della pagina
print<<ENDM;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"  xml:lang="it" lang="it">
	<head>
		<title xml:lang="en">UniTeachers - Modifica Profilo</title>
		
		<meta http-equiv="Content-Type"        content="text/html; charset=utf-8" />
		<meta http-equiv="Content-Script-Type" content="text/javascript" />
		
		<meta name="title"       content="UniTeachers - Modifca Profilo" />
		<meta name="description" content="Modifica il tuo profilo UniTeachers" />
		<meta name="keywords"    content="Universita', Insegnante, Recupero, Profilo" />
		<meta name="author"      content="Zero Productions" />
		<meta name="language"    content="italian IT" />
		
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
			Ti trovi in: Home &raquo; Modifica Profilo		
		</div>
		
ENDM

# Messaggi per inserimenti e cancellazioni
if ( $page -> param ( 'part' ) eq 'info' ) {
	if ( $page -> param ( 'success' ) eq 'true' ) {  
		print "<p class='success'> Le informazioni sono state modificate con successo!</p>\n";
	}
}

# Contenuto della pagina
$database = '../data/database/database.xml';
$parser   = XML::LibXML->new();
$doc      = $parser -> parse_file ( $database ) || die ( "Operazione di parsificazione fallita" ); 
$root     = $doc    -> getDocumentElement || die("Non accedo alla radice" );
$utente   = $root   -> findnodes ( "user[\@id='$login']" ) -> get_node(1);

$name     = $utente -> findnodes ( "info/name" )    -> get_node(1) -> textContent;
$surname  = $utente -> findnodes ( "info/surname" ) -> get_node(1) -> textContent;
$city     = $utente -> findnodes ( "info/city" )    -> get_node(1) -> textContent;
$country  = $utente -> findnodes ( "info/country" ) -> get_node(1) -> textContent;

( $subject, $price ) = split /-/, $page -> param ('editdata');

print<<ENDF;
		<div id="content">
			<div class="edit">
				<form action="isubmit.cgi?part=info" onsubmit="return checkImanage()" method="post"> 
					<fieldset>
						<legend>Gestisci informazioni personali</legend>
						<div class="field">
							<label for="rname">Nome:</label>
							<input name="rname" id="rname" disabled="disabled" value="$name" tabindex="7"/>
						</div>
						<div class="field">
							<label for="rsurname">Cognome:</label>
							<input name="rsurname" id="rsurname" disabled="disabled" value="$surname" tabindex="8"/>
						</div>
						<div class="field">
							<p id="cerror" class="rerror"></p>
ENDF
						if ( $page -> param ( 'citemp' ) ) {
							print "<p class='error'>Campo Città obbligatorio.</p>\n";
						}elsif ( $page -> param ( 'citerr' ) ) {
							print "<p class='error'>Città deve essere lungo al massimo 20 caratteri.</p>\n";
						}
print<<ENDF;
							<label for="rcity">Città:</label>
							<input name="rcity" id="rcity" maxlength="20" value="$city" tabindex="9"/>
						</div>
						<div class="field">
							<p id="coerror" class="rerror"></p>	
ENDF
						if ( $page -> param ( 'couemp' ) ) {
							print "<p class='error'>Campo Paese obbligatorio.</p>\n";
						}elsif ( $page -> param ( 'couerr' ) ) {
							print "<p class='error'>Paese deve essere lungo al massimo 20 caratteri.</p>\n";
						}
print<<ENDF;
							<label for="rcountry">Paese:</label>
							<input name="rcountry" id="rcountry" maxlength="20" value="$country" tabindex="10"/> 
						</div>
						<input class="submit" type="submit" value="Applica Modifiche" tabindex="11"/>
					</fieldset>
				</form>
			</div>
			<div class="edit">
				<form action="isubmit.cgi?part=subject" onsubmit="return checkSmanage()" method="post"> 
					<fieldset>
						<legend> Inserisci nuova materia insegnata </legend>
						<div class="field">
							<p id="serror" class="rerror"></p>
ENDF
						if ( $page -> param ( 'subemp' ) ) {
							print "<p class='error'>Campo Titolo obbligatorio.</p>\n";
						}elsif ( $page -> param ( 'suberr' ) ) {
							print "<p class='error'>Titolo deve essere lungo al massimo 20 caratteri.</p>\n";
						}
print<<ENDF;
							<label for="rsubject">Nome:</label>
							<input name="rsubject" id="rsubject" maxlength="20" tabindex="12" value="$subject"/>
						</div>
						<div class="field">
							<p id="perror" class="rerror"></p>
ENDF
						if ( $page -> param ( 'priemp' ) ) {
							print "<p class='error'>Campo Prezzo obbligatorio.</p>\n";
						}elsif ( $page -> param ( 'prierr' ) ) {
							print "<p class='error'>Campo Prezzo deve contenere un numero.</p>\n";
						}
print<<ENDF;
							<label for="rprice">Prezzo(all\'ora):</label>
							<input name="rprice" id="rprice" maxlength="5" tabindex="13" value="$price"/>
						</div>
						<input class="submit" type="submit" value="Applica Modifiche" tabindex="14"/>
					</fieldset>	
				</form>
			</div>
ENDF

if ( $page -> param ( 'part' ) eq 'course' ) {
	if ( $page -> param ( 'success' ) eq 'false' ) {
		print "<p class='error'> La materia che ha cercato di inserire &egrave; già presente</p>\n";
	}
	
	if ( $page -> param ( 'success' ) eq 'true' ) {  
		print "<p class='success'> La materia &egrave; stata inserito con successo!</p>\n";
	}
}

if ( $page -> param ( 'part' ) eq 'delete' ) {
	if ( $page -> param ( 'success' ) eq 'true' ) {  
		print "<p class='success'> Cancellazione effettuata con successo!</p>\n";
	}
}

$corsi = $utente->findnodes("course");
$tabindex = 15;

if($corsi){
	print<<ENDF;
			<div id="subjectlist" class="data">
				<h2 class="data-heading">Gestisci Materie Insegnate:</h2>
				<table summary="Lista delle materie insegnate da $login, con possibilita' di eliminazione delle stesse.">
					<thead>
						<tr>
							<th></th>
							<th id="nome">Nome</th>
							<th id="prezzo">Prezzo</th>
						</tr>
					</thead>
					<tbody>
ENDF
	for ( $i = 1; $i <= $corsi -> size(); $i++ ) {
		$nome = $corsi -> get_node ( $i ) -> findnodes ( "title" ) -> get_node ( 1 ) -> textContent;
		$prezzo = $corsi -> get_node ( $i ) -> findnodes ( "price" ) -> get_node ( 1 ) -> textContent;
		
		print "\t\t\t\t\t<tr>\n";
		print "\t\t\t\t\t\t<td><a href=\"isubmit.cgi?part=delete&amp;title=$nome\" tabindex=\"$tabindex\">Elimina <span class=\"helper\">la materia $nome a costo orario di $prezzo euro</span></a></td>\n";
		print "\t\t\t\t\t\t<td headers=\"nome\">$nome</td>\n";
		print "\t\t\t\t\t\t<td headers=\"prezzo\">$prezzo €/Ora</td>\n";
		print "\t\t\t\t\t</tr>\n";
		
		$tabindex ++;
	}
	print<<ENDF;
					</tbody>
				</table>
			</div>
		</div>
ENDF

} else {
	print<<ENDF;
			<div class="forms">
				<h2>Gestisci Materie Insegnate:</h2>
				<p>Non ha ancora inserito materie.</p>
			</div>
		</div>
ENDF
}

# Preparo tabindex per footer
$tabTop  = $tabindex ++;
$tabMap  = $tabindex ++;
$tabHtml = $tabindex ++;
$tabCss  = $tabindex ++;

# Footer della pagina
print "
		<!-- Footer della pagina -->
		<div id=\"footer\">
			<div id=\"userbar\">
				<ul>
					<li><a href=\"userprofile.cgi?user=$login\" tabindex=\"5\">Profilo</a></li>
					<li class=\"active\">Modifica Profilo</li>
					<li><a href=\"logout.cgi?url=index.cgi\"    tabindex=\"6\">Esci</a></li>
				</ul>
			</div>
			<div id=\"valid\">
				<a id=\"sitemap\" href=\"sitemap.cgi\" tabindex=\"$tabMap\">Mappa del sito</a>
				<a href=\"http://validator.w3.org/check?uri=referer\" tabindex=\"$tabHtml\">
					<img src=\"http://www.w3.org/Icons/valid-xhtml10\" alt=\"Valid XHTML 1.0 Strict\" height=\"31\" width=\"88\" />
				</a>
				<a href=\"http://jigsaw.w3.org/css-validator/check/referer\" tabindex=\"$tabCss\">
					<img src=\"http://jigsaw.w3.org/css-validator/images/vcss\" alt=\"Valid CSS!\" height=\"31\" width=\"88\" />
				</a>
				<a href=\"#\" id=\"gotop\" tabindex=\"$tabTop\">
					<img src=\"../media/arrow.png\" alt=\"Torna su\"/>
				</a>
			</div>
		</div>
	</body>
</html>";

exit;
