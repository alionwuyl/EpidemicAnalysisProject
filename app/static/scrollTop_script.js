/*global $, console*/

$(function () {
    
    'use strict';
    
//    ٍScroll top - show div
    
	$(window).on("scroll", function () {           /*When Make Scroll*/
        
        if ($(this).scrollTop() > 100) {     /*To Show Div After 100px From Scroll Top*/
            $('.scrollTop_top').slideDown();
        } else {                             /*To Hide Div */
            $('.scrollTop_top').slideUp();
        }
        
	});
	
//    Scroll top - animate
    
	$('.scrollTop_top').on("click", function () {
        
        // To Make Bounce Animate Scroll 
        
        $('html, body').animate({scrollTop : 0}, 300);
        $('html, body').animate({scrollTop : 40}, 150);
        $('html, body').animate({scrollTop : 0}, 100);
        $('html, body').animate({scrollTop : 20}, 100);
        $('html, body').animate({scrollTop : 0}, 100);
        $('html, body').animate({scrollTop : 10}, 50);
        $('html, body').animate({scrollTop : 0}, 100);
        $('html, body').animate({scrollTop : 5}, 50);
        $('html, body').animate({scrollTop : 0}, 100);
        
	});
      
    
});