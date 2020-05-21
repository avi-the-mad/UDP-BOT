#!/usr/bin/env python
'''
Author: Avinash D. J.

Script to open 2 UDP ports
	1. For sending the control data
	2. Recieving the sensor data
'''
from socket import *
import time
import sys
import cv2
import numpy as np


# define the control ports in BOT
# TODO
# change the botname to nodeMCU ip address

# Define input to the BOT
BOT = '192.168.0.23'
BOT_input_port = 2000

# Define output socket of controller
CTRL_output_port = 3000
CTRL_output_socket = socket(AF_INET, SOCK_DGRAM)
CTRL_output_socket.bind(('', CTRL_output_port))

# Define input socket of controller
CTRL_input_port = 2500
CTRL_input_socket = socket(AF_INET, SOCK_DGRAM)
CTRL_input_socket.bind(('', CTRL_input_port))
CTRL_input_socket.settimeout(1)


# define a video capture object
vid = cv2.VideoCapture(0)

# continuously stream control data, and recieve sensor data
while 1:
	t1 = time.time()

	# capture video frame using opencv
	ret, frame = vid.read()
	
	# compress the image to send it to MCU
	compressed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	compressed_frame = cv2.resize(compressed_frame, (160, 120))

	encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 30]
	result, encimg = cv2.imencode('.jpg', compressed_frame, encode_param)
	
	print ('compressed file size: ', sys.getsizeof(bytes(encimg)))
	'''
	# send it to BOT
	CTRL_output_socket.sendto(bytes(compressed_frame), (BOT, BOT_input_port))
	print ('sent')
	# recieve the same image back from the bot
	rec_frame, BOT_output_address = CTRL_input_socket.recvfrom(1024)
	print ('recieved')
	rec_frame = np.fromstring(rec_frame, np.uint8)
	rec_frame = rec_frame.reshape(6,8)
	# show image

	cv2.imshow('MyWebCam', cv2.resize(rec_frame, (400, 300)))
	'''
	decimg = cv2.imdecode(encimg, 1)
	cv2.imshow('MyWebCam', cv2.resize(decimg, (800, 600)))
	
	# controlSocket.sendto(bytes(bf), (BOT_name, BOT_control))
	# message, sensorAddress = sensorSocket.recvfrom(2048)

	t2 = time.time()

	print ("Round trip time: ", t2-t1, " seconds")

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break


