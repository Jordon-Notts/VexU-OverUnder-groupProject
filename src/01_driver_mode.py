# this show how to control the robot using the controller in driver controlled mode
# - [ ] Test this sketch to see if it actually works

from vex import *

global brain

# Brain should be defined by default
brain=Brain()

# Create controller instance
controller = Controller(PRIMARY)

brain.screen.clear_screen()
brain.screen.print("Driver control test sketch")

# define control axis

# left_control_input = controller_1.axis1.position()
left_control_input = controller.axis3
# right_control_input = controller_1.axis3.position()
right_control_input = controller.axis2

# Create drive motors
left_motor = Motor(Ports.PORT2, GearSetting.RATIO_18_1)
right_motor = Motor(Ports.PORT10, GearSetting.RATIO_18_1)

def print_to_brain(message, row):

    global brain

    brain.screen.clear_row(row)
    brain.screen.set_cursor(row,1)
    brain.screen.print(message)

def expo(input):

    value = 2.5

    direction = 1

    if input < 0:
        direction = -1

    print_to_brain(direction,2)

    returned_value = (abs(((input ** value ) / 100 ** value) * 100)) / direction

    print_to_brain(returned_value,3)

    return returned_value

while True:

    left_motor.set_velocity(expo(left_control_input.position()), PERCENT)
    right_motor.set_velocity(expo(right_control_input.position()), PERCENT)

    left_motor.spin(FORWARD)
    right_motor.spin(REVERSE)

    wait(1, MSEC)