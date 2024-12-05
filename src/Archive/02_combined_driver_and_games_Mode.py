# this sketch will switch between auto and drive mode, and in drive mode will allow the driver to drive the robot.
# - [ ] Test this sketch to see if it actually works

# Library imports
from vex import *

brain = Brain()

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

def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    # place automonous code here

def user_control():
    
    brain.screen.clear_screen()
    brain.screen.print("driver control")
    # place driver control in this while loop
    while True:

        left_motor.set_velocity(left_control_input.position(), PERCENT)
        right_motor.set_velocity(right_control_input.position(), PERCENT)

        left_motor.spin(FORWARD)
        right_motor.spin(FORWARD)

        wait(5, MSEC)

# create competition instance
comp = Competition(user_control, autonomous)

# actions to do when the program starts
brain.screen.clear_screen()