import utime
from machine import Pin, I2C

# a dictionary resolving each pin name to the actual pin
name_to_pin = {
"C14_C15" : Pin(0, Pin.OUT),
"C12_C13" : Pin(1, Pin.OUT),
"C10_C11" : Pin(2, Pin.OUT),
"C8_C9" : Pin(3, Pin.OUT),
"C6_C7" : Pin(4, Pin.OUT),
"C4_C5" : Pin(5, Pin.OUT),
"C2_C3" : Pin(6, Pin.OUT),
"C0_C1" : Pin(7, Pin.OUT),
"A14_A15" : Pin(8, Pin.OUT),
"A12_A13" : Pin(9, Pin.OUT),
"A10_A11" : Pin(10, Pin.OUT),
"A8_A9" : Pin(11, Pin.OUT),
"A6_A7" : Pin(12, Pin.OUT),
"A4_A5" : Pin(13, Pin.OUT),
"A2_A3" : Pin(14, Pin.OUT),
"A0_A1" : Pin(15, Pin.OUT),
"Odd_Even_SEL1" : Pin(16, Pin.OUT),
"C_A_CTRL1" : Pin(17, Pin.OUT),
"Odd_Even_SEL2" : Pin(18, Pin.OUT),
"C_SUB_Odd_SEL1" : Pin(19, Pin.OUT),
"C_A_CTRL2" : Pin(20, Pin.OUT),
"C_SUB_Odd_SEL2" : Pin(21, Pin.OUT),
}
# maps each color to a code
color_codes = {
    "Black" : 0,
    "Red" : 1,
    "Green" : 2,
    "Yellow" : 3,
    "Blue" : 4,
    "Purple" : 5,
    "Cyan" : 6,
    "White" : 7,
    }

# Used the code @ 
# https://github.com/Workshopshed/LCD
# to understand the API of the display, with the (big) help of Elad :)
DISP_CMD       = chr(0x0)  # Used to invoke display commands
RAM_WRITE_CMD  = chr(0x40) # Write to display RAM
CLEAR_DISP_CMD = chr(0x01) # Clear display command
DISP_ON_CMD    = chr(0x0C) # Display on command 
DISP_OFF_CMD   = chr(0x08) # Display off Command -> Does not remove the text!
CONTRAST_CMD   = chr(0x70) # Set contrast LCD command


# Backlights etc
RED = Pin(23,Pin.OUT)
GREEN = Pin(22,Pin.OUT)
BLUE = Pin(24,Pin.OUT)
DEBUG_LIGHT = Pin(29,Pin.OUT)
LCD_RESET = Pin(25,Pin.OUT)

# I2C defining
i2c = I2C(1,scl=Pin(27),sda=Pin(26),freq=100000)
i2c_addr= 0x3c


def init():
    LCD_RESET.value(1)
    backlight_color("White")
    i2c.writeto_mem(i2c_addr,0x00,b'\x00') # Send command to the display
    i2c.writeto_mem(i2c_addr,0x00,b'\x38') # Function set - 8 bit, 2 line display 5x8, inst table 0
    i2c.writeto_mem(i2c_addr,0x00,b'\x39') # Function set - 8 bit, 2 line display 5x8, inst table 1
    i2c.writeto_mem(i2c_addr,0x00,b'\x14') # Set BIAS - 1/5
    i2c.writeto_mem(i2c_addr,0x00,b'\x73') # Set contrast low byte
    i2c.writeto_mem(i2c_addr,0x00,b'\x5E') # ICON disp on, Booster on, Contrast high byte 
    i2c.writeto_mem(i2c_addr,0x00,b'\x6D') # Follower circuit (internal), amp ratio (6)
    i2c.writeto_mem(i2c_addr,0x00,b'\x0C') # Display on
    i2c.writeto_mem(i2c_addr,0x00,b'\x01') # Clear display
    i2c.writeto_mem(i2c_addr,0x00,b'\x06') # Entry mode set - increment

def backlight_color(color):
    if color not in color_codes.keys():
        print("Can't pick color: " + color + ", available colors are: Black, Red, Green, Yellow, Blue, Purple, Cyan, White")
        return
    color_code = color_codes[color]
    if (color_code % 2) == 0:
        RED.value(0)
    else:
        RED.value(1)
        
    color_code = int(color_code / 2)
    if (color_code % 2) == 0:
        GREEN.value(0)
    else:
        GREEN.value(1)
        
    color_code = int(color_code / 2)
    if (color_code % 2) == 0:
        BLUE.value(0)
    else:
        BLUE.value(1)
    print("Changed display color to: " + color)

# some base delay between commands
def command_delay():
    utime.sleep_ms(10)

def do_command(command):
    i2c.writeto(i2c_addr, DISP_CMD + command)
    command_delay()

def set_cursor_line_one():
    do_command(chr(0x80)) # Base adress
    
def set_cursor_line_two():
    do_command(chr(0xE8)) # Voodoo magic

def write_to_display(message, message2 = ""):
    # Check message is too long to display
    if len(message) > 20 or len(message2) > 20:
        print("Your message was too long and will be cut down to 20 chars")
    set_cursor_line_one()
    message = message + " "*(20-len(message))  # pad with spaces to clear the rest
    i2c.writeto(i2c_addr, RAM_WRITE_CMD + message)
    # write 2nd message 
    set_cursor_line_two()
    message2 = message2 + " "*(20-len(message2))  # pad with spaces to clear the rest
    i2c.writeto(i2c_addr, RAM_WRITE_CMD + message2)
    print("Updated the display to: " + message + " - " + message2)


def clear_display():
    do_command(CLEAR_DISP_CMD)
    print("Cleared display")
    
def display_on():
    do_command(DISP_ON_CMD)
    print("Display is now on")
    
def display_off():
    do_command(DISP_OFF_CMD)
    print("Display is now off")


# Turns on a specified pin basd on the pin name
def turn_on(pin_name):
    if pin_name in name_to_pin.keys():
        name_to_pin[pin_name].value(1)
        print("Turned on "+pin_name)
    else:
        print ("Could not turn on pin: " + pin_name + " - pin doesn't exist")          

# Turns off a specified pin basd on the pin name
def turn_off(pin_name):
    if pin_name in name_to_pin.keys():
        name_to_pin[pin_name].value(0)
        print("Turned off "+pin_name)
    else:
        print ("Could not turn off pin: " + pin_name + " - pin doesn't exist")

# Turns off all the pins
def reset():
    print("Reseted path pins")
    pins = name_to_pin.values()
    for pin in pins:
        pin.value(0)


    




