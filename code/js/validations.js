$(document).ready(function (){
    $(".pr-password").passwordRequirements({
        numCharacters: 8,
        useLowercase:true,
        useUppercase:true,
        useNumbers:true,
        useSpecial:true,
        style:"dark",
        fadeTime: 500
    });
});



$('#password, #confirm_password').on('keyup', function () {
    if ($('#password').val() == $('#confirm_password').val()) {
      $('.forgot').html('');
      $('#reg').prop('disabled', false);
    } else {
      $('.forgot').html('The passwords donot match!');
      $('#reg').prop('disabled', true);
    }
  });