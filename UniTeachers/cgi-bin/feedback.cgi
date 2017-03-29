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
		<title xml:lang="en">UniTeachers - Valutazioni</title>
		
		<meta http-equiv="Content-Type"        content="text/html; charset=utf-8" />
		<meta http-equiv="Content-Script-Type" content="text/javascript" />
		
		<meta name="title"       content="UniTeachers - Valutazioni" />
		<meta name="description" content="Valuta il tuo insegnante di recupero." />
		<meta name="keywords"    content="Universita', UniTeachers, Insegnante, Recupero, Valutazioni, Valuta il tuo insegnante" />
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
				<li class="active">Valutazioni</li>
				<li><a href="registration.cgi" tabindex="3">Registrazione</a></li>
			 </ul>
		</div>
		
		<div id="breadcrumb">
			Ti trovi in: Home &raquo; Valutazioni
		</div>
		
ENDM

# contenuto pagina
if ( $page -> param ( 'exists' ) eq 'false' ) {
	print "<p class='error'> L'utente a cui hai cercato di rilasciare il <span xml:lang='en'>feedback</span>  &egrave inesistente</p>\n";
}

if ( $page -> param ( 'self' ) eq 'true' ) {
	print "<p class='error'> Non puoi rilasciare <span xml:lang='en'>feedback</span> a te stesso</p>\n";
}

if ( $page -> param ( 'exists' ) eq 'true' ) {  
	print "<p class='success'> Il tuo <span xml:lang='en'>feedback</span> &egrave stato inserito con successo!</p>\n";
}

( $username, $note ) = split /-/, $page -> param ('feeddata');

# stampa del form per il rilascio del feedback
print<<ENDF;
	<div id="content">
		<div class="feedback">
			<form action="fsubmit.cgi" onsubmit="return checkFeed()" method="post"> 
				<fieldset>
					<legend> Form per l'inserimento di <span xml:lang="en">Feedback</span></legend>
					<div class="field">
						<p id="userror" class="rerror"></p>
ENDF
						if ( $page -> param ( 'usremp' ) ) {							
							print "<p class='error'>Campo <span xml:lang='en'>Username</span> obbligatorio.</p>\n";
						} elsif ( $page -> param ( 'usrerr' ) ) {
							print "<p class='error'>Campo <span xml:lang='en'>Username</span> deve contenere una <span xml:lang='en'>Email</span> valida.</p>\n";
						}
print<<ENDF;
						<label for="fusername"><span xml:lang="en">Username (Mail)</span>:</label>
						<input name="fusername" id="fusername" maxlength="30" tabindex="7" value="$username"/>
					</div>
					<div class="field">
						<p id="verror" class="rerror"></p>
ENDF
						if($page->param('grderr')){							
							print "<p class='error'>Scegliere un voto.</p>\n";
						}
print<<ENDF;
						<label for="fgrade">Voto:</label>
						<select name="fgrade" id="fgrade" tabindex="8">
							<option value="0"></option>
							<option value="1">1</option>
							<option value="2">2</option>
							<option value="3">3</option>
							<option value="4">4</option>
							<option value="5">5</option>
						</select>
					</div>
					<div class="field">
						<p id="noerror" class="rerror"></p>
ENDF
						if($page->param('notemp')){							
							print "<p class='error'>Campo Note obbligatorio.</p>\n";
						}elsif($page->param('noterr')){
							print "<p class='error'>Campo Note deve contenere al massimo 150 caratteri.</p>\n";
						}
print<<ENDF;
						<label for="fnote">Note:</label>
						<textarea name="fnote" id="fnote" tabindex="10" rows="5" cols="9">$note</textarea>
					</div>
					<input class="submit" type="submit" value="Inserisci" tabindex="10"/>
				</fieldset>
			</form>
		</div>
	</div>
ENDF

# Errore dovute al login
if ( $page -> param ( 'error' ) eq true ) {
	print "<p class='error'> Le credenziali d'accesso sono invalide</p>\n";
}

# Preparazione tabindex per footer
$tabindex = 11;

# Preparazione del footer dinamico della pagina
printDynamicFooter ();

exit;
