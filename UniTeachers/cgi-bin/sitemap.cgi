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
		<title xml:lang="en">UniTeachers</title>
		
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
		<meta name="title"       content="UniTeachers" />
		<meta name="description" content="Il sito web per trovare il tuo insegnante di recupero." />
		<meta name="keywords"    content="Universita', UniTeachers, sitemap, mappa del sito" />
		<meta name="author"      content="Zero Productions" />
		<meta name="language"    content="italian IT" />
		
		<link rel="stylesheet" type="text/css" href="../css/style.css" media="screen"/>
		<link rel="stylesheet" type="text/css" href="../css/print.css" media="print"/>
		
		<script type="text/javascript" src="../js/backtotop.js"></script>
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
			Ti trovi in: Home &raquo; Mappa del Sito	
		</div>

ENDM

print<<ENDC;	
		<!-- Contenuto della pagina -->
		<div id="content">
			<h2 class="">Mappa del Sito</h2>
			<ul>
				<li><a href="index.cgi"        tabindex="8">Home</a></li>
				<li><a href="insegnanti.cgi"   tabindex="9">Insegnanti</a></li>
				<li><a href="feedback.cgi"     tabindex="10">Valutazioni</a></li>
				<li><a href="registration.cgi" tabindex="11">Registrazione</a></li>
ENDC

if ( $login ) {
	print <<ENDC;
				<li><a href="userprofile.cgi?user=$login" tabindex="12">Profilo</a></li>
				<li><a href="edit.cgi" tabindex="13">Modifica Profilo</a></li>
ENDC
	$tabindex = 14;
} else {
	$tabindex = 12;
}

print <<ENDC;
			</ul>
		</div>

ENDC

# errore dovute al login
if ( $page -> param ( 'error' ) eq true ) {
	print "<p class='error'>Le credenziali d'accesso sono invalide</p>\n";
}

# Preparazione del footer dinamico della pagina
printDynamicFooter ();

exit;
