window.onload = function () {
	var button = document.getElementById ( "gotop" );
	button.style.display = "none";
	
	// Show or hide the sticky footer button
	window.onscroll = function ( e ) {
		if ( document.body.scrollTop > 0 || document.documentElement.scrollTop > 0 )
			button.style.display="block";
		else
			button.style.display="none";
	};
};