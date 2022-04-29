# RSP Pico Tester 
This is a specific tester for RSP, programmed for Opsys and designed to run on Windows


## How to install
In case the RSP already has the code preloaded - skip steps 1-5  
1. Run `pip3 install pyserial`
2. Download [Thonny IDE](https://thonny.org/)
3. Connect the RSP device to a USB port ([Assuming it is already running micropython](https://micropython.org/download/rp2-pico/))
4. Copy the main.py into the RSP device and start it
5. Close Thonny (Sometimes Thonny hogs the COM-port)
6. Reconnect the RSP to the PC 
7. Import sender.py and pathActivator.py into the project folder


## How to use  
Create a new python script.  
Add the following import:
```python
from pathActivator import PathActivator
```
Next we need to make a path activator which will activate all the pins necessary  
It recieves 2 parameters: COM-port and a boolean for activating the debug mode.
```python
pathActivator = PathActivator("COM5", True)
```
After that in order to activate a specific path we simply type:
```python
pathActivator.activate_path_to("SUB","C03)
```
Notice the naming convention, we use C03 and not C3 for example  
When the script is done we use 
```python
pathActivator.close()
```
to close the object -> should be done before exiting the program and NOT in the middle of 2 paths

Example code (Taken from demo.py):
```python
from pathActivator import PathActivator
import sys

# specify the COM port and specify whether or not to be in debug mode
pathActivator = PathActivator("COM5", True)
if len(sys.argv) == 3:
    pathActivator.activate_path_to(sys.argv[1],sys.argv[2])

pathActivator.close()
```

Then we run `.\demo.py C13 SUB` in the CLI and get:
```
Turned off all pins
Turned on C12_C13
Turned on Odd_Even_SEL1
Turned on C_A_CTRL1
Turned on C_SUB_Odd_SEL2
Turned on Odd_Even_SEL2
Turned on C_A_CTRL2
```
## Dependencies  
1.  pyserial.  
