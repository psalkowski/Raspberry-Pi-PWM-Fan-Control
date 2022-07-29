#! /usr/bin/env python3

import pigpio
import time
import signal
import sys

pi = pigpio.pi()

PWM_FREQ = 25000        # 25kHZ

FAN_PIN = 18            #

WAIT_TIME = 1           # [s] time between refreshs

OFF_TEMP = 40           # [C] temp below fan off
MIN_TEMP = 45           # [C] temp above fan start
MAX_TEMP = 70           # [C] temp above fan at max
FAN_LOW = 20            # [%] fan speed
FAN_OFF = 0             # [%] fan speed
FAN_HIGH = 100          # [%] fan speed

FAN_GAIN = float(FAN_HIGH - FAN_LOW) / float(MAX_TEMP - MIN_TEMP)

def getCpuTemperature ():
        with open('/sys/class/thermal/thermal_zone0/temp') as f:
                return float(f.read()) / 1000

def controlFan(frequency):
        pi.hardware_PWM(FAN_PIN, PWM_FREQ, frequency )


def handleFanSpeed(temperature):
        if temperature >= MAX_TEMP:
                controlFan(FAN_HIGH * 10000)
        elif temperature >= MIN_TEMP:
                delta = temperature - MIN_TEMP
                fanspeed = int(FAN_LOW * 10000 + delta * FAN_GAIN * 10000)
                controlFan(fanspeed)
        elif temperature < OFF_TEMP:
                controlFan(FAN_OFF)

try:

        while True:
                handleFanSpeed(getCpuTemperature())
                time.sleep(WAIT_TIME)

except KeyboardInterrupt:
        controlFan(FAN_HIGH *  10000)
        pi.stop()
