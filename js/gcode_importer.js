function FileIO() { }

FileIO.error = function(msg) {
  alert(msg);
}

FileIO.loadPath = function(path, callback) {
  var self = this;
  $.get(path, null, callback, 'text')
    .error(function() { self.error('Unable to load gcode.') });
}

FileIO.load = function(files, callback) {
  if (files.length) {
    var i = 0, l = files.length;
    for ( ; i < l; i++) {
      FileIO.load(files[i], callback);
    }
  }
  else {
    var reader = new FileReader();
    reader.onload = function() {
      callback(reader.result);
    };
    reader.readAsText(files);
  }
}

///////////////////////////////////////////////////////////////////////////////

function GCodeImporter() { }

GCodeImporter.importPath = function(path, callback) {
  FileIO.loadPath(path, function(gcode) {
    GCodeImporter.importText(gcode, callback);
    $('#gcodetext').text(gcode);


    $.ajax
    ({
        type: "POST",
        url: '/gcodefile',
        dataType: 'json',
        contentType: "application/json; charset=utf-8",
        async: false,
        data: gcode,
        success: function () {
        console.log("uploaded!");
        }
    })


  });
}

GCodeImporter.importText = function(gcode, callback) {
  var gcodeModel = gcode; // TODO: actually get the model
  callback(gcodeModel);
}
