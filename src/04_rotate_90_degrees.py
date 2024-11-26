from lib.RobotNavigator import RobotNavigator_calcs

# Robot Initialization Parameters
starting_x = 0  # Initial x-coordinate of the robot
starting_y = 0  # Initial y-coordinate of the robot
starting_a = 90  # Initial angle of the robot (in degrees, facing "up")

wheel_span = 250  # mm, distance between the robot's wheels (wheel span)
wheel_radius = 75  # mm, radius of the robot's wheels

# Create an instance of the RobotNavigator_calcs class
robot_nav = RobotNavigator_calcs(starting_x, starting_y, starting_a, wheel_radius, wheel_span)

from vex import *  # Import VEX library for hardware interaction

# Initialize VEX Brain and Motors
brain = Brain()  # Brain object to control the robot
left_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1)  # Left motor connected to PORT1
right_motor = Motor(Ports.PORT10, GearSetting.RATIO_18_1)  # Right motor connected to PORT10

def control_wheels(rotate_left_wheel_by, rotate_right_wheel_by):
    """
    Controls the robot's wheels to rotate by specific angles.

    Args:
        rotate_left_wheel_by (float): Rotation for the left wheel in degrees.
        rotate_right_wheel_by (float): Rotation for the right wheel in degrees.
    """
    # Debug output for the requested wheel rotations
    print(f"[Control Wheels] Left: {rotate_left_wheel_by:.2f}°, Right: {rotate_right_wheel_by:.2f}°")
    
    # Reset the motor positions to ensure accurate movement
    left_motor.reset_position()
    right_motor.reset_position()
    
    # Command the motors to spin to the specified positions
    left_motor.spin_to_position(rotate_left_wheel_by, DEGREES, 25, RPM, wait=False)
    right_motor.spin_to_position(rotate_right_wheel_by, DEGREES, 25, RPM, wait=True)
    
    # Wait for the motors to finish spinning before proceeding
    while left_motor.is_spinning() or right_motor.is_spinning():
        wait(20, MSEC)  # Check motor status every 20 milliseconds

if __name__ == "__main__":
    """
    Entry point of the program. This block runs when the script is executed.
    Currently, no specific functionality is executed here.
    """
    Test_angle = 90 # degrees
    
    # Calculate the wheel rotations needed for the angular difference
    left_wheel_rotate_by, right_wheel_rotate_by = robot_nav.calculate_wheel_rotation_rotation_mode(Test_angle)

    print(f"A calculation has been carried out, to turn the robot {Test_angle}, the wheels need to rotate {left_wheel_rotate_by} degrees.")
    
    # Execute the rotation using the control_wheels function
    control_wheels(left_wheel_rotate_by, right_wheel_rotate_by)