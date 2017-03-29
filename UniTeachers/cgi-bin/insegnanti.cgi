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
		<title xml:lang="en">UniTeachers - Insegnanti</title>
		
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
		<meta name="title"       content="UniTeachers - Insegnanti" />
		<meta name="description" content="Scegli il tuo insegnante di recupero." />
		<meta name="keywords"    content="Universita', UniTeachers, Insegnante, Recupero, Ricerca insegnante, Trova insegnante" />
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
		
		<!-- Link diretti al contenuto per gli utenti svantaggiati -->
		<div id="accessibility">
			<a class="helper" href="#content" accesskey="c">Vai al contenuto</a>
			<a class="helper" href="#footer"  accesskey="a">Vai all'area personale</a>
		</div>
		
		<!-- Barra di navigazione della pagina -->
		<div id="navbar">
			<ul>
				<li><a href="index.cgi"        tabindex="1"><span xml:lang="en">Home</span></a></li>
				<li class="active">Insegnanti</li>
				<li><a href="feedback.cgi"     tabindex="2">Valutazioni</a></li>
				<li><a href="registration.cgi" tabindex="3">Registrazione</a></li>
			 </ul>
		</div>
		
		<div id="breadcrumb">
			Ti trovi in: Home &raquo; Insegnanti		
		</div>

ENDM

# CONTENUTO PAGINA

# Connessione al database
$database = '../data/database/database.xml';
$parser   = XML::LibXML -> new();
$document = $parser -> parse_file ( $database ) || die ( "Operazione di parsing fallita." );
$root     = $document -> getDocumentElement || die ( "Non riesco ad accedere alla radice." );

# Variabili per accesso a database
$utenti       = $root -> findnodes ( "user" );
$insegnamenti = $root -> findnodes ( "user/course" );

print "\t\t<!-- Contenuto della pagina -->\n";

# Funzionalita' di ricerca
print "\t\t<div id=\"content\">\n";
print "\t\t\t<div class=\"search\">\n";
print "\t\t\t\t<form action=\"search.cgi\" method=\"post\">\n";
print "\t\t\t\t\t<fieldset>\n";
print "\t\t\t\t\t\t<legend>Trova il tuo insegnante</legend>\n";

print "\t\t\t\t\t\t<div class=\"field\">\n";
print "\t\t\t\t\t\t\t<label for=\"search\">Cerca per nominativo: </label>\n";
print "\t\t\t\t\t\t\t<input type=\"text\" name=\"search\" id=\"search\" tabindex=\"7\" />\n";
print "\t\t\t\t\t\t</div>\n";

print "\t\t\t\t\t\t<div class=\"field\">\n";
print "\t\t\t\t\t\t\t<label for=\"teaching\"> Oppure filtra per materia: </label>\n";
print "\t\t\t\t\t\t\t<select name=\"teaching\" id=\"teaching\" tabindex=\"8\" >\n";
print "\t\t\t\t\t\t\t\t<option>-- seleziona una materia --</option>\n";
for ( $i = 1; $i <= $insegnamenti -> size(); $i++ ) {
	$insegnamento = $insegnamenti -> get_node ( $i ) -> findnodes ( "title" ) -> get_node (1) -> textContent;
	$print = 'true';
	foreach $t ( @teachings ) {
		if ( $insegnamento eq $t ) {
			$print = 'false';
		}
	}
	if ( $print eq 'true' ) {
		print "\t\t\t\t\t\t\t\t<option>$insegnamento</option>\n";
	}
	push ( @teachings, $insegnamento );
}
print "\t\t\t\t\t\t\t</select>\n";
print "\t\t\t\t\t\t</div>\n";

print "\t\t\t\t\t\t<input type=\"submit\" value=\"cerca\" class=\"submit\" tabindex=\"9\" />\n";
print "\t\t\t\t\t</fieldset>\n";
print "\t\t\t\t</form>\n";
print "\t\t\t</div>\n";

# Visualizzazione insegnamenti
if ( $page -> url_param ( 'search' ) ) {
	$search = $page -> url_param ( 'search' );
	if ( $utenti ) {
		print "\t\t\t<div class=\"showall\"><a href=\"insegnanti.cgi\">Azzera</a></div>\n";

		$tabindex = 10;
		
		$noresult = 'true';
		for ( $i = 1; $i <= $utenti -> size(); $i++ ) {
			$nome    = $utenti -> get_node ( $i ) -> findnodes ( "info" ) -> get_node ( 1 ) -> findnodes ( "name" )    -> get_node ( 1 ) -> textContent;
			$cognome = $utenti -> get_node ( $i ) -> findnodes ( "info" ) -> get_node ( 1 ) -> findnodes ( "surname" ) -> get_node ( 1 ) -> textContent;
			$mail    = $utenti -> get_node ( $i ) -> findnodes("\@id");
			
			$regexp = "^.*" . uc ( $search ) . ".*\$";
			
			$checkStringA = $nome . ' ' . $cognome;
			$checkStringB = $cognome . ' ' . $nome;
			
			if ( uc ( $checkStringA ) =~ m/$regexp/ || uc ( $checkStringB ) =~ m/$regexp/ ) {
				
				if ( $teaching = $page -> url_param ( 'teaching' ) ) {
					print "\t\t\t<h2 class=\"data-heading\">Risultati per '$search' che insegna $teaching:</h2>\n";
					print "\t\t\t<div class=\"data\">\n";
					print "\t\t\t\t<table summary=\"Lista degli insegnanti con nome simile a $search che insegnano $teaching.\">\n"
				} else {
					print "\t\t\t<h2 class=\"data-heading\">Risultati per '$search':</h2>\n";
					print "\t\t\t<div class=\"data\">\n";
					print "\t\t\t\t<table summary=\"Lista degli insegnanti con nome simile a $search.\">\n"
				}
				
				print<<ENDF;
					<thead>
						<tr>
							<th id="nome">Nome</th>
							<th id="cognome">Cognome</th>
							<th id="materia">Materia</th>
							<th id="costo">Costo</th>
							<th id="profilo">Profilo</th>
						</tr>
					</thead>
					<tbody>
ENDF
				
				$insUtente = $utenti -> get_node ( $i ) -> findnodes ( "course" );
				
				if ( !$teaching ) {
					$noresult = 'false';
				}
				
				for ( $k = 1; $k <= $insUtente -> size(); $k++ ) {
					$insAttuale = $insUtente -> get_node ( $k ) -> findnodes ( "title" ) -> get_node ( 1 ) -> textContent;
					$costo      = $insUtente -> get_node ( $k ) -> findnodes ( "price" ) -> get_node ( 1 ) -> textContent;
					
					if ( $teaching ) {
						if ( uc ( $teaching ) eq uc ( $insAttuale ) ) {
							if ( uc ( $insAttuale ) == uc ( $insegnamento ) ) {
								$noresult = 'false';
								print "\t\t\t\t\t\t<tr>\n";
								print "\t\t\t\t\t\t\t<td headers=\"nome\">$nome</td>\n";
								print "\t\t\t\t\t\t\t<td headers=\"cognome\">$cognome</td>\n";
								print "\t\t\t\t\t\t\t<td headers=\"materia\">$insAttuale</td>\n";
								print "\t\t\t\t\t\t\t<td headers=\"costo\">$costo €/Ora</td>\n";
								print "\t\t\t\t\t\t\t<td headers=\"profilo\"><a href=\"userprofile.cgi?user=$mail\" title=\"$nome\" tabindex=\"$tabindex\">Visualizza <span class=\"helper\"> il profilo di $nome $cognome che insegna $insAttuale al costo orario di $costo euro</span></a></td>\n";
								print "\t\t\t\t\t\t</tr>\n";
								
								$tabindex ++;
							}
						}
					} else {
						if ( uc ( $insAttuale ) == uc ( $insegnamento ) ) {
							print "\t\t\t\t\t\t<tr>\n";
							print "\t\t\t\t\t\t\t<td headers=\"nome\">$nome</td>\n";
							print "\t\t\t\t\t\t\t<td headers=\"cognome\">$cognome</td>\n";
							print "\t\t\t\t\t\t\t<td headers=\"materia\">$insAttuale</td>\n";
							print "\t\t\t\t\t\t\t<td headers=\"costo\">$costo €/Ora</td>\n";
							print "\t\t\t\t\t\t\t<td headers=\"profilo\"><a href=\"userprofile.cgi?user=$mail\" title=\"$nome\" tabindex=\"$tabindex\">Visualizza <span class=\"helper\"> il profilo di $nome $cognome che insegna $insAttuale al costo orario di $costo euro</span></a></td>\n";
							print "\t\t\t\t\t\t</tr>\n";
							
							$tabindex ++;
						}
					}
				}
				print<<ENDF;
					</tbody>
				</table>
			</div>
ENDF
			}
		}

		if ( $noresult eq 'true' ) {
			print "\t\t\t<p class=\"noresult\">La ricerca non ha prodotto alcun risutato.</p>\n";
		}
		print "\t\t</div>\n";

	} # if utenti
} elsif ( $page -> url_param ( 'teaching' ) ) {
	$teaching = $page -> url_param ( 'teaching' );
	if ( $utenti ) {
		print "\t\t\t<h2 class=\"data-heading\">Insegnanti disponibili per il corso di $teaching:</h2>\n";
		print "\t\t\t<div class=\"showall\"><a href=\"insegnanti.cgi\">Azzera</a></div>\n";
		
		print<<ENDF;
			<div class="data">
				<table summary="Lista degli insegnanti per $teaching.">
					<thead>
						<tr>
							<th id="nome">Nome</th>
							<th id="cognome">Cognome</th>
							<th id="costo">Costo</th>
							<th id="profilo">Profilo</th>
						</tr>
					</thead>
					<tbody>
ENDF

		$tabindex = 10;
		for ( $i = 1; $i <= $utenti -> size(); $i++ ) {
			$nome    = $utenti -> get_node ( $i ) -> findnodes ( "info" ) -> get_node ( 1 ) -> findnodes ( "name" ) -> get_node ( 1 ) -> textContent;
			$cognome = $utenti -> get_node ( $i ) -> findnodes ( "info" ) -> get_node ( 1 ) -> findnodes ( "surname" ) -> get_node ( 1 ) -> textContent;
			$mail    = $utenti -> get_node ( $i ) -> findnodes("\@id");

			$insUtente = $utenti -> get_node ( $i ) -> findnodes ( "course" );
			
			for ( $k = 1; $k <= $insUtente -> size(); $k++ ) {
				$insAttuale = $insUtente -> get_node ( $k ) -> findnodes ( "title" ) -> get_node ( 1 ) -> textContent;
				$costo      = $insUtente -> get_node ( $k ) -> findnodes ( "price" ) -> get_node ( 1 ) -> textContent;
				#print $insAttuale;
				if ( uc ( $insAttuale ) eq uc ( $teaching ) ) {
					print "\t\t\t\t\t\t<tr>\n";
					print "\t\t\t\t\t\t\t<td headers=\"nome\">$nome</td>\n";
					print "\t\t\t\t\t\t\t<td headers=\"cognome\">$cognome</td>\n";
					print "\t\t\t\t\t\t\t<td headers=\"costo\">$costo €/Ora</td>\n";
					print "\t\t\t\t\t\t\t<td headers=\"profilo\"><a href=\"userprofile.cgi?user=$mail\" title=\"$nome\" tabindex=\"$tabindex\">Visualizza <span class=\"helper\"> il profilo di $nome $cognome che insegna $insAttuale al costo orario di $costo euro</span></a></td>\n";
					print "\t\t\t\t\t\t</tr>\n";
					
					$tabindex ++;
				}
			}
		}
	print<<ENDF;
					</tbody>
				</table>
			</div>
		</div>
ENDF
	}
} else {
	if ( $utenti ) {
		print "\t\t\t<h2 class=\"data-heading\">I nostri migliori insegnanti</h2>\n";
		
		print<<ENDF;
			<div class="data">
				<table summary="Lista degli insegnanti che hanno ottenuto valutazioni medie pari o superiori a 4.">
					<thead>
						<tr>
							<th id="nome">Nome</th>
							<th id="cognome">Cognome</th>
							<th id="profilo">Profilo</th>
						</tr>
					</thead>
					<tbody>
ENDF
		$tabindex = 10;
		for ( $i = 1; $i <= $utenti -> size(); $i++ ) {
			$nome      = $utenti -> get_node ( $i ) -> findnodes ( "info" ) -> get_node ( 1 ) -> findnodes ( "name" )    -> get_node ( 1 ) -> textContent;
			$cognome   = $utenti -> get_node ( $i ) -> findnodes ( "info" ) -> get_node ( 1 ) -> findnodes ( "surname" ) -> get_node ( 1 ) -> textContent;
			$mail      = $utenti -> get_node ( $i ) -> findnodes ( "\@id" );
			$feedbacks = $utenti -> get_node ( $i ) -> findnodes ( "feedback" );
			
			# Calcolo media feedback
			$average = 0;
			if ( $feedbacks -> size() > 0 ) {
				for ( $j = 1; $j <= $feedbacks -> size(); $j++ ) {
					$feedback = $feedbacks -> get_node ( $j ) -> findnodes ( "grade" ) -> get_node ( 1 ) -> textContent;
					$average += $feedback;
				}
				$average = $average / $feedbacks -> size();
			}
			
			if ( $average >= 4 ) {
				print "\t\t\t\t\t\t<tr>\n";
				print "\t\t\t\t\t\t\t<td headers=\"nome\">$nome</td>\n";
				print "\t\t\t\t\t\t\t<td headers=\"cognome\">$cognome</td>\n";
				print "\t\t\t\t\t\t\t<td headers=\"profilo\"><a href=\"userprofile.cgi?user=$mail\" title=\"$nome\" tabindex=\"$tabindex\">Visualizza <span class=\"helper\"> il profilo di $nome $cognome</span></a></td>\n";
				print "\t\t\t\t\t\t</tr>\n";
				
				$tabindex++;

			}
		} # for
		print<<ENDF;
					</tbody>
				</table>
			</div>
		</div>
ENDF
	} # if
} # else

# FOOTER
# Eventuale errore dovuto al login
if ( $page -> param ( 'error' ) eq 'true' ) {
	print "<p class='error'>Le credenziali d'accesso sono invalide</p>\n";
}

# Preparazione del footer dinamico della pagina
printDynamicFooter ();

exit;
