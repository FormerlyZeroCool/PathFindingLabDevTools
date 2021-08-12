

import sys
import pygame
#automatically set later in program
dim = -1

#Globals for dimensions rendering uses
#change odim to change the size of the grid
odim = 300
gridDim = 4
offset = 45

#init objects for pygame
pygame.init()
pygame.font.init()
FPS = pygame.time.Clock()
#defines frames per second
FPS.tick(25)
DisplaySurf = pygame.display.set_mode((odim,odim))
#these two are for what is saved in the algorithm.txt file
startTag = "from"
endTag = "to"
#you can play with the color settings by chaning the paramas given to each
#pygame.Color(red, green, blue)
#settings class for all objects in runtime
class Settings:
 def __init__(self, pg, surf):
  self.menuText = "Settings"
  self.dataFile = "data.txt"
  self.active = False
  self.pg = pg
  self.surf = surf
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
  i = 1
  deltaY = 20
  fontSize = 15
  self.leaderButton = Button(self, self , pg, surf, "Show Leader Line", fontSize, odim/10, (deltaY+2)*i+dim/3, int(odim - odim/5), deltaY)
  i += 1
  self.coordinatesButton = Button(self, self , pg, surf, "Show Current Coordinates", fontSize, odim/10, (deltaY+2)*i+dim/3, int(odim - odim/5), deltaY)
  i += 1
  self.showGridButton = Button(self, self , pg, surf, "Show Grid Lines", fontSize, odim/10, (deltaY+2)*i+dim/3, int(odim - odim/5), deltaY)
  i += 1
  self.showGridPointsButton = Button(self, self , pg, surf, "Show Grid Points", fontSize, odim/10, (deltaY+2)*i+dim/3, int(odim - odim/5), deltaY)
  i += 1
  self.showGridLabelsButton = Button(self, self , pg, surf, "Show Grid Labels", fontSize, odim/10, (deltaY+2)*i+dim/3, int(odim - odim/5), deltaY)
  i += 1
  self.menuButton = Button(self, self , pg, surf, "Back to Menu", fontSize, odim/10, odim - (deltaY+5), int(odim - odim/5), deltaY)
  for color in self.colors:
    self.buttons.append(Button(self, self , pg, surf, color[0], fontSize, odim/10, (deltaY+2)*i+dim/3, int(odim/2)+dim, deltaY))
    i += 1

 def eventHandler(self, event):
  if event.type == self.pg.MOUSEBUTTONUP:
   self.mouseClicked(event)
 def mouseClicked(self, event):
  if self.menuButton.collision(self.pg.mouse.get_pos()[0], self.pg.mouse.get_pos()[1]):
    self.active = False
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
class Button:
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


class Menu:
  def __init__(self, pg, surf, settings, screens):
    self.active = False
    self.pg = pg
    self.surf = surf
    self.settings = settings
    self.screens = screens
    self.buttons = []
    self.title = (Button(settings, self , pg, surf, "Menu:", 25, dim, (35+2), int(odim/2)+dim, 35))
    i = 1
    for screen in self.screens:
      self.buttons.append(Button(settings, screen , pg, surf, screen.menuText, 25, dim, (35+2)*i+dim, int(odim/2)+dim, 35))
      i += 1
  def eventHandler(self, event):
    if self.active:
      if event.type == self.pg.MOUSEBUTTONUP:
        self.mouseClicked(event)
    else:
      for screen in self.screens:
       if screen.active:
         screen.eventHandler(event)
  def mouseClicked(self, event):
    if self.active:
      for button in self.buttons:
        if button.collision(self.pg.mouse.get_pos()[0], self.pg.mouse.get_pos()[1]):
            self.active = False
            button.screenObj.active = True
    else:
      for button in self.buttons:
       if button.screenObj.active:
        button.screenObj.mouseClicked(event)
  def draw(self):
    if not(self.active):
      found = False
      for screen in self.screens:
        if screen.active:
          found = screen
          screen.draw()
      self.active = not(found)
    if self.active:
      color = self.settings.buttonBackgroundColor
      self.settings.buttonBackgroundColor = self.pg.Color(105, 55, 55)
      self.title.draw()
      self.settings.buttonBackgroundColor = color
      for button in self.buttons:
        button.draw()
class Instructions:
#setup memory for object
 def __init__(self, pg, surf, settings):
  self.settings = settings
  self.menuText = "Instructions"
  self.pg = pg
  self.surf = surf
  self.active = False
  self.menuButton = Button(settings, self, pg, surf, "Menu", 18, odim-90, odim - 45, 53, 35)
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
  self.dim = dim
  self.settings = settings
  self.menuText = "Exit Menu"
  width = 45
  offset = 80
  i = 0
  self.menuButton = Button(settings, self, pg, surf, "Menu", 18, odim-(offset+(width+5)*i), odim - 30, width+5, 27)
  i += 1
  self.loadButton = Button(settings, self, pg, surf, "Load", 18, odim-(offset+(width+5)*i), odim - 30, width, 27)
  i += 1
  self.saveButton = Button(settings, self, pg, surf, "Save", 18, odim-(offset+(width+5)*i), odim - 30, width, 27)
  i += 1
  self.undoButton = Button(settings, self, pg, surf, "Undo", 18, odim-(offset+(width+5)*i), odim - 30, width, 27)
  self.font = pg.font.SysFont('Calibri', 27)  
  self.cons.append(Line(0,0,0,0))
  self.pg = pg#pygame object
  self.surf = surf#pygame surface object
  self.active = True

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
  for y in range(self.dim):
   for x in range(self.dim):
    lastLine = self.cons[len(self.cons)-1]
    if self.pg.mouse.get_pos()[0] > (x*dim+offset-limit) and self.pg.mouse.get_pos()[0] < (x*dim+offset+limit) and self.pg.mouse.get_pos()[1] > y*dim+offset-limit and self.pg.mouse.get_pos()[1] < y*dim+offset+limit:
     if (lastLine.ex !=x or lastLine.ey != y):
      return Line(lastLine.ex, lastLine.ey, x, y)
  return False
#handler code for when the mouse clicked event occurs
 def mouseClicked(self, event):
  if self.menuButton.collision(self.pg.mouse.get_pos()[0], self.pg.mouse.get_pos()[1]):
    self.active = False
  elif self.loadButton.collision(self.pg.mouse.get_pos()[0], self.pg.mouse.get_pos()[1]):
    self.loadFile()
  elif self.saveButton.collision(self.pg.mouse.get_pos()[0], self.pg.mouse.get_pos()[1]):
    self.saveToFile(self.settings.dataFile)
  elif self.undoButton.collision(self.pg.mouse.get_pos()[0], self.pg.mouse.get_pos()[1]):
    self.deleteLast()
  else:
   line = self.calcPointCollision(15)
   if line:
    self.cons.append(line)
  
  for x in range(30):
   self.pg.draw.circle(self.surf, self.pg.Color(0,0,170), self.pg.mouse.get_pos(), int(x/4+2))
   pygame.display.update()
 def draw(self):
  if(self.active):
    self.__draw()
 def __draw(self):
  color = self.settings.buttonBackgroundColor
  self.settings.buttonBackgroundColor = pygame.Color(55, 125, 55)
  self.menuButton.draw()
  self.saveButton.draw()
  self.loadButton.draw()
  self.undoButton.draw()
  self.settings.buttonBackgroundColor = color
  #Draw grid, and labels
  if self.settings.showGridLabels:
   for x in range(self.dim):
    self.surf.blit(self.font.render(str(x), False, (0, 0, 0)), (x*dim+offset-10, 0))
    self.surf.blit(self.font.render(str(x), False, (0, 0, 0)), (10, x*dim+offset-10))
  if self.settings.showGrid:
   for x in range(self.dim):
    self.pg.draw.line(self.surf, self.settings.gridColor,(offset+dim*x,offset), (offset+dim*x, (self.dim-1)*dim+offset))
    self.pg.draw.line(self.surf, self.settings.gridColor,(offset,dim*x+offset),((self.dim-1)*dim+offset,offset+dim*x)) 
  #Draw dots
  if self.settings.showGridPoints:
   for y in range(self.dim):
    for x in range(self.dim):
     self.pg.draw.circle(self.surf, self.settings.dotColor, (int(dim*x+offset), int(dim*y+offset)), 10)
  #Draw lines placed
  for line in self.cons[1:]:
   self.pg.draw.line(self.surf, self.settings.laidLinesColor, (line.sx*dim+offset, line.sy*dim+offset), (line.ex*dim+offset,line.ey*dim+offset), 5)
  line = self.cons[len(self.cons)-1]
  #Draw line to cursor
  if self.settings.leaderOn:
   self.pg.draw.line(self.surf, self.settings.leaderLineColor, (line.ex*dim+offset, line.ey*dim+offset), self.pg.mouse.get_pos(), 4)
  #calulate string for cursor pos
  pos_str = 'x: '+str(int((self.pg.mouse.get_pos()[0]-offset+dim/2)//dim))+' y: '+str(int((self.pg.mouse.get_pos()[1]-offset+dim/2)//dim))
  #generate, text from string, then show with blit
  textsurface = self.font.render(pos_str, False, (0, 0, 0))
  if self.settings.showCoordinates:
   if self.pg.mouse.get_pos()[0] < odim/2+dim/2:
    self.surf.blit(textsurface, (self.pg.mouse.get_pos()[0],self.pg.mouse.get_pos()[1]-35))
   else:
    self.surf.blit(textsurface, (self.pg.mouse.get_pos()[0]-dim, self.pg.mouse.get_pos()[1]-35))

#Don't change instatiation of screens for app
settings = Settings(pygame, DisplaySurf)
f = field(pygame, DisplaySurf,gridDim, settings)
dim = round((odim-offset)/f.dim)
insPage = Instructions(pygame, DisplaySurf, settings)
menu = Menu(pygame, DisplaySurf, settings, [f, insPage, settings])
while True:
#Fill background with white each frame
 pygame.draw.rect(DisplaySurf, settings.backgroundColor, (0,0,odim,odim))
#Draw field
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