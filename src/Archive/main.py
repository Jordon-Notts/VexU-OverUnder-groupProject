# This sketch shows the basic




# Library imports
from vex import *

# Brain should be defined by default
brain=Brain()

# Create controller instance
controller = Controller(PRIMARY)

# define control axis

# left_control_input = controller_1.axis1.position()
left_control_input = controller.axis2.position()
# right_control_input = controller_1.axis3.position()
right_control_input = controller.axis4.position()

# define buttons
button_A = controller.buttonA
button_B = controller.buttonB
button_X = controller.buttonX
button_Y = controller.buttonY
button_L1 = controller.buttonL1
button_L2 = controller.buttonL2
button_R1 = controller.buttonR1
button_R2 = controller.buttonR2
button_UP = controller.buttonUp
button_DOWN = controller.buttonDown
button_LEFT = controller.buttonLeft
button_RIGHT = controller.buttonRight

# Create drive motors
left_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1)
right_motor = Motor(Ports.PORT10, GearSetting.RATIO_18_1)

# Create actuator motors





# Create Controller callback events - 15 msec delay to ensure events get registered
button_A.pressed(controller_L1_Pressed)
controller.buttonL2.pressed(controller_L2_Pressed)
controller.buttonR1.pressed(controller_R1_Pressed)
controller.buttonR2.pressed(controller_R2_Pressed)

wait(15, MSEC)

# Create games modes

def driver_control_mode():


    while True:

        left_motor.set_velocity(left_control_input, PERCENT)
        right_motor.set_velocity(right_control_input, PERCENT)

        left_motor.spin(FORWARD)
        right_motor.spin(FORWARD)

        wait(5, MSEC)

def autonomous_mode():
    pass

# Assign compertition modes to the compertition
vex_over_under = Competition(driver_control_mode, autonomous_mode)































# Main Controller loop to set motors to controller axis postiions













































# Begin project code
# Create callback functions for each controller button event
def controller_L1_Pressed():
    arm_motor.spin(FORWARD)
    while controller.buttonL1.pressing():
        wait(5, MSEC)
    arm_motor.stop()

def controller_L2_Pressed():
    arm_motor.spin(REVERSE)
    while controller.buttonL2.pressing():
        wait(5, MSEC)
    arm_motor.stop()

def controller_R1_Pressed():
    claw_motor.spin(REVERSE)
    while controller.buttonR1.pressing():
        wait(5, MSEC)
    claw_motor.stop()

def controller_R2_Pressed():
    claw_motor.spin(FORWARD)
    while controller.buttonR2.pressing():
        wait(5, MSEC)
    claw_motor.stop()




# Configure Arm and Claw motor hold settings and velocity
arm_motor.set_stopping(HOLD)
claw_motor.set_stopping(HOLD)
arm_motor.set_velocity(60, PERCENT)
claw_motor.set_velocity(30, PERCENT)