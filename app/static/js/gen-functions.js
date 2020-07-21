/**
 * @file
 * Generic functions to be used on sitewide pages.
 */

// TFMAIL Code
var Clicked = 0;
var C12037089126262 = "tfmail/TFmail.pl";
var FormName = "wcform";
var C12037089126261 = "/cgiwrap/webcgi/";

/**
 * Used on form pages and used in the onclick handler to mitigate bots.
 */
function CL() { 

  var baseURL = "http://web.unlv.edu";

  Clicked++;

	if (Clicked > 1) 
	  return; 

  eval("document." + FormName + ".action='" + baseURL + C12037089126261+C12037089126262 + "'");
}

var Clicked2 = 0;

/**
 * Used on form pages and used in the onclick handler to mitigate bots.
 * Works like CL() but can be flexible with the ability to add additional mailer paths.
 *
 * @param string mailerType
 *   Looks for "tfmail" or "formmail".
 */
function CL2(mailerType) { 

  var FormName = "wcform";
  var baseURL = "http://web.unlv.edu";
  var C12037089126261 = "/cgiwrap/webcgi/";
  var C12037089126262 = null;
	
	
	if (mailerType === "tfmail")
	  C12037089126262 = "tfmail/TFmail.pl";
	else if (mailerType === "formmail")
	  C12037089126262 = "formmail/FormMail.pl";
	else {
	  alert("Invalid mailer type submitted");
	  return;
	}

  Clicked2++;

	if (Clicked2 > 1)
	  return; 

  eval("document." + FormName + ".action='" + baseURL + C12037089126261 + C12037089126262 + "'");
}


/**
 * Legacy function used to show and hide elements.
 *
 * @param string elemID
 *   The element's ID.
 *
 * @param bool toggle
 *   Specifies whether to hide or show element.
 */
function showElem(elemID,toggle) {
	
  if (toggle)
	  toggle = "block";
	else
	  toggle = "none";
	
  document.getElementById(elemID).style.display = toggle;
}

// SetEqualHeights
// Sets divs to an equal height.
// Pre-condition: Sends in a comma separated string such as "test1,test2,test3".
// Post-condition: Will set the DIVs to an equal height to the largest DIV.
function setEqualHeights(elemList) {
  var elemArray = elemList.split(",");
  var tallestElemHeight = null;
  var currElemHeight = null;
  var i = 0;
    
	for (i = 0; i<elemArray.length; i++) {
	
	  if (document.getElementById(elemArray[i]))	
	    currElemHeight	= document.getElementById(elemArray[i]).offsetHeight;	
	  else {
      alert("Invalid DIV ID: " + elemArray[i] + " passed in.");
      return;
    }
	
		if (i === 0) {
		  tallestElemHeight = currElemHeight;
		  continue;
		}
		else {
      if (tallestElemHeight < currElemHeight)
        tallestElemHeight = currElemHeight;
		}
		
	} // End for loop.


	for (i = 0; i < elemArray.length; i++) {
	  document.getElementById(elemArray[i]).style.height = tallestElemHeight + "px";
	}
}

jQuery(document).ready(function(){
	// Close button for any messages (white design).
	jQuery( "a.msg-close" ).click(function() {		
    jQuery(this).closest( "div.msg" ).hide();	
    
    // Prevent event bubbling to href.
		return false;
	});
});