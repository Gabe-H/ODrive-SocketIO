import odrive
from odrive.enums import *

serialNumbers = ["206535823056", "205435783056"]

my_odrives = []

for n in serialNumbers:
    my_odrives.append(odrive.find_any(serial_number=n))

for d in my_odrives:
    d.axis0.requested_state = AXIS_STATE_IDLE
    d.axis1.requested_state = AXIS_STATE_IDLE