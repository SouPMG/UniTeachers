#!/usr/bin/perl -w
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use CGI;
use CGI::Session;
use XML::LibXML;
require 'functions.pl';

# Dichiarazioni variabili pagina
$page  = new CGI;
$login = getSession();
$url   = $page -> url ( -relative => 1 );

# Preparo header e contenuto fisso della pagina
print "Content-Type: text/html\n\n";
print<<ENDM;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"  xml:lang="it" lang="it">
	<head>
		<title xml:lang="en">UniTeachers - Registrazione</title>
		
		<meta http-equiv="Content-Type"        content="text/html; charset=utf-8" />
		<meta http-equiv="Content-Script-Type" content="text/javascript" />
		
		<meta name="title"       content="UniTeachers - Registrazione" />
		<meta name="description" content="Registrati come insegnante a UniTeachers" />
		<meta name="keywords"    content="Universita', UniTeachers, Insegnante, Recupero, Registrazione, Registra un account, Registrati come insegnante" />
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
		        <li><a href="index.cgi"      tabindex="1"><span xml:lang="en">Home</span></a></li>
		        <li><a href="insegnanti.cgi" tabindex="2">Insegnanti</a></li>
		        <li><a href="feedback.cgi"   tabindex="3">Valutazioni</a></li>
		        <li class="active">Registrazione</li>
		     </ul>
		</div>

		<div id="breadcrumb">
			Ti trovi in: Home &raquo; Registrazione		
		</div>

ENDM

# Errori dovuti alla registrazione
if ( $login ) {
	print "<h2 class='heading'> Benvenuto in <span xml:lang='en'>UniTeachers</span></h2>";
	print "<p class='success'> Per modificare le tue informazioni personali visita il tuo profilo."
} else {
	if ( $page -> param ( 'exists' ) eq false ) {
		print "<h2 class='heading'> Benvenuto in <span xml:lang='en'>UniTeachers</span></h2>";
		print "<p class='success'> Accedi all'area personale per vedere i tuoi <span xml:lang='en'>feedback</span> e inserire/modificare le materie insegnate </p>";
	} else {
		if ( $page -> param ( 'exists' ) eq true ) {
			print "<p class='error'> Il nome utente scelto non è disponibile!</p>\n";
		}
	
	( $username, $name, $surname, $city, $country ) = split /-/, $page -> param ('userdata');
	
	# Stampa del form di registrazione
	print<<ENDF;
		<div id="content">
			<div class="register">
				<form action="rsubmit.cgi" onsubmit="return checkReg()" method="post"> 
					<fieldset>
						<legend> Form di registrazione ad <span xml:lang="en">UniTeachers</span> </legend>
						<div class="field">
							<p id="uerror" class="rerror"></p>
ENDF
						if ( $page -> param ( 'usremp' ) ) {							
							print "<p class='error'>Campo <span xml:lang='en'>Username</span> obbligatorio.</p>\n";
						} elsif ( $page -> param ( 'usrerr' ) ) {
							print "<p class='error'>Campo <span xml:lang='en'>Username</span> deve contenere una <span xml:lang='en'>Email</span> valida.</p>\n";
						}
print<<ENDF;
							<label for="rusername"><span xml:lang="en">Username (Mail)</span>:</label>
							
							<input name="rusername" id="rusername" maxlength="30" value="$username" tabindex="7"/>
						</div>
						<div class="field">
							<p id="perror" class="rerror"></p>
ENDF
						if ( $page -> param ( 'pwdemp' ) ) {
							print "<p class='error'>Campo <span xml:lang='en'>Password</span> obbligatorio.</p>\n";
						} elsif ( $page -> param ( 'pwderr' ) ) {
							print "<p class='error'><span xml:lang='en'>Password</span> deve essere lunga massimo 8 caratteri.</p>\n";
						}
print<<ENDF;	
							<label for="rpassword"><span xml:lang="en">Password:</span></label>
							<input type="password" name="rpassword" id="rpassword" maxlength="8" tabindex="8"/>
						</div>
						<div class="field">
							<p id="reperror" class="rerror"></p>
ENDF
						if ( $page -> param ( 'repemp' ) ) {
							print "<p class='error'>Campo Conferma <span xml:lang='en'>Password</span> obbligatorio.</p>\n";
						} elsif ( $page -> param ( 'reperr' ) ) {
							print "<p class='error'>Conferma <span xml:lang='en'>Password</span> e <span xml:lang='en'>Password</span> non corrispondono.</p>\n";
						}
print<<ENDF;		
							<label for="rrepassword">Conferma <span xml:lang="en">Password:</span></label>
							<input type="password" name="rrepassword" id="rrepassword" maxlength="8" tabindex="9"/>
						</div>
						<div class="field">
							<p id="nerror" class="rerror"></p>
ENDF
						if ( $page -> param ( 'namemp' ) ) {
							print "<p class='error'>Campo Nome obbligatorio.</p>\n";
						} elsif ( $page -> param ( 'namerr' ) ) {
							print "<p class='error'>Nome deve essere lungo al massimo 20 caratteri.</p>\n";
						}
print<<ENDF;
							<label for="rname">Nome:</label>
							<input name="rname" id="rname" maxlength="20" value="$name" tabindex="10"/>
						</div>
						<div class="field">
							<p id="serror" class="rerror"></p>
ENDF
						if ( $page -> param ( 'suremp' ) ) {
							print "<p class='error'>Campo Cognome obbligatorio.</p>\n";
						} elsif ( $page -> param ( 'surerr' ) ) {
							print "<p class='error'>Cognome deve essere lungo al massimo 20 caratteri.</p>\n";
						}
print<<ENDF;
							<label for="rsurname">Cognome:</label>
							<input name="rsurname" id="rsurname" maxlength="20" value="$surname" tabindex="11"/>
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
							<input name="rcity" id="rcity" maxlength="20" value="$city" tabindex="12"/>
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
							<input name="rcountry" id="rcountry" maxlength="20" value="$country" tabindex="13"/>
						</div>
						<input class="submit" type="submit" value="Registrati" tabindex="14"/>
						<input class="submit" type="reset" value="Cancella" tabindex="15" />
					</fieldset>
				</form>
			</div>
		</div>
ENDF
	}
}
# Errori dovuti al login
if ( $page -> param ( 'error' ) eq true ) {
	print "<p class='error'> Le credenziali d'accesso sono invalide</p>\n";
}

# Preparazione tabindex per il footer
$tabindex = 16;

# Preparazione del footer dinamico della pagina
printDynamicFooter ();

exit;
