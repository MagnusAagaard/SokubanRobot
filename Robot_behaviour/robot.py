#!/usr/bin/env python3

from ev3dev.auto import *
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, MoveDifferential, SpeedRPM
from ev3dev2.wheel import EV3Tire

import signal
from time import sleep

class LegoRobot:
	def __init__(self, solution):
		self._setup_sensors()
		self._setup_motors()
		self._setup_shutdowns()
		self.white = 72
		self.black = 5
		self.solution = solution
		self.simplify()
		#Orientations: 1 = up, 2 = right, 3 = down, 4 = left
		self.robot_orientation = 1
		self.straight_left = 20 #26
		self.straight_right = 30 #36
		self.threshold = (self.white-self.black)/2-5

	def _setup_sensors(self):
		self.mA = LargeMotor('outA')
		self.mD = LargeMotor('outD')
		self.mdiff = MoveDifferential(OUTPUT_A, OUTPUT_D, EV3Tire, 82) #87 tidligere
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
		self.sensorLeft = self.lightSensorLeft.value()
		self.sensorRight = self.lightSensorRight.value()
		cross_detected = False
		cross_left = not self.check_cross()
		while not cross_detected:
			#self.check_touch()
			self.sensorLeft = self.lightSensorLeft.value()
			self.sensorRight = self.lightSensorRight.value()
			if not self.check_cross():
				cross_left=True
			if cross_left:
				cross_detected = self.check_cross()
			self.mD.duty_cycle_sp = self.BASE_SPEED - 0.20*(self.sensorLeft-self.threshold)
			self.mA.duty_cycle_sp = self.BASE_SPEED + 0.20*(self.sensorLeft-self.threshold)


	def check_touch(self):
		tou_val = self.touchSensor.value()
		if tou_val:
			print('Shutting down gracefully')
			self.mA.duty_cycle_sp = 0
			self.mD.duty_cycle_sp = 0
			exit(0)

	def check_cross(self):
		if self.sensorRight < self.black + 25 and self.sensorLeft < self.black + 25:
			return True
		else:
			return False

	def go_straight(self, dist):
		self.mdiff.on_for_distance(self.TURN_SPEED, dist)
		self._setup_motors()

	def turn_right(self):
		dist=self.straight_right
		self.go_straight(dist)
		self.mdiff.turn_right(self.TURN_SPEED, 90)
		self._setup_motors()

	def turn_right_new(self):
		dist=self.straight_right
		self.go_straight(dist)
		self.mD.duty_cycle_sp = -40
		self.mA.duty_cycle_sp = 40
		sleep(0.4)
		while self.lightSensorRight.value()>self.threshold:
			sleep(0.01)
		sleep(0.03)

	def turn_left_new(self):
		dist=self.straight_right
		self.go_straight(dist)
		self.mD.duty_cycle_sp = 40
		self.mA.duty_cycle_sp = -40
		sleep(0.4)
		while self.lightSensorLeft.value()>self.threshold+10:
			sleep(0.01)
		sleep(0.03)


	def turn_left(self):
		dist=self.straight_left
		self.go_straight(dist)
		self.mdiff.turn_left(self.TURN_SPEED, 90)
		self._setup_motors()

	def turn_around(self):
		self.mD.duty_cycle_sp = 40
		self.mA.duty_cycle_sp = -40
		sleep(0.4)
		while self.lightSensorLeft.value()>self.threshold:
			sleep(0.01)
		sleep(0.03)
		sleep(0.4)
		while self.lightSensorLeft.value()>self.threshold:
			sleep(0.01)
		sleep(0.03)
	
	def move_can(self):
		self.go_straight(195)
		self.go_straight(-195)
	
	def solve(self):
		orientations = {'u': 1, 'r': 2, 'd': 3, 'l': 4, 'U': 1, 'R': 2, 'D': 3, 'L': 4}
		self.follow_line()
		for step in self.solution:
			self.check_touch()
			desired_ori=orientations.get(step)
			ori_change = desired_ori - self.robot_orientation
			self.robot_orientation = desired_ori
			if (ori_change == 1 or ori_change == -3):
				self.turn_right_new()
				self.follow_line()
				print ("turning right")
			elif (ori_change == 2 or ori_change == -2):
				self.turn_around()
				self.follow_line()
				print("180 no scope")
			elif (ori_change == -1 or ori_change == 3):
				self.turn_left_new()
				self.follow_line()
				print("turning left")
			else:
				self.follow_line()
				print("going straight")
			if step == 'L' or step == 'U' or step == 'R' or step == 'D':
				self.move_can() 
	
	def simplify(self):
		for i in range(len(self.solution)-1):
			if (self.solution[i] == self.solution[i+1]):
				char = self.solution[i]
				if char == "R":
					self.solution = self.solution[:i] + self.solution[i:i+1].replace("R", "r") + self.solution[i+1:]
				elif char == "U":
					self.solution = self.solution[:i] + self.solution[i:i+1].replace("U", "u") + self.solution[i+1:]
				elif char == "L":
					self.solution = self.solution[:i] + self.solution[i:i+1].replace("L", "l") + self.solution[i+1:]
				elif char == "D":
					self.solution = self.solution[:i] + self.solution[i:i+1].replace("D", "d") + self.solution[i+1:]
		print(self.solution)




if __name__ == "__main__":
	#Hvis problemer, rens hjul og lad batteriet fuldt op

	#Næste gang, lav vores straight om til at bruge noget andet til at køre frem. Enten sæt lys sensor ved aksen, eller lav med tid.
	lr = LegoRobot("llllUddlluRRRRRdrUUruulldRRlddlluLuulldRurDDullDRdRRRdrUUruurrdLulDulldRddlllldlluRRRRRdrUUdlllluurDldRRRdrU")
#	lr = LegoRobot("uldruldruldruldruldruldruldruldruldruldruldruldruldruldr") #left test
#	lr = LegoRobot("rdlurdlurdlurdlurdlurdlurdlurdlurdlurdlurdlurdlurdlurdlu") #right test
	lr.solve()
	print('Shutting down gracefully')
	lr.mA.duty_cycle_sp = 0
	lr.mD.duty_cycle_sp = 0
	exit(0)
#	lr.turn_right_new()
#	while True:
#		lr.check_touch()
#		lr.follow_line()
#		print("Left")
#		print(lr.lightSensorLeft.value())
#		print("right")
#		print(lr.lightSensorRight.value())
#		lr.turn_left()

