import odrive
from odrive.enums import *
import json, time

class ODrive_Calibration():
    def SetAxisParam(self, axis, pids):
        axis.controller.config.pos_gain = pids["pos_gain"]
        axis.controller.config.vel_gain = pids["vel_gain"]
        axis.controller.config.vel_integrator_gain = pids["vel_integrator_gain"]
        axis.controller.config.vel_limit = pids["vel_limit"]

        id = pids["id"]

        print(f"Motor #{id} settings set.")

    def DetermineParameters(self, drive):
        with open("./motors.json") as f:
            data = json.load(f)
            for setting in data:
                if setting["serial"] == str(drive.serial_number):
                    self.SetAxisParam(drive.axis0, setting["pids"][0])
                    self.SetAxisParam(drive.axis1, setting["pids"][1])

        return drive

    def StartDrives(self, serialNumbers, feedrate):
        drives = []

        #Apply PID settings to each axis
        for i in range(len(serialNumbers)):
            print('Searching for ODrive...')
            drives.append(self.DetermineParameters(odrive.find_any(serial_number=serialNumbers[i])))
            print(f'({i + 1}/{len(serialNumbers)}) ODrives Connected...')


        print('Starting calibration...')
        for drive in drives:
            drive.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
            drive.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
        
        while 1:
            drivesNotCalibrated = 0
            for drive in drives:
                if drive.axis0.current_state != AXIS_STATE_IDLE or drive.axis1.current_state != AXIS_STATE_IDLE:
                    drivesNotCalibrated += 1
            if drivesNotCalibrated == 0:
                break
            time.sleep(0.1)
            
        for drive in drives:
            drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
            drive.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
            drive.axis0.controller.config.input_mode = INPUT_MODE_POS_FILTER
            drive.axis1.controller.config.input_mode = INPUT_MODE_POS_FILTER
            drive.axis0.controller.config.input_filter_bandwidth = feedrate
            drive.axis1.controller.config.input_filter_bandwidth = feedrate

        return tuple(drives)