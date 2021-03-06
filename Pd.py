import sys
import os
import threading

from socket     import *
from time       import *  
from subprocess import *



PORT=8667
IP="127.0.0.1"
LOCATION = "./PdObjects/"
PUREDATA = "Pd-extended"






class PD():
	def __init__(self):
		os.system("%s  %sserver.pd &" % (PUREDATA, LOCATION))
		self.modules = {}
		self.UIDcounter = 0
		self.curX = 5
		self.curY = 5
		self.objectCount = 0

		#creates module and returns UID
	def create(self, name):
		msg = "pd-new obj %d %d %s \;" % (self.curX, self.curY,name)
		self.modules[self.UIDcounter] = [name,self.objectCount, self.curX, self.curY]
		curUID = self.UIDcounter
		self.UIDcounter += 1
		self.objectCount += 1
		self.curY += 30
		self.systemCall(msg)
		print self.modules
		return curUID

	def connect(self, mod1ID, outputNum, mod2ID, inputNum):
		id1=self.getID(mod1ID)
		id2=self.getID(mod2ID)
		# self.connections[(mod1ID, outputNum, mod2ID, inputNum)] = cid
		msg = "pd-new connect %d %d %d %d \;" %  (id1, outputNum, id2, inputNum)
		self.systemCall(msg)
		# msg = "pd-new connect %d %d %d %d \;" %  (self.getID(cid), 0, )
		# self.systemCall(msg)

	def remove(self, modID):
		print "REMOVING IN PROGRESS"
		self.objectCount -= 1
		_,curid,x,y = self.modules[modID]
		msg = "pd-new editmode 1, mouse %d %d 0 0, mouseup %d %d 0, cut \;" % (max(0,x - 5), max(0,y - 5), x + 400, y + 25)
		self.systemCall(msg)
		del self.modules[modID]
		for i in self.modules.keys():
			(n, uid, x, y) = self.modules[i]
			if uid > curid:
				self.modules[i] = (n, uid - 1, x, y)

	def disconnect(self, mod1ID, outputNum, mod2ID, inputNum):
		id1=self.getID(mod1ID)
		id2=self.getID(mod2ID)
		# self.connections[(mod1ID, outputNum, mod2ID, inputNum)] = cid
		msg = "pd-new disconnect %d %d %d %d \;" %  (id1, outputNum, id2, inputNum)
		self.systemCall(msg)


	def getID(self, modID):
		print self.modules.keys()
		print self.modules
		print modID
		if modID in self.modules.keys():
			_,uid,_,_ = self.modules[modID]
			return uid
		return -1

	def systemCall(self, msg):
		#print "MESAGE IS " + msg
		os.system(" echo %s | pdsend %d" % (msg, PORT))
		
	def kill(self):
		msg = "pd quit \;"
		self.systemCall(msg)

	def clear(self):
		msg = "pd-new clear \;"
		self.systemCall(msg)
		self.modules = {}
		self.UIDcounter = 0
		self.curX = 5
		self.curY = 5
		self.objectCount = 0

	def save(self, name):
		msg = "pd-new menusaveas \;" 
		self.systemCall(msg)



