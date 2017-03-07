#!/usr/bin/env bash

rm -f /tmp/bluetooth-zone-id.txt
./multiplexed_nfc_reader.py &
cd src && npm start
