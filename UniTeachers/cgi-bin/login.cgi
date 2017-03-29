#!/usr/bin/perl -w
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use CGI;
use CGI::Session;
use XML::LibXML;
require 'functions.pl';

$page = new CGI;

$username = $page -> param ( 'username' );
$password = $page -> param ( 'password' );
$url      = $page -> url_param ( 'url' );
$error    = "false";

$database = '../data/database/database.xml';
$parser   = XML::LibXML->new();
$doc      = $parser -> parse_file ( $database ) || die ( "Operazione di parsing fallita" );
$root     = $doc    -> getDocumentElement || die ( "Non riesco ad accedere alla radice" );
$user     = $root   -> findnodes ( "user[\@id='$username']" );

if ( $user ) {
	my $passcheck = $root -> findnodes ( "user[\@id='$username']/password" );
	if ( $password eq $passcheck ) {
		createSession ();
	} else {
		$error = "true";
	}
} else {
	$error = "true";
}

print $page -> redirect ( "$url?error=$error" );

exit;
