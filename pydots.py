import sys
import pygame 
from pygame.locals import *
#Globals for dimensions rendering uses
odim = 600
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
leaderLineColor = pygame.Color(155,0,150)
backgroundColor = pygame.Color(255,255,255)
#record for a line
class Line:
 def __init__(self,sx,sy,ex,ey):
  self.sx = sx
  self.sy = sy
  self.ex = ex
  self.ey = ey
class field:
#List of lines laid down already
 cons  = []
#setup memory for object
 def __init__(self, pg, surf):
  self.font = pg.font.SysFont('Comic Sans MS', 30)  
  self.cons.append(Line(0,0,0,0))
  self.pg = pg#pygame object
  self.surf = surf#pygame surface object
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
 def mouseClicked(self):
  limit = 15
  for y in range(4):
   for x in range(4):
    lastLine = self.cons[len(self.cons)-1]
    if self.pg.mouse.get_pos()[0] > (x*dim+offset-limit) and self.pg.mouse.get_pos()[0] < (x*dim+offset+limit) and self.pg.mouse.get_pos()[1] > y*dim+offset-limit and self.pg.mouse.get_pos()[1] < y*dim+offset+limit:
     if (lastLine.ex !=x or lastLine.ey != y):
      self.cons.append(Line(lastLine.ex, lastLine.ey, x, y))
 def draw(self):
  #Draw grid, and labels
  for x in range(4):
   self.surf.blit(self.font.render(str(x), False, (0, 0, 0)), (x*dim+offset-10, 0))
   self.surf.blit(self.font.render(str(x), False, (0, 0, 0)), (10, x*dim+offset-10))
   self.pg.draw.line(self.surf, gridColor,(offset+dim*x,offset), (offset+dim*x, odim-offset))
   self.pg.draw.line(self.surf, gridColor,(offset,dim*x+offset),(odim-offset,offset+dim*x)) 
  #Draw dots
  for y in range(4):
   for x in range(4):
    self.pg.draw.circle(self.surf, dotColor, (dim*x+offset, dim*y+offset), 10)
  #Draw lines placed
  for line in self.cons:
   self.pg.draw.line(self.surf, laidLinesColor, (line.sx*dim+offset, line.sy*dim+offset), (line.ex*dim+offset,line.ey*dim+offset), 5)
  line = self.cons[len(self.cons)-1]
  #Draw line to cursor
  self.pg.draw.line(self.surf, leaderLineColor, (line.ex*dim+offset, line.ey*dim+offset), self.pg.mouse.get_pos(), 4)
  #calulate string for cursor pos
  pos_str = 'x: '+str((self.pg.mouse.get_pos()[0]-offset+dim/2)//dim)+' y: '+str((self.pg.mouse.get_pos()[1]-offset+dim/2)//dim)
  #generate, text from string, then show with blit
  textsurface = self.font.render(pos_str, False, (0, 0, 0))
  if self.pg.mouse.get_pos()[0] < odim/2:
   self.surf.blit(textsurface, self.pg.mouse.get_pos())
  else:
   self.surf.blit(textsurface, (self.pg.mouse.get_pos()[0]-dim, self.pg.mouse.get_pos()[1]))
  
f = field(pygame, DisplaySurf)
while True:
#Fill background with white each frame
 pygame.draw.rect(DisplaySurf, backgroundColor, (0,0,odim,odim))
#Draw field
 f.draw()
#Push updates to screen
 pygame.display.update()
 #Defining event handlers
 for event in pygame.event.get():
  if event.type == pygame.QUIT:
   pygame.quit()
   sys.exit()
  elif event.type == pygame.MOUSEBUTTONUP:
   f.mouseClicked()
  elif event.type == pygame.KEYDOWN:
   if event.key == pygame.K_RETURN: 
    f.saveToFile('algorithm.txt')
   elif event.key == pygame.K_0:
    f.clearMemory()