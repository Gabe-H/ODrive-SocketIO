# ODrive SocketIO

## ODrive python socket-io connection to Node.js Leapmotion host.

Python 3.7+, Node 12+
```
Requirements:

pip install python-socketio
pip install python-socketio[client]
pip install --upgrade odrive

npm install express
npm install leapjs
npm install socket.io
```

1. Download and install Leapmotion SDK
2. Enable 'Allow web apps' in Leapmotion control panel
3. Start Node.js host server `node index.js`
4. Start Python ODrive control `python main.py`
    - If using more than 1 board, specify the connection serial number, found in `odrivetool` on board connection