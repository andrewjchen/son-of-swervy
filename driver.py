#!/usr/bin/env python
import serial
import time

def driveChannel(serial, channel, command):
    '''
    Drives a servo on CHANNEL with a target command
    SERIAL is the serial device the maestro is attached to.
    CHANNEL refers to the servo channel [0...5] on a umaestro.
    COMMAND is an unsigned byte [0...254]
    This uses the miniSSC protocol.
    '''
    serial.write(chr(0xFF))
    serial.write(chr(channel))
    serial.write(chr(command))

def pololuDrive(serial, device, channel, target):
    '''
    Drives a servo on a maestro using the pololu protocol.
    SERIAL is the serial device the maestro is attached to.
    DEVICE is the maestro device number. (default 12)
    CHANNEL is the servo's channel number [1...6] on micromaestro.
    TARGET is the pulse width in microseconds.
    '''
    serial.write(chr(0xAA)) # 0xAA
    serial.write(chr(device))
    serial.write(chr(4))
    serial.write(chr(channel))
    serial.write(chr((target*4) & 0x7F))
    serial.write(chr(((target*4) >> 7) & 0x7F))

def getPosition(serial, device, channel):
    '''
    Accesses the position of a channel using the pololu protocol.
    SERIAL is the serial device the maestro is attached to.
    DEVICE is the maestro device number. (default 12)
    CHANNEL is the channel to sample.

    When the channel is an analog channel, it reports a value [0...1023].
    '''
    serial.write(chr(0xAA))
    serial.write(chr(device))
    serial.write(chr(0x10))
    serial.write(chr(channel))
    return ord(serial.read(1)) + 256 * ord(serial.read(1))

if __name__ == '__main__':
    global serial
    print "starting driver.py..."
    serial = serial.Serial("/dev/ttyUSB0", baudrate=57600)
    while True:
        print("0:{0} \t 1:{1} \t 2:{2}".format(
            getPosition(serial, 12, 3),
            getPosition(serial, 12, 4),
            getPosition(serial, 12, 5)))

