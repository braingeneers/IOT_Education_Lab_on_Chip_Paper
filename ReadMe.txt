Local IoT: Raspberry Pi 4
- Keep the python programs in the same folder. There are two files
	- local_IoT.py: The main program to read the json message sent by the remote IoT
	- RunScript_R1.py: This file contains the functions to decode the message and convert to I/O voltage levels
- Run the code "local_IoT.py"
	- When connected to the MQTT broker this will show message "in while loop"
	- Make sure to double check the Topic name.

Remote IoT: GUI 
- Upload the script "HW_Group_xx.txt" and the python program "remote_IoT.ipynb" at the same folder in the Braingeneers Wetai server
- Run the program "remote_IoT.ipynb" in Braingeneers wetai server
- Make sure to double check the Topic name. 	

