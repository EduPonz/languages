window.onload = function() {
	var ip = window.location.origin;
	console.log('Window origin is ' + ip);
	onCreate();
	document.getElementById("btn_sign_up").onclick = function() {insert_user()}
	document.getElementById("btn_loggin").onclick = function() {log_in()}
	document.getElementById("btn_update_user").onclick = function() {update_user()}
	document.getElementById("btn_insert_verb").onclick = function() {insert_verb()}
	document.getElementById("btn_update_verb").onclick = function() {update_verb()}
	// document.getElementById("btn_answer").onclick = function() {isCorrect()}
	// document.getElementById("btn_see_answer").onclick = function() {seeAnswer()}

	function onCreate() {
		document.getElementById("title").innerHTML = "Development page";
		document.getElementById("signup_title").innerHTML = "Sign up";
		document.getElementById("loging_title").innerHTML = "Log in";
		document.getElementById("update_user_title").innerHTML = "Update user";
		document.getElementById("insert_verb_title").innerHTML = "Insert verb";
		document.getElementById("update_verb_title").innerHTML = "Update verb";
	}

	function isCorrect() {
		var word = document.getElementById("word").innerHTML;
		var answer = document.getElementById("answer").value;

		if (word == "Hej" && answer == "hello") {
			document.getElementById("result").innerHTML = "GREAT JOB!";
		} else {
			document.getElementById("result").innerHTML = "WRONG!";
		}
	}

	function seeAnswer() {
		var word = document.getElementById("word").innerHTML;

		if (word == "Hej") {
			document.getElementById("result").innerHTML = "hello";
		}
	}

	function insert_user() {
		var username = document.getElementById("username").value;
		var password = document.getElementById("password").value;
		var confirm_password = document.getElementById("confirm_password").value;
		var e_mail = document.getElementById("e_mail").value;

		if (password != confirm_password) {
			document.getElementById("result").innerHTML = "Input passwords do not match!";
		} else {
			insert_user_request(username, password, e_mail);
		}
	}

	function insert_user_callback(result) {
		document.getElementById("result").innerHTML = result.toString();
	}

	function insert_user_request(username, password, e_mail) {
		var timestamp = new Date().toUTCString();
		type = 'insert_user'
		var data = {
			":id": uuid,
			"data": {
				"username": username,
				"password": password,
				"email": e_mail
			},
			"type": type,
			"timestamp": timestamp,
		};

		$.ajax({
			url: ip + ':5000/insert-user',
			method: 'POST',
			data: JSON.stringify(data),
			dataType: 'json',
			headers: {'Content-type': 'application/json',},
			success: function(response) {
				console.log("Post data " + data['data']);
				console.log("Flask response " + response['data']);
				insert_user_callback(response['data']);
			},
			error: function(error) {
				console.log("Problem sending test request. " + error);
				insert_user_callback(error);
			}
		})
	}

	function log_in() {
		var username = document.getElementById("username_login").value;
		var password = document.getElementById("password_login").value;

		login_request(username, password);
		// document.getElementById("username_login").value = '';
		// document.getElementById("password_login").value = '';
	}

	function login_callback(result) {
		document.getElementById("result_login").innerHTML = result.toString();
	}

	function login_request(username, password) {
		var timestamp = new Date().toUTCString();
		type = 'check_login'
		var data = {
			":id": uuid(),
			"data": {
				"username": username,
				"password": password
			},
			"type": type,
			"timestamp": timestamp,
		};

		$.ajax({
			url: ip + 	':5000/check-login',
			method: 'POST',
			data: JSON.stringify(data),
			dataType: 'json',
			headers: {'Content-type': 'application/json',},
			success: function(response) {
				console.log("Post data " + data['data']);
				console.log("Flask response " + response['data']);
				login_callback(response['data']);
			},
			error: function(error) {
				console.log("Problem sending test request. " + error);
				login_callback(error);
			}
		})
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
			update_user_request(username, password, new_username, new_password, new_email);
		}
	}

	function update_user_callback(result) {
		document.getElementById("update_result").innerHTML = result;
	}

	function update_user_request(username, password, new_username, new_password, new_email) {
		var timestamp = new Date().toUTCString();
		type = 'update_user'
		var data = {
			":id": uuid(),
			"data": {
				"username": username,
				"password": password,
				"new_username": new_username,
				"new_password": new_password,
				"new_email": new_email

			},
			"type": type,
			"timestamp": timestamp,
		};

		$.ajax({
			url: ip + ':5000/update-user',
			method: 'POST',
			data: JSON.stringify(data),
			dataType: 'json',
			headers: {'Content-type': 'application/json',},
			success: function(response) {
				console.log("Post data " + data['data']);
				console.log("Flask response " + response['data']);
				update_user_callback(response['data']);
			},
			error: function(error) {
				console.log("Problem sending test request. " + error);
				update_user_callback(error);
			}
		})
	}

	function insert_verb() {
		var infinitive = document.getElementById("verb_infinitive").value.toLowerCase().trim();
		var present = document.getElementById("verb_present").value.toLowerCase().trim();
		var past = document.getElementById("verb_past").value.toLowerCase().trim();
		var present_perfect = document.getElementById("verb_present_perf").value.toLowerCase().trim();
		var infinitive_eng = document.getElementById("verb_infinitive_eng").value.toLowerCase().trim();
		var topic = document.getElementById("verb_topic").value.toLowerCase().trim();

		insert_verb_request(infinitive, present, past, present_perfect, infinitive_eng, topic);
	}

	function insert_verb_callback(result) {
		document.getElementById("insert_verb_result").innerHTML = result;
	}

	function insert_verb_request(infinitive, present, past, present_perfect, infinitive_eng, topic) {
		var timestamp = new Date().toUTCString();
		type = 'insert_verb'
		var data = {
			":id": uuid(),
			"data": {
				"infinitive": infinitive,
				"present": present,
				"past": past,
				"present_perfect": present_perfect,
				"infinitive_eng": infinitive_eng,
				"topic": topic
			},
			"type": type,
			"timestamp": timestamp,
		};

		$.ajax({
			url: ip + ':5000/insert-verb',
			method: 'POST',
			data: JSON.stringify(data),
			dataType: 'json',
			headers: {'Content-type': 'application/json',},
			success: function(response) {
				console.log("Post data " + data['data']);
				console.log("Flask response " + response['data']);
				insert_verb_callback(response['data']);
			},
			error: function(error) {
				console.log("Problem sending test request. " + error);
				insert_verb_callback(error);
			}
		})
	}

	function update_verb() {
		var infinitive = document.getElementById("verb_infinitive_up").value.toLowerCase().trim();
		var new_infinitive = document.getElementById("new_verb_infinitive").value.toLowerCase().trim();
		var new_present = document.getElementById("new_verb_present").value.toLowerCase().trim();
		var new_past = document.getElementById("new_verb_past").value.toLowerCase().trim();
		var new_present_perfect = document.getElementById("new_verb_present_perf").value.toLowerCase().trim();
		var new_infinitive_eng = document.getElementById("new_verb_infinitive_eng").value.toLowerCase().trim();

		update_verb_request(infinitive, new_infinitive, new_present, new_past,
							new_present_perfect, new_infinitive_eng);
	}

	function update_verb_callback(result) {
		document.getElementById("update_verb_result").innerHTML = result;
	}

	function update_verb_request(infinitive, new_infinitive, new_present, new_past,
							     new_present_perfect, new_infinitive_eng) {
		var timestamp = new Date().toUTCString();
		type = 'update_verb'
		var data = {
			":id": uuid(),
			"data": {
				"infinitive": infinitive,
				"new_infinitive": new_infinitive,
				"new_present": new_present,
				"new_past": new_past,
				"new_present_perfect": new_present_perfect,
				"new_infinitive_eng": new_infinitive_eng
			},
			"type": type,
			"timestamp": timestamp,
		};

		$.ajax({
			url: ip + ':5000/update-verb',
			method: 'POST',
			data: JSON.stringify(data),
			dataType: 'json',
			headers: {'Content-type': 'application/json',},
			success: function(response) {
				console.log("Post data " + data['data']);
				console.log("Flask response " + response['data']);
				update_verb_callback(response['data']);
			},
			error: function(error) {
				console.log("Problem sending test request. " + error);
				update_verb_callback(error);
			}
		})
	}

	function uuid() {
		var uuid = "", i, random;
		for (i = 0; i < 32; i++) {
			random = Math.random() * 16 | 0;

			if (i == 8 || i == 12 || i == 16 || i == 20) {
				uuid += "-";
			}
			uuid += (i == 12 ? 4 : (i == 16 ? (random & 3 | 8) : random)).toString(16);
		}
		return uuid;
	}
}