#!/usr/bin/perl -w
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use CGI;
use CGI::Session;
use XML::LibXML;
require 'functions.pl';

$page = new CGI;

$username   = $page -> param ( 'rusername' );
$password   = $page -> param ( 'rpassword' );
$repassword = $page -> param ( 'rrepassword' );
$name       = $page -> param ( 'rname' );
$surname    = $page -> param ( 'rsurname' );
$city       = $page -> param ( 'rcity' );
$country    = $page -> param ( 'rcountry' );

$userdata = $username . "-" . $name . "-" . $surname . "-" . $city . "-" . $country; 
$regerror = "";

if ( $username eq "" ) {
	$regerror .= 'usremp=true&';
} elsif ( $username !~ /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/ ) {
	$regerror .= 'usrerr=true&';
}

if ( $password eq "" ) {
	$regerror .= 'pwdemp=true&';
} elsif ( ( length $password ) > 8 ) {
	$regerror .= 'pwderr=true&';
}

if ( $repassword eq "" ) {
	$regerror .= 'repemp=true&';
} elsif ( $repassword ne $password ) {
	$regerror .= 'reperr=true&';
}

if ( $name eq "" ) {
	$regerror .= 'namemp=true&';
} elsif ( ( length $name ) > 20 ) {
	$regerror .= 'namerr=true&';
}

if ( $surname eq "" ) {
	$regerror .= 'suremp=true&';
} elsif ( ( length $surname ) > 20 ) {
	$regerror .= 'surerr=true&';
}

if ( $city eq "" ) {
	$regerror .= 'citemp=true&';
} elsif ( ( length $city ) > 20 ) {
	$regerror .= 'citerr=true&';
}

if ( $country eq "" ) {
	$regerror .= 'couemp=true';
} elsif ( ( length $country ) > 20 ) {
	$regerror .= 'couerr=true';
}

if ( $regerror ne "" ) {
	print $page->redirect("registration.cgi?$regerror&userdata=$userdata");
} else {
	$database = '../data/database/database.xml';
	$parser   = XML::LibXML -> new();
	$doc      = $parser -> parse_file ( $database ) || die ( "Operazione di parsificazione fallita" );
	$root     = $doc    -> getDocumentElement || die ( "Non accedo alla radice" );
	
	if ( $root -> findnodes ( "user[\@id='$username']" ) ) {
		print $page->redirect("registration.cgi?exists=true&userdata=$userdata");
	} else {
		my $frammento = "\t<user id=\"".$username."\">
		<password>$password</password>
		<info>
			<name>$name</name>
			<surname>$surname</surname>
			<city>$city</city>
			<country>$country</country>
		</info>
	</user>\n";
	
		my $nodo = $parser -> parse_balanced_chunk ( $frammento ) || die ( "frammento non ben formato" );
		$root -> appendChild ( $nodo ) || die ( "non riesco a trovare il padre" );
		open ( OUT, ">$database" );
		print OUT $doc -> toString;
		close ( OUT );
		print $page -> redirect ( "registration.cgi?exists=false&userdata=$userdata" );
	}
}

exit;
