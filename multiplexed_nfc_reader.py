#!/usr/bin/env python

import RPi.GPIO as GPIO
import MFRC522
import spidev

import time
import signal
import datetime

nfc_uuid_to_tool_map = {
    "136,4,170,99": "Tool A",
    "136,4,80,109": "Tool B",
    "136,4,78,109": "Tool C",
    "136,4,60,110": "Tool D"
}

class MultiplexedNFCReader:
    A0 = 37 # GPIO 26
    A1 = 35 # GPIO 19
    A2 = 33 # GPIO 13
    A3 = 31 # GPIO 6
    A4 = 29 # GPIO 5

    def __init__(self, device_number):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(MultiplexedNFCReader.A0, GPIO.OUT)
        GPIO.setup(MultiplexedNFCReader.A1, GPIO.OUT)
        GPIO.setup(MultiplexedNFCReader.A2, GPIO.OUT)
        GPIO.setup(MultiplexedNFCReader.A3, GPIO.OUT)
        GPIO.setup(MultiplexedNFCReader.A4, GPIO.OUT)
        self.select_device(device_number)
        self.mfrfc_reader = MFRC522.MFRC522()

    def select_device(self, device_number):
        a4_value = (device_number >> 4) & 1
        a3_value = (device_number >> 3) & 1
        a2_value = (device_number >> 2) & 1
        a1_value = (device_number >> 1) & 1
        a0_value = device_number & 1

        # print "Setting value: " + str(a4_value) + " " + str(a3_value) + " " + str(a2_value) + " " + str(a1_value) + " " + str(a0_value)

        GPIO.output(MultiplexedNFCReader.A0, a0_value)
        GPIO.output(MultiplexedNFCReader.A1, a1_value)
        GPIO.output(MultiplexedNFCReader.A2, a2_value)
        GPIO.output(MultiplexedNFCReader.A3, a3_value)
        GPIO.output(MultiplexedNFCReader.A4, a4_value)

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
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()
signal.signal(signal.SIGINT, end_read)

tool_history = []

while continue_reading:
    tools = []
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    for device in range(0, 32):
        multiplexed_nfc_reader = MultiplexedNFCReader(device)
        print "Reading device: " + str(device)
        for _ in range(5):
            if multiplexed_nfc_reader.has_tag():
                tag_uid = multiplexed_nfc_reader.read_NFC()
                if tag_uid.count("") > 0:
                    tools.append(tag_uid)
                # print "Card read " + str(device) + "! UID: "+ tag_uid
        multiplexed_nfc_reader.cleanup()
        tool_history.append({
            'timestamp': timestamp,
            'tools': tools
        })
        print "Tools found: " + ", ".join(map(str, set(tools)))
