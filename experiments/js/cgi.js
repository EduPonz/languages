function callAjax(url, callback) {
	
	var xmlhttp;
	xmlhttp = new XMLHttpRequest();
	
	xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
			callback(xmlhttp.responseText);
		}
	}
	
	xmlhttp.open("GET", url, true);
	xmlhttp.send();
}

function sendRequest(data) {
	var python_url;
 	python_url = '/cgi-bin/who.py?myData=' + encodeURIComponent(data);
 	callAjax(python_url, requestCallback);
}

function requestCallback(response) {
	document.getElementById("result").innerHTML = response;
}