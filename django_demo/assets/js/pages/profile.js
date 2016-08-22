// Notifications - Config
(function($) {

	'use strict';

	// use font awesome icons if available
	if ( typeof PNotify != 'undefined' ) {
		PNotify.prototype.options.styling = "fontawesome";

		$.extend(true, PNotify.prototype.options, {
			shadow: false,
			stack: {
				spacing1: 15,
	        	spacing2: 15
        	}
		});

		$.extend(PNotify.styling.fontawesome, {
			// classes
			container: "notification",
			notice: "notification-warning",
			info: "notification-info",
			success: "notification-success",
			error: "notification-danger",

			// icons
			notice_icon: "fa fa-exclamation",
			info_icon: "fa fa-info",
			success_icon: "fa fa-check",
			error_icon: "fa fa-times"
		});
	}

}).apply(this, [jQuery]);

$(document).ready(function(){

    console.log('js')

    var msg_level = document.getElementById("msg_level").innerText
    var msg_content = document.getElementById("msg_content").innerText
    console.log(msg_level=='success')
    if ( msg_level == 'success '  ) {
        console.log('sending message')
		new PNotify({
			title: 'Success!',
			text: msg_content,
			type: 'success'
		});
    }
    if ( msg_level == 'error '  ) {
        console.log('sending message')
		new PNotify({
			title: 'Error!',
			text: msg_content,
			type: 'error'
		});
    }
    console.log('message done')

})