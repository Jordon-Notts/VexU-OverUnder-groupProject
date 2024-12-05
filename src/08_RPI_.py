from vex import *  # Import VEX library for hardware interaction

link = SerialLink(Ports.PORT7,'Serial_Name',VexlinkType.MANAGER,True)

global brain

# Initialize VEX Brain and Motors
brain = Brain()  # Brain object to control the robot

def serial_recieved_callback(buffer, length):

    global brain
    brain.screen.clear_screen()
    brain.screen.print(buffer)

link.received(serial_recieved_callback)