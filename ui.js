// It will form a div with the information of one finding. It will be shown by clicking
// on a finding.
function getFindingInfoElement(e, ID,  x, y, type, depth, notes, W){
	var z = document.createElement('div');
	z.id = ID;
	var zx = e.pageX;
	var zy = e.pageY-100;
	width= 140; 
	height= 100;
	if (zy<0){
		zy=zy+height;
	}
	if (zy+100>W){
		zy=zy-height;
	}
	if (zx<0){
		zx=zx+width;
	}
	if (zx+140>W){
		zx=zx-width;
	}
	z.style.cssText = "position: absolute; left: "+zx+"px; top:  "+zy+"px; opacity:;"
	+ "background: grey; width:" +width+"px; height:"+height+"px; border-radius: 5px; color: black";
	z.innerHTML = "(X,Y,Z)= ("+x+","+y+","+depth+") <br> Type of Find:"+type+" <br> Field notes:"+notes;
    return z;
}

// The above div will be shown by clicking the finding. If we click again, it will be
// removed by calling removeFindingInfo.
function showFindingInfo(e, ID,  x, y, type, depth, notes){
	var find_info = document.getElementById(ID);
	if (find_info){//I should remove because it has been pressed twice
		removeFindingInfo(e,ID);
	}
	else{//we should add
	find_info = getFindingInfoElement(e, ID,  x, y, type, depth, notes);
	document.getElementById('root').appendChild(find_info);
	}
	
}


// function showFindingInfo(e, ID,  x, y, type, depth, notes){
// 	var find_info = document.getElementById(ID);
// 	if (find_info || (Date.now()-lastAddTime)<2000){
// 		return;
// 	}
// 	lastAddTime = Date.now();
// 	find_info = getFindingInfoElement(e, ID,  x, y, type, depth, notes);
// 	document.getElementById('root').appendChild(find_info);
// 	setTimeout(function(){ document.getElementById('root').removeChild(find_info) }, 5000);
// }

// Removes the info for the specified finding
function removeFindingInfo(e, ID){
	var find_info = document.getElementById(ID);
	if (find_info){
		document.getElementById('root').removeChild(find_info)
	}
// 	setTimeout(function(){var find_info = document.getElementById(ID);if (find_info){document.getElementById('root').removeChild(find_info)}}, 2000);
	
}

//This function makes an AJAX call to delete one row from the specified table (tab).
// tab can be either "fields", or "finds".
function deleteTable(e,fid, tab) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
			 window.location.reload();
        }

    };

    var q = ''
    if (tab=='fields'){
    	q = 'Are you sure you want to delete field "'+fid+'"?';
    }
    else{
	    q = 'Are you sure you want to delete finding "'+fid+'"?';
    }
    
//     We ask the use if he/she is sure about deleting

    if (confirm(q)) {

        xhttp.open("POST", "https://www.geos.ed.ac.uk/~s1757431/cgi-bin/delete.py", true);
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.send("fid=" +fid+"&tab="+tab);
    }

}

// An AJAX call is done to reset the content of a table to its original value.
function resetTable(e, tab) {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			window.location.reload();
    	}

	};


    xhttp.open("POST", "https://www.geos.ed.ac.uk/~s1757431/cgi-bin/reset.py", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("tab="+tab);
}

// Inserting a row into the fields table. The values are checked to be valid. After
// inserting, the window will be reloaded.
function insertField(e,LOWX,LOWY,HIX,HIY,OWNER,CROP) {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			window.location.reload();
    	}

	};
	
	if (!(LOWX && LOWY && HIX && HIY && OWNER && CROP)){
		alert("Please enter values for all the fields.");
		return -1;
	}
	
	LOWX = parseInt(LOWX);
	HIX = parseInt(HIX);
	LOWY = parseInt(LOWY);
	HIY = parseInt(HIY);	
	
	if (LOWX<0 || LOWX>16 ){
		alert("LOWX must be between 0 to 16");
		return -1;
	}
	
	
	if (LOWY<0 || LOWY>16 ){
		alert("LOWY must be between 0 to 16");
		return -1;
	}
	
	if (LOWX>=HIX){
		alert("LOWX must be smaller than HIX");
		return -1
	}
	
	if (LOWY>=HIY){
		alert("LOWY must be smaller than HIY");
		return -1;
	}
	
	if (HIX<0 || HIX>16 ){
		alert("HIX must be between 0 to 16");
		return -1;
	}
	
	
	if (HIY<0 || HIY>16 ){
		alert("HIY must be between 0 to 16");
		return -1;
	}
	
	AREA = (HIX-LOWX)*(HIY-LOWY)/6.74;
	AREA = AREA.toFixed(2);
	
	
    xhttp.open("POST", "https://www.geos.ed.ac.uk/~s1757431/cgi-bin/insert.py", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    post_msg = "tab=fields&LOWX="+LOWX+"&LOWY="+LOWY+"&HIX="+HIX+"&HIY="+HIY+"&AREA="+AREA+"&OWNER="+OWNER+"&CROP="+CROP;
    xhttp.send(post_msg);
}

// Inserting a row into the finds table. The values are checked to be valid. After
// inserting, the window will be reloaded.
function insertFind(e,XCOORD,YCOORD,TYPE,DEPTH,FIELD_NOTES) {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			window.location.reload();
    	}

	};
	
	if (!(XCOORD && YCOORD && TYPE && DEPTH && FIELD_NOTES)){
		alert("Please enter values for all the fields.");
		return -1;
	}
	
	XCOORD = parseInt(XCOORD);
	YCOORD = parseInt(YCOORD);
	
	if (XCOORD<0 || XCOORD>16 ){
		alert("XCOORD must be between 0 to 16");
		return -1;
	}
	
	
	if (YCOORD<0 || YCOORD>16 ){
		alert("YCOORD must be between 0 to 16");
		return -1;
	}
	
    xhttp.open("POST", "https://www.geos.ed.ac.uk/~s1757431/cgi-bin/insert.py", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    post_msg = "tab=finds&XCOORD="+XCOORD+"&YCOORD="+YCOORD+"&TYPE="+TYPE+"&DEPTH="+DEPTH+"&FIELD_NOTES="+FIELD_NOTES;
    xhttp.send(post_msg);
}



