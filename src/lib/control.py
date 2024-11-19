from vex import *

class ClassControl:
    def __init__(self, controller, arm_motor, claw_motor):
        """
        Initialize the control class with the controller, arm motor, and claw motor.
        """
        self.controller = controller
        self.arm_motor = arm_motor
        self.claw_motor = claw_motor

        # Set motor configurations
        self.arm_motor.set_stopping(HOLD)
        self.claw_motor.set_stopping(HOLD)
        self.arm_motor.set_velocity(60, PERCENT)
        self.claw_motor.set_velocity(30, PERCENT)

        # Register button event callbacks
        self.controller.buttonL1.pressed(self.controller_L1_Pressed)
        self.controller.buttonL2.pressed(self.controller_L2_Pressed)
        self.controller.buttonR1.pressed(self.controller_R1_Pressed)
        self.controller.buttonR2.pressed(self.controller_R2_Pressed)

    def controller_L1_Pressed(self):
        """
        Handle L1 button press to spin the arm motor forward.
        """
        self.arm_motor.spin(FORWARD)
        while self.controller.buttonL1.pressing():
            wait(5, MSEC)
        self.arm_motor.stop()

    def controller_L2_Pressed(self):
        """
        Handle L2 button press to spin the arm motor in reverse.
        """
        self.arm_motor.spin(REVERSE)
        while self.controller.buttonL2.pressing():
            wait(5, MSEC)
        self.arm_motor.stop()

    def controller_R1_Pressed(self):
        """
        Handle R1 button press to spin the claw motor in reverse.
        """
        self.claw_motor.spin(REVERSE)
        while self.controller.buttonR1.pressing():
            wait(5, MSEC)
        self.claw_motor.stop()

    def controller_R2_Pressed(self):
        """
        Handle R2 button press to spin the claw motor forward.
        """
        self.claw_motor.spin(FORWARD)
        while self.controller.buttonR2.pressing():
            wait(5, MSEC)
        self.claw_motor.stop()


