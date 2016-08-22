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

(function($) {

	'use strict';

	// we overwrite initialize of all datatables here
	// because we want to use select2, give search input a bootstrap look
	// keep in mind if you overwrite this fnInitComplete somewhere,
	// you should run the code inside this function to keep functionality.
	//
	// there's no better way to do this at this time :(
	if ( $.isFunction( $.fn[ 'dataTable' ] ) ) {

		$.extend(true, $.fn.dataTable.defaults, {
			sDom: "<'row datatables-header form-inline'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>r><'table-responsive't><'row datatables-footer'<'col-sm-12 col-md-6'i><'col-sm-12 col-md-6'p>>",
			oLanguage: {
				sLengthMenu: '_MENU_ records per page',
				sProcessing: '<i class="fa fa-spinner fa-spin"></i> Loading'
			},
			fnInitComplete: function( settings, json ) {
				// select 2
				if ( $.isFunction( $.fn[ 'select2' ] ) ) {
					$('.dataTables_length select', settings.nTableWrapper).select2({
						minimumResultsForSearch: -1
					});
				}

				var options = $( 'table', settings.nTableWrapper ).data( 'plugin-options' ) || {};

				// search
				var $search = $('.dataTables_filter input', settings.nTableWrapper);

				$search
					.attr({
						placeholder: typeof options.searchPlaceholder !== 'undefined' ? options.searchPlaceholder : 'Search'
					})
					.addClass('form-control');

				if ( $.isFunction( $.fn.placeholder ) ) {
					$search.placeholder();
				}
			}
		});

	}

}).apply( this, [ jQuery ]);


/*Datatable - default*/
(function( $ ) {

	'use strict';

	var datatableInit = function() {

		$('#datatable-default').dataTable();

	};

	$(function() {
		datatableInit();
	});

}).apply( this, [ jQuery ]);


$(document).ready(function(){

    console.log('js')

    var msg_level = document.getElementById("msg_level").innerText
    var msg_content = document.getElementById("msg_content").innerText
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

});