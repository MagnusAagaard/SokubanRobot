#!/usr/bin/env python3
from ev3dev.auto import *
#from ev3dev2.motor import OUTPUT_A, OUTPUT_D, MoveDifferential, SpeedRPM
#from ev3dev2.wheel import EV3Tire

import signal
from time import sleep

class LegoRobot:
	def __init__(self, solution):
		self._setup_sensors()
		self._setup_motors()
		self._setup_shutdowns()
#		self.white = 72
		self.black = 5
		self.solution = solution
		self.simplify()
		#Orientations: 1 = up, 2 = right, 3 = down, 4 = left
		self.robot_orientation = 4
		self.threshold_left = 35 #26
		self.threshold_right = 50 #36
		self.threshold = 25

	def _setup_sensors(self):
		self.mA = LargeMotor('outB')
		self.mD = LargeMotor('outC')
		#self.mdiff = MoveDifferential(OUTPUT_A, OUTPUT_D, EV3Tire, 82) #87 tidligere
		self.lightSensorCross = ColorSensor('in1')
		self.lightSensorCan = LightSensor('in2')
		self.lightSensorLine = ColorSensor('in4')
		assert self.lightSensorCross.connected, "lightSensorCross(ColorSensor) is not connected"
		assert self.lightSensorCan.connected, "lightSensorCan(ColorSensor) is not connected"
		assert self.lightSensorLine.connected, "lightSensorLine(ColorSensor) is not conected"
		self.BASE_SPEED = 40
		self.TURN_SPEED = 25

	def _setup_motors(self):
		self.mA.polarity = "normal"
		self.mD.polarity = "normal"
		self.mD.run_direct()
		self.mA.run_direct()
	
	def _setup_shutdowns(self):
		signal.signal(signal.SIGINT, self._signal_handler)

	def _signal_handler(self, sig, frame):
		#print('Shutting down gracefully')
		self.mA.duty_cycle_sp = 0
		self.mD.duty_cycle_sp = 0
		sleep(1)
		exit(0)

	def follow_line(self, sensor, count = 0):
		self.mD.duty_cycle_sp = self.BASE_SPEED
		self.mA.duty_cycle_sp = self.BASE_SPEED
		counter = count
		#self.sensorCross = self.lightSensorCross.value()
		#self.sensorLine = self.lightSensorLine.value()
		cross_detected = False
		#cross_left = not self.check_cross()
#		tic = time.perf_counter()
		while not cross_detected:
			self.sensorLine = self.lightSensorLine.value()
			#if not self.check_cross():
			#	cross_left=True
			#if cross_left:
			if counter > 50:
#				toc = time.perf_counter()
#				print("Time: {} seconds".format(toc-tic))
				if sensor == 1 or sensor == 3:
					self.sensorCross = self.lightSensorCross.value()
					cross_detected = self.check_cross()
				else:
					self.sensorCross = self.lightSensorCan.value()
					cross_detected = self.check_cross_can()
			else:
				counter += 1
			if sensor == 3:
				self.mD.duty_cycle_sp = - self.BASE_SPEED
				self.mA.duty_cycle_sp = - self.BASE_SPEED
			else:
				self.mD.duty_cycle_sp = self.BASE_SPEED - 0.25*(self.sensorLine-self.threshold)
				self.mA.duty_cycle_sp = self.BASE_SPEED + 0.25*(self.sensorLine-self.threshold)



#	def check_touch(self):
#		tou_val = self.touchSensor.value()
#		if tou_val:
#			print('Shutting down gracefully')
#			self.mA.duty_cycle_sp = 0
#			self.mD.duty_cycle_sp = 0
#			exit(0)

	def check_cross(self):
		if self.sensorCross < self.black + 25:
			print("Cross")
			return True
		else:
			return False

	def check_cross_can(self):
		if self.sensorCross < 400:
			print(self.sensorCross)
			return True
		else:
			return False

	#def go_straight(self, dist):
	#	self.mdiff.on_for_distance(self.TURN_SPEED, dist)
	#	self._setup_motors()

	#def turn_right(self):
	#	dist=self.straight_right
	#	self.go_straight(dist)
	#	self.mdiff.turn_right(self.TURN_SPEED, 90)
	#	self._setup_motors()

	def turn_right_new(self):
	#	dist=self.straight_right
	#	self.go_straight(dist)
		sleep(0.20)
		tic = time.perf_counter()
		toc = tic
		while (toc-tic)<0.7:
			self.mD.duty_cycle_sp = -self.TURN_SPEED
			self.mA.duty_cycle_sp = self.TURN_SPEED
			toc = time.perf_counter()
		while self.lightSensorLine.value()>self.threshold_right:
			sleep(0.01)
	#	sleep(0.03)

	def turn_left_new(self):
	#	dist=self.straight_right
	#	self.go_straight(dist)
	#	sleep(0.02)
		tic = time.perf_counter()
		toc = tic
		while (toc-tic)<0.7:
			self.mD.duty_cycle_sp = self.TURN_SPEED
			self.mA.duty_cycle_sp = -self.TURN_SPEED
			toc = time.perf_counter()
		while self.lightSensorLine.value()>self.threshold_left:
			sleep(0.01)
		sleep(0.13)
		print("does this fucking work")


	#def turn_left(self):
	#	dist=self.straight_left
	#	self.go_straight(dist)
	#	self.mdiff.turn_left(self.TURN_SPEED, 90)
	#	self._setup_motors()

	def turn_around(self):
		tic = time.perf_counter()
		toc = tic
		while (toc-tic)<0.55: #0.45 0.55
			#self.mD.duty_cycle_sp = -self.BASE_SPEED+30
			#self.mA.duty_cycle_sp = -self.BASE_SPEED-30
			self.mD.duty_cycle_sp = -50+23
			self.mA.duty_cycle_sp = -50-23
			toc = time.perf_counter()
		print("sleep done")
		tic = time.perf_counter()
		toc = tic
		while (toc-tic)<0.7:
			self.mD.duty_cycle_sp = self.TURN_SPEED
			self.mA.duty_cycle_sp = -self.TURN_SPEED
			toc = time.perf_counter()
		while self.lightSensorLine.value()>self.threshold_left:
			sleep(0.01)
		sleep(0.13)
		#self.mD.duty_cycle_sp = 40
		#self.mA.duty_cycle_sp = -40
		#sleep(0.4)
		#while self.lightSensorLine.value()>self.threshold:
		#	sleep(0.01)
		#sleep(0.4)
		#while self.lightSensorLine.value()>self.threshold:
		#	sleep(0.01)
	
	def move_can(self):
		self.BASE_SPEED=40
		self.follow_line(2)
		sleep(0.15)
		self.turn_around()
		#self.follow_line(3)
		#sleep(0.5)
		self.follow_line(1, 70)
	
	def solve(self):
		orientations = {'u': 1, 'r': 2, 'd': 3, 'l': 4, 'U': 1, 'R': 2, 'D': 3, 'L': 4}
		self.follow_line(1)
		i = 0
		for step in self.solution:
			#self.check_touch()
			desired_ori=orientations.get(step)
			ori_change = desired_ori - self.robot_orientation
			self.robot_orientation = desired_ori
			if i < len(self.solution)-1:
				if ord(self.solution[i+1]) == ord(step) or ord(self.solution[i+1]) == ord(step)-32:
					self.BASE_SPEED = 70
				#elif ord(self.solution[i-1])-32 == ord(step):
				#	self.BASE_SPEED = 70
				else:
					self.BASE_SPEED = 40
			i += 1
			if (ori_change == 1 or ori_change == -3):
				#print ("turning right")
				self.BASE_SPEED = 40
				self.turn_right_new()
				self.follow_line(1)
				#print(self.robot_orientation)
			elif (ori_change == 2 or ori_change == -2):
				#print("180 no scope")
				self.BASE_SPEED = 40
				self.turn_around()
				self.follow_line(1)
				#print(self.robot_orientation)
			elif (ori_change == -1 or ori_change == 3):
				#print("turning left")
				self.BASE_SPEED = 40
				self.turn_left_new()
				self.follow_line(1)
				#print(self.robot_orientation)
			else:
				#print("going straight")
				self.follow_line(1)
				#print(self.robot_orientation)
			if step == 'L' or step == 'U' or step == 'R' or step == 'D':
				#print("Move can")
				self.move_can()
				self.robot_orientation = (self.robot_orientation+2)%4
				#print(self.robot_orientation)
	
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
		#print(self.solution)




if __name__ == "__main__":
	count = 0
	#Hvis problemer, rens hjul og lad batteriet fuldt op
	#Spænding skal være 8.05V før det virker

	#Næste gang, lav vores straight om til at bruge noget andet til at køre frem. Enten sæt lys sensor ved aksen, eller lav med tid.
	#En lys sensor i midten i stedet for 2, og så bare ikke have sleep efter den drejer til venstre men kun når den drejer til højre
	lr = LegoRobot("llDlLLLulDrrrrrurrdLLLLLLLDrdLrdrrruUdldlluuurrurrrddLuLLLLulDDrddrrruUruLLLLulDulD")
#	lr = LegoRobot("ldruldruldruldruldruldruldruldruldruldruldruldruldruldr") #left test
#	lr = LegoRobot("rdlurdlurdlurdlurdlurdlurdlurdlurdlurdlurdlurdlurdlurdlu") #right test
#	lr = LegoRobot("lUddlluRRRRRdrUUruulldRRlddlluLuulldRurDDullDRdRRRdrUUruurrdLulDulldRddlllldlluRRRRRdrUUdlllluurDldRRRdrU") #Test map
	lr.solve()
	print('Shutting down gracefully')
	lr.mA.duty_cycle_sp = 0
	lr.mD.duty_cycle_sp = 0
	sleep(1)
	exit(0)
#	lr.follow_line(1)
#	lr.move_can()
#	lr.mA.duty_cycle_sp = 0
#	lr.mD.duty_cycle_sp = 0
#	sleep(1)
#	exit(0)
#	while True:
#		lr.follow_line(1)
#		lr.turn_around()
#		count += 1
#		print(count)
#		lr.check_touch()
#		lr.follow_line(1)
#		lr.turn_left_new()
#		lr.follow_line(1)
#		lr.turn_right_new()
#		lr.follow_line(1)
#		lr.turn_right_new()
#		lr.follow_line(1)
#		lr.turn_right_new()
#		lr.follow_line(1)
#		lr.turn_right_new()
#		lr.follow_line(1)
#		lr.turn_left_new()
#		lr.follow_line(1)
#		lr.turn_left_new()
#		lr.follow_line(1)
#		lr.turn_left_new()
#		print("Can")
#		print(lr.lightSensorCan.value())
#		print("Line")
#		print(lr.lightSensorLine.value())
#		lr.turn_left()

