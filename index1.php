<!DOCTYPE HTML>
<!--
	Solarize by TEMPLATED
	templated.co @templatedco
	Released for free under the Creative Commons Attribution 3.0 license (templated.co/license)
-->
<html>
	<head>
		<title>Prediction Kaya</title>
		<meta http-equiv="content-type" content="text/html; charset=utf-8" />
		<meta name="description" content="" />
		<meta name="keywords" content="" />
		<!--[if lte IE 8]><script src="css/ie/html5shiv.js"></script><![endif]-->
		<script src="js/jquery.min.js"></script>
		<script src="js/jquery.dropotron.min.js"></script>
		<script src="js/skel.min.js"></script>
		<script src="js/skel-layers.min.js"></script>
		<script src="js/init.js"></script>

		<link rel="stylesheet" media="all" type="text/css" href="jquery-ui.css" />
		<link rel="stylesheet" media="all" type="text/css" href="jquery-ui-timepicker-addon.css" />
		<script type="text/javascript" src="jquery-1.10.2.min.js"></script>
		<script type="text/javascript" src="jquery-ui.min.js"></script>
		<script type="text/javascript" src="jquery-ui-timepicker-addon.js"></script>
		<script type="text/javascript" src="jquery-ui-sliderAccess.js"></script> 

		
		<!-- <link rel="stylesheet" type="text/css" href="css/bootstrap/css/bootstrap.min.css" /> -->
		

		<noscript>
			<link rel="stylesheet" href="css/skel.css" />
			<link rel="stylesheet" href="css/style.css" />
		</noscript>
		<!--[if lte IE 8]><link rel="stylesheet" href="css/ie/v8.css" /><![endif]-->
	</head>
	<style>
		.button {
			  display: inline-block;
			  border-radius: 4px;
			  background-color: #f4511e;
			  border: none;
			  color: #FFFFFF;
			  text-align: center;
			  font-size: 28px;
			  padding: 20px;
			  width: 350px;
			  transition: all 0.5s;
			  cursor: pointer;
			  margin: 5px;
			}
			.button span {
			  cursor: pointer;
			  display: inline-block;
			  position: relative;
			  transition: 0.5s;
			}
			.button span:after {
			  content: '';
			  position: absolute;
			  opacity: 0;
			  top: 0;
			  right: -20px;
			  transition: 0.5s;
			}

			.button:hover span {
			  padding-right: 25px;
			}

			.button:hover span:after {
			  opacity: 1;
			  right: 0;
			}
			.overlay {   
				position: absolute;  
				top: 0px;   
				left: 0px;  
				background: #ccc;   
				width: 100%;   
				height: 100%;   
				opacity: .75;   
				filter: alpha(opacity=75);   
				-moz-opacity: .75;  
				z-index: 999;  
				background: #fff url(http://i.imgur.com/KUJoe.gif) 50% 50% no-repeat;
			}   
			.main-contain{
				position: absolute;  
				top: 0px;   
				left: 0px;  
				width: 100%;   
				height: 100%;   
				overflow: hidden;
			}
				</style>
	<body class="homepage">

		<!-- Header Wrapper -->
			<div class="wrapper style1">
			
			
				
			<!-- Banner -->
				<div id="banner">
					<section class="container">
						<h2>prediction kaya</h2>                    
					</section>
				</div>

			</div>
		
			<!-- Section One -->
				<div class="wrapper style2">
					<section class="container">
						<div class="row double">
							<div class="6u">
								<header class="major">
									<h2>กรุณาเลือกถังขยะ</h2>
									<span class="byline">   
									<!-- <form action="Noname2.php" method="post"> -->
									<select name="ddlStatus1" id="ddlStatus1">
										<?  
													header('Content-Type: text; charset=utf-8');
													$json = file_get_contents('http://localhost:5000/todo/api/v1.0/tasks');
													$array = json_decode($json,true);
													$obj = json_decode($json);
												foreach($array['task'] as $key=> $i){?>
												<!-- <option value="<?//echo $array['task'][$key]['sensor']['id'];?>"> --><? //enter
													// echo $array['task'][$key]['sensor']['id']; // enter
														// echo $array['task'][$key]['sensor']['id'];
												
												if($i["node"] != null){
													foreach($i["node"] as $bb=>$aa){?> 
														<option value='<?echo $aa['sensor']['id'];?>'>
														<?
														$ii += 1;
														echo ("ถังที่".$ii."....".$aa['name']); //
														echo "</option>";
													}
														$ii = 0;
												}
												// echo "</option>";
												// $aa['sensor']['id']
											}

										
											?>
										
											</select>

									

													
													

											</span>


								
								<!--  -->
											
											<?          
											//print $obj->coord[0]->lon;
											//print $obj->coord[0]->lon;
											//echo $obj->task->"10"->sensor->id ."\n";;
											#print_r($obj);
											//echo $array['task']['10']['sensor']['id']."\n";
											//$a = $array['task']['10']['sensor']['id'];
											#print_r($array);
											?>
											
											

									
										
											
										<!--    <button  class="MyButton" id="submit"   type="summit">Register </button>
											<input type="text" name="ddlStatus" id="ddlStatus" value="ddlStatus1" /> -->
								</header>
							</div>
							<div class="6u">

								<h3>กรุณาเลือกเวลาในการทำนาย</h3>
								<?php 
								date_default_timezone_set("Asia/Bangkok");?>

								<script type="text/javascript" id="time1">
									$(function(){
									$("#dateInput").datetimepicker({
									dateFormat: 'yy-mm-dd',
									timeFormat: "HH:mm:ss"
									 });
									});
									
							</script>
							<div id="div1"></div>
							<form action="Noname2.php" method="post" >
								<input type="text" name="dateInput" id="dateInput" value="" /><br>
								<center ><button  class="button" style="vertical-align:middle" id="submit" type="button"><span>ให้คุกกี้ทำนายกัน..!!</span></button>
								</form>
								</div>
							
							
								
								
							



							
						</div>

					</section>
				
				</div>

<br><br>
		<font color="yellow"><h1><p>Output: <input type="text" id="test3" value=""></p></h1></font>

			
	<!-- Footer -->
		<div id="footer">
			<section class="container">
				<header class="major">
					<h2>Connect with us</h2>
					<span class="byline">parninw</span>
				</header>
				<ul class="icons">
					<li class="active"><a href="#" class="fa fa-facebook"><span>Facebook</span></a></li>
					<li><a href="#" class="fa fa-twitter"><span>Twitter</span></a></li>
					<li><a href="#" class="fa fa-dribbble"><span>Pinterest</span></a></li>
					<li><a href="#" class="fa fa-google-plus"><span>Google+</span></a></li>
				</ul>
				<hr />
			</section>
			
					
		</div>

	</body>
   <!--  <div class="overlay"></div> -->
<script>
		$(function() {
		$('#submit').click(function() {
			 $("#div1").addClass("overlay");
			 // $(".overlay").fadeOut("slow");
			// $(".main-contain").removeClass("main-contain");
			var sensor = $(ddlStatus1).val();
			var date = $(dateInput).val();
			var current_local_time = new Date();
			var current_date = current_local_time.getFullYear() + "-" + (current_local_time.getMonth("m")+1) + "-" + current_local_time.getDate("d") + " " + current_local_time.getHours("H") + ":" + current_local_time.getMinutes("i") + ":" +current_local_time.getSeconds("s");
			current_date = current_date.replace(" ","T");
			current_date = current_date +'+07:00';
			// modify date value
			date = date.replace(" ", "T");
			date = date +'+07:00';
			var url = 'http://localhost:5000/predict_bin/'+sensor+"/"+date
			console.log(url);
			// if(date < current_date){
			//  console.log(current_date);
			//  alert("Time error");
			// }
			//else{
			$.ajax({
				url: url,
				type: 'GET',
				success: function(response) {
					console.log(response);
					$("#div1").removeClass("overlay");
					 $("#test3").val(response["predicted_lv"]);
				},
				error: function(error) {
					console.log(error);
					$("#div1").removeClass("overlay");
				}
			});
			//}
		});
	});
</script>

<!-- <script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>   -->
<!-- <script   src="//ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>  -->
<!-- <script type="text/javascript">
$(function(){
	$("#overlay").fadeOut();
	$(".main-contain").removeClass("main-contain");
});
</script> -->

</html>

<script>
$(function () {
	$('#ddlStatus2').click(function() {

		if($(ddlStatus2).val() == "ตรงข้ามโรงแรมบ้านไท"){
		console.log("55555555555");
		document.getElementById("mySelect").options;
		
	}


	});
});

 	
</script>



