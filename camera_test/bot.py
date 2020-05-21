#!/usr/bin/env python

'''
Simple program to send whatever is recieved
'''

from socket import *


# define the sensor port in controller
CTRL = '192.168.0.48'
CTRL_input_port = 2500

# create socket for sending sensor data at port 1500
BOT_output_port = 1500
BOT_output_socket = socket(AF_INET, SOCK_DGRAM)
BOT_output_socket.bind(('', BOT_output_port))

# create a socket for recieving the control command
BOT_input_port = 2000
BOT_input_socket = socket(AF_INET, SOCK_DGRAM)
BOT_input_socket.bind(('', BOT_input_port))

print ("Feedback loop started...")
# continuously stream sensor data, and recieve control data
while 1:
	byteFrame, CTRL_address = BOT_input_socket.recvfrom(1024)
	print ('recived')
	BOT_output_socket.sendto(byteFrame, (CTRL, CTRL_input_port))
	print ('sent')
	
