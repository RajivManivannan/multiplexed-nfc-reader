#!/usr/bin/env python

import RPi.GPIO as GPIO
import MFRC522
import spidev

import json
import time
import signal

from uuid import uuid4

BLUETOOTH_FILE = "/tmp/bluetooth-zone-id.txt"
JSON_OUTPUT_FILE = "./src/output.json"
CART_ID_FILE = "./cart-id.txt"

def get_file_text(file_path):
    try:
        with open(file_path, "r") as file:
            return file.read()
    except IOError:
        return str(uuid4())

rack_id = get_file_text(CART_ID_FILE)

class MultiplexedNFCReader:
    A0 = 3 # GPIO 2
    A1 = 5 # GPIO 3
    A2 = 7 # GPIO 4
    A3 = 11 # GPIO 17
    A4 = 13 # GPIO 27
    A5 = 15 # GPIO 22

    def __init__(self, device_number):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(MultiplexedNFCReader.A0, GPIO.OUT)
        GPIO.setup(MultiplexedNFCReader.A1, GPIO.OUT)
        GPIO.setup(MultiplexedNFCReader.A2, GPIO.OUT)
        GPIO.setup(MultiplexedNFCReader.A3, GPIO.OUT)
        GPIO.setup(MultiplexedNFCReader.A4, GPIO.OUT)
        GPIO.setup(MultiplexedNFCReader.A5, GPIO.OUT)
        self.select_device(device_number)
        self.mfrfc_reader = MFRC522.MFRC522()

    def select_device(self, device_number):
        a5_value = (device_number >> 5) & 1
        a4_value = (device_number >> 4) & 1
        a3_value = (device_number >> 3) & 1
        a2_value = (device_number >> 2) & 1
        a1_value = (device_number >> 1) & 1
        a0_value = device_number & 1

        GPIO.output(MultiplexedNFCReader.A0, a0_value)
        GPIO.output(MultiplexedNFCReader.A1, a1_value)
        GPIO.output(MultiplexedNFCReader.A2, a2_value)
        GPIO.output(MultiplexedNFCReader.A3, a3_value)
        GPIO.output(MultiplexedNFCReader.A4, a4_value)
        GPIO.output(MultiplexedNFCReader.A5, a5_value)

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
    return get_file_text(BLUETOOTH_FILE)

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
                    tag_uid = multiplexed_nfc_reader.read_NFC().replace(",", "-")
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
