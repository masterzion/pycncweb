$( "#tabs" ).tabs({ heightStyle: "auto"}).find('.ui-tabs-nav li').off('keydown')
$(".spinner").spinner();
$( ".checkbox" ).checkboxradio();




$.getJSON({
    url: "/js/config.json"
}).done(function (data, status, xhr) {
  var items = [];
  $.each( data, function( key, val ) {
    items.push( "<p class='configheader'>" + key + "</p><ul>" );

		$.each( val, function( key2, val2 ) {
			if (val2 == "int") {
				str="</span><input type='number' class='spinner'>"
			} else {
				str="<input type='checkbox' class='checkbox'></span>"
			}
	    items.push( "<li id='" + key2 + "'><span class='configitem'>" + key2.replace(/_/g, ' ').toLowerCase() +":"+str+"</li>" );
	  });
    items.push( "</ul><hr>" );
	});



  $("#divconfigitems" ).html(items.join( "" ));
}).fail(function (xhr, status, error) {
    alert("Result: " + status + " " + error + " " + xhr.status + " " + xhr.statusText)
});






//JS to make it work on single page/codepen
var MainNav = $('.MainNav-Button');

MainNav.on('mousedown', function(){
	var $this = $(this);
	$this.parent().find('.MainNav-Button').removeClass('MainNav-Button_LeftOfActive MainNav-Button_RightOfActive MainNav-Button_Active');
	$this.addClass('MainNav-Button_Active').prev().addClass('MainNav-Button_LeftOfActive');
	$this.next().addClass('MainNav-Button_RightOfActive');
});

MainNav.on('mouseup', function(){
	var $this = $(this);
	$this.parent().find('.MainNav-Button').removeClass('MainNav-Button_LeftOfActive MainNav-Button_RightOfActive MainNav-Button_Active');
});

MainNav.on('click', function(event){
	event.preventDefault();
});



$(document).keydown(function(e) {
    switch(e.which) {
        case 37: // left
            $("#y_down").mousedown();
        break;

        case 38: // up
            $("#x_up").mousedown();
        break;

        case 39: // right
            $("#y_up").mousedown();
        break;

        case 40: // down
            $("#x_down").mousedown();
        break;

        case 33: // page up
            $("#z_up").mousedown();
        break;

        case 34: // page down
            $("#z_down").mousedown();
        break;
        default: return; // exit this handler for other keys
    }
    e.preventDefault(); // prevent the default action (scroll / move caret)
});


$(document).keyup(function(e) {
    switch(e.which) {
        case 37: // left
            $("#y_down").mouseup();
        break;

        case 38: // up
            $("#x_up").mouseup();
        break;

        case 39: // right
            $("#y_up").mouseup();
        break;

        case 40: // down
            $("#x_down").mouseup();
        break;

        case 33: // page up
            $("#z_up").mouseup();
        break;

        case 34: // page down
            $("#z_down").mouseup();
        break;
        default: return; // exit this handler for other keys
    }
    e.preventDefault(); // prevent the default action (scroll / move caret)
});
