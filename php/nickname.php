<?php

include 'creds.php';

if($_GET['nickname']){

	$connection = mysqli_connect($host, $user, $pass, $db_name);

	if(mysqli_connect_errno()){
		die("connection failed: ".mysqli_connect_error()." (".mysqli_connect_errno().")");
	}

	$result = mysqli_query($connection, "UPDATE hosts SET nickname='".$_GET['nickname']."' WHERE id=".$_GET['id']."");

	if(! $result){
		die("could not update data: ".mysql_error());
	}	

	header('Location: index.php');
	exit();

} else {
	echo '<form>';
	echo ' <input type="hidden" name="id" id="id" value="'.$_GET['id'].'">';
	echo ' <input type="text" id="nickname" name="nickname">';
	echo ' <input type="submit" value="Submit">';
	echo '</form>';
}
?>
