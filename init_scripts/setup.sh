#!/usr/bin/env bash

# sudo cp ./etc/systemd/system/nearest-beacon.service /etc/systemd/system/nearest-beacon.service
# sudo systemctl enable nearest-beacon.service
# sudo systemctl start nearest-beacon.service
# sudo systemctl status nearest-beacon.service

sudo cp ./etc/systemd/system/nfc-reader.service /etc/systemd/system/nfc-reader.service
sudo systemctl enable nfc-reader.service
sudo systemctl start nfc-reader.service
sudo systemctl status nfc-reader.service

sudo cp ./etc/systemd/system/smart-crib.service /etc/systemd/system/smart-crib.service
sudo systemctl enable smart-crib.service
sudo systemctl start smart-crib.service
sudo systemctl status smart-crib.service
