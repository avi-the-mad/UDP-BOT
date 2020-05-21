#!/usr/bin/env python

from machine import Pin, PWM, ADC
from socket import *

# define sensor pins
# TODO: currently using LDR for sensing
LDR = ADC(0)

# define actuator pin
# TODO: currently using piezo for actuating
BUZZER = Pin(14)
buzz_freq = 50
freq_step = 5
MAX_FREQ = 1024
MIN_FREQ = 10

# define the sensor port in controller
controller_name = '192.168.0.48'
controller_sensor = 2500

# create socket for sending sensor data at port 1500
sensorPort = 1500
sensorSocket = socket(AF_INET, SOCK_DGRAM)
sensorSocket.bind(('', sensorPort))

# create a socket for recieving the control command
controlPort = 2000
controlSocket = socket(AF_INET, SOCK_DGRAM)
controlSocket.bind(('', controlPort))

# continuously stream sensor data, and recieve control data
while 1:
	beeper = PWM(BUZZER, freq=buzz_freq, duty=512)
	# read sensor data
	light = LDR.read()
	# send sensor data to sensor port of controller
	sensorSocket.sendto(bytes(str(light), 'ascii'), (controller_name, controller_sensor))
	# print ('data sent')
	ctrlCmd, controlAddress = controlSocket.recvfrom(2048)
	controlCommand = ctrlCmd.decode('ascii')
	bf = int(controlCommand)
	buzz_freq = bf
	'''
	if controlCommand!='empty':
		if (controlCommand=='w' and buzz_freq<MAX_FREQ):
			buzz_freq=buzz_freq+freq_step
			print('incrementing frequency: ', buzz_freq)

		elif (controlCommand == 's' and buzz_freq>MIN_FREQ):
			buzz_freq=buzz_freq-freq_step
			print('decrementing frequency: ', buzz_freq)

		if (buzz_freq>=MAX_FREQ):
			print ('Max frequency reached: ', buzz_freq)
			buzz_freq=1024
								

		if (buzz_freq<=MIN_FREQ):
			print ('Min frequency reached.')
			buzz_freq=4
	'''
