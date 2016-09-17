//$(document).ready(function(){
//    namespace = 'robo';
//
//	var cam_left_interval = null;
//
//    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
//
//    socket.on('my response', function(msg) {
//        $('#console.log').append('<br>Received #' + msg.count + ': ' + msg.data);
//    });
//
//    socket.on('connect', function() {
//        socket.emit('my event', {data: 'I\'m connected!'});
//    });
//
//	$('.cam').change(function(){
//      var val = $(this).val();
//      console.console.log(val);
//      socket.emit('cam_rotate', {value: val});
//	});
//
//    $('#led_shim').change(function(){
//      var val = $(this).val();
//      console.console.log(val);
//      socket.emit('led_shim', {value: val});
//    })
//});

(function () {
    'use strict';

    var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function(){});
    socket.on('event', function(data){});
    socket.on('disconnect', function(){});

    var joystickLeft = new Joystick("joystick-left");

    joystickLeft.setCallback(function(x, y, toggled){
        console.log(x, y, toggled);
    });

    var joystickRight = new Joystick("joystick-right", true);

    joystickRight.setCallback(function(x, y, toggled){
        socket.emit('movement', {x: x, y: y, toggled: toggled});
    });
})();