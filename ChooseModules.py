# from modulelist import modules
# from module import Module

# class chooseModules():

#   @staticmethod
#   def getAllModules():
#     return sorted(modules.keys())



  # def __init__(self, canvas, x1, y1, parent):
  #   self.tag = "M" + str(id(self))
  #   self.canvas = canvas
  #   self.elements = []
  #   self.parent = parent
  #   self.buildButtons(canvas,x1, y1)


  # def buildButtons(self, canvas, x1, y1):
  #   for mod in sorted(modules.keys()):
  #     enclosure = self.canvas.create_rectangle(x1,y1, x1 + 30, y1+ 20, tags=("choose", mod))
  #     text = self.canvas.create_text(x1+ 15, y1 + 10, font=("Purisa", 8), text =mod, tags=("choose", mod))
  #     self.elements.append([enclosure, text])
  #     self.canvas.tag_bind (mod, "<ButtonPress-1>", self.onPress)
  #     self.canvas.tag_bind (mod, "<B1-Motion>", self.onMotion)
  #     self.canvas.tag_bind (mod, "<ButtonRelease-1>", self.onRelease)
  #     x1 += 35

  # def onPress(self, event):
  #     item = self.canvas.find_closest(event.x, event.y)[0]
  #     self.pressedX = event.x
  #     self.pressedY = event.y
  #     for element, text in self.elements:
  #       if element == item or text == item:
  #         module_type = self.canvas.gettags(element)[1]
  #         print module_type
  #         self.currentModule =  Module(self.canvas, module_type, event.x, event.y, self.parent)
  #         self.parent.AllModules.append(self.currentModule)
  #         return

  # def onRelease(self, event):
  #   self.currentModule = None


  # def onMotion(self, event):
  #   self.canvas.move(self.currentModule.tag, event.x - self.pressedX, event.y - self.pressedY)
  #   self.currentModule.reCenter()
  #   self.pressedX = event.x
  #   self.pressedY = event.y

