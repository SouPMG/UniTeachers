#!/usr/bin/perl -w
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use CGI;
use CGI::Session;
use XML::LibXML;
require 'functions.pl';

$page  = new CGI;
$login = getSession();

# reindirizzamento a homepage se non autenticato
if ( $login ) {
	$database = '../data/database/database.xml';
	$parser   = XML::LibXML -> new();
	$doc      = $parser -> parse_file($database) || die("Operazione di parsificazione fallita"); 
	$root     = $doc    -> getDocumentElement || die("Non accedo alla radice");
	$utente   = $root   -> findnodes("user[\@id='$login']")->get_node(1);	
} else {
	print $page->redirect("index.cgi");
}
# gestione modifiche
if ( $page -> url_param ( "part" ) eq "info" ) {
	$city    = $page -> param ( 'rcity' );
	$country = $page -> param ( 'rcountry' );
	$suberr  = "";

	if ( $city eq "" ) {
		$suberr .= 'citemp=true&';
	} elsif ( ( length $city ) > 20 ) {
		$suberr .= 'citerr=true&';
	}
	
	if ( $country eq "" ) {
		$suberr .= 'couemp=true';
	} elsif ( ( length $country ) > 20 ) {
		$suberr .= 'couerr=true';
	}	

	if ( $suberr ne "" ) {
		print $page -> redirect ( "edit.cgi?$suberr" );
	} else {
		$cinode = $utente -> findnodes ( "info/city/text()" ) -> get_node(1);
		$cinode -> setData ( $city );
		
		$conode = $utente -> findnodes ( "info/country/text()" ) -> get_node(1);
		$conode -> setData ( $country );
		
		open ( OUT, ">$database" );
		print OUT $doc -> toString;
		close ( OUT );
		print $page -> redirect ( "edit.cgi?success=true&part=info" );
	}
}

if ( $page -> url_param ( "part" ) eq "subject" ) {
	$subject = $page -> param ( 'rsubject' );
	$price   = $page -> param ( 'rprice' );
	$submerr = "";
	
	$editdata = $subject . "-" . $price; 
	
	if ( $subject eq "" ) {
		$submerr .= 'subemp=true&';
	} elsif ( ( length $subject ) > 20 ) {
		$submerr .= 'suberr=true&';
	}
	
	if ( $price eq "" ) {
		$submerr .= 'priemp=true';
	} elsif ( $price !~ /^[0-9]+[\.\,]*[0-9]*+$/ ) {
		$submerr .= 'prierr=true';
	}

	if ( $submerr ne "" ) {
		print $page -> redirect ( "edit.cgi?$submerr&editdata=$editdata#subjectlist" );
	} else {
		if ( $utente -> findnodes ( "course[title = \"$subject\"]" ) ) {
			print $page -> redirect ( "edit.cgi?success=false&part=course&editdata=$editdata#subjectlist" );
		} else {
			$price =~ tr/,/./;
			$frammento = "\n\t\t<course>
			<title>$subject</title>
			<price>$price</price>
		</course>\t";
			$nodo = $parser -> parse_balanced_chunk ( $frammento ) || die ( "frammento non ben formato" );
			$prev = $utente -> findnodes ( "info" ) -> get_node(1);
			$utente -> insertAfter ( $nodo, $prev ) || die ( "non riesco a trovare il padre" );
			open ( OUT, ">$database" );
			print OUT $doc -> toString;
			close( OUT );
			print $page -> redirect ( "edit.cgi?success=true&part=course#subjectlist" );
		}			
	}
}

if ( $page -> url_param ( "part" ) eq "delete" ) {
	$materia = $page   -> url_param ( "title" );
	$tbr     = $utente -> findnodes ( "course[title = \"$materia\"]" ) -> get_node(1);
	$padre   = $tbr    -> parentNode;
	
	$padre -> removeChild ( $tbr );
	
	open ( OUT, ">$database" );
	print OUT $doc -> toString;
	close ( OUT );
	print $page -> redirect ( "edit.cgi?success=true&part=delete#subjectlist" );
}
