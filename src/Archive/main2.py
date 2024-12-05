# Library imports
from vex import *

# Initialize Brain
brain = Brain()

# Create controller instance
controller = Controller(PRIMARY)

# Motors and Buttons
class Drive:
    def __init__(self, left_motor, right_motor, left_control_input, right_control_input):
        # Define drive motors
        self.left_motor = left_motor
        self.right_motor = right_motor

        self.left_control_input = left_control_input
        self.right_control_input = right_control_input

    def driver_control_mode(self):
        """
        Driver control loop: Handles joystick inputs for robot control.
        """
        while True:

            # Set motor velocities
            self.left_motor.set_velocity(self.left_control_input, PERCENT)
            self.right_motor.set_velocity(self.right_control_input, PERCENT)

            # Spin motors forward
            self.left_motor.spin(FORWARD)
            self.right_motor.spin(FORWARD)

            wait(5, MSEC)

class Actuator:
    def __init__(self, ):

        # Define actuator motors
        self.arm_motor = Motor(Ports.PORT2, GearSetting.RATIO_18_1)
        self.claw_motor = Motor(Ports.PORT3, GearSetting.RATIO_18_1)

        # Configure motors
        self.arm_motor.set_stopping(HOLD)
        self.claw_motor.set_stopping(HOLD)
        self.arm_motor.set_velocity(60, PERCENT)
        self.claw_motor.set_velocity(30, PERCENT)

        # Define buttons
        self.button_A = controller.buttonA
        self.button_B = controller.buttonB
        self.button_L1 = controller.buttonL1
        self.button_L2 = controller.buttonL2
        self.button_R1 = controller.buttonR1
        self.button_R2 = controller.buttonR2

        # Register button callbacks
        self.button_L1.pressed(self.arm_up)
        self.button_L2.pressed(self.arm_down)
        self.button_R1.pressed(self.claw_close)
        self.button_R2.pressed(self.claw_open)

    # Button Actions
    def arm_up(self):
        self.arm_motor.spin(FORWARD)
        while controller.buttonL1.pressing():
            wait(5, MSEC)
        self.arm_motor.stop()

    def arm_down(self):
        self.arm_motor.spin(REVERSE)
        while controller.buttonL2.pressing():
            wait(5, MSEC)
        self.arm_motor.stop()

    def claw_open(self):
        self.claw_motor.spin(FORWARD)
        while controller.buttonR2.pressing():
            wait(5, MSEC)
        self.claw_motor.stop()

    def claw_close(self):
        self.claw_motor.spin(REVERSE)
        while controller.buttonR1.pressing():
            wait(5, MSEC)
        self.claw_motor.stop()

def autonomous_mode():
    pass

# Main Program
if __name__ == "__main__":

    left_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1)
    right_motor = Motor(Ports.PORT10, GearSetting.RATIO_18_1)

    left_control_input = controller.axis3.position()  # Left stick vertical
    right_control_input = controller.axis2.position()  # Right stick vertical

    # Initialize robot
    drive_class = Drive(left_motor=left_motor,
                        right_motor=right_motor,
                        left_control_input=left_control_input, 
                        right_control_input=right_control_input
                        )
    

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



    # Assign competition modes
    vex_over_under = Competition(drive_class.driver_control_mode, autonomous_mode)