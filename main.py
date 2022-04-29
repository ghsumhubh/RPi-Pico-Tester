from machine import Pin

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
"led" : Pin(25, Pin.OUT)
}

def led_on():
    print("Turned on the led")
    name_to_pin["led"].value(1)

def led_off():
    print("Turned off the led")
    name_to_pin["led"].value(0)

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
    print("Turned off all pins")
    pins = name_to_pin.values()
    for pin in pins:
        pin.value(0)
    




