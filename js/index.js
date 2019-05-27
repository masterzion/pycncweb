$( "#tabs" ).tabs({ heightStyle: "auto"}).find('.ui-tabs-nav li').off('keydown')
$(".spinner").spinner();
$( ".checkbox" ).checkboxradio();



$( "#divabout" ).dialog({
   autoOpen: false,
   modal: true,
   open: function(){
      jQuery('.ui-widget-overlay').bind('click',function(){
         dialogopen.dialog('close');
      });
   },
   width: "70%",
   maxWidth: "768px"
});

function openabout(){
  $("#divabout").dialog("open");
}

$.getJSON({
    url: "/js/config.json"
}).done(function (data, status, xhr) {

  $.getJSON({
      url: "/config"
  }).done(function (datacontent, statuscontent, xhr) {

  var items = [];
  $.each( data, function( key, val ) {
    items.push( "<p class='configheader'>" + key.toUpperCase() + "</p><ul>" );

		$.each( val, function( key2, val2 ) {
			if (val2 == "int") {
				str="</span><input type='number' class='spinner' id='"+key2+"' value='"+datacontent[key][key2]+"'>"
			} else {
        if ( datacontent[key][key2] ) {
           strchecked="checked";
        } else {
          strchecked="";
        }

				str="<input type='checkbox' class='checkbox'  id='"+key2+"' "+strchecked+"></span>"
			}
	    items.push( "<li><span class='configitem'>" + key2.replace(/_/g, ' ').toLowerCase() +":"+str+"</li>" );
	  });
    items.push( "</ul><hr>" );
	});



  $("#divconfigitems" ).html(items.join( "" ));
}).fail(function (xhr2, status2, error2) {
      alert("Result: " + status2 + " " + error2 + " " + xhr2.status + " " + xhr2.statusText)
  });
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
    if ( $('#tabs').tabs('option','active') == 0 ) {
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
    }
});


$(document).keyup(function(e) {
    switch(e.which) {
        case 37: // left
            $("#y_down").click();
            $("#y_down").mouseup();
        break;

        case 38: // up
            $("#x_up").click();
            $("#x_up").mouseup();
        break;

        case 39: // right
            $("#y_up").click();
            $("#y_up").mouseup();
        break;

        case 40: // down
            $("#x_down").click();
            $("#x_down").mouseup();
        break;

        case 33: // page up
            $("#z_up").click();
            $("#z_up").mouseup();
        break;

        case 34: // page down
            $("#z_down").click();
            $("#z_down").mouseup();
        break;
        default: return; // exit this handler for other keys
    }
    e.preventDefault(); // prevent the default action (scroll / move caret)
});

$("body").css("overflow", "hidden");

function savedata() {
  $.getJSON({
      url: "/js/config.json"
  }).done(function (data, status, xhr) {
    $.each( data, function( key, val ) {
  		$.each( val, function( key2, val2 ) {
  			if (val2 == "int") {
  				data[key][key2]=$("#"+key2).val();
  			} else {
          data[key][key2]=$("#"+key2).prop( "checked" );
  			}
          console.log(key2+':'+data[key][key2]);
  	  });
  	});

    console.log(data);
    $.ajax
    ({
        type: "POST",
        url: '/config',
        dataType: 'json',
        contentType: "application/json; charset=utf-8",
        async: false,
        data: JSON.stringify(data),
        success: function () {
        console.log("saved");
        }
    });
  });
}


function addpos(axis, value) {
    data={}
    data["add"]= {}
    data["add"][axis] = value;
    console.log(data);
    $.ajax
    ({
        type: "POST",
        url: '/positions',
        dataType: 'json',
        contentType: "application/json; charset=utf-8",
        async: false,
        data: JSON.stringify(data),
        success: function () {
          console.log("addpos");
        }
    });
}

function reset() {
    $.ajax
    ({
        type: "POST",
        url: '/reset',
        dataType: 'json',
        contentType: "application/json; charset=utf-8",
        async: false,
        data: "reset",
        success: function () {
          console.log("reset");
        }
    });
}
