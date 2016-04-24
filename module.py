import sys, os, string, time, copy
import random
import Tkinter as tk
from Tkinter import *
from modules import modules
from jack import Jack
from slider import Slider
import OSC

scalar = 1.0
cordoffset = 2


class Module():

  def __init__(self, canvas, name, x1, y1, parent, osc):
    self.name = name
    self.tag = "M" + str(id(self))
    self.pdID, self.senders, self.oscRouter = parent.PureData.addModule(name, self.tag)
    self.canvas = canvas
    self.elements = []
    self.InputJacks = []
    self.OutputJacks = []
    self.buildModule(name, x1, y1)
    self.canMove = True
    self.parent = parent
    self.osc = osc
    self.currentValues = {}

  def sendValue(self, values, sliderName):
      oscmsg = OSC.OSCMessage()
      oscmsg.setAddress("/" + self.tag +"/" + self.name + "/" + sliderName)
      print "/" + self.tag + "/" + self.name + "/" + sliderName
      oscmsg.append(values)
      self.osc.send(oscmsg)

  def getPresets(self):
      presets = {}
      for element in self.elements:
        if isinstance(element, Slider):
          address = "/" + self.tag +"/" + self.name + "/" + element.name
          presets[address] = element.value
      return presets

  def getMidiCC(self):
      presets = {}
      for element in self.elements:
        if isinstance(element, Slider):
          if element.cc != None:
            address = "/" + self.tag +"/" + self.name + "/" + element.name
            presets[element.cc] = address
      return presets




  def reCenter(self):
    for element in self.elements:
      if isinstance(element,Jack):
        element.getCenter()

  def findLocalJack(self, jackID):
    for element in self.elements:
      if isinstance(element,Jack):
        if element.jackID == jackID:
          return element
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
    toRemove = list()
    for cable, jack1, jack2, _ , _ in self.parent.Cables:
      if jack1 in self.elements or jack2 in self.elements:
        toRemove.append(cable)
    for cable in toRemove:
        self.parent.removeCable(cable)
    for element in self.elements:
      element.delete()
    for sender in self.senders:
      self.parent.PureData.removeModule(sender)    
    self.parent.PureData.removeModule(self.oscRouter)
    self.parent.PureData.removeModule(self.pdID)
    self.canvas.delete(self.module)
    self.canvas.delete(self.title)
    self.canvas.unbind("<ButtonPress-1>", self.bp)
    self.canvas.unbind("<B1-Motion>", self.bm)

  def buildColumn(self, x1, y1, elements):
    distance = (self.height - 10 ) / len(elements)
    current = y1 + (distance / (len(elements) + 1))
    
    for element in elements:
      if element[0] == "Input":
        newJack = Jack(self.canvas, x1, current, self.tag, element[1], self, element[0])
        self.elements.append(newJack)
        self.InputJacks.append(newJack)
      if element[0] == "Output":
        newJack = Jack(self.canvas, x1, current, self.tag, element[1], self, element[0])
        self.elements.append(newJack)
        self.OutputJacks.append(newJack)

      if element[0] == "Text":
        self.canvas.create_text(x1+10 * scalar, current + (distance / 4), font=("Purisa", 8), text =element[1], tags=(self.tag, "Module"))
      current += distance

  def buildModule(self, name, x1, y1):
    layout = modules[name]
    self.width = len(layout) * 30 * scalar + 10
    self.height = 130 * scalar
    self.module = self.canvas.create_rectangle(x1,y1,x1+self.width,y1+self.height, tags=(self.tag, "Module"), fill="lightgrey")#, outline="lightgrey")
    self.title = self.canvas.create_text(x1+(20 * scalar), y1+(5 * scalar), font=("Purisa", 10,"bold"), text =name, tags=(self.tag, "Module"), justify=RIGHT)
    current = x1+10 * scalar
    for segment in layout:
      if segment[0] == "List":
        self.buildColumn(current, y1, segment[1])
      elif segment[0] == "Slider":
        self.elements.append(Slider(self.canvas, current, y1 + (10 * scalar), self.tag, segment[2], segment[1], self))
      else:
        print "This is not a valid module"
      current += 30 * scalar


    self.bp = self.canvas.tag_bind (self.tag, "<ButtonPress-1>", self.onPress)
    self.bm = self.canvas.tag_bind (self.tag, "<B1-Motion>", self.onMotion)
    self.rc = self.canvas.tag_bind (self.tag, "<ButtonPress-2>", self.popUp)
    self.rcr = self.canvas.tag_bind (self.tag, "<ButtonRelease-2>", self.unpopUp)

  def popUp(self, event):
    self.popupLocation = [event.x, event.y, event.x + 40, event.y + 15]
    self.popup = self.canvas.create_rectangle(event.x, event.y, event.x + 40, event.y +15, fill="white", activefill="white")
    self.popuptext = self.canvas.create_text(event.x + 20, event.y + 7.5, font=("Purisa", 10), text ="DELETE")

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
        if jack1 in self.elements or jack2 in self.elements:
            jack1x, jack1y = jack1.getCenter()
            jack2x, jack2y = jack2.getCenter()
            midpointx = (jack1x + jack2x) / 2
            midpointy = ((jack1y + jack2y) / 2) + 40
            self.parent.cablesToFront()
            self.canvas.coords(cable, jack1x, jack1y, midpointx, midpointy, jack2x, jack2y)
            # if cable in jack1.cableBackground.keys():
            #   cable2 = jack1.cableBackground[cable]
            # elif cable in jack2.cableBackground.keys():
            #   cable2 = jack2.cableBackground[cable]
            # else: 
            #   print "FAILURE!!!!!"
            # self.canvas.coords(cable2, jack1x - cordoffset, jack1y + cordoffset, midpointx - cordoffset,\
            #                    midpointy + cordoffset, jack2x - cordoffset, jack2y + cordoffset)
      self.pressedX = event.x
      self.pressedY = event.y

  def shouldMove(self, truth):
    self.canMove = truth