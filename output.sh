#!/usr/bin/env bash

./ibeacon_scan.sh | ./bluetooth.rb &
./multiplexed_nfc_reader.py
