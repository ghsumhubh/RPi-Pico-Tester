from pathActivator import PathActivator
import sys

# specify the COM port and specify whether or not to be in debug mode
pathActivator = PathActivator("COM6", True)
if len(sys.argv) == 3:
    pathActivator.activate_path_to(sys.argv[1],sys.argv[2])

pathActivator.close()