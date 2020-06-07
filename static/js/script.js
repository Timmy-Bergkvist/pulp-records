(function($){
  $(function(){

    $('.sidenav').sidenav();
    $('.parallax').parallax();

  }); // end of document ready
})(jQuery); // end of jQuery name space


$(document).ready(function() {
  $('.collapsible').collapsible();
  $('select').formSelect();
  $('.tabs').tabs();
})

//Bug fix so that the task records can be displayed
document.getElementById("recordfix").addEventListener("click", function(e) {
  e.stopPropagation();
});