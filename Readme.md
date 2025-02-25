# Electro-mechanical Engineering Degree Apprenticeship, Electromechinical group project, Year 2024-2025

This is the code for the Electromechinical group project.

The group project is to build two robots to compete in the VexU over under compertision. The VEXu over under was held last year, so the robots wont be entered in the offical compertition.

## Install

To install the software and upload the code to the robots please see [Install documentation](Install.md).

## Trials

A number of trials need to be carried out during the in person weeks, for information on the trials see [Trail information](Trials.md)

## Log

For a log of changes please see [build log](Log.md)

---

## Updated `Go_to_position` Function
The `Go_to_position` function now integrates the `RobotNavigator_calcs` class and includes the following steps:
1. **Rotate to Face the Target**:
    - Calculates the angle difference to the target.
    - Rotates the robot to face the target position.

2. **Drive Forward**:
    - Calculates the distance to the target position.
    - Commands the robot to drive forward to the target position.

3. **Rotate to Final Heading** *(Optional)*:
    - If a final heading is provided, rotates the robot to the desired orientation.

Example:
```python
Go_to_position(500, 500, final_heading=90)

```



---

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

