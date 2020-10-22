#!/usr/bin/env python3

from ev3dev.auto import *
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, MoveDifferential, SpeedRPM
from ev3dev2.wheel import EV3Tire

import signal

class LegoRobot:
	def __init__(self, solution):
		self._setup_sensors()
		self._setup_motors()
		self._setup_shutdowns()
		self.white = 76
		self.black = 5
		self.solution = solution
		#Orientations: 1 = up, 2 = right, 3 = down, 4 = left
		self.robot_orientation = 1

	def _setup_sensors(self):
		self.mA = LargeMotor('outA')
		self.mD = LargeMotor('outD')
		self.mdiff = MoveDifferential(OUTPUT_A, OUTPUT_D, EV3Tire, 87)
		self.touchSensor = TouchSensor('in3')
		self.lightSensorLeft = ColorSensor('in1')
		self.lightSensorRight = ColorSensor('in4')
		assert self.lightSensorLeft.connected, "LightSensorLeft(ColorSensor) is not connected"
		assert self.lightSensorRight.connected, "LightSensorRight(ColorSensor) is not conected"
		assert self.touchSensor.connected, "Touch sensor is not connected"
		self.BASE_SPEED = 50
		self.TURN_SPEED = 25

	def _setup_motors(self):
		self.mA.polarity = "normal"
		self.mD.polarity = "normal"
		self.mD.run_direct()
		self.mA.run_direct()
	
	def _setup_shutdowns(self):
		signal.signal(signal.SIGINT, self._signal_handler)

	def _signal_handler(self, sig, frame):
		print('Shutting down gracefully')
		self.mA.duty_cycle_sp = 0
		self.mD.duty_cycle_sp = 0
		exit(0)

	def follow_line(self):
		sensorLeft = self.lightSensorLeft.value()
		sensorRight = self.lightSensorRight.value()
		threshold = (self.white-self.black)/2

		self.mD.duty_cycle_sp = self.BASE_SPEED - 0.2*(sensorLeft-threshold)
		self.mA.duty_cycle_sp = self.BASE_SPEED + 0.2*(sensorLeft-threshold)


	def check_touch(self):
		tou_val = self.touchSensor.value()
		if tou_val:
			print('Shutting down gracefully')
			self.mA.duty_cycle_sp = 0
			self.mD.duty_cycle_sp = 0
			exit(0)

	def check_cross(self):
		sensorLeft = self.lightSensorLeft.value()
		sensorRight = self.lightSensorRight.value()
		if sensorLeft < self.black + 10 and sensorRight < self.black + 10:
			return True
		else:
			return False

	def go_straight(self, dist):
		self.mdiff.on_for_distance(self.TURN_SPEED, dist)
		self._setup_motors()

	def turn_right(self):
		self.go_straight(29)
		self.mdiff.turn_right(self.TURN_SPEED, 90)
		self._setup_motors()

	def turn_left(self):
		self.go_straight(35)
		self.mdiff.turn_left(self.TURN_SPEED, 90)
		self._setup_motors()

	def turn_around(self):
		self.mdiff.turn_left(self.TURN_SPEED, 180)
		self._setup_motors()

if __name__ == "__main__":
	lr = LegoRobot("Sol")
	cross_detected = False
	cross_detected2 = False
	while True:
		lr.check_touch()
		lr.follow_line()
		cross_detected = lr.check_cross()
		if cross_detected:
			lr.go_straight(-280)
			#lr.turn_around()
			while True:
				lr.check_touch()
				lr.follow_line()
				cross_detected2 = lr.check_cross()
				if cross_detected2:
					lr.turn_left()

