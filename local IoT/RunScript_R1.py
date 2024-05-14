import time
import os
import logging
from turtle import end_fill
import RPi.GPIO as GPIO
from time import sleep

## change made on 8/14/2022 by MJNS 
#start
from braingeneers.iot import messaging
import uuid
#end


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

delay_period = 0.01

switch = True
# 3/2 - added all pins (16)
channel_num = 16
# the list indices (0~15) are according to the valve indices (1~16)
channel_pin = [11,13,15,16,18,12,22,29,40,38,36,32,37,35,33,31]


#defines


#run commands
def action(command):
  command_type = command[0]
  command_param = command[1:-1]
  if command_type == 'o':
    print("open " + command_param)
    GPIO.output(channel_pin[int(command_param)-1], GPIO.HIGH)
  elif command_type == 'c':
    print("close " + command_param)
    GPIO.output(channel_pin[int(command_param)-1], GPIO.LOW)
  elif command_type == 'w':
    print("wait " + command_param)
    time.sleep(float(int(command_param))/1000)
  else:
    print("invalid command type")

#(recursively) read and run functions
#in future if there is performance issue, this code can be optimized by locating
#  the function bodies first so we don't have to find start and end points every
#  time.
def run_function(items):
 #print(items) #show func params(debug purpose)
  iteration = 1 #by default it runs once.
  if len(items) > 2:
    iteration = int(items[2])
 #find where the function starts and ends
  for i, func_line in enumerate(file_lines):
    if func_line[0:-1] == items[1]: #items[1] = function name
      start_line = i
   #print(items[1])
   #print(str(i))
      for i, func_line in enumerate(file_lines[start_line:]):
        if func_line[0:3] == "end":
          end_line = i + start_line
          break
      break
 #function start executing here
  funclines = file_lines[start_line+1:end_line] #does not include the function name
  #function iteration:
  for i in range(iteration):
    print("instance " + str(i+1) + " of function " + items[1])
    for command in funclines:
   #if it calls a function
      if command[0:4] == "call":
        run_function(command.split())
   #else it must be a command
      else:
        action(command)
 #print(funclines) #show funclines (debug purpose)

#run main til end
def run_main(content):
  for i, lines in enumerate(content):  
    if lines == "main\n":
      start = i
  global file_lines
  file_lines = content
  print("starting main")
  for main_line in file_lines[start+1:]:
    if main_line == "end\n": #end of the main
      print("end of main")
      break;
    elif main_line[0:4] == "call": # go to function
      items = main_line.split()
      run_function(items)
      pass
    else:
      action(main_line)


#start here
def run_script(script_name):
 print("Start executing" + script_name)
 filename = script_name
 file = open(filename)
 file_content = file.readlines()
 file.close()
 run_main(file_content)


