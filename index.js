const Leap = require('leapjs')
var app = require('express')();
var http = require('http').createServer(app);
var io = require('socket.io')(http);

const FEEDRATE = 50;

app.get('/', (req, res) => {
  res.send();
});

io.on('connection', (socket) => {
  console.log('connected!');
});

http.listen(4444, () => {
  console.log('listening on *:4444');
});


var data = {
    elevation: 0,
    strafe: 0,
    surge: 0,
    pinchStrength: 0
}

function update_pos(data) {
  io.emit('position_update', data)
}

console.log('Starting loop!')
Leap.loop({enableGestures:true}, function(frame){
//   // Reset data array
//   data = {
//       position: [0,0,0],
//       side: 'blank',
//       grip: 0,
//       valid: false,
//       palmNormal: [0, 0, 0]
//     }
  // Get data for both hands, if they exist
  if (frame.hands.length > 0) {
      data.strafe = frame.hands[0].palmPosition[0]
      data.elevation = frame.hands[0].palmPosition[1]
      data.surge = frame.hands[0].palmPosition[2]
      data.pinchStrength = frame.hands[0].pinchStrength
  }
});

setInterval(() => {
    update_pos(data)
}, 1000/FEEDRATE);