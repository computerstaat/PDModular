import sys, os, string, time, copy
import random
import Tkinter as tk
from Tkinter import *
from slider import Slider
from jack import Jack
from module import Module
from ChooseCableColor import chooseCableColor
# from ChooseModules import chooseModules
from modules import modules
from pythonosc import *
from Pd import *
import mido

import OSC

PORT=9001
IP="127.0.0.1"

SizeScaler = 1.0
CanvasWidth = 900
CanvasHeight = 900
MIDIDEVICE = "MPKmini2e"


class PureData():
  def __init__(self):
    self.pd = PD()
    sleep(5)
    self.mp = self.pd.create("import mrpeach")
    self.rec = self.pd.create("udpreceive 9001")
    self.osc = self.pd.create("unpackOSC")
    self.pd.connect(self.rec, 0, self.osc, 0)


  def addModule(self, name, uniqueName):
    if name == "MIDI":
      uid = self.pd.create(name)
      self.pd.connect(self.osc, 0, uid, 0)
      x = 0
      senders = []

      if uniqueName != None:
        for column in modules[name]:
          if column[0] == "List":
            for element in column[1]:
              if element[0] == "Output":
                jid = self.pd.create("send~ " + uniqueName + str(x))
                senders.append(jid)
                self.pd.connect(uid,x,jid,0)
                x += 1
      return uid, senders, None
    if name == "OUT":
      uid = self.pd.create(name)
      return uid, [], None
    else: 
      router = self.pd.create("routeOSC /" + uniqueName)
      uid = self.pd.create(name)
      x = 0
      senders = []
      for column in modules[name]:
        if column[0] == "List":
            for element in column[1]:
              if element[0] == "Input":
                x += 1
      self.pd.connect(router, 0, uid, x)
      self.pd.connect(self.osc, 0, router, 0)
      x = 0
      if uniqueName != None:
        for column in modules[name]:
          if column[0] == "List":
            for element in column[1]:
              if element[0] == "Output":
                jid = self.pd.create("send~ " + uniqueName + str(x))
                senders.append(jid)
                self.pd.connect(uid,x,jid,0)
                x += 1
      return uid, senders, router



  def removeModule(self, name):
    if name == None:
      return
    self.pd.remove(name)


  def connect(self, jack1, jack2):
    if jack1.parent.isInputJack(jack1) and jack2.parent.isOutputJack(jack2):
      inputJack = jack1
      inputNum = jack1.parent.getJackNum(jack1)
      outputName = jack2.tag
      outputNum = jack2.parent.getJackNum(jack2)
      print "THIS WAY"
    elif jack2.parent.isInputJack(jack2) and jack1.parent.isOutputJack(jack1):
      inputJack = jack2
      inputNum = jack2.parent.getJackNum(jack2)
      outputName = jack1.tag
      outputNum = jack1.parent.getJackNum(jack1)
      print "THAT WAY"
    else:
      print "ILLEGAL CONNECTION"
      return None
    name = outputName + str(outputNum)
    receiver = self.pd.create("receive~ " + name)
    inputJack.receivers[name] = receiver
    self.pd.connect(receiver, 0, inputJack.parent.pdID, inputNum)
    return


  def disconnect(self, jack1, jack2):
    if jack1.parent.isInputJack(jack1) and jack2.parent.isOutputJack(jack2):
      inputJack = jack1
      inputNum = jack1.parent.getJackNum(jack1)
      outputName = jack2.tag
      outputNum = jack2.parent.getJackNum(jack2)
      print "THIS WAY"
    elif jack2.parent.isInputJack(jack2) and jack1.parent.isOutputJack(jack1):
      inputJack = jack2
      inputNum = jack2.parent.getJackNum(jack2)
      outputName = jack1.tag
      outputNum = jack1.parent.getJackNum(jack1)
      print "THAT WAY"
    else:
      print "ILLEGAL CONNECTION"
      return None
    name = outputName + str(outputNum)
    receiver = inputJack.receivers.pop(name, -1)
    print "RECEIVER = " + str(receiver)
    if(receiver == -1):
      return
    self.pd.remove(receiver)

class Application (tk.Frame):

  def hello(self):
      print "hello"

  def findJack(self, jackID):
    for module in self.AllModules:
      jack = module.findLocalJack(jackID)
      if jack != None:
        return jack

  def removeCable(self, cableToFind):
    print "REMOVING: " + str(cableToFind)
    for cable, jack1, jack2, bp, br in self.Cables:
      if cableToFind == cable:
        self.PureData.disconnect(jack1, jack2)
        self.canvas.unbind("<ButtonPress-2>", bp)
        self.canvas.unbind("<ButtonRelease-2>", br)
        self.Cables.remove((cable, jack1, jack2, bp, br))
        self.canvas.delete(cable)
        return
    print "CABLE NOT FOUND"

  def getConnectionFromCable(self, cableToFind):
    for cable, jack1, jack2, _, _ in self.Cables:
      if cableToFind == cable:
        return (cable, jack1, jack2)
    return None

  def addCable(self, cable, jack1, jack2, bp, br):
    print "Connection added: " + str(cable)
    print "JACK1 = " + str(jack1)
    print "JACK2 = " + str(jack2)
    print self
    self.PureData.connect(jack1, jack2)
    self.Cables.append((cable, jack1, jack2, bp, br))
    print self.Cables

  def cablesToFront(self):
    for cable, _, _, _, _ in self.Cables:
      self.canvas.tag_raise(str(cable) + " cable")

  def isCable(self, c):
    for cable, _, _, _, _ in self.Cables:
      if cable == c:
        return True
    return False

  def killEmAll(self):
    pid = os.getpid()
    self.PureData.pd.kill()
    os.system ("kill -9 " + str(pid))

  def saveEmAll(self, name):
    patchFile = open('./patches/' + name + ".py", 'w+')
    modules = {}
    cables = {}
    x = 0
    for module in self.AllModules:
      modules[x] = module.getRepresentation()
      x += 1
    x = 0
    for cable in self.Cables:
      cables[x] = cable.getRepresentation()
      x += 1
    patchFile.write(modules)
    patchFile.write(cables)

  def loadEmAll(self, name):
    patchFile = open('./patches/' + name + ".py", 'r')

  
  def __init__ (self, master):
    self.master =master
    self.PureData = PureData()
    self.loc =self.dragged =0
    tk.Frame.__init__ (self, master)

    self.AllModules = list()
    self.Cables = list()
    self.osc = OSC.OSCClient()
    self.osc.connect((IP, PORT))

    self.menubar = Menu(self)

    menu = Menu(self.menubar, tearoff=0)
    self.menubar.add_cascade(label="File", menu=menu)
    menu.add_command(label="Save", command=self.PureData.pd.save)
    menu.add_command(label="New")
    menu.add_command(label="Exit", command=self.killEmAll)

    menu = Menu(self.menubar, tearoff=0)
    self.menubar.add_cascade(label="Choose Module", menu=menu)
    for module in sorted(modules.keys()):
      menu.add_command(label=module, command=(lambda module :lambda :self.AllModules.append(Module(self.canvas, module, CanvasWidth/2, CanvasHeight/2, self, self.osc)))(module))
    
    menu = Menu(self.menubar, tearoff=0)
    self.menubar.add_cascade(label="Cable Color", menu=menu)
    for color in chooseCableColor.getAllColors():
      menu.add_command(label=color, command=(lambda color :lambda :chooseCableColor.setCurrentColor(color))(color))



    self.canvas =tk.Canvas (self, width =CanvasWidth, height =CanvasHeight,
      relief =tk.RIDGE, background ="white", borderwidth =1)

    menubar = Menu(root)

    try:
        self.master.config(menu=self.menubar)
    except AttributeError:
        # master is a toplevel window (Python 1.4/Tkinter 1.63)
        self.master.tk.call(master, "config", "-menu", self.menubar)

    # chooseModules(self.canvas, 10, 10, self)

    self.canvas.pack (expand =1, fill =tk.BOTH)

    #mp = self.midiParameter(self.master, self.canvas)


  

root =tk.Tk()
root.title ("PD-Modular")
Application(root).pack()
root.mainloop()
