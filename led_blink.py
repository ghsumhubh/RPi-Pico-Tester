import time
from sender import Sender

# The COM port should be changed to the correct one found on the machine
# can leave empty if using linux?
s = Sender('COM5')
while True:
    s.send('led_on()')
    time.sleep(0.5)
    s.send('led_off()')
    time.sleep(0.5)
