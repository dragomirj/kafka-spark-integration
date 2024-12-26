jQuery(function () {
    var socket = io();
    socket.on('connect', function () {
        console.log('CONNECTED!');
    });

    //Keep track of how many events were emitted
    var event_counter_map = {
        device1: 0,
        device2: 0
    }

    //Async - On every new message update information
    socket.on('emit', function (msg, cb) {
        var device_name = msg.message.device_name;
        $(`#${device_name}_data`).text(msg.message.data); //Show new data
        $(`#${device_name}_time`).text(msg.message.start + " - " + msg.message.end); //Show the event's window of measurement
        $(`#${device_name}_count`).text(++event_counter_map[device_name]); //Update event counter

        //CALLBACK
        if (cb) { cb(); }
    });
});