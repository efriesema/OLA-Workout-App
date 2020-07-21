/*
 * This script handles menu and search functionality for this theme.
 * It is also used to handle theme-wide JavaScript functions.
 */

  jQuery(document).ready(function() {

    // Check if Hash in URL, if so, scroll to offset to compensate
    // for fixed header.
    if (window.location.hash && jQuery(window.location.hash).length > 0) {
      var navOffset = _getNavOffset();
      var offset = jQuery( window.location.hash ).offset();
      // Scroll based on offset.
      var scrollTo = (offset.top - navOffset);
      jQuery('html, body').animate({scrollTop:scrollTo}, 600);
    }

    // Load balance text to run on any elements with balance_text class.
    // balanceText library loaded within template.php of Mars theme.
    //balanceText();

  	////////////////////////////////////////
    /// Load various jQuery UI Components.
  	////////////////////////////////////////

    jQuery('[data-toggle="tooltip"]').tooltip();
    jQuery('[data-toggle="popover"]').popover();

    // Accordions

    // Extends accordion functionality.
    jQuery.fn.extend({
      loadAccordion: function() {
        // Using attr instead of data for compatibility for older jQuery versions.
        var collapsed = jQuery(this).attr("data-collapsed");
        var heightStyleVal = jQuery(this).attr("data-height-style");

          if(collapsed === "true")
            activeState = false; // Close all panels.
          else
            activeState = 0; // Open first panel.

        return jQuery(this).accordion({
          heightStyle: heightStyleVal,
          autoHeight: false,
          collapsible: collapsed,
          active: activeState,
          icons: false
        });
      }
    });


  	jQuery(".accordion").each(function() {
  		jQuery(jQuery(this)).loadAccordion();
  	});

  	////////////////////////////////////////
    /// Menu/Nav related.
  	////////////////////////////////////////

    jQuery("#global-search-tabs").tabs();

    var AZlinkClicked = false;

    jQuery( "#global-search-tabs" ).on( "tabsactivate", function( event, ui ) {
      var active = jQuery( "#global-search-tabs" ).tabs( "option", "active" );

      // The A-Z index tab is index 1.
      if (active === 1 && AZlinkClicked === false) {
        /*
        var request = jQuery.ajax({
          url: basePath + "global-includes/a-z",
          type: "GET",
          cache: false,
        });

        // AJAX Response
        request.done(function(data) {
          jQuery("#a-z-tab").hide().html(data).fadeIn();
          AZlinkClicked = true;
        });
        */
      }

    });


    // Menu Button Click handler
    jQuery("#menu-button").click(function(e) {
      jQuery("#navigation").toggle("fast");
      jQuery("#modal-menu-overlay").fadeToggle("fast", function() {
        jQuery("#menu-close").focus();
      });

      jQuery("body").addClass("stop-scrolling");
  		e.preventDefault();
    });

    /*
    jQuery( "#menu-button" ).keyup(function(e) {
      if (!jQuery("#modal-menu-overlay").is(":visible") && e.keyCode === 13) {
        console.log('test');
        //jQuery("#menu-close").focus();
      }
    });
    */
      // Close All Menus and overlay.
      function closeAllMenus() {
        jQuery("#navigation").hide("fast");
        jQuery("#search").hide("fast");
        jQuery("#modal-menu-overlay").fadeToggle("fast");
        jQuery(".modal-backdrop").fadeToggle("fast");
        jQuery("body").removeClass("stop-scrolling");
      }

      // Close menu or search if escape key is pressed.
      jQuery(document).keyup(function(e) {

        // Escape key maps to keycode `27`
        if (jQuery("#modal-menu-overlay").is(":visible") && e.keyCode === 27) {
          closeAllMenus();
        }
      });

  	// Search Button Click handler
      jQuery("#search-button").click(function(e) {
        jQuery("#search").toggle("fast");

        jQuery("#modal-menu-overlay").fadeToggle("fast", function() {
          jQuery("#gsc-i-id1").focus();

          // When a browser or handheld device requires a scroll for the search
          // scroll to the top of the find drawer.
          jQuery("#search-scroller").animate({ scrollTop: 0 }, "fast");
        });

        jQuery("body").addClass("stop-scrolling");
        jQuery("#gsc-i-id1").focus();
        e.preventDefault();
      }); //end click handler

  	// Overlay Click handler
  	// The overlay appears when a menu or search is open, this prevents a user
  	// from clicking a link outside of these areas.
  	// When clicked, it should close all menus and hide itself.
      jQuery("#modal-menu-overlay").click(function() {
        closeAllMenus();
      });

  	// Menu Close Button Click handler
      jQuery("#menu-close").click(function() {
          jQuery("#navigation").hide("fast", function() {
            jQuery("#menu-button").focus();
          });

          jQuery("#modal-menu-overlay").fadeToggle("fast");
          jQuery("body").removeClass("stop-scrolling");
          //jQuery("#menu-button").focus();
      });

      // Search Close Button Click handler
      jQuery("#search-close").click(function () {
          jQuery("#search").hide("fast");
          jQuery("#modal-menu-overlay").fadeToggle("fast");
          jQuery(".modal-backdrop").fadeToggle("fast");
          jQuery("body").removeClass("stop-scrolling");
      });


      // Works with Drupal menu system to expand/collapse nested menu items.
      var lastExpandedMenu = null;

      jQuery("ul.menu-section-level-2 > li.expanded > a").click(function(e) {

          var expandedMenu = jQuery(this).siblings("ul.menu-section-level-3"); //should return 1 menu

          // If menu is hidden, then open it.
  		if(jQuery(expandedMenu).is(":hidden")) {

  		// If there was a previously opened menu, then close it.
          //console.log(jQuery(lastExpandedMenu).parent());

  		    if(lastExpandedMenu !== null) {
  		        jQuery(lastExpandedMenu).hide(200,function() {

  		            //console.log("remove Class from previous menu");
  		            //console.log(jQuery(lastExpandedMenu).parent());

  		            // Remove class from previously opened menu.
  		            jQuery(lastExpandedMenu).parent().removeClass("menu-opened");

  		            // Append class to active menu.
  		            jQuery(expandedMenu).parent().addClass("menu-opened");

  		            // Display active menu update last expanded menu variable.
  		            jQuery(expandedMenu).show(200,function() {
  		                lastExpandedMenu = expandedMenu;
  		            });

  		        });
  		    }
  		    else {
  			    // No previously opened menu
  			    jQuery(expandedMenu).parent().addClass("menu-opened");

  			    jQuery(expandedMenu).show(200,function() {
  			        lastExpandedMenu = expandedMenu;
  			    });
  		    }
          }
  		else if(jQuery(expandedMenu).is(":visible")) { //user clicking on already opened menu, so close it
  		lastExpandedMenu = null;

  			jQuery(expandedMenu).hide(200,function() {
  				jQuery(expandedMenu).parent().removeClass("menu-opened");
  			});
  		}

  	// Do not follow link, this link is used to expand menu.
  	e.preventDefault();
  	}); //end click handler


  	jQuery("#section-nav-toggle").click(function() {
  	  jQuery("#section-nav ul.menu-sections ul").toggle("fade");
  	});

  	// For A-Z index tab, located within Search menu, go to A-Z section.
    jQuery( "#a-z-glossary-tab-index .az-index-category-link" ).on( "click", function(e) {
  		//console.log(e.target.hash);
  		//jQuery( e.target.hash ).focus();
  		window.location.hash = e.target.hash;
      jQuery(e.target.hash).focus();
  		e.preventDefault();
  	});


    /*
    // For A-Z index AJAX call.
    var AZlinkClicked = false;
  	jQuery("#findtab-az-index").focus(function() {
      if (AZlinkClicked === false) {
        var request = jQuery.ajax({
          url: "/global-includes/a-z",
          type: "GET",
        });

        // AJAX Response
        request.done(function(data) {
          jQuery("#a-z-tab").hide().html(data).fadeIn();
          AZlinkClicked = true;
        });
      }

    });
    */

    // Hero video player related.

    // Show pause button if a video within a hero ends.
    if (jQuery( ".hero-video" ).length ) {
      jQuery( ".hero-video" ).on( "ended", function() {
        jQuery( ".hero-video-pause" ).hide();
        jQuery( ".hero-video-play" ).show();
      });
    }

    // Toggle play/pause button on a hero video.
    jQuery( ".hero-video-pause, .hero-video-play" ).on( "click", function() {
      // Return a DOM object
      // Will expand to handle multiple videos in the future
      // Re-tool this code for that
      //jQuery( ".hero-video").each(this.pause());

      var video = jQuery( ".hero-video" ).get(0);
      //console.log(video);

      if (video.paused) {
        video.play();
        jQuery( ".hero-video-pause" ).show();
        jQuery( ".hero-video-play" ).hide();
      }
      else {
        video.pause();
        jQuery( ".hero-video-pause" ).hide();
        jQuery( ".hero-video-play" ).show();
      }
      return false;

    });

    jQuery( ".jcarousel li img" ).each(function() {
      if (jQuery(this).data( "src" ))
        jQuery(this).attr( "src", jQuery(this).data("src")).data("loaded", true);
    });

    // For RFI form validator.
    jQuery( ".rfi-sign-up-form" ).submit(function( event ) {

      // Hide error message box for this form.
      jQuery(this).find('div.rfi-signup-form-msg').hide();
      
      // Create empty error message array.
      var errorMsgs = [];

      // Clear the error message box text span.
      jQuery(this).find('span.rfi-signup-form-msg-text').html('');

      // Find input elements for this specific form instance.
      var firstName = jQuery(this).find('input.rfi-first_name').val();
      var lastName = jQuery(this).find('input.rfi-last_name').val();
      var email = jQuery(this).find('input.rfi-email').val();
      
      // Remove error class for these form instances.
      jQuery(this).find('input.rfi-first_name').parent().removeClass( "has-error" );
      jQuery(this).find('input.rfi-last_name').parent().removeClass( "has-error" );
      jQuery(this).find('input.rfi-email').parent().removeClass( "has-error" );
      
      // Validate fields.

      if( firstName === "" ) {
        jQuery(this).find('input.rfi-first_name').parent().addClass( "has-error" );
        errorMsgs.push( "First Name" );
      }
      
      if( lastName === "" ) {
        jQuery(this).find('input.rfi-last_name').parent().addClass( "has-error" );
        errorMsgs.push( "Last Name" );        
      }      

      if ( !_isValidEmailAddress(email)) {
        jQuery(this).find('input.rfi-email').parent().addClass( "has-error" );
        errorMsgs.push( "Valid Email" );                
      }

      if ( errorMsgs.length > 0 ) {
        jQuery(this).find('span.rfi-signup-form-msg-text').html('Please provide the following: ');
        jQuery(this).find('span.rfi-signup-form-msg-text').append(errorMsgs.join(", "));
        jQuery(this).find('div.rfi-signup-form-msg').show();
        event.preventDefault();          
      }
      
      // Made through checks, allow form to submit.
      // @todo
      // The fields updated below are not form specific, consider updating using 
      // the same find methods above if necessary.
      // At this point, it should not matter.

      // Necessary js for UGRD RFI to work. 
      // Set sourcepageurl hidden input dynamically.
      jQuery( ".rfi-sourcepageurl" ).val( window.location.href );
      
      // For production use:
      var fullRFIpageurl = 'https://unlvcrm.force.com/students/CRFI';
      
      // For development use:
      //var fullRFIpageurl = 'https://ko-unlvcrm.cs54.force.com/students/CRFI';
      
      jQuery('.rfi-retURL').val(encodeURI(fullRFIpageurl +'?source=SimpleRFI&email=' + email + '&fname=' + firstName + '&lname=' + lastName));
    
    });

    // Any links targeting anchors will trigger this listener.
    // @todo
    // Change this to "on()" for dynamic markup.
    jQuery('#content-main a[href^="#"]').click(function () {

      // Extract hash from URL and append it to URL in browser.
      // Must do manually because of event.preventDefault().
      var href = this.href;
      var hash = href.substring(href.indexOf('#')); 
      window.location.hash = hash;


      var offset = jQuery( jQuery.attr(this, 'href') ).offset();
      var navOffset = _getNavOffset();

      // Scroll based on offset.
      var scrollTo = offset.top - navOffset;

      jQuery('html, body').animate({scrollTop:scrollTo}, 600);
      event.preventDefault();

    });

    // Helper function used to validate email addresses.
    function _isValidEmailAddress( emailAddress ) {
        var pattern = /^([a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+(\.[a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+)*|"((([ \t]*\r\n)?[ \t]+)?([\x01-\x08\x0b\x0c\x0e-\x1f\x7f\x21\x23-\x5b\x5d-\x7e\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|\\[\x01-\x09\x0b\x0c\x0d-\x7f\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))*(([ \t]*\r\n)?[ \t]+)?")@(([a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.)+([a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.?$/i;
        return pattern.test(emailAddress);
    }

    // Helper function used to return the navOffset used to scroll to when using
    // hash tags.
    function _getNavOffset() {

      // Not logged in default
      var navOffset = 73;

      // Change top navigation offset based on screen resolution.
      // Also, changes if user is logged in or not.
      if (jQuery( "body" ).hasClass( "admin-menu" ))
        var hasAdminMenu = true;
      else
        var hasAdminMenu = false;

      // User is logged in, account for admin bar.
      if (hasAdminMenu === true) {

        // Admin toolbar Default
        var navOffset = 120;

        if (jQuery(window).width() <= 767) 
          var navOffset = 120;
        else if (jQuery(window).width() <= 1023) 
          var navOffset = 152;      
        else if (jQuery(window).width() > 1024) 
          var navOffset = 133;   
      }
      else {
        // User not logged in.

        if (jQuery(window).width() <= 767) 
          var navOffset = 73;
        else if (jQuery(window).width() > 767) 
          var navOffset = 105;
      }

      return navOffset;
      //console.log('Viewport: ' + jQuery(window).width());
      //console.log('navOffset: ' + navOffset);
    }

  });
