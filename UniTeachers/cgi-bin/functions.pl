#funzioni relative alla gestione delle sessioni

sub createSession () {
	$session = new CGI::Session();
	$session -> param ( 'username', $username );
	if ( $url eq "" ) {
		$url = "index.cgi";
	}
	print $session -> header ( -location => "$url" );
};

sub getSession () {
	$session = CGI::Session -> load() or die$!;
	if ( $session -> is_expired || $session -> is_empty ) {
		return undef;
	} else {
		my $login = $session -> param ( 'username' );
		return $login;
	}
};

sub destroySession () {
	$session = CGI::Session->load() or die$!;
	$SID     = $session -> id();
	$session -> close();
	$session -> delete();
	$session -> flush();
};

sub printDynamicFooter () {
	$tabTop  = $tabindex++;
	$tabMap  = $tabindex++;
	$tabHtml = $tabindex++;
	$tabCss  = $tabindex++;
	
	if ( $login ) {
		print<<ENDUSR;
		<!-- Footer della pagina -->
		<div id="footer">
			<div id="userbar">
				<ul>
					<li><a href="userprofile.cgi?user=$login" tabindex="4">Profilo</a></li>
					<li><a href="edit.cgi" tabindex="5">Modifica Profilo</a></li>
					<li><a href="logout.cgi?url=$url" tabindex="6">Esci</a></li>
				</ul> 
			</div>
			<div id="valid">
ENDUSR
		if ( $url eq "sitemap.cgi" ) {
			print <<ENDUSR;
				<span id="sitemap">Mappa del sito</span>
ENDUSR
		} else {
			print <<ENDUSR;
				<a id="sitemap" href="sitemap.cgi" tabindex="$tabMap">Mappa del sito</a>
ENDUSR
		}
		print <<ENDUSR;
				<a href="http://validator.w3.org/check?uri=referer" tabindex="$tabHtml">
					<img src="http://www.w3.org/Icons/valid-xhtml10" alt="Valid XHTML 1.0 Strict" height="31" width="88" />
				</a>
				<a href="http://jigsaw.w3.org/css-validator/check/referer" tabindex="$tabCss">
					<img src="http://jigsaw.w3.org/css-validator/images/vcss" alt="Valid CSS!" height="31" width="88" />
				</a>
				<a href="#" id="gotop" tabindex="$tabTop">
					<img src="../media/arrow.png" alt="Torna su"/>
				</a>
			</div>
		</div>
	</body>
</html>
ENDUSR
	} else {
		print<<ENDFTR;
		<!-- Footer della pagina -->
		<div id="footer">
			<div class="login">
				<form method="post" action="login.cgi?url=$url"> 
					<fieldset>
						<legend> Accedi all'area riservata </legend>
						<div class="field">
							<label for="username"><span xml:lang="en">Username</span>:</label>
							<input type="text" name="username" id="username" maxlength="30" tabindex="4"/>
						</div>
						<div class="field">					
							<label for="password"><span xml:lang="en">Password:</span></label>
							<input type="password" name="password" id="password" maxlength="8" tabindex="5"/>
						</div>
						<input type="submit" value="Accedi" tabindex="6"/>
					</fieldset>
				</form>
			</div>
			<div id="valid">
ENDFTR
		if ( $url eq "sitemap.cgi" ) {
			print <<ENDFTR;
				<a class="active" id="sitemap" href="sitemap.cgi" tabindex="$tabMap">Mappa del sito</a>
ENDFTR
		} else {
			print <<ENDFTR;
				<a id="sitemap" href="sitemap.cgi" tabindex="$tabMap">Mappa del sito</a>
ENDFTR
		}
		print <<ENDFTR;
				<a href="http://validator.w3.org/check?uri=referer" tabindex="$tabHtml">
					<img src="http://www.w3.org/Icons/valid-xhtml10" alt="Valid XHTML 1.0 Strict" height="31" width="88" />
				</a>
				<a href="http://jigsaw.w3.org/css-validator/check/referer" tabindex="$tabCss">
					<img src="http://jigsaw.w3.org/css-validator/images/vcss" alt="Valid CSS!" height="31" width="88" />
				</a>
				<a href="#" id="gotop" tabindex="$tabTop">
					<img src="../media/arrow.png" alt="Torna su"/>
				</a>
			</div>
		</div>
	</body>
</html>
ENDFTR
	} # else
}; # printDynamicFooter

1;
