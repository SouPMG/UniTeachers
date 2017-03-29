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
		<meta name="keywords"    content="Universita', UniTeachers, Insegnante, Recupero, Studenti" />
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
		        <li class="active"><span xml:lang="en">Home</span></li>
		        <li><a href="insegnanti.cgi"   tabindex="1">Insegnanti</a></li>
		        <li><a href="feedback.cgi"     tabindex="2">Valutazioni</a></li>
		        <li><a href="registration.cgi" tabindex="3">Registrazione</a></li>
		     </ul>
		</div>
		
		<div id="breadcrumb">
			Ti trovi in: Home		
		</div>

ENDM

print<<ENDC;	
		<!-- Contenuto della pagina -->
		<div id="content">
			<div class="description">
				<h2>Benvenuto in <span xml:lang="en">UniTeachers</span></h2>
				<p>
					<span xml:lang="en"><strong>UniTeachers</strong></span>, il sito che ti permette di metterti in contatto con chi vuole <strong>insegnare</strong> o <strong>apprendere</strong>!
				</p>
				<p>
					Sei ferrato in una disciplina e ti senti in grado di diffondere le tue conoscenze?
					Hai bisogno di lezioni supplementari o ripetizioni?
				</p>
				<p>
					<strong>Registrati</strong> e scopri come possiamo aiutarti.
				</p>
			</div>
			<div class="panel">
				<h2>Diventa un insegnante!</h2>
				<a href="registration.cgi" tabindex="7">
					<img src="../media/teacher.jpg" alt="Registrati"/>
				</a>
			</div>
			<div class="panel">
				<h2>Trova il tuo insegnante!</h2>
				<a href="insegnanti.cgi" tabindex="8">
					<img src="../media/student.jpg" alt="Trova insegnanti"/>
				</a>
			</div>
			<div class="panel">
				<h2>Valuta il tuo insegnante!</h2>
				<a href="feedback.cgi" tabindex="9">
					<img src="../media/grade.jpg" alt="Valuta un insegnante"/>	
				</a>
			</div>
		</div>

ENDC

# errore dovute al login
if ( $page -> param ( 'error' ) eq true ) {
	print "<p class='error'> Le credenziali d'accesso sono invalide</p>\n";
}

# Tabindex per il footer
$tabindex = 10;

# Preparazione del footer dinamico della pagina
printDynamicFooter ();

exit;
