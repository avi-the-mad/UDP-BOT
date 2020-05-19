#!/usr/bin/env python
'''
Author: Avinash D. J.

Script to open 2 UDP ports
	1. For sending the control data
	2. Recieving the sensor data
'''

from socket import *
import time
import getch

# define the control ports in BOT
# TODO
# change the botname to nodeMCU ip address
BOT_name = '192.168.0.23'
BOT_control = 2000

# create a socket for sending command at 3000
# since this acts as a server, we need to bind the port
controlPort = 3000
controlSocket = socket(AF_INET, SOCK_DGRAM)
controlSocket.bind(('', controlPort))

# create a socket for recieving command
sensorPort = 2500
sensorSocket = socket(AF_INET, SOCK_DGRAM)
sensorSocket.bind(('', sensorPort))

# continuously stream control data, and recieve sensor data
while 1:
	bef = time.time()
	# send control data to control port of bot
	# get the keystroke
	key_stroke = getch.getch()

	controlSocket.sendto(bytes(key_stroke, 'ascii'), (BOT_name, BOT_control))
	print ('sent control data')
	# recieve sensor data from sensor port
	message, sensorAddress = sensorSocket.recvfrom(2048)
	print ('Sensor data as follows:')
	print (message.decode('ascii'), 'from: ', sensorAddress)
	after = time.time()
	print(after-bef)
