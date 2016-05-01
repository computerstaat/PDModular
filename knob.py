import sys, os, string, time, copy
from math import cos, sin
import random
import Tkinter as tk
from Tkinter import *

scalar = 1.0

class Knob():
    def __init__(self, canvas, x1, y1, tag, name, title, parent):
      self.tag = tag
      self.name = name
      self.title = title
      self.knobtag = "K" + str(id(self))
      self.wholeKnobTag = "WK" + str(id(self))
      self.centerx = x1 + 10 * scalar
      self.centery = y1 + 10 * scalar
      self.r = 8 * scalar
      self.value = .5


      self.ylocation = y1+50
      self.height = 90.0
      self.starty = y1+50
      self.value = 0.5
      self.canvas = canvas
      self.parent = parent
      self.marks = []
      color="red"
      darkcolor="darkred"

      self.knobShadow = self.canvas.create_oval(x1+ 2,y1 + 6, x1+2*self.r, y1+2*self.r+ 6, \
        fill=darkcolor, outline=darkcolor,tags=(self.tag, self.knobtag))

      self.knob = self.canvas.create_oval(x1+ 4,y1 + 4, x1+2*self.r + 2, y1+2*self.r + 2, \
        fill=color, outline=color,tags=(self.tag, self.knobtag))

      self.textID = self.canvas.create_text(self.centerx,y1+self.r*2 + 9 , \
        font=("Purisa", 7, "bold"), text =title, tags=(self.tag, "Module"))

      self.knobLine = self.canvas.create_line(self.centerx, self.centery, self.centerx, self.centery - self.r, \
        tags=(self.tag, self.knobtag), fill="white",width = 2)

      self.bp = canvas.tag_bind (self.knobtag, "<ButtonPress-1>", self.onPress)
      self.bm = canvas.tag_bind (self.knobtag, "<B1-Motion>", self.onMotion)
      self.br = canvas.tag_bind (self.knobtag, "<ButtonRelease-1>", self.onRelease)
      rbp = self.canvas.tag_bind (self.knobtag, "<ButtonPress-2>", self.popUp)
      rbr = self.canvas.tag_bind (self.knobtag, "<ButtonRelease-2>", self.unpopUp)
      #canvas.tag_bind ("Slider", "<B1-Motion>", self.enter)

    def onPress(self, event):
      self.eventstarty = event.y
      self.parent.shouldMove(False)


    def onRelease(self, event):
      self.parent.shouldMove(True)


    def onMotion(self, event):


      print "SLIDER VALUE: " + str(self.value)
      print event.x
      print event.y
      self.value += (self.eventstarty - event.y) * 0.001
      self.value = max(min(self.value, 1), 0) #put between 0 and 1
      degree = 320 * self.value
      newx = self.centerx + self.r * cos(degree)
      newy = self.centery - self.r * sin(degree)

      self.canvas.delete(self.knobLine)
      self.knobLine = self.canvas.create_line(self.centerx, self.centery, newx, newy, \
        tags=(self.tag, self.knobtag), fill="white",width = 2)


      self.parent.sendValue(self.value, self.name)
      

    def delete(self):
      self.canvas.delete(self.knobShadow)
      self.canvas.delete(self.knob)
      self.canvas.delete(self.textID)
      self.canvas.delete(self.knobLine)
      self.canvas.unbind("<ButtonPress-1>", self.bp)
      self.canvas.unbind("<B1-Motion>", self.bm)
      self.canvas.unbind("<ButtonRelease-1>", self.br)

    def entered(self):
      print "IT HAPPENED"
      self.midipopup.destroy()

    def popupmsg(self, msg):
      self.midipopup = tk.Tk()
      self.midipopup.wm_title("MIDI SELECTION")
      label = tk.Label(self.midipopup, text=msg, font="Purisa")
      label.pack(side="top", fill="x", pady=10)
      e1 = Entry(self.midipopup)
      e1.insert(0, "00")
      e1.pack()
      B1 = tk.Button(self.midipopup, text="Okay", command =self.entered)
      B1.pack()
      self.midipopup.mainloop()

    def popUp(self, event):
      print "SLIDER PRESSED"
      self.popup = self.canvas.create_rectangle(event.x, event.y+ 15, event.x + 40, event.y +30, fill="white", activefill="white")
      self.popuptext = self.canvas.create_text(event.x + 20, event.y + 22.5, font=("Purisa", 10), text ="MIDI")


    def unpopUp(self, event):
      print "LET GO"
      for item in self.canvas.find_overlapping(event.x, event.y, event.x, event.y):
          if item == self.popup:
            self.canvas.delete(self.popup)
            self.canvas.delete(self.popuptext)
            self.popupmsg("Chose CC Number")
      self.canvas.delete(self.popup)
      self.canvas.delete(self.popuptext)

