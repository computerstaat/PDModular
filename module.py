import sys, os, string, time, copy
import random
from math import floor
import Tkinter as tk
from Tkinter import *
from modules import modules
from ChooseCableColor import chooseCableColor
from jack import Jack
from knob import Knob
from slider import Slider
from presets import Presets

import OSC

scalar = Presets['scalar']
cordoffset = 2
singleModuleWidth = 30 * scalar
moduleHeight = Presets['ModuleHeight'] * scalar


class Module():

  def __init__(self, canvas, name, x1, y1, parent, osc):
    self.name = name
    self.tag = "M" + str(id(self))
    self.pdID, self.oscRouter = parent.PureData.addModule(name, self.tag)
    self.canvas = canvas
    self.InputJacks = []
    self.OutputJacks = []
    self.Sliders = []
    self.Knobs = []
    self.buildModule(name, x1, y1)
    self.canMove = True
    self.parent = parent
    self.osc = osc
    self.currentValues = {}
    self.mapToGrid(None)

  def sendValue(self, values, sliderName):
      oscmsg = OSC.OSCMessage()
      oscmsg.setAddress("/" + self.tag +"/" + self.name + "/" + sliderName)
      print "/" + self.tag + "/" + self.name + "/" + sliderName
      oscmsg.append(values)
      self.osc.send(oscmsg)

  def setValues(self, values):
      x = 0
      for v,s in zip(values, self.Sliders):
        s.updateValue(v)

  def getPresets(self):
      presets = {}
      for slider in self.Sliders:
          address = "/" + self.tag +"/" + self.name + "/" + slider.name
          presets[address] = slider.value
      return presets

  def getMidiCC(self):
      presets = {}
      for slider in self.Sliders:
        if slider.cc != None:
          address = "/" + self.tag +"/" + self.name + "/" + slider.name
          presets[slider.cc] = address
      return presets

  def getRepresentation(self):
    coords = self.canvas.coords(self.module)
    rep = {}
    rep['Name'] = self.name
    rep['x'] = coords[0]
    rep['y'] = coords[1]
    sliders = []
    for slider in self.Sliders:
        sliders.append(slider.value)
    rep['Values'] = sliders
    return {self.tag : rep}


  def reCenter(self):
    for jack in self.InputJacks + self.OutputJacks:
        jack.getCenter()

  def findLocalJack(self, jackID):
    for jack in self.InputJacks + self.OutputJacks:
        if jack.jackID == jackID:
          return jack
    return

  def findGlobalJack(self, jackID):
    return self.parent.findJack(jackID)

  def getJackNum(self, jackToFind):
    if jackToFind in self.InputJacks:
      return self.InputJacks.index(jackToFind)
    if jackToFind in self.OutputJacks:
      return self.OutputJacks.index(jackToFind)
    print "FAILURE FAILURE FAILURE"

  def isInputJack(self, jack):
    return jack in self.InputJacks

  def isOutputJack(self, jack):
    return jack in self.OutputJacks

  def delete(self):
    print "DELETING" 
    toRemove = list()
    for cable, jack1, jack2, _ , _ in self.parent.Cables:
      if jack1 in self.InputJacks + self.OutputJacks or jack2 in self.InputJacks + self.OutputJacks:
        toRemove.append(cable)
    for cable in toRemove:
      self.parent.removeCable(cable)
    for element in self.InputJacks + self.OutputJacks + self.Sliders:
      element.delete()
    if self in self.parent.AllModules:
      self.parent.AllModules.remove(self)  
    self.parent.PureData.removeModule(self.oscRouter)
    self.parent.PureData.removeModule(self.pdID)
    self.canvas.delete(self.module)
    self.canvas.delete(self.title)
    try:
      self.canvas.unbind("<ButtonPress-1>", self.bp)
      self.canvas.unbind("<B1-Motion>", self.bm)
    except:
      print "FAILED TO UNBIND TAGS"

  def buildColumn(self, x1, y1, elements):
    distance = (self.height - 10 ) / len(elements)
    current = y1 + (distance / (len(elements) + 1))
    
    for element in elements:
      if element[0] == "Input":
        self.InputJacks.append( 
          Jack(self.canvas, x1, current, self.tag, element[1], self, element[0]))
      elif element[0] == "Output":
        self.OutputJacks.append( 
          Jack(self.canvas, x1, current, self.tag, element[1], self, element[0]))
      elif element[0] == "Knob":
        self.Knobs.append( 
          Knob(self.canvas, x1, current, self.tag, element[2], element[1], self))
      elif element[0] == "Text":
        self.canvas.create_text(x1+10 * scalar, current + (distance / 4),fill=Presets['Text'], font=("Purisa", 8), text =element[1], tags=(self.tag, "Module"))
      current += distance

  def buildModule(self, name, x1, y1):
    layout = modules[name]
    self.width = len(layout) * singleModuleWidth #+ 10
    self.height = moduleHeight
    self.module = self.canvas.create_rectangle(x1,y1,x1+self.width,y1+self.height, tags=(self.tag, "Module"), fill=Presets['Module'])#, outline="lightgrey")
    self.title = self.canvas.create_text(x1+(20 * scalar), y1+(5 * scalar), font=("Purisa", 10,"bold"),fill=Presets['Text'], text =name, tags=(self.tag, "Module"), justify=LEFT)
    current = x1 + 5 * scalar
    for segment in layout:
      if segment[0] == "List":
        self.buildColumn(current, y1, segment[1])
      elif segment[0] == "Slider":
        newSlider = Slider(self.canvas, current, y1 + (10 * scalar), self.tag, segment[2], segment[1], self)
        self.Sliders.append(newSlider)
      else:
        print "This is not a valid module"
      current += 30 * scalar


    self.bp = self.canvas.tag_bind (self.tag, "<ButtonPress-1>", self.onPress)
    self.bm = self.canvas.tag_bind (self.tag, "<B1-Motion>", self.onMotion)
    self.br = self.canvas.tag_bind (self.tag, "<ButtonRelease-1>", self.mapToGrid)
    self.rc = self.canvas.tag_bind (self.tag, "<ButtonPress-2>", self.popUp)
    self.rcr = self.canvas.tag_bind (self.tag, "<ButtonRelease-2>", self.unpopUp)

  def popUp(self, event):
    self.popupLocation = [event.x, event.y, event.x + 40, event.y + 15]
    self.popup = self.canvas.create_rectangle(event.x, event.y, event.x + 40, event.y +15, fill="white", activefill="white")
    self.popuptext = self.canvas.create_text(event.x + 20, event.y + 7.5, font=("Purisa", 10), text ="DELETE",fill=Presets['Text'])

  def unpopUp(self, event):
    for item in self.canvas.find_overlapping(event.x, event.y, event.x, event.y):
      if item == self.popup:
        self.canvas.delete(self.popup)
        self.canvas.delete(self.popuptext)
        self.delete()
    self.canvas.delete(self.popup)
    self.canvas.delete(self.popuptext)

  def onPress(self, event):
    self.pressedX = event.x
    self.pressedY = event.y


  def onMotion(self, event):
    if self.canMove:
      self.canvas.tag_raise(self.tag)
      self.canvas.move(self.tag, event.x - self.pressedX, event.y - self.pressedY)
      for cable, jack1, jack2, bp, br in self.parent.Cables:
        if jack1 in self.InputJacks + self.OutputJacks or jack2 in self.InputJacks + self.OutputJacks:
            jack1x, jack1y = jack1.getCenter()
            jack2x, jack2y = jack2.getCenter()
            midpointx = (jack1x + jack2x) / 2
            midpointy = ((jack1y + jack2y) / 2) + 40
            self.parent.cablesToFront()
            self.canvas.coords(cable, jack1x, jack1y, midpointx, midpointy, jack2x, jack2y)
      self.pressedX = event.x
      self.pressedY = event.y


 

  def mapToGrid(self, event):
        coords = self.canvas.coords(self.module)
        x = floor((coords[0] +  (singleModuleWidth * .5)) / singleModuleWidth) * singleModuleWidth
        y = floor((coords[1] +  (moduleHeight * .5)) / moduleHeight) * moduleHeight
        offsetx = x - coords[0] 
        offsety = y - coords[1] 
        if self.canMove:
          self.canvas.tag_raise(self.tag)
          self.canvas.move(self.tag, offsetx, offsety)
          for cable, jack1, jack2, bp, br in self.parent.Cables:
            if jack1 in self.InputJacks + self.OutputJacks or jack2 in self.InputJacks + self.OutputJacks:
                jack1x, jack1y = jack1.getCenter()
                jack2x, jack2y = jack2.getCenter()
                midpointx = (jack1x + jack2x) / 2
                midpointy = ((jack1y + jack2y) / 2) + 40
                self.parent.cablesToFront()
                self.canvas.coords(cable, jack1x, jack1y, midpointx, midpointy, jack2x, jack2y)

  def shouldMove(self, truth):
    self.canMove = truth


  def connectCable(self, jack1, jack2):
    jack1x, jack1y = jack1.getCenter()
    jack2x, jack2y = jack2.getCenter()
    midpointx = (jack1x + jack2x) / 2
    midpointy = ((jack1y + jack2y) / 2) + 40
    cable = self.canvas.create_line(jack1x, jack1y, midpointx, midpointy, jack2x, jack2y, \
            fill=chooseCableColor.getCurrentColor(), width = Presets['CableWidth'], tags=(jack1.tag + "cable"),smooth=Presets['CableSmooth'])
    self.canvas.addtag_withtag(str(cable) + " cable", cable)

    bp = self.canvas.tag_bind (jack1.tag + " cable", "<ButtonPress-2>", jack1.popUp)
    br = self.canvas.tag_bind (jack1.tag + " cable", "<ButtonRelease-2>", jack1.unpopUp)
    if jack1.parent.parent.addCable(cable, jack1, jack2, bp, br) == False:
      self.canvas.delete(cable)
      self.canvas.delete(bp)
      self.canvas.delete(br)
    return 