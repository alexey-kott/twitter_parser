<!--
EXPERIMENT


news.php

<br>
<script src="modal-window.js"></script>
<br>
<a class="modalWindow" id="thoilliez" data-toggle="modal" data-target="#ModalEx">Bianca Thoilliez</a>
<p id="information">!!!</p>
<br>



for-ajax.php

<?php
//		if (isset($_POST['name']))
		{
//		$name = $_POST['name'];
//		$nameId = $_POST['nameId'];
//		$links = "members/".$nameId.".php";
//		echo $links;
		}
		?>



news.php

<div class="modal fade" id="ModalEx" tabindex="-1" role="dialog" aria-labelledby="ModalLongTitle" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
      	<h4 class="modal-title" id="ModalLongTitle"></h4>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body" id="modalBodyId">
    	<?php
//			if (isset($_POST['name']))
			{
//				$name = $_POST['name'];
//				$nameId = $_POST['nameId'];
//				$links = "members/".$nameId.".php";
//				require $links;
//			}
    	?>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Cerrar</button>
      </div>
    </div>
  </div>
</div>


modal-window.js

//function funcBefore () {$("#information").text ("Ожидание данных...");}

//function funcSuccess (data) {
//	$("#information").text (data);
//}

$(document).ready (function () {
	$(".modalWindow").bind("click", function () {
		var person = this.innerHTML;
		var personId = this.id;
		$.ajax ({
			url: "for-ajax.php",
			type: "POST",
			data: ({name: person, nameId: personId}),
			dataType: "html",
			//beforeSend: funcBefore,
			//success: funcSuccess
		})
	})
})

-->