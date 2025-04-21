from vex import *

global brain

brain = Brain()
controller = Controller(PRIMARY)

# Define drive motors
left_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1)
right_motor = Motor(Ports.PORT2, GearSetting.RATIO_18_1)

button_R1 = controller.buttonR1
button_R2 = controller.buttonR2

button_x = controller.buttonX

head_motor = Motor(Ports.PORT3, GearSetting.RATIO_18_1)

def print_to_brain(message, row):

    global brain

    brain.screen.clear_row(row)
    brain.screen.set_cursor(row,1)
    brain.screen.print(message)

def head_up():

    head_motor.spin_to_position(180, DEGREES,25,RPM,True)
    print_to_brain("Head up",5)

    pass

def head_down():

    head_motor.spin_to_position(0, DEGREES,25,RPM,True)
    print_to_brain("Head down",5)

    pass

# Exponential control for smoother handling
def expo(input_value):
    expo_factor = 2.5
    direction = 1 if input_value >= 0 else -1
    output = ((abs(input_value) ** expo_factor) / (100 ** (expo_factor - 1))) * direction
    return output

def skid_steer_control():
    # Speed from right stick (forward/backward)
    speed = expo(controller.axis3.position())
    # Turning from left stick
    turn = expo(controller.axis1.position())

    # Calculate motor speeds
    left_speed = speed + turn
    right_speed = speed - turn

    # Limit motor speeds to [-100, 100]
    left_speed = max(min(left_speed, 100), -100)
    right_speed = max(min(right_speed, 100), -100)

    # Set motor velocities
    left_motor.set_velocity(left_speed, PERCENT)
    right_motor.set_velocity(right_speed, PERCENT)

    # Spin motors
    left_motor.spin(FORWARD)
    right_motor.spin(REVERSE)

# Define the input pins:
# Common clock and chip select (CS) for all channels
cs_pin     = DigitalIn(brain.three_wire_port.a)   # Chip Select (input from sensor)
clock_pin  = DigitalIn(brain.three_wire_port.b)   # Clock (input from sensor)

# Data channels: X, Y, and Angle (using separate ports for parallel data)
data_x_pin = DigitalIn(brain.three_wire_port.c)   # Data for X channel
data_y_pin = DigitalIn(brain.three_wire_port.d)   # Data for Y channel
angle_pin  = DigitalIn(brain.three_wire_port.e)   # Data for angle

# Define the request pin (DigitalOut) that we control to ask for data.
# When this pin is pulled LOW, it requests the sensor to transmit data.
request_pin = DigitalOut(brain.three_wire_port.f) # Request pin

# Global buffers to store received bits for each channel
buffer_x     = []
buffer_y     = []
buffer_angle = []

# Expected number of bits per transmission for each channel (updated to 12 bits)
NUM_BITS_XY    = 12  # for X and Y (12-bit signed)
NUM_BITS_ANGLE = 12  # for angle (12-bit unsigned, later divided by 10)

def handle_clock():
    """
    Callback for each falling edge of the clock pin.
    Reads one bit from each of the data lines and appends them to their respective buffers.
    """
    global buffer_x, buffer_y, buffer_angle
    buffer_x.append(data_x_pin.value())
    buffer_y.append(data_y_pin.value())
    buffer_angle.append(angle_pin.value())

def convert_bits_to_int(bits):
    """
    Converts a list of bits (MSB first) into an integer.
    """
    value = 0
    for bit in bits:
        value = (value << 1) | bit
    return value

def twos_complement(value, bits):
    """
    Converts an integer in two's complement format to a signed integer.
    """
    if value & (1 << (bits - 1)):
        value -= (1 << bits)
    return value

def request_location():
    """
    Generates a low pulse on the request pin to ask the sensor to transmit data.
    """
    # A short low pulse (adjust delay as needed to meet sensor requirements)

    request_pin.set(False)
    print("WHERE AM I")
    wait(0.01, SECONDS)
    request_pin.set(True)

def handle_cs():
    """
    Callback triggered when the CS (chip select) pin goes HIGH, indicating the end of transmission.
    Processes the received bits for each channel, converting them to proper numeric values.
    """
    global buffer_x, buffer_y, buffer_angle
    if (len(buffer_x) == NUM_BITS_XY and 
        len(buffer_y) == NUM_BITS_XY and 
        len(buffer_angle) == NUM_BITS_ANGLE):
        
        # Convert bit buffers to raw integer values
        raw_x     = convert_bits_to_int(buffer_x)
        raw_y     = convert_bits_to_int(buffer_y)
        raw_angle = convert_bits_to_int(buffer_angle)
        
        # Convert raw X and Y to signed integers using two's complement conversion
        data_x = twos_complement(raw_x, NUM_BITS_XY)
        data_y = twos_complement(raw_y, NUM_BITS_XY)
        
        # Convert angle: scale the raw value (e.g., 3565 represents 356.5°)
        angle = raw_angle / 10.0
        
        print("Received values:")
        print("X =", data_x, ", Y =", data_y, ", Angle =", angle)
        print_to_brain("X = {}".format(data_x),3)
        print_to_brain("Y = {}".format(data_y),4)
        print_to_brain("Angle = {}".format(angle),5)

    else:
        print("Incomplete transmission:")
        print("X bits =", len(buffer_x), ", Y bits =", len(buffer_y), ", Angle bits =", len(buffer_angle))
        # Optionally, re-trigger the request if the data was incomplete
        request_location()
    
    # Clear buffers for the next transmission
    buffer_x     = []
    buffer_y     = []
    buffer_angle = []

if __name__ == "__main__":

    """
    Entry point of the program. This block runs when the script is executed.
    Currently, no specific functionality is executed here.
    """

    print_to_brain("DRIVER MODE SKETCH", 1)

    print("")

    # Set up callbacks:
    # On each falling edge of the clock, capture the bits in parallel.
    clock_pin.low(handle_clock)
    # When CS goes HIGH, process the complete transmission.
    cs_pin.high(handle_cs)

    request_pin.set(1)

    controller.buttonR1.pressed(head_up)
    controller.buttonR2.pressed(head_down)

    button_x.pressed(request_location)

    while True:
        skid_steer_control()
        wait(10, MSEC)