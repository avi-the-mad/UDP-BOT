#!/usr/bin/env python
'''
Author: Avinash D. J.

Script to open 2 UDP ports
	1. For sending the control data
	2. Recieving the sensor data
'''
import sys, termios, atexit
from socket import *
import time
import sys
import pyautogui as gui
from select import select

def kbhit():
	dr,dw,de = select([sys.stdin], [], [], 0)
	return dr <> []

# save the terminal settings
fd = sys.stdin.fileno()
new_term = termios.tcgetattr(fd)
old_term = termios.tcgetattr(fd)

# new terminal setting unbuffered
new_term[3] = (new_term[3] & ~termios.ICANON & ~termios.ECHO)

# switch to normal terminal
def set_normal_term():
    termios.tcsetattr(fd, termios.TCSAFLUSH, old_term)

# switch to unbuffered terminal
def set_curses_term():
    termios.tcsetattr(fd, termios.TCSAFLUSH, new_term)

def putch(ch):
    sys.stdout.write(ch)

def getch():
    return sys.stdin.read(1)

def getche():
    ch = getch()
    putch(ch)
    return ch

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

atexit.register(set_normal_term)
set_curses_term()

# continuously stream control data, and recieve sensor data
while 1:
	bef = time.time()
	# send control data to control port of bot
	# get the keystroke
	'''
	key_stroke = 'empty'
	if kbhit():
		key_stroke = getch()
		print ('Sending key: ', key_stroke)
		controlSocket.sendto(bytes(key_stroke), (BOT_name, BOT_control))
	else:
		controlSocket.sendto(bytes('empty'), (BOT_name, BOT_control))
	'''
	bf = 1080 - gui.position()[1]	
	controlSocket.sendto(bytes(bf), (BOT_name, BOT_control))
	# print ('sent control data')
	# recieve sensor data from sensor port
	message, sensorAddress = sensorSocket.recvfrom(2048)
	# print ('Sensor data as follows:')
	# print (message.decode('ascii'), 'from: ', sensorAddress)
	after = time.time()
	# print(after-bef)



