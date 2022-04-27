from sender import Sender


# The COM port should be changed to the correct one found on the machine
# can leave empty if using linux?
s = Sender('COM5')
s.send('2+2')
print(s.receive())
