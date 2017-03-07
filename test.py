#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

A0 = 3 # GPIO 2
A1 = 5 # GPIO 3
A2 = 7 # GPIO 4
A3 = 11 # GPIO 17
A4 = 13 # GPIO 27
A5 = 15 # GPIO 22

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(A0, GPIO.OUT)
GPIO.setup(A1, GPIO.OUT)
GPIO.setup(A2, GPIO.OUT)
GPIO.setup(A3, GPIO.OUT)
GPIO.setup(A4, GPIO.OUT)
GPIO.setup(A5, GPIO.OUT)

def select_device(device_number):
    a5_value = (device_number >> 5) & 1
    a4_value = (device_number >> 4) & 1
    a3_value = (device_number >> 3) & 1
    a2_value = (device_number >> 2) & 1
    a1_value = (device_number >> 1) & 1
    a0_value = device_number & 1
    GPIO.output(A0, a0_value)
    GPIO.output(A1, a1_value)
    GPIO.output(A2, a2_value)
    GPIO.output(A3, a3_value)
    GPIO.output(A4, a4_value)
    GPIO.output(A5, a5_value)

def loop():
    for device in range(0, 40):
        select_device(device)
        print "Selecting device: " + str(device)
        time.sleep(1)
