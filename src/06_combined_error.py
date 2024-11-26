from lib.RobotNavigator import RobotNavigator_calcs

# Robot Initialization Parameters
starting_x = 0  # Initial x-coordinate of the robot
starting_y = 0  # Initial y-coordinate of the robot
starting_a = 0  # Initial angle of the robot (in degrees, facing "up")

wheel_span = 250  # mm, distance between the robot's wheels (wheel span)
wheel_radius = 75  # mm, radius of the robot's wheels

# Create an instance of the RobotNavigator_calcs class
robot_nav = RobotNavigator_calcs(starting_x, starting_y, starting_a, wheel_radius, wheel_span)

from vex import *  # Import VEX library for hardware interaction
import math  # Import math library for calculations

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

def Go_to_position(x_position, y_position, final_heading=None):
    """
    Moves the robot to a specified (x, y) position and optionally orients it to a final heading.

    Args:
        x_position (float): Target x-coordinate in mm.
        y_position (float): Target y-coordinate in mm.
        final_heading (float, optional): Desired final orientation in degrees. Defaults to None.
    """
    # Step 1: Rotate to face the target position
    # Calculate the angle and distance to the target
    desired_angle, distance = robot_nav.calculate_target_angle_and_distance(x_position, y_position)
    
    # Calculate the angular difference required to face the target
    angle_difference = robot_nav.calculate_angle_difference(desired_angle)
    
    # Calculate the wheel rotations needed for the angular difference
    left_wheel_rotate_by, right_wheel_rotate_by = robot_nav.calculate_wheel_rotation_rotation_mode(angle_difference)
    
    # Execute the rotation using the control_wheels function
    control_wheels(left_wheel_rotate_by, right_wheel_rotate_by)
    
    # Update the robot's orientation after the rotation
    robot_nav.update_position(new_a=desired_angle)

    # Step 2: Drive forward to the target position
    # Calculate the wheel rotations needed to travel the distance to the target
    left_wheel_rotate_by, right_wheel_rotate_by = robot_nav.calculate_wheel_rotation_drive_mode(distance)
    
    # Execute the forward movement using the control_wheels function
    control_wheels(left_wheel_rotate_by, right_wheel_rotate_by)
    
    # Update the robot's position after moving forward
    robot_nav.update_position(new_x=x_position, new_y=y_position)

    # Step 3: Optionally rotate to the final heading
    if final_heading is not None:
        # Calculate the angular difference needed to achieve the final heading
        final_angle_difference = robot_nav.calculate_angle_difference(final_heading)
        
        # Calculate the wheel rotations needed for the angular difference
        left_wheel_rotate_by, right_wheel_rotate_by = robot_nav.calculate_wheel_rotation_rotation_mode(final_angle_difference)
        
        # Execute the final rotation using the control_wheels function
        control_wheels(left_wheel_rotate_by, right_wheel_rotate_by)
        
        # Update the robot's orientation after the final rotation
        robot_nav.update_position(new_a=final_heading)

if __name__ == "__main__":
    """
    Entry point of the program. This block runs when the script is executed.
    Currently, no specific functionality is executed here.
    """
    Go_to_position(1000,-1000) # top left corner of a square
    Go_to_position(1000,1000) # top right
    Go_to_position(-1000,1000) # bottom right
    Go_to_position(-1000,-1000) # bottom left

    # back to centre

    Go_to_position(0,0, final_heading=0) # back to centre, and face the same direction
