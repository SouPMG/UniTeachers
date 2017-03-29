#!/usr/bin/perl -w
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use CGI;
use CGI::Session;
use XML::LibXML;
require 'functions.pl';

$page = new CGI;

$search   = $page -> param ( 'search' );
$teaching = $page -> param ( 'teaching' );

$query = "";

if ( $search ne "" ) {
	$query .= "search=$search";
	if ( $teaching ne "-- seleziona una materia --" ) {
		$query .= "&teaching=$teaching";
	}
} elsif ( $teaching ne "-- seleziona una materia --" ) {
	$query .= "teaching=$teaching";
	if ( $search ne "" ) {
		$query .= "&search=$search";
	}
}

print $page -> redirect ( "insegnanti.cgi?$query" );

exit;
