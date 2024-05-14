from braingeneers.iot import messaging
import uuid

#start
import time
import os
import logging
import json
import datetime
import RPi.GPIO as GPIO
from time import sleep

#import our decoder functions
from RunScript_R1 import run_script
from RunScript_R1 import run_main

# RPi 4 and 3B+ has same GPIO 
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
# valves 1-4
GPIO.setup(11, GPIO.OUT)
GPIO.output(11, GPIO.LOW)
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, GPIO.LOW)
GPIO.setup(15, GPIO.OUT)
GPIO.output(15, GPIO.LOW)
GPIO.setup(16, GPIO.OUT)
GPIO.output(16, GPIO.LOW)
# valves 5-8
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, GPIO.LOW)
GPIO.setup(12, GPIO.OUT)
GPIO.output(12, GPIO.LOW)
GPIO.setup(22, GPIO.OUT)
GPIO.output(22, GPIO.LOW)
GPIO.setup(29, GPIO.OUT)
GPIO.output(29, GPIO.LOW)
#valves 9-12
GPIO.setup(31, GPIO.OUT)
GPIO.output(31, GPIO.LOW)
GPIO.setup(33, GPIO.OUT)
GPIO.output(33, GPIO.LOW)
GPIO.setup(35, GPIO.OUT)
GPIO.output(35, GPIO.LOW)
GPIO.setup(37, GPIO.OUT)
GPIO.output(37, GPIO.LOW)
#valves 13-16
GPIO.setup(32, GPIO.OUT)
GPIO.output(32, GPIO.LOW)
GPIO.setup(36, GPIO.OUT)
GPIO.output(36, GPIO.LOW)
GPIO.setup(38, GPIO.OUT)
GPIO.output(38, GPIO.LOW)
GPIO.setup(40, GPIO.OUT)
GPIO.output(40, GPIO.LOW)

#mode defines here (maybe dictionary or enumate in the future)
MANUAL=1
SAVED_SCRIPTS=2
REMOTE_SCRIPTS=3
EXIT = 0

#script name dict
script_names = {
 1:"Dummy.txt",
 2:"Dummy2.txt",
 3:"TestAll.txt"
}

# added all pins (16)
channel_num = 16
# the list indices (0~15) are according to the valve indices (1~16)
channel_pin = [11,13,15,16,18,12,22,29,40,38,36,32,37,35,33,31]

# When the mode is MANUAL, this function will be called. It changes status of
#	the pins according to the manual commands
def manual_control(param):
        i = 0;
        for channels in range(channel_num):
                if ((param>>((channel_num-1)-i))&1) >0:
                        GPIO.output(channel_pin[i], GPIO.HIGH)
                else:
                        GPIO.output(channel_pin[i], GPIO.LOW)
                i+=1

# When the mode is SAVED_SCRIPTS, this function will be called.
#	It runs one of the saved scripts
def saved_scripts(param):
	print("running script "+ script_names[param])
	run_script("saved_scripts/" + script_names[param])

# When the mode is REMOTE_SCRIPTS, this function will be called.
#	It executes the script's command sent remotely
#	and saves a copy in the history folder
def remote_scripts(param):
	print("Running remote script")
	param_list = json.loads(param)
	print(type(param_list), param_list)
	run_main(param_list)
	current_time = datetime.datetime.now()
	filename ="history/"+ str(current_time)+".txt" #This is where we name the history file
	history = open(filename, "w")
	for lines in param_list:
		history.write(lines)
	print("script saved in " + filename)

#When the mode is EXIT, this function exits the subscriber loop
def exit_subscriber():
	print("Ending subscriber")
	os._exit(0)

# this is for reding message structure from the Json
def read_msg_struct(message):
	print("Message: ", message)
	mode = message['mode']
	param = message['param']

	print(mode)

	if (mode == MANUAL):
		manual_control(param)
	elif (mode == SAVED_SCRIPTS):
		saved_scripts(param)
	elif (mode == REMOTE_SCRIPTS):
		remote_scripts(param)
	elif (mode == EXIT):
		exit_subscriber()
	else:
		print("Tick the manual box!!")
#end

#### Please check the topic name #######
if __name__ == '__main__':
	mb = messaging.MessageBroker(str(uuid.uuid4))
	q=messaging.CallableQueue()
	mb.subscribe_message( topic="Sampad_Device", callback=q )
	while True:
		received_message = q.get()
		read_msg_struct(received_message[1])
		print("in while loop")
	device.end();
	GPIO.cleanup()
