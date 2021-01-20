function openForm() {
  document.getElementById("myForm").style.display = "block";
}

function checkForm() {
  var fever = document.forms["Form"]["fever"].selectedOptions[0].value;
  var cough = document.forms["Form"]["cough"].selectedOptions[0].value;
  var breath = document.forms["Form"]["breath"].selectedOptions[0].value;
  var muscle = document.forms["Form"]["muscle"].selectedOptions[0].value;
  var tired = document.forms["Form"]["tired"].selectedOptions[0].value;
  var nasal = document.forms["Form"]["nasal"].selectedOptions[0].value;
  var throat = document.forms["Form"]["throat"].selectedOptions[0].value;
  var nausea = document.forms["Form"]["nausea"].selectedOptions[0].value;
  var taste = document.forms["Form"]["taste"].selectedOptions[0].value;
  var chills = document.forms["Form"]["chills"].selectedOptions[0].value;
  var isolate = document.forms["Form"]["isolate"].selectedOptions[0].value;
  if (fever == "-- Select --" || cough == "-- Select --" || breath == "-- Select --" || muscle == "-- Select --" || tired == "-- Select --" || nasal == "-- Select --" || throat == "-- Select --" || nausea == "-- Select --" || taste == "-- Select --" || chills == "-- Select --" || isolate == "-- Select --") {
    alert("Please answer all the questions asked!");
  }
  else {
    document.getElementById("myForm").style.display = "none";
  }
  
}

function myMap() {
  document.getElementById("myMap").style.display = "block"
  var mapProp= {
    center:new google.maps.LatLng(51.508742,-0.120850),
    zoom:5,
  };
  var map = new google.maps.Map(document.getElementById("googleMap"),mapProp);
}