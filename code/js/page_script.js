function displayForm() {
  document.getElementById("myForm").style.display = "block";
  $('#check_button').hide()
  $('#stats_button').hide()
  $('#prec').hide()
  $('.forgot').text('');
}

function hideForm() {
  document.getElementById("myForm").style.display = "none";
  $('#check_button').show()
  $('#stats_button').show()
  $('#prec').show ()
  $('.forgot').text('');
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
  if (fever == '' || cough == '' || breath == '' || muscle == '' || tired == '' || nasal == '' || throat == '' || nausea == '' || taste == '' || chills == '' || isolate == '') {
    alert("Please answer all the questions asked!");
    displayForm();
  }
}

function showStats(){
  window.location.href = "/stats";
}