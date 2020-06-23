
$(document).ready(function() {
  $('.collapsible').collapsible(); // Functions for the collapsible body.
  $('select').formSelect(); // Functions for the select input through specified options.
  $('.tabs').tabs();  // Function for tabs when you click on each tab.
  $('.sidenav').sidenav(); // Function for sidenav hamburger menu button.
  $('.parallax').parallax(); // Function for parallax background image.
  $(".dropdown-trigger").dropdown();
});


//Bug fix so that the records can be displayed
document.getElementById("recordfix").addEventListener("click", function(e) {
  e.stopPropagation();
});