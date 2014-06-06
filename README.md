cgi-autoreload
==============

cgi-autoreload is a tool used to automatically reload a web URL when a list of files are changed. This allows the development-testing cycle to be partially automated, saving some time.

To use, choose your backend script from the directories such as 
* python/
* php/

and place in your development server's cgi-bin (or appropriate location).

The JavaScript must be included in the webpage (as well as its dependency, JQuery). Use an HTML <meta> tag to track a list of files for updates.
The JavaScript is found in /js/ and an example html file in /test/
