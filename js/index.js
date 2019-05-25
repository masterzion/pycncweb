var CNC_AXIS = {};
$( "#tabs" ).tabs();
$( "#tabs" ).tabs().find('.ui-tabs-nav li').off('keydown')

CNC_AXIS['x']=0;
CNC_AXIS['y']=0;
CNC_AXIS['z']=0;


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
            CNC_AXIS['x']+=1;
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
    console.log(CNC_AXIS);
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
    console.log(CNC_AXIS);
    e.preventDefault(); // prevent the default action (scroll / move caret)
});
