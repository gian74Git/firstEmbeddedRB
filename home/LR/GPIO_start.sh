#!/bin/bash
modprobe i2c-dev
cd /home/LR
nohup python /home/LR/LEDServer.py > /dev/null &
nohup python /home/LR/GPIOInt_FF.py > /dev/null &
nohup python /home/LR/GPIOInt_AUX.py > /dev/null &
nohup python /home/LR/GPIOInt_MESS.py > /dev/null &

