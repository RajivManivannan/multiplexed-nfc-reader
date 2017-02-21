#!/usr/bin/env python

import RPi.GPIO as GPIO
import MFRC522
import signal

import spidev
import time

class MultiplexedNFCReader:
    A0 = 18 # GPIO 24
    A1 = 16 # GPIO 23
    A2 = 12 # GPIO 18

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(MultiplexedNFCReader.A2, GPIO.OUT)
        GPIO.setup(MultiplexedNFCReader.A1, GPIO.OUT)
        GPIO.setup(MultiplexedNFCReader.A0, GPIO.OUT)
        self.mfrfcReader = MFRC522.MFRC522()

    def selectDevice(self, deviceNumber):
        self.deviceNumber = deviceNumber
        GPIO.output(MultiplexedNFCReader.A2, (deviceNumber >> 2) & 1)
        GPIO.output(MultiplexedNFCReader.A1, (deviceNumber >> 1) & 1)
        GPIO.output(MultiplexedNFCReader.A0, deviceNumber & 1)

    def readNFC(self):
        (status, uid) = self.mfrfcReader.MFRC522_Anticoll()

        if status == self.mfrfcReader.MI_OK:
          print "Card read " + str(self.deviceNumber) + "! UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])

    def cleanup(self):
        GPIO.cleanup()


multiplexedNFCReader = MultiplexedNFCReader()

while 1:
    for device in range(0, 8):
        multiplexedNFCReader.selectDevice(device)
        multiplexedNFCReader.readNFC()

multiplexedNFCReader.cleanup()
