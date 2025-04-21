from vex import *

global brain

brain = Brain()
controller = Controller(PRIMARY)

# Define drive motors
left_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1)
right_motor = Motor(Ports.PORT2, GearSetting.RATIO_18_1)

button_R1 = controller.buttonR1
button_R2 = controller.buttonR2

head_motor = Motor(Ports.PORT3, GearSetting.RATIO_18_1)

def print_to_brain(message, row):

    global brain

    brain.screen.clear_row(row)
    brain.screen.set_cursor(row,1)
    brain.screen.print(message)

def head_up():

    head_motor.spin_to_position(180, DEGREES,25,RPM,True)
    print_to_brain("Head up",5)

    pass

def head_down():

    head_motor.spin_to_position(0, DEGREES,25,RPM,True)
    print_to_brain("Head down",5)

    pass

# Exponential control for smoother handling
def expo(input_value):
    expo_factor = 2.5
    direction = 1 if input_value >= 0 else -1
    output = ((abs(input_value) ** expo_factor) / (100 ** (expo_factor - 1))) * direction
    return output

def skid_steer_control():
    # Speed from right stick (forward/backward)
    speed = expo(controller.axis3.position())
    # Turning from left stick
    turn = expo(controller.axis1.position())

    # Calculate motor speeds
    left_speed = speed + turn
    right_speed = speed - turn

    # Limit motor speeds to [-100, 100]
    left_speed = max(min(left_speed, 100), -100)
    right_speed = max(min(right_speed, 100), -100)

    # Set motor velocities
    left_motor.set_velocity(left_speed, PERCENT)
    right_motor.set_velocity(right_speed, PERCENT)

    # Spin motors
    left_motor.spin(FORWARD)
    right_motor.spin(REVERSE)

if __name__ == "__main__":

    print_to_brain("DRIVER MODE SKETCH", 1)

    controller.buttonR1.pressed(head_up)
    controller.buttonR2.pressed(head_down)

    while True:
        skid_steer_control()
        wait(10, MSEC)