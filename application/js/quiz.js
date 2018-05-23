function onCreate() {
	document.getElementById("title").innerHTML = "Development page";
	document.getElementById("signup_title").innerHTML = "Sign up";
	document.getElementById("loging_title").innerHTML = "Log in";
	document.getElementById("update_user_title").innerHTML = "Update user";
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
	
	} else if (response == 'login correct' || response == 'Cannot check login') {
		document.getElementById("result_login").innerHTML = response;
		document.getElementById("username_login").value = '';
		document.getElementById("password_login").value = '';

	} else if (response == 'login not correct') {
		document.getElementById("result_login").innerHTML = response;
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

function check_login() {
	var username = document.getElementById("username_login").value;
	var password = document.getElementById("password_login").value;

	var url;
	url = '/cgi-bin/db_manager.py?';
	url += 'login=' + encodeURIComponent('login');
	url += '&username=' + encodeURIComponent(username);
	url += '&password=' + encodeURIComponent(password);
	callAjax(url, requestCallback);
}

function update_user() {
	var username = document.getElementById("update_username").value;
	var password = document.getElementById("update_password").value;
	var new_username = document.getElementById("update_new_username").value;
	var new_password = document.getElementById("update_new_password").value;
	var confirm_password = document.getElementById("update_new_confirm_pwd").value;
	var new_email = document.getElementById("update_new_e_mail").value;

	if (new_password != confirm_password) {
		document.getElementById("update_result").innerHTML = "New passwords do not match!";
	} else {
		var url;
		url = '/cgi-bin/db_manager.py?';
		url += 'update_user=' + encodeURIComponent('update');
		url += '&username=' + encodeURIComponent(username);
		url += '&password=' + encodeURIComponent(password);
		url += '&new_username=' + encodeURIComponent(new_username);
		url += '&new_password=' + encodeURIComponent(new_password);
		url += '&new_email=' + encodeURIComponent(new_email);
		callAjax(url, requestCallback);
	}
}