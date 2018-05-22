function onCreate() {
	document.getElementById("title").innerHTML = "Development page";
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
	// console.log('URL -> ' + url);
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
	// document.getElementById("result").innerHTML = response;
	console.log(response);
	if (response == "User already exists!") {
		document.getElementById("result").innerHTML = response;

	} else if (response == "User inserted!") {
		document.getElementById("result").innerHTML = response;
		document.getElementById("username").value = '';
		document.getElementById("password").value = '';
		document.getElementById("confirm_password").value = '';
		document.getElementById("e_mail").value = '';
	}
}

function create_tables() {
	var url;
	var table = 'verbs'
	url = '/cgi-bin/db_manager.py?';
	url += 'create table=' + encodeURIComponent(table);
	callAjax(url, requestCallback);

	table = 'nouns'
	url = '/cgi-bin/db_manager.py?';
	url += 'create table=' + encodeURIComponent(table);
	callAjax(url, requestCallback);

	table = 'users';
	url = '/cgi-bin/db_manager.py?';
	url += 'create table=' + encodeURIComponent(table);
	callAjax(url, requestCallback);
}

function insert_user() {
	var username = document.getElementById("username").value;
	var password = document.getElementById("password").value;
	var confirm_password = document.getElementById("confirm_password").value;
	var e_mail = document.getElementById("e_mail").value;

	if (password != confirm_password) {
		document.getElementById("result").innerHTML = "Input passwords do not match!";
	} else {
		var url;
		var table = 'users';
		url = '/cgi-bin/db_manager.py?';
		url += 'insert=' + encodeURIComponent(table);
		url += '&username=' + encodeURIComponent(username);
		url += '&password=' + encodeURIComponent(password);
		url += '&email=' + encodeURIComponent(e_mail);
		callAjax(url, requestCallback);
	}
}