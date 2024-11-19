# this shows how the robot move in maths mode

# from vex import *

# # Brain should be defined by default
# brain=Brain()

# # Create drive motors
# left_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1)
# right_motor = Motor(Ports.PORT10, GearSetting.RATIO_18_1)

import math

global actual_x, actual_y, actual_a, wheel_span, wheel_radius

actual_x = 0 # starting x coordinates, then used to store current robot location
actual_y = 0 # starting y coordinates, then used to store current robot location
actual_a = 90 # starting robot angle, then used to store current robot direction

wheel_span = 250 # mm, the distance between the wheels in mm
wheel_radius = 75 # mm, the radius of the wheels in mm

def calculate_target_angle_and_distance(desired_x, desired_y):
    """
    Calculate the angle and distance to the target position relative to the current position.

    Args:
        desired_x (float): Target x-coordinate.
        desired_y (float): Target y-coordinate.

    Returns:
        tuple: (absolute angle in degrees, distance in the same units as the coordinates)

    """

    global actual_x, actual_y, actual_a
    
    delta_x = desired_x - actual_x
    delta_y = desired_y - actual_y
   
    theta = math.degrees(math.atan2(delta_y , delta_x))

    distance = math.sqrt(delta_x**2 + delta_y**2)

    # Debugging output
    print(f"Inside calculate_target_angle_and_distance function\n")
    print(f"\t(delta_x = {delta_x}) = (desired_x = {desired_x}) - (actual_x = {actual_x})")
    print(f"\t(delta_y = {delta_y}) = (desired_y = {desired_y}) - (actual_y = {actual_y})\n")
    print(f"\t(theta = {theta} degrees) = atan2({delta_y}, {delta_x})\n")
    print(f"\t(distance = {distance}) = sqrt({delta_x}^2 + {delta_y}^2)\n")
    
    return theta, distance

def calculate_angle_difference(desired_angle):
    """
    Calculate the difference between the current facing direction and the angle to the desired position.

    Args:
        desired_x (float): Target x-coordinate.
        desired_y (float): Target y-coordinate.

    Returns:
        float: Angle difference in degrees (normalized between -180 and 180).
    """
    global actual_a

    # Calculate angle difference
    angle_difference = desired_angle - actual_a

    # Normalize to the range -180 to 180 degrees
    angle_difference = (angle_difference + 180) % 360 - 180

    # Debugging output
    print(f"Angle Difference:\n")
    print(f"\t(Target Angle = {desired_angle} degrees)")
    print(f"\t(Current Angle = {actual_a} degrees)")
    print(f"\t(Angle Difference = {angle_difference} degrees)\n")

    return angle_difference

def rotate_by_angle(angle_to_rotate_by):

    global wheel_span, wheel_radius, actual_a

    # Radius of robot's rotation
    robot_radius = wheel_span / 2

    # Convert angle to radians
    angle_to_rotate_by_rad = math.radians(angle_to_rotate_by)

    # Calculate the distance along the circumference for wheels
    distance_along_circumference = robot_radius * angle_to_rotate_by_rad

    # Calculate the wheel rotation required (in radians)
    wheel_rotation = distance_along_circumference / wheel_radius

    # Convert wheel rotation to degrees
    wheel_rotation_deg = math.degrees(wheel_rotation)

    # Debugging output
    print(f"Rotate By Angle:")
    print(f"\tAngle to Rotate By = {angle_to_rotate_by} degrees")
    print(f"\twheels travel distance = {distance_along_circumference} mm")
    print(f"\tWheel Rotation = {wheel_rotation_deg} degrees")

    # Simulate motor commands (replace with actual motor calls)
    print(f"\tRotating left motor by {-wheel_rotation_deg} degrees")
    print(f"\tRotating right motor by {wheel_rotation_deg} degrees")

    # Update actual angle
    actual_a = (actual_a + angle_to_rotate_by) % 360
    print(f"\tUpdated actual_a: {actual_a} degrees")

def Go_to_position(x_position, y_position, angle=None):

    desired_angle, distance = calculate_target_angle_and_distance(x_position, y_position)

    angle_difference = calculate_angle_difference(desired_angle)

    rotate_by_angle(angle_difference)

    drive_forward(distance)

    # Step 3: Optionally rotate to a final orientation
    if angle != None:
        final_angle_difference = calculate_angle_difference(angle)
        rotate_by_angle(final_angle_difference)

def drive_forward(distance):

    global actual_x, actual_y, actual_a

    # Calculate distance in terms of wheel rotation
    wheel_rotation = distance / wheel_radius
    wheel_rotation_deg = math.degrees(wheel_rotation)

    # Debugging output
    print(f"Drive Forward:")
    print(f"\tDistance = {distance} mm")
    print(f"\tWheel Rotation = {wheel_rotation_deg} degrees")

    # Simulate motor commands (replace with actual motor calls)
    print(f"Driving forward with wheel rotation: {wheel_rotation_deg} degrees")

    # Update position
    rad_angle = math.radians(actual_a)
    actual_x += distance * math.cos(rad_angle)
    actual_y += distance * math.sin(rad_angle)
    print(f"Updated Position: ({actual_x}, {actual_y})")

if __name__ == "__main__":
    Go_to_position(50,50)
    drive_forward(-50)
    Go_to_position(2000, 2000, 90)
    #rotate_by_angle(-45)