//function funcBefore () {$("#information").text ("Ожидание данных...");}

//function funcSuccess (data) {
//	$("#information").text (data);
//}

$(document).ready (function () {
	$(".modalWindow").bind("click", function () {
		var person = this.innerHTML;
		var personId = this.id;
		$.ajax ({
			url: "header.php",
			type: "POST",
			data: ({name: person, nameId: personId}),
			dataType: "html",
			//beforeSend: funcBefore,
			//success: funcSuccess
		})
	})
})