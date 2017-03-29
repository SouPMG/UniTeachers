function checkEmail ( email ) { 
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test ( email );
}

function isIE () {
	var myNav = navigator.userAgent.toLowerCase();
	return (myNav.indexOf('msie') != -1) ? parseInt(myNav.split('msie')[1]) : false;
}

function checkReg () {
	if (isIE () && isIE () < 9) {
		return true;
	}
	var msg = document.getElementsByClassName ( 'rerror' );
	for ( i = 0; i < msg.length; i++ ) {
		msg[i].style.display = "none";
	}
	var perlerrors = document.getElementsByClassName ( 'error' );
	for ( i = 0; i < perlerrors.length; i++ ) {
		perlerrors[i].style.display = "none";
	}
	var username   = document.getElementById ( 'rusername' ); 
	var password   = document.getElementById ( 'rpassword' );
	var repassword = document.getElementById ( 'rrepassword' );
	var name       = document.getElementById ( 'rname' );
	var surname    = document.getElementById ( 'rsurname' );
	var city       = document.getElementById ( 'rcity' );
	var country    = document.getElementById ( 'rcountry' );
	
	var isOk  = true;
	var check = true;
	var err   = '';
	
	if ( username.value == "" ) {
		err  = 'Campo <span xml:lang="en">Username</span> obbligatorio.';
		isOk = false;				 		
	} else if ( !checkEmail ( username.value ) ) {
		err  = 'Campo <span xml:lang="en">Username</span> deve essere una <span xml:lang="en">Email</span> valida.';
		isOk = false;		
	}
	
	if ( !isOk ) {
		document.getElementById ( 'uerror' ).style.display = "block";
		document.getElementById ( 'uerror' ).innerHTML = err;
		
		isOk  = true;
		check = false;
	}

	if ( password.value == "" ) {
		err  = 'Campo <span xml:lang="en">Password</span> obbligatorio.';
		isOk = false;				 		
	} else if ( password.length > 8 ) {
		err  = '<span xml:lang="en">Password</span> deve essere lunga massimo 8 caratteri.';
		isOk = false;		
	}
	
	if ( !isOk ) {
		document.getElementById ( 'perror' ).style.display = "block";
		document.getElementById ( 'perror' ).innerHTML = err;
		
		isOk  = true;
		check =false;
	}
	
	if ( repassword.value == "" ) {
		err = 'Campo Conferma <span xml:lang="en">Password</span> obbligatorio.';
		isOk = false;				 		
	} else if ( !( rrepassword.value == password.value ) ) {
		err  = 'Conferma <span xml:lang="en">Password</span> e <span xml:lang="en">Password</span> non corrispondono.';
		isOk = false;		
	}
	
	if ( !isOk ) {
		document.getElementById ( 'reperror' ).style.display = "block";
		document.getElementById ( 'reperror' ).innerHTML = err;
		isOk  = true;
		check = false;
	}

	if ( name.value == "" ) {
		err  = 'Campo Nome obbligatorio.';
		isOk = false;				 		
	} else if ( name.length > 20 ) {
		err  = 'Campo Nome deve essere lungo massimo 20 caratteri.';
		isOk = false;		
	}
	
	if ( !isOk ) {
		document.getElementById ( 'nerror' ).style.display = "block";
		document.getElementById ( 'nerror' ).innerHTML = err;
		
		isOk  = true;
		check = false;
	}

	if ( surname.value == "" ) {
		err  = 'Campo Cognome obbligatorio.';
		isOk = false;				 		
	} else if ( surname.length > 20 ) {
		err  = 'Campo Cognome deve essere lungo massimo 20 caratteri.';
		isOk = false;		
	}
	
	if ( !isOk ) {
		document.getElementById ( 'serror' ).style.display = "block";
		document.getElementById ( 'serror' ).innerHTML = err;
		
		isOk  = true;
		check = false;
	}

	if ( city.value == "" ) {
		err  = 'Campo Città obbligatorio.';
		isOk = false;				 		
	} else if ( city.length > 20 ) {
		err  = 'Campo Città deve essere lungo massimo 20 caratteri.';
		isOk = false;		
	}
	
	if ( !isOk ) {
		document.getElementById ( 'cerror' ).style.display = "block";
		document.getElementById ( 'cerror' ).innerHTML = err;
		
		isOk  = true;
		check = false;
	}

	if ( country.value == "" ) {
		err  = 'Campo Paese obbligatorio.';
		isOk = false;				 		
	} else if ( city.length > 20 ) {
		err  = 'Campo Paese deve essere lungo massimo 20 caratteri.';
		isOk = false;		
	}
	
	if ( !isOk ) {
		document.getElementById ( 'coerror' ).style.display ="block";
		document.getElementById ( 'coerror' ).innerHTML = err;
		check = false;
	}
	
	return check;
}	

function checkFeed () {
	if (isIE () && isIE () < 9) {
		return true;
	}
	var msg = document.getElementsByClassName ( 'rerror' );
	for ( i = 0; i < msg.length; i++ ) {
		msg[i].style.display = "none";
	}
	var perlerrors = document.getElementsByClassName ( 'error' );
	for ( i = 0; i < perlerrors.length; i++ ) {
		perlerrors[i].style.display = "none";
	}
	
	var username = document.getElementById ( 'fusername' ); 
	var grade    = document.getElementById ( 'fgrade' );
	var note     = document.getElementById ( 'fnote' );
	
	var isOk  = true;
	var err   = '';
	var check = true;
	
	if ( username.value == "" ) {
		err  = 'Campo <span xml:lang="en">Username</span> obbligatorio.';
		isOk = false;				 		
	} else if ( !checkEmail ( username.value ) ) {
		err  = 'Campo <span xml:lang="en">Username</span> deve essere una <span xml:lang="en">Email</span> valida.';
		isOk = false;		
	}
	
	if ( !isOk ) {
		document.getElementById ( 'userror' ).style.display = "block";
		document.getElementById ( 'userror' ).innerHTML = err;
		
		isOk  = true;
		check = false;
	}

	if ( grade.value == "0" ) {
		err  = 'Scegliere un voto';
		isOk = false;	
	}
	
	if ( !isOk ) {
		document.getElementById ( 'verror' ).style.display ="block";
		document.getElementById ( 'verror' ).innerHTML = err;
		isOk  = true;
		check = false;
	}

	if ( note.value == "" ) {
		err  = 'Campo Note obbligatorio.';
		isOk = false;				 		
	} else if ( note.length > 150 ) {
		err  = 'Campo Note deve contenere al massimo 150 caratteri.';
		isOk = false;		
	}
	
	if ( !isOk ) {
		document.getElementById ( 'noerror' ).style.display = "block";
		document.getElementById ( 'noerror' ).innerHTML = err;
		
		isOk  = true;
		check = false;
	}
	return check;
}

function checkImanage () {
	if (isIE () && isIE () < 9) {
		return true;
	}
	var msg = document.getElementsByClassName ( 'rerror' );
	for ( i = 0; i < msg.length; i++) {
		msg[i].style.display = "none";
	}
	var perlerrors = document.getElementsByClassName ( 'error' );
	for ( i = 0; i < perlerrors.length; i++ ) {
		perlerrors[i].style.display = "none";
	}
	
	var city    = document.getElementById ( 'rcity' ); 
	var	country = document.getElementById ( 'rcountry' );
	
	var isOk = true;
	var err = '';
	var check = true;
	
	if ( city.value == "" ) {
		err  = 'Campo Città obbligatorio.';
		isOk = false;				 		
	} else if ( city.length > 20 ) {
		err  = 'Campo Città deve essere lungo massimo 20 caratteri.';
		isOk = false;		
	}
	
	if ( !isOk ) {
		document.getElementById ( 'cerror' ).style.display = "block";
		document.getElementById ( 'cerror' ).innerHTML = err;
		
		isOk  = true;
		check = false;
	}

	if ( country.value == "" ) {
		err  = 'Campo Paese obbligatorio.';
		isOk = false;				 		
	} else if ( city.length > 20 ) {
		err  = 'Campo Paese deve essere lungo massimo 20 caratteri.';
		isOk = false;		
	}
	
	if ( !isOk ) {
		document.getElementById ( 'coerror' ).style.display ="block";
		document.getElementById ( 'coerror' ).innerHTML = err;
		check = false;
	}

	return check;
}

function checkSmanage () {
	if (isIE () && isIE () < 9) {
		return true;
	}
	var msg = document.getElementsByClassName ( 'rerror' );
	for ( i = 0; i < msg.length; i++ ) {
		msg[i].style.display = "none";
	}
	var perlerrors = document.getElementsByClassName ( 'error' );
	for ( i = 0; i < perlerrors.length; i++ ) {
		perlerrors[i].style.display = "none";
	}
	
	var title = document.getElementById ( 'rsubject' );
	var	price = document.getElementById ( 'rprice' );
	
	var isOk = true;
	var err = '';
	var check = true;
	
	if ( title.value == "" ) {
		err  = 'Campo Titolo obbligatorio.';
		isOk = false;				 		
	} else if ( title.length > 20 ) {
		err  = 'Campo Titolo deve essere lungo massimo 20 caratteri.';
		isOk = false;		
	}
	
	if ( !isOk ) {
		document.getElementById ( 'serror' ).style.display = "block";
		document.getElementById ( 'serror' ).innerHTML = err;
		
		isOk  = true;
		check = false;
	}

	if ( price.value == "" ) {
		err  = 'Campo Prezzo obbligatorio.';
		isOk = false;				 		
	} else if ( isNaN ( parseFloat ( price.value ) ) ) {
		err = 'Campo Prezzo deve contenere un numero.';
		isOk = false;		
	}
	
	if ( !isOk ) {
		document.getElementById ( 'perror' ).style.display ="block";
		document.getElementById ( 'perror' ).innerHTML = err;
		check = false;
	}

	return check;
}
