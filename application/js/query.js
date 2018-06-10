window.onload = function() {
	var ip = window.location.origin;
	console.log('Window origin is ' + ip);
	document.getElementById("btn_loggin").click(function() {
		console.log('clicked!')
		var username = document.getElementById("username_login").value;
		var password = document.getElementById("password_login").value;

		var timestamp = new Date().toUTCString();
		data = 'test message'
		var test_data = {
			":id": "e704de14-7e10-4436-bb81-c334bacd419a",
			"data": data,
			"username": username,
			"password": password,
			"timestamp": timestamp,
		};

		$.ajax({
			url: ip+':5000/test',
			method: 'POST',
			data: JSON.stringify(test_data),
			dataType: 'json',
			headers: {'Content-type': 'application/json',},
			success: function(response) {
				console.log("Post data " + data);
				console.log("Flask response " + response);
			},
			error: function(error) {
				console.log("Problem sending test request " + error);
			}
		})
	});
}