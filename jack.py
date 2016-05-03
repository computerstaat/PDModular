import sys, os, string, time, copy
import random
import Tkinter as tk
from Tkinter import *
from ChooseCableColor import chooseCableColor
from presets import Presets


cordoffset = 2
scalar = Presets['scalar']

class Jack():
    def __init__(self, canvas, x1, y1, tag, title, parent, type):
      self.tag = tag
      self.jacktag = "J" + str(id(self))
      self.canvas = canvas
      self.parent = parent
      self.centerx = x1 + 10 * scalar
      self.centery = y1 + 10 * scalar
      self.r = 8 * scalar
      self.receivers = {}
      self.textID = None
      if type == "Input":
        color = Presets['InputJack']
        darkcolor = Presets['InputJackShadow']
      else:
        color = Presets['OutputJack']
        darkcolor = Presets['OutputJackShadow']
      self.jackShadow = self.canvas.create_oval(x1+ 2,y1 + 6, x1+2*self.r, y1+2*self.r+ 6, fill=darkcolor, outline=darkcolor,tags=(self.tag, self.jacktag))
      self.jackLoop = self.canvas.create_oval(x1+ 4,y1 + 4, x1+2*self.r + 2, y1+2*self.r + 2, fill=color, outline=color,tags=(self.tag, self.jacktag))
      self.jackID = self.canvas.create_oval(x1+ 6,y1 + 6, x1+2*self.r , y1+2*self.r, fill=Presets['JackHole'], tags=(self.tag, self.jacktag, "Jack"))

      if title != "":
        self.textID = self.canvas.create_text(self.centerx,y1+self.r*2 + 9 , font=Presets['JackFont'], text=title, tags=(self.tag, "Module"),fill=Presets['Text'])

      self.jackCoords = self.canvas.coords(self.jackID)
      self.bp = canvas.tag_bind (self.jacktag, "<ButtonPress-1>", self.onPress)
      self.bm = canvas.tag_bind (self.jacktag, "<B1-Motion>", self.onMotion)
      self.br = canvas.tag_bind (self.jacktag, "<ButtonRelease-1>", self.onRelease)


    def delete(self):
      self.canvas.delete(self.textID)
      self.canvas.delete(self.jackID)
      self.canvas.delete(self.jackLoop)
      self.canvas.delete(self.jackShadow)
      self.canvas.unbind("<ButtonPress-1>", self.bp)
      self.canvas.unbind("<B1-Motion>", self.bm)
      self.canvas.unbind("<ButtonRelease-1>", self.br)

    def popUp(self, event):
      for item in self.canvas.find_overlapping(event.x, event.y, event.x, event.y):
        if self.parent.parent.isCable(item):
          self.currentCable = item
      self.popup = self.canvas.create_rectangle(event.x, event.y, event.x + 40, event.y +15, fill="white", activefill="white")
      self.popuptext = self.canvas.create_text(event.x + 20, event.y + 7.5, font=("Purisa", 10), text ="DELETE")

    def unpopUp(self, event):
      for item in self.canvas.find_overlapping(event.x, event.y, event.x, event.y):
        if item == self.popup:
          self.canvas.delete(self.popup)
          self.canvas.delete(self.popuptext)
          self.parent.parent.removeCable(self.currentCable)
      self.currentCable = None
      self.canvas.delete(self.popup)
      self.canvas.delete(self.popuptext)

    def getCenter(self):
      self.jackCoords = self.canvas.coords(self.jackLoop)
      self.centerx = self.jackCoords[0] + self.r
      self.centery = self.jackCoords[1] + self.r
      return self.centerx, self.centery

    def onPress(self, event):
      self.parent.shouldMove(False)
      self.jackCoords = self.canvas.coords(self.jackID)
      self.centerx, self.centery = self.getCenter()
      global cableColor
      
      self.currentConnection1 = self.canvas.create_line(self.centerx, self.centery, event.x, event.y, \
            fill=chooseCableColor.getCurrentColor(), width = Presets['CableWidth'], tags=(self.tag + "cable"),smooth=Presets['CableSmooth'])
      self.canvas.addtag_withtag(str(self.currentConnection1) + " cable", self.currentConnection1)


    def onRelease(self, event):
      self.parent.shouldMove(True)
      for item in self.canvas.find_overlapping(event.x, event.y, event.x, event.y):
        if "Jack" in self.canvas.gettags(item):

          newConnection = self.parent.findGlobalJack(item)
          jack1x, jack1y = self.getCenter()
          jack2x, jack2y = newConnection.getCenter()
          midpointx = (jack1x + jack2x) / 2
          midpointy = ((jack1y + jack2y) / 2) + 40
          self.canvas.coords(self.currentConnection1, jack1x, jack1y, midpointx, midpointy, jack2x, jack2y)

          bp = self.canvas.tag_bind (str(self.currentConnection1) + " cable", "<ButtonPress-2>", self.popUp)
          br = self.canvas.tag_bind (str(self.currentConnection1) + " cable", "<ButtonRelease-2>", self.unpopUp)
          if self.parent.parent.addCable(self.currentConnection1, self, newConnection, bp, br) == False:
            self.canvas.delete(self.currentConnection1)
            self.canvas.delete(bp)
            self.canvas.delete(br)
          return 
      self.canvas.delete(self.currentConnection1)

      self.currentConnection1 = None
      #self.currentConnection2 = None
     
    def onMotion(self, event):
      midpointx = (self.centerx + event.x) / 2
      midpointy = ((self.centery + event.y) / 2) + 40
      
      self.canvas.coords(self.currentConnection1, self.centerx, self.centery, midpointx, midpointy,event.x, event.y)



