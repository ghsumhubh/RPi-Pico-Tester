from time import sleep
from pathActivator import PathActivator
import sys

# specify the COM port and specify whether or not to be in debug mode
pathActivator = PathActivator("COM6", True)
if len(sys.argv) == 3:
    pathActivator.activate_path_to(sys.argv[1],sys.argv[2])
    pathActivator.set_display_color("Blue")
    pathActivator.set_display_text(sys.argv[1], sys.argv[2])
    sleep(5)
    pathActivator.set_display_text("Shutting display off")
    sleep(3)
    pathActivator.display_off()

pathActivator.close()