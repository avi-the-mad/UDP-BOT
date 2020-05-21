#!/usr/bin/env python

'''
Version 2 of simple camera stream module

Split the image into 5 parts of 500 bytes each
send it over 5 ports
'''

from socket import *


# define the sensor port in controller
CTRL = '192.168.0.48'
CTRL_input_port_1 = 2500
CTRL_input_port_2 = 2501
CTRL_input_port_3 = 2502
CTRL_input_port_4 = 2503
CTRL_input_port_5 = 2504

# create socket for sending sensor data at port 1500
BOT_output_port_1 = 1500
BOT_output_port_2 = 1501
BOT_output_port_3 = 1502     
BOT_output_port_4 = 1503
BOT_output_port_5 = 1504 

BOT_output_socket_1 = socket(AF_INET, SOCK_DGRAM)
BOT_output_socket_2 = socket(AF_INET, SOCK_DGRAM)
BOT_output_socket_3 = socket(AF_INET, SOCK_DGRAM)
BOT_output_socket_4 = socket(AF_INET, SOCK_DGRAM)
BOT_output_socket_5 = socket(AF_INET, SOCK_DGRAM)

BOT_output_socket_1.bind(('', BOT_output_port_1))
BOT_output_socket_2.bind(('', BOT_output_port_2))
BOT_output_socket_3.bind(('', BOT_output_port_3))
BOT_output_socket_4.bind(('', BOT_output_port_4))
BOT_output_socket_5.bind(('', BOT_output_port_5))

# create a socket for recieving the control command
BOT_input_port_1 = 2000
BOT_input_port_2 = 2001
BOT_input_port_3 = 2002
BOT_input_port_4 = 2003
BOT_input_port_5 = 2004

BOT_input_socket_1 = socket(AF_INET, SOCK_DGRAM)
BOT_input_socket_2 = socket(AF_INET, SOCK_DGRAM)
BOT_input_socket_3 = socket(AF_INET, SOCK_DGRAM)
BOT_input_socket_4 = socket(AF_INET, SOCK_DGRAM)
BOT_input_socket_5 = socket(AF_INET, SOCK_DGRAM)

BOT_input_socket_1.bind(('', BOT_input_port_1))
BOT_input_socket_2.bind(('', BOT_input_port_2))
BOT_input_socket_3.bind(('', BOT_input_port_3))
BOT_input_socket_4.bind(('', BOT_input_port_4))
BOT_input_socket_5.bind(('', BOT_input_port_5))


print ("Feedback loop started...")
# continuously stream sensor data, and recieve control data
while 1:
	# Recieve inputs from the 5 input ports first.
	byteFrame_1, CTRL_address = BOT_input_socket_1.recvfrom(1024)
	byteFrame_2, CTRL_address = BOT_input_socket_2.recvfrom(1024)
	byteFrame_3, CTRL_address = BOT_input_socket_3.recvfrom(1024)
	byteFrame_4, CTRL_address = BOT_input_socket_4.recvfrom(1024)
	byteFrame_5, CTRL_address = BOT_input_socket_5.recvfrom(1024)

	print ('recived')
	BOT_output_socket_1.sendto(byteFrame_1, (CTRL, CTRL_input_port_1))
	BOT_output_socket_2.sendto(byteFrame_2, (CTRL, CTRL_input_port_2))
	BOT_output_socket_3.sendto(byteFrame_3, (CTRL, CTRL_input_port_3))
	BOT_output_socket_4.sendto(byteFrame_4, (CTRL, CTRL_input_port_4))
	BOT_output_socket_5.sendto(byteFrame_5, (CTRL, CTRL_input_port_5))

	print ('sent')
	
