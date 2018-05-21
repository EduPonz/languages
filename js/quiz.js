function onCreate() {
	document.getElementById("title").innerHTML = "Word Quiz";
	create_tables();
}

function isCorrect() {
	var word = document.getElementById("word").innerHTML;
	var answer = document.getElementById("answer").value;

	if (word == "Hej" && answer == "hello") {
		document.getElementById("result").innerHTML = "GREAT JOB!";
	}

}

function seeAnswer() {
	var word = document.getElementById("word").innerHTML;

	if (word == "Hej") {
		document.getElementById("result").innerHTML = "hello";
	}

}

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

function create_tables() {
	var url;
	var verbs_table = 'verbs'
	url = '/cgi-bin/db_manager.py?';
	url += 'create table=' + encodeURIComponent(verbs_table);
	callAjax(url, requestCallback);	
}