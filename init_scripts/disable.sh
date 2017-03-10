#!/usr/bin/env bash

sudo systemctl stop smart-crib.service
sudo systemctl disable smart-crib.service

sudo systemctl stop nfc-reader.service
sudo systemctl disable nfc-reader.service
