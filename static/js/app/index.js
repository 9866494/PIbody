$(document).ready(function(){
    namespace = 'robo';
	
	var cam_left_interval = null;

    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);

    socket.on('my response', function(msg) {
        $('#log').append('<br>Received #' + msg.count + ': ' + msg.data);
    });

    socket.on('connect', function() {
        socket.emit('my event', {data: 'I\'m connected!'});
    });

	$('.cam').change(function(){
      var val = $(this).val();
      console.log(val);
      socket.emit('cam_rotate', {value: val});
	});
	
    $('#led_shim').change(function(){
      var val = $(this).val();
      console.log(val);
      socket.emit('led_shim', {value: val});
    })
});
