import serial


class Sender:
    TERMINATOR = '\r'.encode('UTF8')

    def __init__(self, device='/dev/ttyACM0', baud=9600, timeout=1):
        self.serial = serial.Serial(device, baud, timeout=timeout)

    def receive(self) -> str:
        line = self.serial.read_until(self.TERMINATOR)
        return line.decode('UTF8').strip()

    def send(self, text: str):
        line = '%s\r\f' % text
        self.serial.write(line.encode('UTF8'))
        # dismiss the echo
        self.receive()

    def close(self):
        self.serial.close()
