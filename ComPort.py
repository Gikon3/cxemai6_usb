import serial


class ComPort:
    LENGTHWORD = 8  # in half bytes
    INITWORD = "F0DA"

    def __init__(self, portname="COM11", baundrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                 stopbits=serial.STOPBITS_ONE, timeout=1):
        self.PORTNAME = portname
        self.BAUNDRATE = baundrate
        self.BYTESIZE = bytesize
        self.PARITY = parity
        self.STOPBITS = stopbits
        self.TIMEOUT = timeout

        self.port = serial.Serial(
            port=self.PORTNAME,
            baudrate=self.BAUNDRATE,
            bytesize=self.BYTESIZE,
            parity=self.PARITY,
            stopbits=self.STOPBITS,
            timeout=self.TIMEOUT)

        print(self.PORTNAME, "is Open")

    def read(self, four_byte):
        line = ""
        cnt_byte = 0
        if four_byte is False:
            while line[-self.LENGTHWORD:-self.LENGTHWORD + len(self.INITWORD)] != self.INITWORD \
                    and cnt_byte != self.LENGTHWORD:
                byte = bytearray(self.port.read(1)).hex().upper()
                line += byte
                cnt_byte += 1
        else:
            line = bytearray(self.port.read(4)).hex().upper()

        return line
