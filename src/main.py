# Library imports
from vex import *

from lib.control import ClassControl

import vex as vx

# Brain should be defined by default
brain=Brain()

# Robot configuration code
claw_motor = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
arm_motor = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)
controller_1 = Controller(PRIMARY)
left_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
right_motor = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)

# Example usage:
# Assuming `controller_1`, `arm_motor`, and `claw_motor` are already defined and initialized
control = ClassControl(controller_1, arm_motor, claw_motor)







# Main Controller loop to set motors to controller axis postiions
while True:
    left_motor.set_velocity(controller_1.axis3.position(), PERCENT)
    right_motor.set_velocity(controller_1.axis2.position(), PERCENT)
    left_motor.spin(FORWARD)
    right_motor.spin(FORWARD)
    wait(5, MSEC)

    controller_1.