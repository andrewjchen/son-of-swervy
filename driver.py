#!/usr/bin/env python
import serial

def driveChannel(channel, command):
    '''
    Drives a servo on CHANNEL with a target command
    CHANNEL refers to the servo channel [0...5] on a umaestro
    COMMAND is an unsigned byte [0...254]
    This uses the miniSSC protocol.
    '''
    global serial
    serial.write(chr(0xFF))
    serial.write(chr(channel))
    serial.write(chr(command))

if __name__ == '__main__':
    global serial
    print "starting driver.py..."
    serial = serial.Serial("/dev/ttyUSB0", baudrate=57600)
    driveChannel(0, 0);
    driveChannel(1, 0);
    driveChannel(2, 0);

