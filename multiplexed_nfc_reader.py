import RPi.GPIO as GPIO
import MFRC522
import signal

import spidev
import time

class MultiplexedNFCReader:
    A2 = 18 # GPIO 24
    A1 = 16 # GPIO 23
    A0 = 12 # GPIO 18

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(MultiplexedNFCReader.A2, GPIO.OUT)
        GPIO.setup(MultiplexedNFCReader.A1, GPIO.OUT)
        GPIO.setup(MultiplexedNFCReader.A0, GPIO.OUT)
        self.mfrfcReader = MFRC522.MFRC522()

    def selectDevice(self, deviceNumber):
        GPIO.output(MultiplexedNFCReader.A2, (deviceNumber >> 2) & 1)
        GPIO.output(MultiplexedNFCReader.A1, (deviceNumber >> 1) & 1)
        GPIO.output(MultiplexedNFCReader.A0, deviceNumber & 1)

    def readNFC(self):
        (status, TagType) = self.mfrfcReader.MFRC522_Request(self.mfrfcReader.PICC_REQIDL)

        print "**********"
        print status
        print TagType

        if status == self.mfrfcReader.MI_OK:
          print "Card detected"

        (status, uid) = self.mfrfcReader.MFRC522_Anticoll()

        print "----------"
        print status
        print uid

        if status == self.mfrfcReader.MI_OK:
          print "Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])

        print "Finished Reading"

    def cleanup(self):
        GPIO.cleanup()


multiplexedNFCReader = MultiplexedNFCReader()

DEVICES = [0, 1]

for device in DEVICES:
    print "Selecting device: "+ str(device)
    multiplexedNFCReader.selectDevice(device)
    multiplexedNFCReader.readNFC()

multiplexedNFCReader.cleanup()
