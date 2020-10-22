#!/usr/bin/env python3

from ev3dev.auto import *
from time import sleep
from ev3dev2.sound import Sound
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, MoveDifferential, SpeedRPM
from ev3dev2.wheel import EV3Tire
#from pybricks.robotics import DriveBase

import signal

sound = Sound()
#sound.speak('Welcome to the hunger games')

mA = LargeMotor('outA')
mD = LargeMotor('outD')
mdiff = MoveDifferential(OUTPUT_A, OUTPUT_D, EV3Tire, 111)
#mdiff.turn_right(SpeedRPM(40), 90)

TouchSensor = TouchSensor('in3')

#THRESHOLD_LEFT = 30 
#THRESHOLD_RIGHT = 350

BASE_SPEED = 50

lightSensorLeft = ColorSensor('in1')
lightSensorRight = ColorSensor('in4') 

assert lightSensorLeft.connected, "LightSensorLeft(ColorSensor) is not connected"
assert lightSensorRight.connected, "LightSensorRight(ColorSensor) is not conected"
assert TouchSensor.connected, "Touch sensor is not connected"

mD.run_direct()
mA.run_direct()


mA.polarity = "normal"
mD.polarity = "normal"

def signal_handler(sig, frame):
	print('Shutting down gracefully')
	mA.duty_cycle_sp = 0
	mB.duty_cycle_sp = 0

	exit(0)

signal.signal(signal.SIGINT, signal_handler)
#print('Press Ctrl+C to exit')
#robot.straight(50)
white = 76
black = 5
counter = 0


while True:
	sensorLeft = lightSensorLeft.value()
	sensorRight = lightSensorRight.value()
	Threshold = (white-black)/2


	mD.duty_cycle_sp = BASE_SPEED - (sensorLeft-Threshold)*0.1
	mA.duty_cycle_sp = BASE_SPEED + 0.1*(sensorLeft-Threshold)

	

	tou_val = TouchSensor.value()
	#print("Touch sensor value: ", tou_val)
	if tou_val:
		print('Shutting down gracefully')
		mA.duty_cycle_sp = 0
		mB.duty_cycle_sp = 0
		exit(0)
	print("sensorLeft: ", sensorLeft, " sensorRight: ", sensorRight)
	#if sensorRight < THRESHOLD_RIGHT:
	#	mA.duty_cycle_sp = TURN_SPEED
	#else:
	#	mA.duty_cycle_sp = BASE_SPEED
	

	#if sensorLeft < THRESHOLD_LEFT:
	#	mB.duty_cycle_sp = TURN_SPEED
	#else:
	#	mB.duty_cycle_sp = BASE_SPEED

