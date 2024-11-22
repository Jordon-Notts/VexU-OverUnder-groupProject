# Trials

These are a list of things to test during the December in person week.
### Switching between games mode

Does the VEXnet Field Controller, switch automatically between auto mode and driver control mode. [[#Driver control mode]]
### Test the Go_to_position function

Test to see if the Go to position function actually causes the robot to go to the desired location. [[#Go to position]]

It is important to find out if the combined error after moving to several consecutive locations is too big to be useable for the 45 seconds of autonomous game play.
# Install

1. Install vs code
	* go to https://code.visualstudio.com/
	* Install vscode
2. Install the VEX extention
	* click this icon 
		![[Pasted image 20241112102703.png]]
	* search for vex robotics.
		![[Pasted image 20241112102757.png]]
	* Install the extension.

# Download the code

> [!error] Todo
> - [x] Document how to install the programming software
> - [ ] How to pull project from git.

# Upload

> [!error] Todo
> Document how to upload the sketch to the vex brain v5

# Functions

## Competition modes

The controllers are connected to the VEXnet Field Controller for the entirety of the game.

![image](images\Pasted image 20241112105355.png)

![[Pasted image 20241112105355.png]]

In order to take commands from the VEXnet Field Controller, and change the robots to different modes. Call back modes need to be assigned to the Competition, one for driver control mode and one for autonomous mode.

```python
def driver_control_mode():
    pass

def autonomous_mode():
    pass

vex_over_under = Competition(driver_control_mode, autonomous_mode)
```
### Driver control mode

This is called by the VEXnet Field Controller, which puts the robots in either Driver control mode or autonomous mode.

This function takes control signals from the controller and has the robot carry out these actions.

```python
def driver_control_mode():
	while True:
	    left_motor.set_velocity(ctrl.axis3.position(), PERCENT)
		right_motor.set_velocity(ctrl.axis2.position(), PERCENT)
```
#### Reading control inputs

A controller class needs to be generated for actions to be read by the controller.

```python
import vex as vx

ctrl = vx.Controller(PRIMARY)
```

We can either create call-backs for each of the buttons or manually poll each button while in the while routine. for the sake of clean programming it would be best to poll the analogue sticks and create call-backs for the buttons.
##### button call-backs

The function to be called, lets say we have a functions that operates the grab mechanism:

```python
grab_is_open = True

def grab_toggle()
	# This will open the grab mecanism if closed and close it if open
	if grab_is_open:
		#Close the mechanism
		pass
	else:
		#Open the mechanism
		pass
```

Assign the function to a button on the controller:

```python
ctrl.buttonA.pressed(grab_toggle)

vx.wait(15, MSEC) # 15 msec delay to ensure events get registered
```

Possible issues are that the call-backs might be actionable during the autonomous mode. For the sake of clearly abiding by the rules, and ensuring no accidental key presses are made, the controllers should be put down during the autonomous control period.
##### analogue stick actions

These have to be polled in a while loop.

```python
left_motor.set_velocity(ctrl.axis3.position(), PERCENT)
right_motor.set_velocity(ctrl.axis2.position(), PERCENT)
```

The axisX is the analogue reading from the controller. I believe axis 1 and 2 are for the left stick, the vertical and the horizontal axises. Axises 3, 4 for the right stick, the vertical and the horizontal axises. The position() returns the position of analogue sticks. This is then passed into the motor, set_velocity function for the desired motors.
### Autonomous mode

This is called by the VEXnet Field Controller, which puts the robots in either Driver control mode or autonomous mode.

This function carries out the programmed actions required for the autonomous game period.

```python
def autonomous_mode():
	pass
```

#### Go to position

The game plan might change, for the sake of making the autonomous game easier to change a function called go_to_possiton will be created. This will be called from the autonomous_mode function.

The go_to_possiton takes 2 arguments and a further optional argument. 
1. x position,
2. y position,
3. optional argument, angle

The go_to_posstion causes the robot to

1. calculate the direction to face
2. rotate on the spot to the desired direction
3. move in a straight line to the desired location
4. optionally, face in the desired direction

##### initialisation

When the robot is first positioned on the field, it is to be placed in a know location. The initial location is to be coded in the robot, from here every move is referenced.

The units are to be mm. The origin is the centre of the field, to align with the V5 GPS Sensor.

```python
actual_x = 0 # starting x coordinates, then used to store current robot location
actual_y = 0 # starting y coordinates, then used to store current robot location
actual_a = 90 # starting robot angle, then used to store current robot direction
```

##### 1. calculate the direction to face

The desired robot position is passed to the function as desired_x, desired_y.

$$\delta_x = x_{desired} - x_{actual}$$
$$\delta_y = y_{desired} - y_{actual}$$
$$\theta = tan^{-1}({\delta_y\over \delta_x})$$
##### 2. rotate on the spot to the desired direction.

ensure the motor positions are zeroed.

	motor_group.reset_position()

tell the motor to spin to the desired position.

The desired rotation of each motor group is based on the wheel position from the centre of rotation, and the wheel diameter.

Assume the wheels take the circumference of a circle, the radius is half the distance between the wheels.

$$r_{robot} = {WheelSpan \over 2}$$

the distance the wheels need to move along the circumference is the radius times the aligning angle in rads.

$$d_{alongCircumfrance} =  \omega_{alignment} \times r_{robot}$$
the aligning angle is the desired angle minus the actual angle.

$$\Delta\theta=\theta_{desired}​−\theta_{actual​}$$

$$\omega_{alignment} = \Delta_{\theta}\times{\pi\over180}$$

the angle the wheels need to rotate is the along circumference divided by the wheel radius.

$$\omega_{wheel} = {d_{alongCircumfrance}\over r_{wheel}} $$
tell the motor to spin to the desired position.

	motor.spin_to_position(rotation, units, velocity, units_v, wait)

make sure the motors have finished before moving to the next step.

	while not motor.is_spinning()
##### 3. move in a straight line to the desired location

ensure the motor positions are zeroed.

	motor_group.reset_position()

tell the motor to spin to the desired position.

	motor.spin_to_position(rotation, units, velocity, units_v, wait)

make sure the motors have finished before moving to the next step.

	while not motor.is_spinning()


