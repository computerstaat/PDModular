import sys, os, string, time, copy
import random
import Tkinter as tk
from Tkinter import *

scalar = 1.0

class Slider():
    def __init__(self, canvas, x1, y1, tag, name, title, parent):
      self.tag = tag
      self.name = name
      self.title = title
      self.slidertag = "S" + str(id(self))
      self.wholeSliderTag = "WS" + str(id(self))
      self.x1 = x1
      self.y1 = y1
      self.ylocation = y1+50
      self.height = 90.0
      self.starty = y1+50
      self.value = 0.5
      self.canvas = canvas
      self.parent = parent
      self.marks = []
      self.cc = None
       


      for y in range(10):
        self.marks.append(canvas.create_rectangle(x1,y1 +(y*10 * scalar) + 5, x1+5 * scalar, y1 + (y*10 * scalar) + 7, \
          fill="lightslategrey", outline="lightslategrey", tags=(self.tag, "Module", self.wholeSliderTag)))
        self.marks.append(canvas.create_rectangle(x1+ 15,y1 +(y*10 * scalar) + 5, x1+20 * scalar, y1 + (y*10 * scalar) + 7, \
          fill="lightslategrey", outline="lightslategrey", tags=(self.tag, "Module", self.wholeSliderTag)))
     
      self.containerID = canvas.create_rectangle(x1+10,y1+ 2, x1 + 11 * scalar, y1 + 98 * scalar, \
          fill="black", tags=(self.tag, "Module", self.wholeSliderTag))


      self.sliderIDdark = canvas.create_rectangle(x1+4,y1+46, x1 + 17 * scalar, y1 + 55 * scalar, \
            tags=(self.tag, self.slidertag), fill="royalblue", outline="royalblue")
      self.sliderID = canvas.create_rectangle(x1+6,y1+45, x1 + 18 * scalar, y1 + 53 * scalar, \
            tags=(self.tag, self.slidertag), fill="deepskyblue", outline="deepskyblue")
      self.sliderIDnotch = self.canvas.create_line(x1+6,y1+50, x1 + 18 * scalar, y1 + 50 * scalar, \
            tags=(self.tag, self.slidertag), fill="white",width = 2)

      self.textID = canvas.create_text(x1+10 * scalar, y1+110 * scalar, font=("Purisa", 7, "bold"), text =title, tags=(self.tag, "Module"))
      self.containerCoords = canvas.coords(self.containerID)
      self.sliderCoords = canvas.coords(self.sliderID)


      self.bp = canvas.tag_bind (self.slidertag, "<ButtonPress-1>", self.onPress)
      self.bm = canvas.tag_bind (self.slidertag, "<B1-Motion>", self.onMotion)
      self.br = canvas.tag_bind (self.slidertag, "<ButtonRelease-1>", self.onRelease)
      rbp = self.canvas.tag_bind (self.slidertag, "<ButtonPress-2>", self.popUp)
      rbr = self.canvas.tag_bind (self.slidertag, "<ButtonRelease-2>", self.unpopUp)
      #canvas.tag_bind ("Slider", "<B1-Motion>", self.enter)

    def onPress(self, event):
      self.parent.shouldMove(False)
      self.sliderCoords = self.canvas.coords(self.sliderID)
      self.containerCoords = self.canvas.coords(self.containerID)
      self.currentY = event.y


    def onRelease(self, event):
      self.parent.shouldMove(True)


    def onMotion(self, event):
      print "SLIDER VALUE: " + str(self.value)
      self.sliderCoords = self.canvas.coords(self.sliderID)
      moved =  event.y - self.currentY
      if  self.sliderCoords[1] + moved + 2  < self.containerCoords[1]:
        return
      if self.sliderCoords[3] + moved > self.containerCoords[3]:
        return
      self.value = 1 - ((event.y - self.containerCoords[1] )/ self.height) + .05   #This math could be better
      self.value = max(self.value, 0)
      self.value = min(self.value, 1)
      self.canvas.move(self.slidertag, 0, event.y - self.currentY)
      self.currentY = event.y
      self.canvas.sliderCoords = self.canvas.coords(self.sliderID)
      self.parent.sendValue(self.value, self.name)
      

    def delete(self):
      self.canvas.delete(self.containerID)
      self.canvas.delete(self.sliderID)
      self.canvas.delete(self.sliderIDdark)
      self.canvas.delete(self.sliderIDnotch)
      self.canvas.delete(self.textID)
      for mark in self.marks:
        self.canvas.delete(mark)
      self.canvas.unbind("<ButtonPress-1>", self.bp)
      self.canvas.unbind("<B1-Motion>", self.bm)
      self.canvas.unbind("<ButtonRelease-1>", self.br)

    def entered(self):
      self.cc = self.e.get()
      print  "Midi channel for " + self.name + ": " + str(self.cc)
      self.midipopup.destroy()

    def popupmsg(self, msg):
      self.midipopup = tk.Tk()
      self.midipopup.wm_title("MIDI SELECTION")
      label = tk.Label(self.midipopup, text=msg, font="Purisa")
      label.pack(side="top", fill="x", pady=10)
      self.e = Entry(self.midipopup)
      self.e.insert(0, "00")
      self.e.pack()
      B1 = tk.Button(self.midipopup, text="Okay", command =self.entered)
      B1.pack()
      self.midipopup.mainloop()

    def popUp(self, event):
      self.popup = self.canvas.create_rectangle(event.x, event.y+ 15, event.x + 40, event.y +30, fill="white", activefill="white")
      self.popuptext = self.canvas.create_text(event.x + 20, event.y + 22.5, font=("Purisa", 10), text ="MIDI")


    def unpopUp(self, event):
      for item in self.canvas.find_overlapping(event.x, event.y, event.x, event.y):
          if item == self.popup:
            self.canvas.delete(self.popup)
            self.canvas.delete(self.popuptext)
            self.popupmsg("Chose CC Number")
      self.canvas.delete(self.popup)
      self.canvas.delete(self.popuptext)

