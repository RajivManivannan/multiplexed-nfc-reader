#!/usr/bin/env bash

rm -f /tmp/bluetooth-zone-id.txt
./ibeacon_scan.sh | ./bluetooth.rb &
./multiplexed_nfc_reader.py
