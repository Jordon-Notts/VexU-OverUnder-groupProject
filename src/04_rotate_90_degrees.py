# Robot Initialization Parameters
starting_x = 0  # Initial x-coordinate of the robot
starting_y = 0  # Initial y-coordinate of the robot
starting_a = 180  # Initial angle of the robot (in degrees, facing "up")

wheel_span = 279.4  # mm, distance between the robot's wheels (wheel span)
wheel_radius = 50.8  # mm, radius of the robot's wheels

import math

class RobotNavigator_calcs:
    """
    A class to perform navigation calculations for a robot, including angle, distance,
    and wheel rotations for movement and rotation.
    """

    def __init__(self, starting_x, starting_y, starting_a, wheel_radius, robot_width_between_wheels):
        """
        Initializes the robot navigator with the starting position, orientation,
        wheel radius, and robot width.

        Args:
            starting_x (float): Initial x-coordinate of the robot.
            starting_y (float): Initial y-coordinate of the robot.
            starting_a (float): Initial angle of the robot in degrees.
            wheel_radius (float): Radius of the robot's wheels (in mm).
            robot_width_between_wheels (float): Distance between the wheels (wheel span) (in mm).
        """
        self.wheel_span = robot_width_between_wheels  # Distance between wheels
        self.wheel_radius = wheel_radius  # Radius of the robot's wheels
        self.x = starting_x  # Current x-coordinate of the robot
        self.y = starting_y  # Current y-coordinate of the robot
        self.a = starting_a  # Current orientation of the robot (in degrees)
        self.robot_radius = robot_width_between_wheels / 2  # Radius of the robot's rotation

    def calculate_target_angle_and_distance(self, desired_x, desired_y):
        """
        Calculates the angle and distance to a target position relative to the robot's current position.

        Args:
            desired_x (float): Target x-coordinate.
            desired_y (float): Target y-coordinate.

        Returns:
            tuple: Angle to the target in degrees, distance to the target in mm.
        """
        delta_x = desired_x - self.x  # Difference in x-coordinates
        delta_y = desired_y - self.y  # Difference in y-coordinates

        # Calculate the angle using atan2 for proper quadrant handling
        theta = math.degrees(math.atan2(delta_y, delta_x))

        # Calculate the Euclidean distance to the target position
        distance = math.sqrt(delta_x**2 + delta_y**2)

        # Debug output
        # print(f"[Target Angle & Distance] Angle: {theta:.2f}°, Distance: {distance:.2f} mm")

        return theta, distance

    def calculate_angle_difference(self, desired_angle):
        """
        Calculates the angular difference between the robot's current orientation
        and the desired angle, normalized to the range [-180, 180].
# 
        Args:
            desired_angle (float): Desired angle in degrees.

        Returns:
            float: Angular difference in degrees.
        """
        # Normalize angle difference to [-180, 180]
        angle_difference = (desired_angle - self.a + 180) % 360 - 180

        # Debug output
        # print(f"[Angle Difference] Desired: {desired_angle:.2f}°, Current: {self.a:.2f}°, Difference: {angle_difference:.2f}°")

        return angle_difference

    def calculate_wheel_rotation_rotation_mode(self, angle_to_rotate_by):
        """
        Calculates the amount of wheel rotation needed to rotate the robot
        by a specified angle in-place.

        Args:
            angle_to_rotate_by (float): Angle to rotate by in degrees.

        Returns:
            tuple: Wheel rotation in degrees for the left and right wheels.
        """
        # Convert angle to radians for calculation
        angle_to_rotate_by_rad = math.radians(angle_to_rotate_by)

        # Calculate the distance each wheel travels along the robot's rotation circle
        distance_along_circumference = self.robot_radius * angle_to_rotate_by_rad

        # Calculate the rotation of the wheels (in radians)
        wheel_rotation = distance_along_circumference / self.wheel_radius

        # Convert wheel rotation to degrees for motor control
        wheel_rotation_deg = math.degrees(wheel_rotation)

        # Debug output
        # print(f"[Rotate Mode] Rotate By: {angle_to_rotate_by:.2f}°, Wheel Rotation: {wheel_rotation_deg:.2f}°")

        # Left and right wheels rotate in opposite directions for in-place rotation
        return wheel_rotation_deg, -wheel_rotation_deg

    def calculate_wheel_rotation_drive_mode(self, distance):
        """
        Calculates the amount of wheel rotation needed to drive the robot
        a specified distance forward or backward.

        Args:
            distance (float): Distance to travel in mm.

        Returns:
            tuple: Wheel rotation in degrees for the left and right wheels.
        """
        # Calculate wheel rotation in radians
        wheel_rotation = distance / self.wheel_radius

        # Convert wheel rotation to degrees for motor control
        wheel_rotation_deg = math.degrees(wheel_rotation)

        # Debug output
        # print(f"[Drive Mode] Distance: {distance:.2f} mm, Wheel Rotation: {wheel_rotation_deg:.2f}°")
# 
        # Both wheels rotate by the same amount for straight-line motion
        return wheel_rotation_deg, wheel_rotation_deg

    def update_position(self, new_x=None, new_y=None, new_a=None):
        """
        Updates the robot's current position and orientation.

        Args:
            new_x (float, optional): New x-coordinate. Defaults to None.
            new_y (float, optional): New y-coordinate. Defaults to None.
            new_a (float, optional): New angle (orientation) in degrees. Defaults to None.
        """
        if new_x is not None:
            self.x = new_x  # Update x-coordinate
        if new_y is not None:
            self.y = new_y  # Update y-coordinate
        if new_a is not None:
            self.a = new_a  # Update orientation

        # Debug output
        # print(f"[Update Position] New Position: ({self.x:.2f}, {self.y:.2f}), Angle: {self.a:.2f}°")

# Create an instance of the RobotNavigator_calcs class
robot_nav = RobotNavigator_calcs(starting_x, starting_y, starting_a, wheel_radius, wheel_span)

from vex import *  # Import VEX library for hardware interaction

# Initialize VEX Brain and Motors
brain = Brain()  # Brain object to control the robot

left_motor = Motor(Ports.PORT2, GearSetting.RATIO_18_1)
right_motor = Motor(Ports.PORT10, GearSetting.RATIO_18_1)

def control_wheels(rotate_left_wheel_by, rotate_right_wheel_by):
    """
    Controls the robot's wheels to rotate by specific angles.

    Args:
        rotate_left_wheel_by (float): Rotation for the left wheel in degrees.
        rotate_right_wheel_by (float): Rotation for the right wheel in degrees.
    """
    # Debug output for the requested wheel rotations
    # print(f"[Control Wheels] Left: {rotate_left_wheel_by}°, Right: {rotate_right_wheel_by}°")
    
    # Reset the motor positions to ensure accurate movement
    left_motor.reset_position()
    right_motor.reset_position()
    
    # Command the motors to spin to the specified positions
    left_motor.spin_to_position(rotate_left_wheel_by, DEGREES, 25, RPM, wait=False)
    right_motor.spin_to_position(-rotate_right_wheel_by, DEGREES, 25, RPM, wait=False)
    
    # Wait for the motors to finish spinning before proceeding
    while left_motor.is_spinning() or right_motor.is_spinning():
        wait(20, MSEC)  # Check motor status every 20 milliseconds

if __name__ == "__main__":
    """
    Entry point of the program. This block runs when the script is executed.
    Currently, no specific functionality is executed here.
    """
    Test_angle = -90 # degrees
    
    # Calculate the wheel rotations needed for the angular difference
    left_wheel_rotate_by, right_wheel_rotate_by = robot_nav.calculate_wheel_rotation_rotation_mode(Test_angle)

    # print(f"A calculation has been carried out, to turn the robot {Test_angle}, the wheels need to rotate {left_wheel_rotate_by} degrees.")

    brain.screen.clear_screen()
    brain.screen.print("Autonomous mode")

    # Execute the rotation using the control_wheels function
    control_wheels(left_wheel_rotate_by, right_wheel_rotate_by)