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
        self.mfrfc_reader = MFRC522.MFRC522()

    def select_device(self, deviceNumber):
        GPIO.output(MultiplexedNFCReader.A2, (deviceNumber >> 2) & 1)
        GPIO.output(MultiplexedNFCReader.A1, (deviceNumber >> 1) & 1)
        GPIO.output(MultiplexedNFCReader.A0, deviceNumber & 1)

    def has_tag(self):
        (status, TagType) = self.mfrfc_reader.MFRC522_Request(self.mfrfc_reader.PICC_REQIDL)
        return status == self.mfrfc_reader.MI_OK

    def read_NFC(self):
        (status, uid) = self.mfrfc_reader.MFRC522_Anticoll()
        if status == self.mfrfc_reader.MI_OK:
            return str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
        else:
            return ""

    def cleanup(self):
        GPIO.cleanup()

continue_reading = True

multiplexed_nfc_reader = MultiplexedNFCReader()

def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    multiplexed_nfc_reader.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

while continue_reading:
    for device in range(0, 8):
        multiplexed_nfc_reader.select_device(device)
        if multiplexed_nfc_reader.has_tag():
            tag_uid = multiplexed_nfc_reader.read_NFC()
            print "Card read " + str(device) + "! UID: "+ tag_uid
