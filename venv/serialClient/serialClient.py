import serial

class SerialClient:
    def __init__(self, port, baudrate=115200, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_instance = None

    def open(self):
        try:
            self.serial_instance = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            return True
        except serial.SerialException:
            return False

    def send_data(self, data):
        if self.serial_instance and self.serial_instance.isOpen():
            self.serial_instance.write(data.encode())

    def receive_data(self):
        if self.serial_instance and self.serial_instance.isOpen():
            return self.serial_instance.read(1024).decode()
        return ""

    def close(self):
        if self.serial_instance and self.serial_instance.isOpen():
            self.serial_instance.close()