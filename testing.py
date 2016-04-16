# import argparse
# import random
# import time
# from pythonosc import osc_message_builder
# from pythonosc import udp_client
import os
PORT=8666
IP="127.0.0.1"



# client = udp_client.UDPClient(IP, PORT)
# msg = osc_message_builder.OscMessageBuilder(address = "/Builder")
# msg.add_arg("msg 30 30 wouw!")
# msg.build()
# client.send(msg)import OSC
import OSC
c = OSC.OSCClient()
c.connect((IP, PORT))
oscmsg = OSC.OSCMessage()
oscmsg.setAddress("/BUILDER")
oscmsg.append("300 130 print ;")
#c.send(oscmsg)
msg =  "pd-new obj 20 20 MIDI \;"
msg =  "pd-new obj 30 60 DIV \;" 
msg =  "pd-new connect 0 1 1 0 \;"
msg =  "pd-new editmode 1, mouse 0 0 0 0, mouseup 400 65 0, cut \;"
#msg =  "pd-new cut \;"
#msg =  "pd-new mouseover"

os.system(" echo %s | /Applications/Pd-extended.app/Contents/Resources/bin/pdsend %d" % (msg, PORT))
