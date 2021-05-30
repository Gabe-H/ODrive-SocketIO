import socketio
import Calibration

# Left Connection Serial: 206535823056
# Right Connection Serial: = 205435783056

# Left Board Serial: 35619061510230
# Right Board Serial: 35546046410838

serialNumbers = ["206535823056", "205435783056"]
feedrate = 50

driveSupport = Calibration.ODrive_Calibration()

leftdrv, rightdrv = driveSupport.StartDrives(serialNumbers, 30)

print('Calibration done! Connecting to socket...')

# server = subprocess.Popen('node index.js')
sio = socketio.Client()

@sio.event
def position_update(data):
    # print(data['vertical'], data['horizontal'])
    leftdrv.axis1.controller.input_pos = (data['elevation'] / 300) - 1
    leftdrv.axis0.controller.input_pos = (data['surge'] / 300) - 1
    rightdrv.axis0.controller.input_pos = (data['strafe'] / 300) - 1
    rightdrv.axis1.controller.input_pos = data['pinchStrength']

sio.connect('http://localhost:4444')
