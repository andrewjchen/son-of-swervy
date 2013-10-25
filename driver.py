#!/usr/bin/env python
import serial
import time
import PID

class Caster:
    """ A controlled steerable wheel.
    Currently uses a servo to rotate and a potentiometer for feedback.
    """

    driveChannel = -1
    senseChannel = -1
    pid = PID.PID(P=2)
    device = 12
    last_time = time.time()
    fps = 0

    def __init__(self, serial, driveChannel, senseChannel, zero):
        self.serial = serial
        self.driveChannel = driveChannel
        self.senseChannel = senseChannel 
        self.zero = zero

    def setAngle(self, angle):
        """ sets the controller setpoint """
        self.pid.setPoint(angle)

    def tick(self):
        """ performs a control loop tick. """
        now = time.time()
        self.fps = (now - self.last_time) * 0.9 + self.fps * 0.1
        self.last_time = now
        out = self.pid.update(
            getPosition(self.serial, self.device, self.senseChannel))
        setVelocity(
            self.serial,
            self.device,
            self.driveChannel,
            int(out),
            self.zero)

def driveChannel(serial, channel, command):
    """ Drives a servo on CHANNEL with a target command
    SERIAL is the serial device the maestro is attached to.
    CHANNEL refers to the servo channel [0...5] on a umaestro.
    COMMAND is an unsigned byte [0...254]
    This uses the miniSSC protocol.
    """
    serial.write(chr(0xFF))
    serial.write(chr(channel))
    serial.write(chr(command))

def pololuDrive(serial, device, channel, target):
    """ Drives a servo on a maestro using the pololu protocol.
    SERIAL is the serial device the maestro is attached to.
    DEVICE is the maestro device number. (default 12)
    CHANNEL is the servo's channel number [1...6] on micromaestro.
    TARGET is the pulse width in microseconds.
    """
    serial.write(chr(0xAA)) # 0xAA
    serial.write(chr(device))
    serial.write(chr(4))
    serial.write(chr(channel))
    serial.write(chr((target*4) & 0x7F))
    serial.write(chr(((target*4) >> 7) & 0x7F))

def getPosition(serial, device, channel):
    """ Accesses the position of a channel using the pololu protocol.
    SERIAL is the serial device the maestro is attached to.
    DEVICE is the maestro device number. (default 12)
    CHANNEL is the channel to sample.

    When the channel is an analog channel, it reports a value [0...1023].
    """
    serial.write(chr(0xAA))
    serial.write(chr(device))
    serial.write(chr(0x10))
    serial.write(chr(channel))
    return ord(serial.read(1)) + 256 * ord(serial.read(1))

def setVelocity(serial, device, channel, velocity, zero):
    pololuDrive(serial, device, channel, velocity + zero)

if __name__ == '__main__':
    global serial
    print "starting driver.py..."
    serial = serial.Serial("/dev/ttyUSB0", baudrate=250000)

    caster_a = Caster(serial, 0, 3, 1520)
    caster_b = Caster(serial, 1, 4, 1530)
    caster_c = Caster(serial, 2, 5, 1548)
    caster_a.setAngle(700)
    caster_b.setAngle(700)
    caster_c.setAngle(700)


    while True:
        caster_a.tick()
        caster_b.tick()
        caster_c.tick()