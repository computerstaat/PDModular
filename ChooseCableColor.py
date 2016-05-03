cableColor = "darkorchid"
cableColors = [ "medium blue", "cyan", "chartreuse", "forest green", "goldenrod", "yellow", "orange", "red", "magenta"]

class chooseCableColor():
  @staticmethod
  def setCurrentColor(newColor):
    global cableColor
    cableColor = newColor

  @staticmethod
  def getCurrentColor():
    return cableColor

  @staticmethod
  def getAllColors():
    return cableColors