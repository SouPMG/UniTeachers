#!/usr/bin/perl -w
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use CGI;
use CGI::Session;
use XML::LibXML;
require 'functions.pl';

$page  = new CGI;
$login = getSession();

$username  = $page -> param ( 'fusername' );
$grade     = $page -> param ( 'fgrade' );
$note      = $page -> param ( 'fnote' );
$feederror = "";

$feeddata = $username . "-" . $note; 

# Controllo errori inserimento
if ( $username eq "" ) {
	$feederror .= "usremp=true&";
} elsif ( $username !~ /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/ ) {
	$feederror .= "usrerr=true&";
}

if ( $grade eq "0" ) {
	$feederror .= "grderr=true&";
}

if ( $note eq "" ) {
	$feederror .= "notemp=true";
} elsif ( ( length $note ) > 150 ) {
	$feederror .= "noterr=true";
}

# Un utente non puo' rilasciare feedback su se stesso
if ( $username eq $login && $login ne "" ) {
	print $page -> redirect("feedback.cgi?self=true&feeddata=$feeddata");
} else {
	if ( $feederror ne "" ) {
		print $page -> redirect ( "feedback.cgi?$feederror&feeddata=$feeddata" );
	} else {
		$database = '../data/database/database.xml';
		$parser   = XML::LibXML -> new ();
		$doc      = $parser -> parse_file ( $database ) || die ( "Operazione di parsificazione fallita" );
		$root     = $doc    -> getDocumentElement || die ( "Non accedo alla radice" );
		$utente   = $root   -> findnodes ( "user[\@id='$username']" ) -> get_node (1);
		
		if ( $utente ) {
			$frammento = "\t<feedback>
			<teacher>$username</teacher>
			<grade>$grade</grade>
			<note>$note</note>
		</feedback>\n\t";
			
			$nodo = $parser -> parse_balanced_chunk ( $frammento ) || die ( "Frammento non ben formato" );
			$prev = $utente -> findnodes ( "feedback" );
			
			if ( $prev ) {
				$utente -> insertAfter ( $nodo, $prev ) || die ( "Non riesco a trovare il padre" );
			} else {
				$prev = $utente -> findnodes ( "course" );
				if ( $prev ) {
					$utente -> insertAfter ( $nodo, $prev ) || die ( "Non riesco a trovare il padre" );
				} else {
					$prev = $utente -> findnodes ( "info" );
					$utente -> insertAfter ( $nodo, $prev ) || die ( "Non riesco a trovare il padre" );
				}
			}
			
			open ( OUT, ">$database" );
			print OUT $doc -> toString;
			close ( OUT );
			print $page -> redirect ( "feedback.cgi?exists=true" );
		} else {
			print $page -> redirect ( "feedback.cgi?exists=false&feeddata=$feeddata" );
		}
	}
}
