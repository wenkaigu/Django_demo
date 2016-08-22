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

/*
Masked Input
*/
(function( $ ) {

	'use strict';

	if ( $.isFunction($.fn[ 'mask' ]) ) {

		$(function() {
			$('[data-plugin-masked-input]').each(function() {
				var $this = $( this ),
					opts = {};

				var pluginOptions = $this.data('plugin-options');
				if (pluginOptions)
					opts = pluginOptions;

				$this.themePluginMaskedInput(opts);
			});
		});

	}

}).apply(this, [ jQuery ]);

(function(theme, $) {

	theme = theme || {};

	var instanceName = '__maskedInput';

	var PluginMaskedInput = function($el, opts) {
		return this.initialize($el, opts);
	};

	PluginMaskedInput.defaults = {
	};

	PluginMaskedInput.prototype = {
		initialize: function($el, opts) {
			if ( $el.data( instanceName ) ) {
				return this;
			}

			this.$el = $el;

			this
				.setData()
				.setOptions(opts)
				.build();

			return this;
		},

		setData: function() {
			this.$el.data(instanceName, this);

			return this;
		},

		setOptions: function(opts) {
			this.options = $.extend( true, {}, PluginMaskedInput.defaults, opts );

			return this;
		},

		build: function() {
			this.$el.mask( this.$el.data('input-mask'), this.options );

			return this;
		}
	};

	// expose to scope
	$.extend(theme, {
		PluginMaskedInput: PluginMaskedInput
	});

	// jquery plugin
	$.fn.themePluginMaskedInput = function(opts) {
		return this.each(function() {
			var $this = $(this);

			if ($this.data(instanceName)) {
				return $this.data(instanceName);
			} else {
				return new PluginMaskedInput($this, opts);
			}

		});
	}

}).apply(this, [ window.theme, jQuery ]);


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