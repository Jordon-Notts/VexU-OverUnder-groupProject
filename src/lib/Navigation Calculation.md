# A document to explain the calculations used for moving the robot

## Initialisation

When the robot is first positioned on the field, it is to be placed in a know location. The initial location is to be coded in the robot, from here every move is referenced.

The units are to be mm. The origin is the centre of the field, to align with the V5 GPS Sensor.

```python
actual_x = 0 # starting x coordinates, then used to store current robot location
actual_y = 0 # starting y coordinates, then used to store current robot location
actual_a = 90 # starting robot angle, then used to store current robot direction
```

## 1. Calculatate the global angle and the distance between two points

![alt text](/images/image.png)

If the robot starts at -3,0 and would like to face 0,4

### 1. calculate the direction to face

The desired robot position is passed to the function as desired_x, desired_y.

$$\delta_x = x_{desired} - x_{actual} = 0 - - 3 = 3$$
$$\delta_y = y_{desired} - y_{actual} = 4 - 0 = 4$$
$$\theta = tan^{-1}({\delta_y\over \delta_x}) = tan^{-1}({4\over3}) = 53.13\degree$$

### 2. calcualate the disnce between the two points

$$disance = \sqrt{delta_x^2 + delta_y^2 }$$

### As a function

```python

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
        print(f"[Target Angle & Distance] Angle: {theta:.2f}°, Distance: {distance:.2f} mm")

        return theta, distance

```

## 2 Calculated the angle differnce between the direction the robot is facing and need to face

If the robot is facing 90° (ie north) and needs to face 53.13° (north east)

$$\delta_{\theta} = \theta_{actual} - \theta_{desired} = 90-53.13 = 36.87°$$

### As a function

```python
    def calculate_angle_difference(self, desired_angle):
        """
        Calculates the angular difference between the robot's current orientation
        and the desired angle, normalized to the range [-180, 180].

        Args:
            desired_angle (float): Desired angle in degrees.

        Returns:
            float: Angular difference in degrees.
        """
        # Normalize angle difference to [-180, 180]
        angle_difference = (desired_angle - self.a + 180) % 360 - 180

        # Debug output
        print(f"[Angle Difference] Desired: {desired_angle:.2f}°, Current: {self.a:.2f}°, Difference: {angle_difference:.2f}°")

        return angle_difference

```
## 3. rotate on the spot to the desired direction.

![alt text](/images/image-1.png)

The robot starts looking north and would like to rotate clockwise 36.87°

The distance between the robot wheels is 4 units on this image.

$$radius_{robot} = {WheelSpan \over 2} = {4\over 2} = 2$$

Both sets of wheel are rotating at the same speed at the same time in oposite directions, so the robot should stay centred over the point of rotation.

The distance the left wheel moves along the wheel path is

$$ \delta_{\omega} = \delta_{\theta} \times {\pi\over 180} = 0.644 [rads]$$

$$ Dist_{alongPath} = \delta_{\omega} \times Radius_{robot} = 0.644 * 2 =  1.284 [mm]$$

The angle the wheel needs to rotate to travel the distance along the path is

$$\omega_{wheel} = {Dist_{alongPath}\over radius_{wheel}}$$

then convert this back to degrees

$$\theta_{wheel} = \omega_{wheel} \times {180\over\pi}$$

### As a function

```python

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
        print(f"[Drive Mode] Distance: {distance:.2f} mm, Wheel Rotation: {wheel_rotation_deg:.2f}°")

        # Both wheels rotate by the same amount for straight-line motion
        return wheel_rotation_deg, wheel_rotation_deg

```

---

## New Additions

### Class-based Navigation System
We introduced the `RobotNavigator_calcs` class to handle all calculations related to robot movement and orientation. This modular approach simplifies managing the robot's navigation logic.

#### Key Features:
1. **Target Angle and Distance Calculation**:
    - Calculates the angle and distance to a target position relative to the robot's current position.
    - Handles the geometry and provides the required rotation and travel distance.
    
    Example:
    ```python
    desired_angle, distance = robot_nav.calculate_target_angle_and_distance(x_position, y_position)
    ```

2. **Angle Difference Calculation**:
    - Determines the shortest angular difference between the robot's current orientation and a target angle.
    - Normalizes the difference to be between `-180°` and `180°`.

    Example:
    ```python
    angle_difference = robot_nav.calculate_angle_difference(desired_angle)
    ```

3. **Wheel Rotation for Rotation Mode**:
    - Calculates the degrees the wheels need to rotate in opposite directions to turn the robot in place by a specific angle.

    Example:
    ```python
    left_rotation, right_rotation = robot_nav.calculate_wheel_rotation_rotation_mode(angle_difference)
    ```

4. **Wheel Rotation for Driving Forward**:
    - Calculates the degrees the wheels need to rotate to drive forward by a specific distance.

    Example:
    ```python
    left_rotation, right_rotation = robot_nav.calculate_wheel_rotation_drive_mode(distance)
    ```

5. **State Update**:
    - Updates the robot's internal state (position and orientation) after movement or rotation.

    Example:
    ```python
    robot_nav.update_position(new_x=500, new_y=500, new_a=90)
    ```
