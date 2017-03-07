#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

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

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(A0, GPIO.OUT)
GPIO.setup(A1, GPIO.OUT)
GPIO.setup(A2, GPIO.OUT)
GPIO.setup(A3, GPIO.OUT)

for enable_pin in ENABLE_PINS:
    GPIO.setup(enable_pin, GPIO.out)

def select_device(device_number):
    a3_value = (device_number >> 3) & 1
    a2_value = (device_number >> 2) & 1
    a1_value = (device_number >> 1) & 1
    a0_value = device_number & 1
    GPIO.output(A0, a0_value)
    GPIO.output(A1, a1_value)
    GPIO.output(A2, a2_value)
    GPIO.output(A3, a3_value)

    chip_number = device_number / NO_OF_PINS_PER_CHIP

    for index, enable_pin in enumerate(ENABLE_PINS):
        value = int(chip_number == index)
        GPIO.output(enable_pin, value)

def loop():
    for device in range(0, 40):
        select_device(device)
        print "Selecting device: " + str(device)
        time.sleep(1)

loop()

GPIO.cleanup()
