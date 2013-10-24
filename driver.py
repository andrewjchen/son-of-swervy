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

def pololuDrive(device, channel, target):
    '''
    Drives a servo on a maestro using the pololu protocol.
    DEVICE is the maestro device number. (default 12)
    CHANNEL is the servo's channel number [1...6] on micromaestro
    TARGET is the pulse width in microseconds.
    '''
    global serial
    serial.write(chr(0xAA)) # 0xAA
    serial.write(chr(device))
    serial.write(chr(4))
    serial.write(chr(channel))
    serial.write(chr((target*4) & 0x7F))
    serial.write(chr(((target*4) >> 7) & 0x7F))

if __name__ == '__main__':
    global serial
    print "starting driver.py..."
    serial = serial.Serial("/dev/ttyUSB0", baudrate=57600)
    pololuDrive(12, 0, 1500);