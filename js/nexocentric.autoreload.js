//──────────────────────────────────────────────────────────────────────────────
// Function Declarations
//──────────────────────────────────────────────────────────────────────────────

/*
 * Define these variables for your environment :-
 *  ajaxHandlerPath = "http://development.server/path/to/AjaxHandler.cgi";
 *  ajaxTimeout = 300; // seconds
 */
var ajaxHandlerPath = "http://localhost/cgi-bin/AjaxHandler.py";
var ajaxTimeout = 300;
var ajaxRequest = null;

//==========================================================
// [author]
// Dodzi Y. Dzakuma
// [summary]
// This function determines whether to refresh the browser
// based on the information in it's first parameter.
// [parameters]
// 1) a json object processed by statMonitoredFiles
// [return]
// 1) true on browser reload
// 2) false if no reload needed
//==========================================================
function forceBrowserRefresh(json)
{
	//----------------------------------
	// initializations
	//----------------------------------
	var updateStatus = json.updateStatus; // the status sent from the PHP script
	var previousUpdateStatusList = json.previousUpdateStatusList; // compressed
	var initialized = $('meta[name=previousUpdateStatusList]').attr('content');
	
	//----------------------------------
	// load the list of update stats
	// into the meta tag for this page
	//----------------------------------
	$('meta[name=previousUpdateStatusList]').attr(
		'content', 
		previousUpdateStatusList
	);

	//----------------------------------
	// check to see if reload needed
	// or if this is the first display
	// of the page
	//----------------------------------
	if (updateStatus) {
		// data updated
		location.reload();
		//return true;
		return false;
	} else if (!initialized) {
		// first load of the page
		console.log("auto-reload initialized");
	}
	return false;
}

//==========================================================
// [author]
// Dodzi Y. Dzakuma
// [summary]
// If this website is in development mode, this sends a
// a request to the site's AJAX handler to check for any
// changes made to files that the current page being 
// displayed uses. Upon a successful request the the process
// calls forceBrowserRefresh.
// [parameters]
// none
// [return]
// none
//==========================================================
(function statMonitoredFiles() {
	//----------------------------------
	// get the needed information for
	// file monitoring from the meta
	// tags of this page
	//----------------------------------
	var monitorList = $('meta[name=monitorList]').attr('content');
	var previousUpdateStatusList = $('meta[name=previousUpdateStatusList]').attr('content');
	
	//----------------------------------
	// make the AJAX call and wait
	// for a reply from PHP
	//----------------------------------
	$.ajax({
		url: ajaxHandlerPath,
		type: 'POST',
		data: {
			requestType : 'statMonitoredFiles',
			'monitorList' : monitorList,
			'previousUpdateStatusList' : previousUpdateStatusList,
			timeout : ajaxTimeout
		},
		success: forceBrowserRefresh,
		dataType: 'json',
		complete: statMonitoredFiles, // this is the key to long polling
		timeout: (ajaxTimeout*1000)+5000  // add 5000 ms to timeout to give script time to return
	});
})();
