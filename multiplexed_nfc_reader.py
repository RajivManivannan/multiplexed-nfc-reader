#!/usr/bin/env python

import RPi.GPIO as GPIO
import MFRC522
import spidev

import json
import time
import signal

from uuid import uuid4

FILE_TO_WRITE = "/tmp/bluetooth-zone-id.txt"
JSON_OUTPUT_FILE = "./src/output.json"

rack_id = str(uuid4())

class MultiplexedNFCReader:
    NO_OF_PINS_PER_CHIP = 16
    TOTAL_PINS = 48

    A0 = 31 # GPIO 6
    A1 = 33 # GPIO 13
    A2 = 35 # GPIO 19
    A3 = 37 # GPIO 26

    ENABLE_PINS = [
        40, # GPIO 21 -> Chip 0
        38, # GPIO 20 -> Chip 1
        36, # GPIO 16 -> Chip 2
    ]

    def __init__(self, device_number):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(MultiplexedNFCReader.A0, GPIO.OUT)
        GPIO.setup(MultiplexedNFCReader.A1, GPIO.OUT)
        GPIO.setup(MultiplexedNFCReader.A2, GPIO.OUT)
        GPIO.setup(MultiplexedNFCReader.A3, GPIO.OUT)

        for enable_pin in MultiplexedNFCReader.ENABLE_PINS:
            GPIO.setup(enable_pin, GPIO.out)

        self.select_device(device_number)
        self.mfrfc_reader = MFRC522.MFRC522()

    def select_device(self, device_number):
        a3_value = (device_number >> 3) & 1
        a2_value = (device_number >> 2) & 1
        a1_value = (device_number >> 1) & 1
        a0_value = device_number & 1

        GPIO.output(MultiplexedNFCReader.A0, a0_value)
        GPIO.output(MultiplexedNFCReader.A1, a1_value)
        GPIO.output(MultiplexedNFCReader.A2, a2_value)
        GPIO.output(MultiplexedNFCReader.A3, a3_value)

        chip_number = device_number / MultiplexedNFCReader.NO_OF_PINS_PER_CHIP

        for index, enable_pin in enumerate(MultiplexedNFCReader.ENABLE_PINS):
            value = int(chip_number == index)
            GPIO.output(enable_pin, value)


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

def get_zone_uuid():
    try:
        with open(FILE_TO_WRITE, "r") as file:
            return file.read()
    except IOError:
        return ""

def save_as_json(output):
    try:
        with open(JSON_OUTPUT_FILE, 'w') as outfile:
            json.dump(output, outfile)
    except IOError:
        print "Unable to save as json!!! :("

def main():
    while continue_reading:
        tag_ids = []

        timestamp = int(time.time())
        zone_id = get_zone_uuid()

        for device in range(0, 40):
            multiplexed_nfc_reader = MultiplexedNFCReader(device)
            for _ in range(5):
                if multiplexed_nfc_reader.has_tag():
                    tag_uid = multiplexed_nfc_reader.read_NFC()
                    print "Device " + str(device) + " -> Tag: " + tag_uid
                    if tag_uid.count("") > 0:
                        tag_ids.append(tag_uid)
            multiplexed_nfc_reader.cleanup()

        save_as_json({
            "rackID": rack_id,
            "tags": map(str, set(tag_ids)),
            "zoneUUID": zone_id,
            "timestamp": timestamp
        })

        print "Tag ids found: " + ", ".join(map(str, set(tag_ids)))
        print "Near: " + zone_id

if __name__ == "__main__":
    main()
