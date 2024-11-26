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

### Combined Driver mode and games mode

A script that switches between driver control mode and autonmous mode has been written. This script has the driver control section added to the code so when in driver control mode the drive should be able to controll the robot.

Does this code:
    1. switch between the different modes?
    2. allow the driver to contol the robot when in driver control mode?

please see [02_combined...](src/02_combined_driver_and_games_Mode.py)

## Autonomous mode rotate on the spot

To test if the calculations for turning the robot on the spot are correct, a test script has been writen

Does the robot turn on the spot be the desired angle?

please see [04_rotate_90](src/04_rotate_90_degrees.py)

## Test goto position

A script that directs the robot to a disired location has been writen.

Does the robot go to the desired location?

please see [05_auto_in_class](src/05_auto_in_class.py)

## Combined error

The robot has 45 seconds to complete its autonomous objectives. The robot is blind as it moves, the only way to know where the robot is, is by knowing where it has been. Each move will add and error to the location of the robot, the question is, is the combined error after 45 seconds worth of movments still userble. ie is a blind robot after lets say 10 moves still capable of accruatly collecting a triball?

make a mark on the field, start the robot at this possiton. run the script, how far from the starting mark the the robot finish.

please see [combined error test script](src\06_combined_error.py)

if the combine error is too big to be userble, 

1. can changes to the script increase the accuracy, 
   1. are there things i havent accounted for in my calculations
2. additional sensors might need to be used.