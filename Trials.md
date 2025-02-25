# Decemember 2024 In person week

This appentiship is block release, as such assess to the physical robots is limited. Calculations can be carried out remotly, however testing the code that drives the robots can only be carried out during the in person weeks. Below in a list of tests to be carried out during the December in person week.

### Document how to upload to the robot

The user guide for how to upload the code to the robot is incomplete. This need to be carried out in person

please see [Install.md](Install.md)

### Switching between games mode

Does the VEXnet Field Controller, switch automatically between auto mode and driver control mode?

please see [00_games_mode code](src/00_games_modes.py)

### Driver controlled mode

A basic script that takes commands from the controller to control the robot has been writen. Does this code allow the driver to controll the robot?

please see [01_driver_mode code](src/01_driver_mode.py)

#### Reflection

##### Controller input

Controller input made the motors turn, however the right joystick did not control the right motor.

the following adjustments were made

```python
* left_control_input = controller.axis3
* right_control_input = controller.axis2
```

and 

```python
left_motor = Motor(Ports.PORT2, GearSetting.RATIO_18_1)
right_motor = Motor(Ports.PORT10, GearSetting.RATIO_18_1)
```

##### Motor direction

the one of the motors turned in the wrong direction, the following changes were made;

```python

right_motor.spin(REVERSE)

```

##### Motor speed

It was noticed that the robot was too fast to be controllable. it was decided to slow the robot down to 70%

```python
left_motor.set_velocity(left_control_input.position()*0.7, PERCENT)
```

### Combined Driver mode and games mode

A script that switches between driver control mode and autonmous mode has been written. This script has the driver control section added to the code so when in driver control mode the drive should be able to controll the robot.

Does this code:
    1. switch between the different modes?
    2. allow the driver to contol the robot when in driver control mode?

please see [02_combined...](/src/02_combined_driver_and_games_Mode.py)

## Autonomous mode rotate on the spot

To test if the calculations for turning the robot on the spot are correct, a test script has been writen

Does the robot turn on the spot be the desired angle?

please see [04_rotate_90](/src/04_rotate_90_degrees.py)

#### Reflection

##### print()

print() does not work. The diagnostic feed back coded into the fucntions had to be commented out. For diagnostic feed back print to the brain

```python
brain.screen.clear_screen()
brain.screen.print("Autonomous mode")
```

##### Import from...

It was found that when code is split up into seperate scripts, ie using

```python
from lib.example_script import *
```
The code results in an error. this make it difficult to write structured easy to read code.

##### Operation

The car moved to approxmately 90°, ajusting the parameters for wheel radius and wheel distance impoved the accuracy.

The wheels skid resultsing in incorrect movement, this can be reduced by slowing the wheel rotation speed. Later an acceration ramp could be utilited.

## Test goto position

A script that directs the robot to a disired location has been writen.

Does the robot go to the desired location?

please see [05_auto_in_class](/src/Archive/05_auto_in_class.py)

#### Reflection

When the robot is commanded to turn to a specific heading and travel the specific point, ie xy coordinate. The robot does travel to the point, this seams to be promising plue or minus 2mm and plus or minus 2 degrees. Research into whether combined movments create combined errors, ie does chaining 5 plus movments mean the poistion of the robot is out by 100mm. Please see Combined error section.

## Combined error

The robot has 45 seconds to complete its autonomous objectives. The robot is blind as it moves, the only way to know where the robot is, is by knowing where it has been. Each move will add and error to the location of the robot, the question is, is the combined error after 45 seconds worth of movments still userble. ie is a blind robot after lets say 10 moves still capable of accruatly collecting a triball?

This expariment make the robot drive in a 500mm square, ie forward 500m right 90 degrees, foward 500mm then right 90 degrees, repeatedly until 5 squares have been completed.

make a mark on the field, start the robot at this possiton. run the script, how far from the starting mark the the robot finish.

please see [combined error test script](/src/06_combined_error.py)

if the combine error is too big to be userble, 

1. can changes to the script increase the accuracy (dial in wheel diameter and wheel span vairibles), 
   1. are there things i havent accounted for in my calculations
2. additional sensors might need to be used.

#### Reflection

An experaiment was made doing 5 circuits of a 500mm square at 25rpm. the angle error at the end of the circuits was... The picture shows the final position after the 5 rotations, the bar in the picture can be used as a datum.

![final picture 25 rpm](/images/25rpm.jpeg)

Another expariment was taken at 12rpm, again 5 circuits. the angle error was.

![fianl picture 12 rpm](/images/12rpm.jpeg)

Another expariment was made, rubber bands were applied to the wheels with the intention of increasing grip. THis has the uninternted consequence of incresing the wheel radius. This was run at 12 rpm. The error after this run was far better.

![final picture 12 rpm, with rubber](/images/12rpm_with_rubber.jpeg)

A further test was carried out at 50rpm, the test had to be stopped as the error was too great to take meaningful results.

It was found that the wheels skid at higher speeds. It was noticed that adding weight above the driving wheels increased the accuracy.

Due to the fact that the robot is required complete a series of moves within 45 seconds, at 50rpm this is too unreliable to complete this objective and at 12 rmp this is too slow to complete this objective.

An acceleration ramp could be a solotion to the skid and speed issue. 

## Acceleration ramp

An acceleration ramp was programmed into the movement of the robot, this allows for slow accelleration and a slow decelleration resulting in no skids.

The code was updated see [](/src/07_Accel_Ramp.py)

#### Reflection

A couple of parameter needed to be tweeked to make the code work, however the results were good. the robot could acheve a high overall speed, with out loosing its possition.

A compined error trail was carried out with the new acceleration ramp software. the speed of the robot was increased however after a number of momement the robot still lost its position.

It has been decided that the robot need to have some sort of positional feed back mechanism.

## Positional feedback



# Trials March 2025 in person week

1. Test comms between RPI and vex 5 brain
2. Test camera possitioning system

