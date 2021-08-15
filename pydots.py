

import sys
import pygame

#these two are for what is saved in the algorithm.txt file
startTag = "from"
endTag = "to"
#you can play with the color settings by chaning the paramas given to each
#pygame.Color(red, green, blue)
#settings class for all objects in runtime
class Settings:
 def __init__(self, pg, surf, gridDim, offset):
  self.unitDim = round((surf.get_size()[0]-offset)/gridDim)
  self.odim = surf.get_size()[0]
  self.parent = self
  self.offset = offset
  self.menuText = "Settings"
  self.dataFile = "data.txt"
  self.active = False
  self.pg = pg
  self.surf = surf
  self.gridDim = gridDim
  self.leaderOn = True
  self.showCoordinates = True
  self.showGrid = True
  self.showGridPoints = True
  self.showGridLabels = True
  self.gridColor = pygame.Color(255,0,0)
  self.dotColor = pygame.Color(5,205,175)
  self.laidLinesColor = pygame.Color(0,60,200)
  self.leaderLineColor = pygame.Color(125,125,150)
  self.backgroundColor = pygame.Color(255,255,255)
  self.buttonBackgroundColor = pygame.Color(55, 55, 55)
  self.buttonSelectedBackgroundColor = pygame.Color(55, 55, 155)
  self.colors = [("Grid Color", self.gridColor),
  ("Grid Dot Color", self.dotColor),
  ("Laid Line Color", self.laidLinesColor),
  ("Leader Color", self.leaderLineColor),
  ("Background Color", self.backgroundColor),
  ("Button Background Color", self.buttonBackgroundColor) ]
  self.colors.clear()
  self.buttons = []
  i = 30
  deltaY = 20
  fontSize = 15
  self.leaderButton = Button(self, self , pg, surf, "Show Leader Line", fontSize, odim/10, i)
  i += self.leaderButton.height + 5
  self.coordinatesButton = Button(self, self , pg, surf, "Show Current Coordinates", fontSize, odim/10, i)
  i += self.coordinatesButton.height + 5
  self.showGridButton = Button(self, self , pg, surf, "Show Grid Lines", fontSize, odim/10, i)
  i += self.showGridButton.height + 5
  self.showGridPointsButton = Button(self, self , pg, surf, "Show Grid Points", fontSize, odim/10, i)
  i += self.showGridPointsButton.height + 5
  self.showGridLabelsButton = Button(self, self , pg, surf, "Show Grid Labels", fontSize, odim/10, i)
  i += self.showGridLabelsButton.height + 5
  self.gridDimLabel = Button(self, self , pg, surf, "Grid Dim:", fontSize, odim/10, i)
  self.gridDimTB = TextBox(pg, surf, self, self, fontSize-4, self.gridDimLabel.x + self.gridDimLabel.width + 10, i,100)
  
  self.menuButton = Button(self, self , pg, surf, "Back to Menu", fontSize, odim/10, odim - (deltaY+5))
  for color in self.colors:
    self.buttons.append(Button(self, self , pg, surf, color[0], fontSize, odim/10, (deltaY+2)*i+dim/3))
    i += self.buttons[len(buttons)-1].height + 5

 def eventHandler(self, event):
  self.gridDimTB.eventHandler(event)
  if event.type == self.pg.MOUSEBUTTONUP:
   self.mouseClicked(event)
 def mouseClicked(self, event):
  if self.menuButton.collision(self.pg.mouse.get_pos()[0], self.pg.mouse.get_pos()[1]):
    self.active = False
    self.parent.active = True
    try:
      if len(self.gridDimTB.data) != 0:
        self.gridDim = int(self.gridDimTB.data)
        intoffset = 30
        if self.gridDim <= 5:
          intoffset = 0
        elif self.gridDim > 30:
          intoffset += 15
        self.unitDim = round((self.surf.get_size()[0]-self.offset-intoffset)/self.gridDim)
    except:
      print("Error not an integer input for grid dimensions!")
    self.gridDimTB.data = ""
  elif self.leaderButton.collision(self.pg.mouse.get_pos()[0], self.pg.mouse.get_pos()[1]):
    self.leaderOn = not self.leaderOn
  elif self.coordinatesButton.collision(self.pg.mouse.get_pos()[0], self.pg.mouse.get_pos()[1]):
    self.showCoordinates = not self.showCoordinates
  elif self.showGridButton.collision(self.pg.mouse.get_pos()[0], self.pg.mouse.get_pos()[1]):
   self.showGrid = not self.showGrid
  elif self.showGridPointsButton.collision(self.pg.mouse.get_pos()[0], self.pg.mouse.get_pos()[1]):
   self.showGridPoints = not self.showGridPoints
  elif self.showGridLabelsButton.collision(self.pg.mouse.get_pos()[0], self.pg.mouse.get_pos()[1]):
   self.showGridLabels = not self.showGridLabels
 def drawButton(self, button, isSelected):
   color = self.buttonBackgroundColor
   if isSelected:
     self.buttonBackgroundColor = self.buttonSelectedBackgroundColor
   button.draw()
   self.buttonBackgroundColor = color

 def draw(self):
   self.gridDimLabel.draw()
   self.gridDimTB.draw()
   self.drawButton(self.leaderButton, self.leaderOn)
   self.drawButton(self.coordinatesButton, self.showCoordinates)
   self.drawButton(self.showGridLabelsButton, self.showGridLabels)
   self.drawButton(self.showGridPointsButton, self.showGridPoints)
   self.drawButton(self.showGridButton, self.showGrid)
   color = self.buttonBackgroundColor
   self.buttonBackgroundColor = pygame.Color(55, 125, 55)
   self.menuButton.draw()
   self.buttonBackgroundColor = color
   for button in self.buttons:
     button.draw()
  
def absPoint(p):
  #removes incoherent +- values from student work
  p.sx = abs(p.sx)
  p.sy = abs(p.sy)
  p.ex = abs(p.ex)
  p.ey = abs(p.ey)
def loadDataFile(filepath):
 file = open(filepath,'r')
 data = file.read()
 file.close()
 x = 0
 arr = []
 maxWidth = 0
 maxHeight = 0
 arr.append(Line(0,0,0,0))
 while x < len(data):
     point = Line(-1,-1,-1,-1)
     start = data.find("(",x)
     if start == -1:
         break
     end = data.find(",", start+1)
     start2 = end+1
     end2 = data.find(")", end)
     point.sx = int(data[start+1 :  end : 1])
     point.sy = int(data[start2 :  end2 : 1])
     #print("start: (", point.sx, ",", point.sy,") ", sep = "", end = " ")
     if end2 >= 0:
         x = end2
     else:
         continue
     start = data.find("(",x+1)
     end = data.find(",", start+1)
     point.ex = int(data[start+1 :  end : 1])
     start = end+1
     end = data.find(")", start)
     point.ey = int(data[start :  end : 1])
     #print("end: (", point.ex, ",", point.ey,")", sep = "")
     absPoint(point)
     arr.append(point)
     maxWidth = max(point.sx, point.ex, maxWidth)
     maxHeight = max(point.sy, point.ey, maxHeight)
     x = end+1
 return arr


#record for a line
class Line:
 def __init__(self,sx,sy,ex,ey):
  self.sx = sx
  self.sy = sy
  self.ex = ex
  self.ey = ey
class FixedWidthButton:
  def __init__(self, settings, screenObj, pg, surf, text, fontSize, x, y, width, height):
    self.screenObj = screenObj
    self.settings = settings
    self.pg = pg
    self.surf = surf
    self.text = text
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.offset = height/10
    self.font = pg.font.SysFont('Calibri', fontSize) 
  def draw(self):
    self.pg.draw.rect(self.surf, self.settings.buttonBackgroundColor, (self.x, self.y, self.width, self.height))
    x = self.x+self.offset
    y = self.y+self.offset
    self.surf.blit(self.font.render(self.text, False, (255, 255, 255)), (x, y))

  def collision(self, point0, point1):
    return point0 >= self.x and point0 <= (self.x+self.width) and point1 >= self.y and point1 <= (self.y+self.height)

class Button:
  def __init__(self, settings, screenObj, pg, surf, text, fontSize, x, y):
    self.screenObj = screenObj
    self.settings = settings
    self.pg = pg
    self.surf = surf
    self.text = text
    self.x = x
    self.y = y
    self.font = pg.font.SysFont('Calibri', fontSize) 
    self.txt_surf = self.font.render(self.text, False, (255, 255, 255))
    self.width = self.txt_surf.get_width()+10
    self.height = fontSize+5
    self.offset = self.height/10
  def draw(self):
    self.pg.draw.rect(self.surf, self.settings.buttonBackgroundColor, (self.x, self.y, self.width, self.height))
    x = self.x+self.offset
    y = self.y+self.offset
    self.surf.blit(self.txt_surf, (x, y))

  def collision(self, point0, point1):
    return point0 >= self.x and point0 <= (self.x+self.width) and point1 >= self.y and point1 <= (self.y+self.height)
#text box class
class TextBox:
  def __init__(self, pg, surf, settings, parent,fontSize ,x,y,width):
    self.parent = parent
    self.fontSize = fontSize
    self.x = x
    self.y = y
    self.width = width
    self.active = False
    self.pg = pg
    self.surf = surf
    self.settings = settings
    self.data = ""
    self.font = pg.font.SysFont('Calibri', fontSize)
    self.color_inactive = pg.Color(125,125,125)
    self.color_active = pg.Color(0,0,0)
    self.color = self.color_inactive
  def collision(self, point):
    txt_surf = self.font.render(self.data, True, self.color)
    self.width = max(self.width, txt_surf.get_width()+10)
    return point[0] > self.x and point[0] < self.x+self.width and point[1] > self.y and point[1] < self.y+self.fontSize+5
  def eventHandler(self,event):
    if event.type == self.pg.MOUSEBUTTONUP:
      if self.collision(event.pos):
        self.active = True
      else:
        self.active = False
      self.color = self.color_inactive
      if self.active:
        self.color = self.color_active
    elif self.active and event.type == self.pg.KEYDOWN:
      if event.key == self.pg.K_BACKSPACE:
        self.data = self.data[:-1]
      elif event.key != self.pg.K_RETURN:
        self.data += event.unicode
  def draw(self):
    txt_surf = self.font.render(self.data, True, self.color)
    # Resize the box if the text is too long.
    self.width = max(self.width, txt_surf.get_width()+10)
   
    self.pg.draw.rect(self.surf, self.color, (int(self.x), int(self.y), int(self.width), int(self.fontSize) + 10))
    self.pg.draw.rect(self.surf, self.pg.Color(225,225,225), (int(self.x)+2, int(self.y)+2, int(self.width)-4, int(self.fontSize) + 10 - 4))
 
    # Blit the text.
    self.surf.blit(txt_surf, (self.x+5, self.y+5))
#Class that handles a set of screens, nested menus can be written too
#ie a Menu than handles other menus
class Menu:
  def __init__(self, pg, surf, settings, screens, menuText):
    self.parent = self
    self.active = False
    self.menuText = menuText
    self.pg = pg
    self.surf = surf
    self.settings = settings
    self.screens = screens
    self.buttons = []
    self.title = (FixedWidthButton(settings, self , pg, surf, "Menu:", 25, settings.odim/5 , (35+2), int(settings.odim/2)+settings.unitDim , 35))
    i = 1
    for screen in self.screens:
      screen.parent = self
      self.buttons.append(FixedWidthButton(settings, screen , pg, surf, screen.menuText, 25, settings.odim/5 , (35+2)*i+settings.unitDim , int(settings.odim/4)*3 , 35))
      i += 1
  def eventHandler(self, event):
    if self.active:
      if event.type == self.pg.MOUSEBUTTONUP:
        self.mouseClicked(event)
    else:
      activeScreen = self.findActive()
      if activeScreen:
        activeScreen.eventHandler(event)
  def mouseClicked(self, event):
    if self.active:
      for button in self.buttons:
        if button.collision(self.pg.mouse.get_pos()[0], self.pg.mouse.get_pos()[1]):
            self.active = False
            button.screenObj.active = True
    else:
      if activeScreen:
        activeScreen.mouseClicked(event)
  def findActive(self):
    if self.active:
      return self
    for screen in self.screens:
      if isinstance(screen, Menu):
        return screen.findActive()
      elif screen.active:
        return screen
    return False
  def draw(self):
    found = False
    if not(self.active):
      for screen in self.screens:
        if isinstance(screen, Menu):
          if screen.active:
            found = screen
            screen.draw()
          else:
             found = screen.draw()
        elif screen.active:
          found = screen
          screen.draw()
      self.active = not(found)
    else:
      found = self
      color = self.settings.buttonBackgroundColor
      self.settings.buttonBackgroundColor = self.pg.Color(105, 55, 55)
      self.title.draw()
      self.settings.buttonBackgroundColor = color
      for button in self.buttons:
        button.draw()
    return found
class Instructions:
#setup memory for object
 def __init__(self, pg, surf, settings):
  self.parent = self
  self.settings = settings
  self.menuText = "Instructions"
  self.pg = pg
  self.surf = surf
  self.active = False
  self.menuButton = Button(settings, self, pg, surf, "Menu", 18, odim-90, odim - 45)
  self.font = pg.font.SysFont('Calibri', 25)  
  self.text = ['1.) Press 0 to delete','all laid lines.','2.) Press 9 to delete','or undo last laid line.','3.) Click on a point','To place a line.','4.) Save/Load buttons','Save/Load to data.txt']
#generic event handler mapper for class
 def eventHandler(self, event):
  if event.type == self.pg.MOUSEBUTTONUP:
   self.mouseClicked(event)
#handler code for when the mouse clicked event occurs
 def mouseClicked(self, event):
  if self.menuButton.collision(self.pg.mouse.get_pos()[0], self.pg.mouse.get_pos()[1]):
    self.active = False
    self.parent.active = True
 def draw(self):
  color = self.settings.buttonBackgroundColor
  self.settings.buttonBackgroundColor = pygame.Color(55, 125, 55)
  self.menuButton.draw()
  self.settings.buttonBackgroundColor = color
  i = 0
  for text in self.text:
   self.surf.blit(self.font.render(text, False, (0, 0, 0)), (15, 15+30*i))
   i += 1
class field:
#List of lines laid down already
 cons  = []
#setup memory for object
 def __init__(self, pg, surf, dim, settings):
  self.parent = self
  settings.gridDim = dim
  self.settings = settings
  self.menuText = "Drawing Grid"
  width = 45
  offset = 80
  i = settings.odim/4
  self.menuButton = Button(settings, self, pg, surf, "Menu", 18, settings.odim-i, settings.odim -  30)
  i += self.menuButton.width + 10
  self.loadButton = Button(settings, self, pg, surf, "Load", 18, settings.odim-(i), settings.odim -  30)
  i += self.loadButton.width + 10
  self.saveButton = Button(settings, self, pg, surf, "Save", 18, settings.odim-(i), settings.odim -  30)
  i += self.saveButton.width + 10
  self.undoButton = Button(settings, self, pg, surf, "Undo", 18, settings.odim-(i), settings.odim -  30)
  self.font = pg.font.SysFont('Calibri', 27)  
  self.cons.append(Line(0,0,0,0))
  self.pg = pg#pygame object
  self.surf = surf#pygame surface object
  self.active = False

 def eventHandler(self, event):
  if event.type == self.pg.MOUSEBUTTONUP:
   self.mouseClicked(event)
  elif event.type == pygame.KEYDOWN:
   if event.key == pygame.K_0:
    self.clearMemory()
   elif event.key == pygame.K_9:
    self.deleteLast()
 def loadFile(self):
   try:
    self.cons = loadDataFile(self.settings.dataFile)
   except:
    print("Error loading file data.txt does not exist")
 def deleteLast(self):
   if(len(self.cons) > 1):
    self.cons.pop()
#handler code for when 0 pushed
 def clearMemory(self):
  self.cons.clear() 
  self.cons.append(Line(0,0,0,0))
#handler code for when enter button pushed
 def saveToFile(self, filePath):
   file = open(filePath, 'w')
   contents = ''
   for line in self.cons[1:]:
    contents += (startTag+': ('+str(line.sx)+', '+str(line.sy)+') '+endTag+': ('+str(line.ex)+', '+str(line.ey)+')\n')
   file.write(contents)
   file.close()
 def calcPointCollision(self, limit):
  dim = self.settings.unitDim
  for y in range(self.settings.gridDim):
   for x in range(self.settings.gridDim):
    lastLine = self.cons[len(self.cons)-1]
    if self.pg.mouse.get_pos()[0] > (x*dim+self.settings.offset-limit) and self.pg.mouse.get_pos()[0] < (x*dim+self.settings.offset+limit) and self.pg.mouse.get_pos()[1] > y*dim+self.settings.offset-limit and self.pg.mouse.get_pos()[1] < y*dim+self.settings.offset+limit:
     if (lastLine.ex !=x or lastLine.ey != y):
      return Line(lastLine.ex, lastLine.ey, x, y)
  return False
#handler code for when the mouse clicked event occurs
 def mouseClicked(self, event):
  if self.menuButton.collision(self.pg.mouse.get_pos()[0], self.pg.mouse.get_pos()[1]):
    self.active = False
    self.parent.active = True
  elif self.loadButton.collision(self.pg.mouse.get_pos()[0], self.pg.mouse.get_pos()[1]):
    self.loadFile()
  elif self.saveButton.collision(self.pg.mouse.get_pos()[0], self.pg.mouse.get_pos()[1]):
    self.saveToFile(self.settings.dataFile)
  elif self.undoButton.collision(self.pg.mouse.get_pos()[0], self.pg.mouse.get_pos()[1]):
    self.deleteLast()
  else:
   if self.settings.unitDim/3 < 7:
    line = self.calcPointCollision(self.settings.unitDim/2)
   else:
    line = self.calcPointCollision(self.settings.unitDim/3)
   if line:
    self.cons.append(line)
  
  for x in range(30):
   self.pg.draw.circle(self.surf, self.pg.Color(0,0,170), self.pg.mouse.get_pos(), int(x/4+2))
   pygame.display.update()
 def draw(self):
  if(self.active):
    self.__draw()
 def __draw(self):
  dim = self.settings.unitDim
  color = self.settings.buttonBackgroundColor
  self.settings.buttonBackgroundColor = pygame.Color(55, 125, 55)
  self.menuButton.draw()
  self.saveButton.draw()
  self.loadButton.draw()
  self.undoButton.draw()
  self.settings.buttonBackgroundColor = color
  #Draw grid, and labels
  if self.settings.showGridLabels:
   for x in range(self.settings.gridDim):
    self.surf.blit(self.font.render(str(x), False, (0, 0, 0)), (x*dim+self.settings.offset-10, 0))
    self.surf.blit(self.font.render(str(x), False, (0, 0, 0)), (10, x*dim+self.settings.offset-10))
  if self.settings.showGrid:
   for x in range(self.settings.gridDim):
    self.pg.draw.line(self.surf, self.settings.gridColor,(self.settings.offset+dim*x,self.settings.offset), (self.settings.offset+dim*x, (self.settings.gridDim-1)*dim+self.settings.offset))
    self.pg.draw.line(self.surf, self.settings.gridColor,(self.settings.offset,dim*x+self.settings.offset),((self.settings.gridDim-1)*dim+self.settings.offset,self.settings.offset+dim*x)) 
  
  #Draw dots
  if self.settings.showGridPoints:
   for y in range(self.settings.gridDim):
    for x in range(self.settings.gridDim):
     self.pg.draw.circle(self.surf, self.settings.dotColor, (int(dim*x+self.settings.offset), int(dim*y+self.settings.offset)), self.settings.unitDim/4)
  #Draw lines placed
  for line in self.cons[1:]:
   self.pg.draw.line(self.surf, self.settings.laidLinesColor, (line.sx*dim+self.settings.offset, line.sy*dim+self.settings.offset), (line.ex*dim+self.settings.offset,line.ey*dim+self.settings.offset), 5)
  #Draw line to cursor
  line = self.cons[len(self.cons)-1]
  if self.settings.leaderOn:
   self.pg.draw.line(self.surf, self.settings.leaderLineColor, (line.ex*dim+self.settings.offset, line.ey*dim+self.settings.offset), self.pg.mouse.get_pos(), 4)
  #calulate string for cursor pos
  pos_str = 'x: '+str(int((self.pg.mouse.get_pos()[0]-self.settings.offset+dim/2)//dim))+' y: '+str(int((self.pg.mouse.get_pos()[1]-self.settings.offset+dim/2)//dim))
  #generate, text from string, then show with blit
  textsurface = self.font.render(pos_str, False, (0, 0, 0))
  if self.settings.showCoordinates:
   if self.pg.mouse.get_pos()[0] < odim/2+dim/2:
    self.surf.blit(textsurface, (self.pg.mouse.get_pos()[0],self.pg.mouse.get_pos()[1]-35))
   else:
    self.surf.blit(textsurface, (self.pg.mouse.get_pos()[0]-dim, self.pg.mouse.get_pos()[1]-35))




odim = 300
#init objects for pygame
pygame.init()
pygame.font.init()
FPS = pygame.time.Clock()
#defines frames per second
FPS.tick(25)
DisplaySurf = pygame.display.set_mode((odim,odim))
#Don't change instatiation of screens for app
settings = Settings(pygame, DisplaySurf, 4, 45)
f = field(pygame, DisplaySurf,4, settings)

insPage = Instructions(pygame, DisplaySurf, settings)
menu = Menu(pygame, DisplaySurf, settings, [f, insPage, settings], "Main Menu")
#f.active = True
while True:
#Fill background with white each frame
 pygame.draw.rect(DisplaySurf, settings.backgroundColor, (0,0,odim,odim))
#Draws anything by searching recursively through a tree of menus, 
#and screens for an active screen/menu
#if none is active this will be set to active
 menu.draw()
#Push updates to screen
 pygame.display.update()
 #Defining event handlers
 for event in pygame.event.get():
  if event.type == pygame.QUIT:
   pygame.quit()
   sys.exit()
  else:
   menu.eventHandler(event)