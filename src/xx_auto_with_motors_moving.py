from vex import *
import math

# Brain and Motors
brain = Brain()
left_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1)
right_motor = Motor(Ports.PORT10, GearSetting.RATIO_18_1)

# Global Robot Parameters
global actual_x, actual_y, actual_a, wheel_span, wheel_radius

actual_x = 0  # Current x-coordinate
actual_y = 0  # Current y-coordinate
actual_a = 90  # Current robot angle in degrees

wheel_span = 250  # mm, distance between the wheels
wheel_radius = 75  # mm, wheel radius

# Helper Functions
def calculate_target_angle_and_distance(desired_x, desired_y):
    global actual_x, actual_y
    delta_x = desired_x - actual_x
    delta_y = desired_y - actual_y
    theta = math.degrees(math.atan2(delta_y, delta_x))
    distance = math.sqrt(delta_x**2 + delta_y**2)
    print(f"[Target Angle & Distance] Angle: {theta:.2f}°, Distance: {distance:.2f} mm")
    return theta, distance

def calculate_angle_difference(desired_angle):
    global actual_a
    angle_difference = (desired_angle - actual_a + 180) % 360 - 180
    print(f"[Angle Difference] Desired: {desired_angle:.2f}°, Current: {actual_a:.2f}°, Difference: {angle_difference:.2f}°")
    return angle_difference

def calculate_wheel_rotation_rotation_mode(angle_to_rotate_by):
    robot_radius = wheel_span / 2
    angle_to_rotate_by_rad = math.radians(angle_to_rotate_by)
    distance_along_circumference = robot_radius * angle_to_rotate_by_rad
    wheel_rotation = distance_along_circumference / wheel_radius
    wheel_rotation_deg = math.degrees(wheel_rotation)
    print(f"[Rotate Mode] Rotate By: {angle_to_rotate_by:.2f}°, Wheel Rotation: {wheel_rotation_deg:.2f}°")
    return wheel_rotation_deg, -wheel_rotation_deg

def calculate_wheel_rotation_drive_mode(distance):
    wheel_rotation = distance / wheel_radius
    wheel_rotation_deg = math.degrees(wheel_rotation)
    print(f"[Drive Mode] Distance: {distance:.2f} mm, Wheel Rotation: {wheel_rotation_deg:.2f}°")
    return wheel_rotation_deg, wheel_rotation_deg

def control_wheels(rotate_left_wheel_by, rotate_right_wheel_by):
    print(f"[Control Wheels] Left: {rotate_left_wheel_by:.2f}°, Right: {rotate_right_wheel_by:.2f}°")
    left_motor.reset_position()
    right_motor.reset_position()
    left_motor.spin_to_position(rotate_left_wheel_by, DEGREES, 25, RPM, wait=False)
    right_motor.spin_to_position(rotate_right_wheel_by, DEGREES, 25, RPM, wait=True)
    while left_motor.is_spinning() or right_motor.is_spinning():
        wait(20, MSEC)

    

def update_position(new_x=None, new_y=None, new_a=None):
    global actual_x, actual_y, actual_a
    if new_x is not None:
        actual_x = new_x
    if new_y is not None:
        actual_y = new_y
    if new_a is not None:
        actual_a = new_a
    print(f"[Update Position] New Position: ({actual_x:.2f}, {actual_y:.2f}), Angle: {actual_a:.2f}°")

# Main Functionality
def Go_to_position(x_position, y_position, final_heading=None):
    # Step 1: Rotate to face the target
    desired_angle, distance = calculate_target_angle_and_distance(x_position, y_position)
    angle_difference = calculate_angle_difference(desired_angle)
    left_wheel_rotate_by, right_wheel_rotate_by = calculate_wheel_rotation_rotation_mode(angle_difference)
    control_wheels(left_wheel_rotate_by, right_wheel_rotate_by)
    update_position(new_a=desired_angle)

    # Step 2: Drive forward to the target position
    left_wheel_rotate_by, right_wheel_rotate_by = calculate_wheel_rotation_drive_mode(distance)
    control_wheels(left_wheel_rotate_by, right_wheel_rotate_by)
    update_position(new_x=x_position, new_y=y_position)

    # Step 3: Optionally rotate to final heading
    if final_heading is not None:
        final_angle_difference = calculate_angle_difference(final_heading)
        left_wheel_rotate_by, right_wheel_rotate_by = calculate_wheel_rotation_rotation_mode(final_angle_difference)
        control_wheels(left_wheel_rotate_by, right_wheel_rotate_by)
        update_position(new_a=final_heading)

# Testing the Functionality
if __name__ == "__main__":
    Go_to_position(500, 500, final_heading=180)