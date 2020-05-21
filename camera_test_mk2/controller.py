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
BOT_input_port_1 = 2000
BOT_input_port_2 = 2001
BOT_input_port_3 = 2002
BOT_input_port_4 = 2003
BOT_input_port_5 = 2004


# Define output socket of controller
CTRL_output_port_1 = 3000
CTRL_output_port_2 = 3001
CTRL_output_port_3 = 3002
CTRL_output_port_4 = 3003
CTRL_output_port_5 = 3004

CTRL_output_socket_1 = socket(AF_INET, SOCK_DGRAM)
CTRL_output_socket_2 = socket(AF_INET, SOCK_DGRAM)
CTRL_output_socket_3 = socket(AF_INET, SOCK_DGRAM)
CTRL_output_socket_4 = socket(AF_INET, SOCK_DGRAM)
CTRL_output_socket_5 = socket(AF_INET, SOCK_DGRAM)

CTRL_output_socket_1.bind(('', CTRL_output_port_1))
CTRL_output_socket_2.bind(('', CTRL_output_port_2))
CTRL_output_socket_3.bind(('', CTRL_output_port_3))
CTRL_output_socket_4.bind(('', CTRL_output_port_4))
CTRL_output_socket_5.bind(('', CTRL_output_port_5))


# Define input socket of controller
CTRL_input_port_1 = 2500
CTRL_input_port_2 = 2501
CTRL_input_port_3 = 2502
CTRL_input_port_4 = 2503
CTRL_input_port_5 = 2504

CTRL_input_socket_1 = socket(AF_INET, SOCK_DGRAM)
CTRL_input_socket_2 = socket(AF_INET, SOCK_DGRAM)
CTRL_input_socket_3 = socket(AF_INET, SOCK_DGRAM)
CTRL_input_socket_4 = socket(AF_INET, SOCK_DGRAM)
CTRL_input_socket_5 = socket(AF_INET, SOCK_DGRAM)

CTRL_input_socket_1.bind(('', CTRL_input_port_1))
CTRL_input_socket_2.bind(('', CTRL_input_port_2))
CTRL_input_socket_3.bind(('', CTRL_input_port_3))
CTRL_input_socket_4.bind(('', CTRL_input_port_4))
CTRL_input_socket_5.bind(('', CTRL_input_port_5))

# define a video capture object
vid = cv2.VideoCapture(0)

'''
Utility function to split the bytes array into n chunks
'''
def split_bytes(bytes_array, chunk_size):
	for i in range(0,len(bytes_array), chunk_size):
		yield bytes_array[i:i+chunk_size] 
def combine_bytes(bytes_list):
	comb = b''
	for b in bytes_list:
		comb = comb + b
	return comb
# continuously stream control data, and recieve sensor data
while 1:
	t1 = time.time()

	# capture video frame using opencv
	ret, frame = vid.read()
	
	# compress the image to send it to MCU
	compressed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	compressed_frame = cv2.resize(compressed_frame, (160, 120))

	encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
	result, encimg = cv2.imencode('.jpg', compressed_frame, encode_param)
	
	print ('compressed file size: ', sys.getsizeof(bytes(encimg)))

	# split the encoded image into 5 chunks for now
	encimg_chunks = list(split_bytes(bytes(encimg), 600))

	print ("Number of chunks: ", len(encimg_chunks))
	for chunk in encimg_chunks:
		print ("Chunk size: ", sys.getsizeof(chunk))

	
	# send it to BOT
	CTRL_output_socket_1.sendto(bytes(encimg_chunks[0]), (BOT, BOT_input_port_1))
	CTRL_output_socket_2.sendto(bytes(encimg_chunks[1]), (BOT, BOT_input_port_2))
	CTRL_output_socket_3.sendto(bytes(encimg_chunks[2]), (BOT, BOT_input_port_3))
	CTRL_output_socket_4.sendto(bytes(encimg_chunks[3]), (BOT, BOT_input_port_4))
	CTRL_output_socket_5.sendto(bytes(encimg_chunks[4]), (BOT, BOT_input_port_5))

	print ('sent all 5 chunks to the bot')
	# recieve the same image back from the bot
	rec_frame_1, BOT_output_address = CTRL_input_socket_1.recvfrom(1024)
	rec_frame_2, BOT_output_address = CTRL_input_socket_2.recvfrom(1024)
	rec_frame_3, BOT_output_address = CTRL_input_socket_3.recvfrom(1024)
	rec_frame_4, BOT_output_address = CTRL_input_socket_4.recvfrom(1024)
	rec_frame_5, BOT_output_address = CTRL_input_socket_5.recvfrom(1024)

	rec_frame = [rec_frame_1, rec_frame_2, rec_frame_3, rec_frame_4, rec_frame_5]
	rec_frame = combine_bytes(rec_frame) 
	print ('recieved and combined all chunks')
	rec_frame = np.fromstring(rec_frame, np.uint8)
	# show image

	cv2.imshow('MyWebCam', cv2.resize(rec_frame, (400, 300)))

	decimg = cv2.imdecode(encimg, 1)
	cv2.imshow('MyWebCam', cv2.resize(decimg, (800, 600)))
	
	# controlSocket.sendto(bytes(bf), (BOT_name, BOT_control))
	# message, sensorAddress = sensorSocket.recvfrom(2048)

	t2 = time.time()

	print ("Round trip time: ", t2-t1, " seconds")

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break


