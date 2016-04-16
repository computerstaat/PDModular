import socket
import sys
import os

SERVERPORT =8666
HELLOMESSAGE = ?
FILEFINISHED = ?

# 8) Now we need to tell the RPi to launch our script at start-up. To do this we have to edit a file called “rc.local”. Open it in the nano editor with :
# sudo nano /etc/rc.local
# 9) Add the following line after the first comments (comments start with a #) :
# /home/pi/bin/script_pd


HOSTNAME = "conductor"
LOAD = "1"

PUREDATA = "/Applications/Pd-extended.app/Contents/MacOS/Pd-extended"
PATCHES = "~/Synthesizer/patches/"

maxVoices = 3

def syncFile(address):
	os.system("rsync -avrz /opt/data/filename pi@" + address + ":/opt/data/file")	

main():
	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	addr = socket.gethostbyname(HOSTNAME)
	server_address = (addr, SERVERPORT)
	sock.connect(server_address)
	syncFiles()
	
