#!/usr/bin/env python


from socket import *

# define the sensor port in controller
# TODO
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
	# send sensor data to sensor port of the controller
	sensorSocket.sendto(bytes('some sensor data', 'ascii'), (controller_name, controller_sensor))
	print ('sent the sensor data')
	# recieve control data to actuate the actuator
	ctrlCmd, controlAddress = controlSocket.recvfrom(2048)
	print ('Control command as follows:')
	print (ctrlCmd.decode('ascii'), 'from: ', controlAddress)
