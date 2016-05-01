import sys, os, string, time, copy
import random
import Tkinter as tk
from Tkinter import *
from slider import Slider
from jack import Jack
from knob import Knob
from module import Module
from ChooseCableColor import chooseCableColor
# from ChooseModules import chooseModules
from modules import modules
from pythonosc import *
from Pd import *
import mido
import json

import OSC

PORT=8668
IP="127.0.0.1"

SizeScaler = 1.0
CanvasWidth = 900
CanvasHeight = 900
MIDIDEVICE = "MPKmini2e"


class PureData():
  def __init__(self):
    self.pd = PD()
    sleep(5)
    self.osc = 0
    #self.osc = self.pd.create("inlet")
    # self.rec = self.pd.create("udpreceive " + str(PORT))
    # self.osc = self.pd.create("unpackOSC")
    # self.pd.connect(self.rec, 0, self.osc, 0)

  def reset(self):
    self.pd.clear()
    #self.osc = self.pd.create("inlet")
    # self.rec = self.pd.create("udpreceive " + str(PORT))
    # self.osc = self.pd.create("unpackOSC")
    # self.pd.connect(self.rec, 0, self.osc, 0)

  def kill(self):
    self.pd.kill()


  def addModule(self, name, uniqueName):
      needsRouter = False
      if uniqueName != None:
        x = 0
        for column in modules[name]:
          if column[0] == "List":
              for element in column[1]:
                if element[0] == "Input":
                  x += 1
          if column[0] == "Slider":
            needsRouter = True
      if needsRouter == True:
            router = self.pd.create("routeOSC /" + uniqueName)
            uid = self.pd.create(name)
            self.pd.connect(self.osc, 0, router, 0)
            self.pd.connect(router, 0, uid, x)
      else :
        uid = self.pd.create(name)
        router = None
      return uid, router

  def removeModule(self, name):
    if name == None:
      return
    self.pd.remove(name)


  def connect(self, jack1, jack2):
    if jack1.parent.isInputJack(jack1) and jack2.parent.isOutputJack(jack2):
      inputID = jack1.parent.pdID
      inputNum = jack1.parent.getJackNum(jack1)
      outputID = jack2.parent.pdID
      outputNum = jack2.parent.getJackNum(jack2)
      print "THIS WAY"
    elif jack2.parent.isInputJack(jack2) and jack1.parent.isOutputJack(jack1):
      inputID = jack2.parent.pdID
      inputNum = jack2.parent.getJackNum(jack2)
      outputID = jack1.parent.pdID
      outputNum = jack1.parent.getJackNum(jack1)
      print "THAT WAY"
    else:
      print "ILLEGAL CONNECTION"
      return False
    print "CONNECTING %d %d" % (inputNum, outputNum)
    self.pd.connect(outputID, outputNum, inputID, inputNum)
    return True

  def disconnect(self, jack1, jack2):
      if jack1.parent.isInputJack(jack1) and jack2.parent.isOutputJack(jack2):
        inputID = jack1.parent.pdID
        inputNum = jack1.parent.getJackNum(jack1)
        outputID = jack2.parent.pdID
        outputNum = jack2.parent.getJackNum(jack2)
        print "THIS WAY"
      elif jack2.parent.isInputJack(jack2) and jack1.parent.isOutputJack(jack1):
        inputID = jack2.parent.pdID
        inputNum = jack2.parent.getJackNum(jack2)
        outputID = jack1.parent.pdID
        outputNum = jack1.parent.getJackNum(jack1)
        print "THAT WAY"
      else:
        print "ILLEGAL CONNECTION"
        return False
      self.pd.disconnect(outputID, outputNum, inputID, inputNum)
      return True


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
    if self.PureData.connect(jack1, jack2) == False:
      return False
    self.Cables.append((cable, jack1, jack2, bp, br))
    return True


  def cablesToFront(self):
    for cable, _, _, _, _ in self.Cables:
      self.canvas.tag_raise(str(cable) + " cable")

  def isCable(self, c):
    for cable, _, _, _, _ in self.Cables:
      if cable == c:
        return True
    return False

  def killEmAll(self):
    self.osc.close()
    pid = os.getpid()
    self.PureData.pd.kill()
    os.system ("kill -9 " + str(pid))

  def Save(self):
    self.savePopup = tk.Tk()
    self.savePopup.wm_title("Save")
    label = tk.Label(self.savePopup, text="Please Name Synthesizer:", font="Purisa")
    label.pack(side="top", fill="x", pady=10)
    self.e = Entry(self.savePopup)
    self.e.insert(0, "name")
    self.e.pack()
    B1 = tk.Button(self.savePopup, text="Enter", command =self.SaveEntered)
    B1.pack()
    self.savePopup.mainloop()

  def Load(self):
    self.loadPopup = tk.Tk()
    self.loadPopup.wm_title("Save")
    label = tk.Label(self.loadPopup, text="Please Name Synthesizer:", font="Purisa")
    label.pack(side="top", fill="x", pady=10)
    self.e = Entry(self.loadPopup)
    self.e.insert(0, "name")
    self.e.pack()
    B1 = tk.Button(self.loadPopup, text="Enter", command =self.LoadEntered)
    B1.pack()
    self.loadPopup.mainloop()

  def LoadEntered(self):
      name = self.e.get()
      self.loadPopup.destroy()
      with open("./Patches/patches.json",'r') as json_file:
        patchDictionary = json.load(json_file)
        for m in self.AllModules:
          m.delete()
        self.PureData.reset()
        patch = patchDictionary[name]
        for n, module in patch['modules'].iteritems():
          newM = Module(self.canvas, module['Name'], module['x'], module['y'], self, self.osc)
          newM.setValues(module['Values'])
          tempDict[n] = newM
          self.AllModules.append(newM)
        for cable in patch['cables']:
          print cable

  def SaveEntered(self):
      name = self.e.get()
      self.savePopup.destroy()
      patchDictionary = {}
      with open("./Patches/patches.json",'r') as json_file:
        patchDictionary = json.load(json_file)
        mods = {}
        cabs = {}
        presets = {}
        midi = {}
        for module in self.AllModules:
          mods.update(module.getRepresentation())
          midi.update(module.getMidiCC())
          presets.update(module.getPresets())
        x = 0
        for _, j1, j2, _, _  in self.Cables:
          if j1 in j1.parent.InputJacks:
            cabs[x] = [j1.parent.tag, j1.parent.getJackNum(j1), 
                           j2.parent.tag, j2.parent.getJackNum(j2)]
          elif j2 in j2.parent.InputJacks:
            cabs[x] = [j2.parent.tag, j2.parent.getJackNum(j2), 
                           j1.parent.tag, j1.parent.getJackNum(j1)]
          x += 1
        patch = {name:  { 'cables' : cabs, 'modules' : mods, 'presets' : presets, 'midi': midi}}
        patchDictionary.update(patch)
      with open("./Patches/patches.json",'w') as json_file:
        json.dump(patchDictionary, json_file, indent=4, sort_keys=True, separators=(',', ':'))
        self.PureData.pd.save(name)


  # def saveEmAll(self, name):
  #   patchDictionary = {}
  #   with open("./Patches/patches.json",'r') as json_file:
  #     patchDictionary = json.load(json_file)
  #     mods = {}
  #     cabs = {}
      
  #     for module in self.AllModules:
  #       mods.update(module.getRepresentation())
  #     for _, j1, j2, _, _  in self.Cables:
  #       if j1 in j1.parent.InputJacks:
  #         cabs[x] = [j1.parent.tag, j1.parent.getJackNum(j1), 
  #                        j2.parent.tag, j2.parent.getJackNum(j2)]
  #       elif j2 in j2.parent.InputJacks:
  #         cabs[x] = [j2.parent.tag, j2.parent.getJackNum(j2), 
  #                        j1.parent.tag, j1.parent.getJackNum(j1)]
  #       x += 1
  #     patch = {name:  { 'cables' : cabs, 'modules' : mods}}
  #     patchDictionary.update(patch)
  #   with open("./Patches/patches.json",'w') as json_file:
  # #     json.dump(patchDictionary, json_file, indent=4, sort_keys=True, separators=(',', ':'))


  #   def loadEmAll(self, name):
  #     with open("./Patches/patches.json",'r') as json_file:
  #       patchDictionary = json.load(json_file)
  #       for m in self.AllModules:
  #         m.delete()
  #       self.PureData.kill()
  #       self.PureData = PureaData()
  #       patch = patchDictionary[name]
  #       for n, module in patch['modules'].iteritems():
  #         newM = Module(self.canvas, module['Name'], module['x'], module['Y'], self, self.osc)
  #         newM.setValues(module['Values'])
  #         tempDict[n] = newM
  #         self.AllModules.append(newM)
  #       for cable in patch['cables']:
  #         print cable






  
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
    menu.add_command(label="Save", command=self.Save)
    menu.add_command(label="Load", command=self.Load)
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
