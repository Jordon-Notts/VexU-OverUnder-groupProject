# this show how to control the robot using the controller in driver controlled mode
# - [ ] Test this sketch to see if it actually works

from vex import *

# Brain should be defined by default
brain=Brain()

# Create controller instance
controller = Controller(PRIMARY)

# define control axis

# left_control_input = controller_1.axis1.position()
left_control_input = controller.axis2
# right_control_input = controller_1.axis3.position()
right_control_input = controller.axis4

# Create drive motors
left_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1)
right_motor = Motor(Ports.PORT10, GearSetting.RATIO_18_1)

while True:

    left_motor.set_velocity(left_control_input.position(), PERCENT)
    right_motor.set_velocity(right_control_input.position(), PERCENT)

    left_motor.spin(FORWARD)
    right_motor.spin(FORWARD)

    wait(5, MSEC)