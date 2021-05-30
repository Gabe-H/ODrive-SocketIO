import odrive
from odrive.enums import *
import time, subprocess, socketio

print('Searching for ODrive...')
my_drive = odrive.find_any()

print(f'Found ODrive: {my_drive.vbus_voltage}')

time.sleep(0.1)

my_drive.axis0.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION
my_drive.axis1.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION

while ((my_drive.axis0.current_state != AXIS_STATE_IDLE) or (my_drive.axis1.current_state != AXIS_STATE_IDLE)):
    time.sleep(0.1)

my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
# my_drive.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
my_drive.axis0.controller.config.input_filter_bandwidth = 5
# my_drive.axis1.controller.config.input_filter_bandwidth = 5
my_drive.axis0.controller.config.input_mode = INPUT_MODE_POS_FILTER
# my_drive.axis1.controller.config.input_mode = INPUT_MODE_POS_FILTER

print('Calibration done! Starting node server...')

while True:
    my_drive.axis0.controller.input_pos = 0
    time.sleep(2)
    my_drive.axis0.controller.input_pos = 1
    time.sleep(2)
