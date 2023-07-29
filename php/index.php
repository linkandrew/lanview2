<?php

include 'creds.php';

//create connection
$connection = mysqli_connect($host, $user, $pass, $db_name);

//test if connection failed
if(mysqli_connect_errno()){
    die("connection failed: " . mysqli_connect_error() . " (" . mysqli_connect_errno() . ")");
}

echo '<head><meta http-equiv="refresh" content="600"></head>';
echo '<form method="post" action="index.php">';
echo ' <button name="display" type="submit" value="all">All</button>';
echo ' <button name="display" type="submit" value="old">Old</button>';
echo ' <button name="display" type="submit" value="new">New</button>';
echo '</form>';

$query_string_new = "SELECT id,status,mac,ip,hostname,vendor,nickname,first_seen,last_seen FROM hosts WHERE visible = 0";
$query_string_old = "SELECT id,status,mac,ip,hostname,vendor,nickname,first_seen,last_seen FROM hosts WHERE visible = 1";
$query_string_all = "SELECT id,status,mac,ip,hostname,vendor,nickname,first_seen,last_seen FROM hosts";
$query_string_use = "";

$display = $_POST['display'];

if(empty($display) or $display == "new"){
	$query_string_use = $query_string_new;
} elseif ($display == "all") {
	$query_string_use = $query_string_all;
} elseif ($display == "old") {
	$query_string_use = $query_string_old;
} else {
	echo "Somthing went wrong using post to get display options!";
}

$result = mysqli_query($connection, $query_string_use);
$all_property = array();  //declare an array for saving property

//showing property
echo '<table class="data-table" border=1 cellpadding=5>';
echo '<tr class="data-heading">';
while ($property = mysqli_fetch_field($result)) {
    echo '<td>' . $property->name . '</td>';  //get field name for header
    array_push($all_property, $property->name);  //save those to array
}
echo '</tr>';
$count = 0;
$col_count = count($all_property) - 1; // hmmmm.

//showing all data
while ($row = mysqli_fetch_array($result)) {
    echo "<tr>";

    foreach ($all_property as $key => $item) {

    	if($row[$item] == 'unknown'){
    		$bg = 'grey';
	} elseif($row[$item] == 'up'){
		$bg = 'green';
	} elseif($row[$item] == 'down'){
		$bg = 'red';
    	} else {
        	$bg = 'white';
    	}

	// Maybe move to column operation
	$epoch_regex = '/^[0-9]{10}$/';
	if(preg_match($epoch_regex, $row[$item])){
		$row[$item] = date('Y-m-d H:i:s', $row[$item]);
		$bg = 'lightblue';
	}

	// Column operations
	if ($count == 6) {

		if ($row[$item] == '')
			$row[$item] = 'set nickname';

       		echo '<td column='.$count.' bgcolor='.$bg.'><a href=nickname.php?id='.$row[0].' id='.$row[0].'>'.$row[$item].'</a></td>';
	} else {
       		echo '<td column='.$count.' bgcolor='.$bg.'>'.$row[$item].'</td>';
	}

	// Reset column counter
	if ($count == $col_count) {
		$count = 0;
	} else {
		$count++;
	}
    }
    echo '</tr>';
}

echo "</table>";
?>
