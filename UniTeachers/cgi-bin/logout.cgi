#!/usr/bin/perl -w
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use CGI;
use CGI::Session;
use XML::LibXML;
require 'functions.pl';

$page = new CGI;
$url  = $page -> param ( 'url' );

destroySession ();

print $page -> redirect ( "$url" );

exit;
