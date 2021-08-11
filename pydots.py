import sys
import pygame 
from pygame.locals import *
#Globals for dimensions rendering uses
#change odim to change the size of the grid
odim = 300
offset = 100/2
dim = (odim - offset*2)/3
#init objects for pygame
pygame.init()
pygame.font.init()
FPS = pygame.time.Clock()
#defines frames per second
FPS.tick(30)
DisplaySurf = pygame.display.set_mode((odim,odim))
#these two are for what is saved in the algorithm.txt file
startTag = "from"
endTag = "to"
#you can play with the color settings by chaning the paramas given to each
#pygame.Color(red, green, blue)
gridColor = pygame.Color(255,0,0)
dotColor = pygame.Color(5,205,175)
laidLinesColor = pygame.Color(0,60,200)
leaderLineColor = pygame.Color(195,0,190)
backgroundColor = pygame.Color(255,255,255)
buttonBackgroundColor = pygame.Color(125, 125, 125)
#record for a line
class Line:
 def __init__(self,sx,sy,ex,ey):
  self.sx = sx
  self.sy = sy
  self.ex = ex
  self.ey = ey
class Button:
  def __init__(self, screenObj, pg, surf, text, fontSize, x, y, width, height):
    self.screenObj = screenObj
    self.pg = pg
    self.surf = surf
    self.text = text
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.offset = height/10
    self.font = pg.font.SysFont('Comic Sans MS', fontSize) 
  def draw(self):
    self.pg.draw.rect(self.surf, buttonBackgroundColor, (self.x, self.y, self.width, self.height))
    x = self.x+self.offset
    y = self.y+self.offset
    self.surf.blit(self.font.render(self.text, False, (255, 255, 255)), (x, y))

  def collision(self, point0, point1):
    return point0 >= self.x and point0 <= (self.x+self.width) and point1 >= self.y and point1 <= (self.y+self.height)


class Menu:
  def __init__(self, pg, surf, screens):
    self.active = True
    self.pg = pg
    self.surf = surf
    self.screens = screens
    self.buttons = []
    i = 0
    for screen in self.screens:
      self.buttons.append(Button(screen , pg, surf, screen.menuText, 25, dim, dim*i+dim, int(odim/2)+dim, int(dim)))
      i += 1
  def mouseClicked(self):
    if self.active:
      for button in self.buttons:
        if button.collision(self.pg.mouse.get_pos()[0], self.pg.mouse.get_pos()[1]):
            self.active = False
            button.screenObj.active = True
    else:
      for button in self.buttons:
        button.screenObj.mouseClicked(self)
  def draw(self):
    if not(self.active):
      for screen in self.screens:
        if screen.active:
          screen.draw()
    if self.active:
      for button in self.buttons:
        button.draw()
class Instructions:
#setup memory for object
 def __init__(self, pg, surf):
  self.menuText = "Instructions"
  self.pg = pg
  self.surf = surf
  self.active = False
  self.menuButton = Button(self, pg, surf, "Menu", 15, odim-90, odim - 45, 45, 20)
  self.font = pg.font.SysFont('Comic Sans MS', 25)  
  self.text = ['1.) Press enter to save',' to file algorithm.txt','2.) Press 0 to delete','algorithm.','3.) Press 9 to delete','last line.','4.) Click on a point','To place a line.']



#handler code for when the mouse clicked event occurs
 def mouseClicked(self, menu):
  if self.menuButton.collision(self.pg.mouse.get_pos()[0], self.pg.mouse.get_pos()[1]):
    self.active = False
    menu.active = True
 def draw(self):
  self.menuButton.draw()
  i = 0
  for text in self.text:
   self.surf.blit(self.font.render(text, False, (0, 0, 0)), (15, 15+30*i))
   i += 1
class field:
#List of lines laid down already
 cons  = []
#setup memory for object
 def __init__(self, pg, surf):
  self.menuText = "Exit Menu"
  self.menuButton = Button(self, pg, surf, "Menu", 15, odim-90, odim - 35, 45, 20)
  self.font = pg.font.SysFont('Comic Sans MS', 20)  
  self.cons.append(Line(0,0,0,0))
  self.pg = pg#pygame object
  self.surf = surf#pygame surface object
  self.active = False
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
#handler code for when the mouse clicked event occurs
 def mouseClicked(self, menu):
  if self.menuButton.collision(self.pg.mouse.get_pos()[0], self.pg.mouse.get_pos()[1]):
    self.active = False
    menu.active = True
  else:
   limit = 15
   for y in range(4):
    for x in range(4):
     lastLine = self.cons[len(self.cons)-1]
     if self.pg.mouse.get_pos()[0] > (x*dim+offset-limit) and self.pg.mouse.get_pos()[0] < (x*dim+offset+limit) and self.pg.mouse.get_pos()[1] > y*dim+offset-limit and self.pg.mouse.get_pos()[1] < y*dim+offset+limit:
      if (lastLine.ex !=x or lastLine.ey != y):
       self.cons.append(Line(lastLine.ex, lastLine.ey, x, y))
   for x in range(15):
    self.pg.draw.circle(self.surf, self.pg.Color(0,0,170), self.pg.mouse.get_pos(), int(x/2+2))
   pygame.display.update()
 def draw(self):
  if(self.active):
    self.__draw()
 def __draw(self):
  self.menuButton.draw()
  #Draw grid, and labels
  for x in range(4):
   self.surf.blit(self.font.render(str(x), False, (0, 0, 0)), (x*dim+offset-10, 0))
   self.surf.blit(self.font.render(str(x), False, (0, 0, 0)), (10, x*dim+offset-10))
   self.pg.draw.line(self.surf, gridColor,(offset+dim*x,offset), (offset+dim*x, odim-offset))
   self.pg.draw.line(self.surf, gridColor,(offset,dim*x+offset),(odim-offset,offset+dim*x)) 
  #Draw dots
  for y in range(4):
   for x in range(4):
    self.pg.draw.circle(self.surf, dotColor, (int(dim*x+offset), int(dim*y+offset)), 10)
  #Draw lines placed
  for line in self.cons:
   self.pg.draw.line(self.surf, laidLinesColor, (line.sx*dim+offset, line.sy*dim+offset), (line.ex*dim+offset,line.ey*dim+offset), 5)
  line = self.cons[len(self.cons)-1]
  #Draw line to cursor
  self.pg.draw.line(self.surf, leaderLineColor, (line.ex*dim+offset, line.ey*dim+offset), self.pg.mouse.get_pos(), 4)
  #calulate string for cursor pos
  pos_str = 'x: '+str(int((self.pg.mouse.get_pos()[0]-offset+dim/2)//dim))+' y: '+str(int((self.pg.mouse.get_pos()[1]-offset+dim/2)//dim))
  #generate, text from string, then show with blit
  textsurface = self.font.render(pos_str, False, (0, 0, 0))
  if self.pg.mouse.get_pos()[0] < odim/2+dim/2:
   self.surf.blit(textsurface, (self.pg.mouse.get_pos()[0],self.pg.mouse.get_pos()[1]-35))
  else:
   self.surf.blit(textsurface, (self.pg.mouse.get_pos()[0]-dim, self.pg.mouse.get_pos()[1]-35))
  
f = field(pygame, DisplaySurf)
insPage = Instructions(pygame, DisplaySurf)
menu = Menu(pygame, DisplaySurf, [f, insPage])
while True:
#Fill background with white each frame
 pygame.draw.rect(DisplaySurf, backgroundColor, (0,0,odim,odim))
#Draw field
 menu.draw()
#Push updates to screen
 pygame.display.update()
 #Defining event handlers
 for event in pygame.event.get():
  if event.type == pygame.QUIT:
   pygame.quit()
   sys.exit()
  elif event.type == pygame.MOUSEBUTTONUP:
   menu.mouseClicked()
  elif event.type == pygame.KEYDOWN:
   if event.key == pygame.K_RETURN:
    f.saveToFile('algorithm.txt')
   elif event.key == pygame.K_0:
    f.clearMemory()
   elif event.key == pygame.K_9:
    f.deleteLast()