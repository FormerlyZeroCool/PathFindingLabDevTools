import sys
import pygame 
from pygame.locals import *
odim = 500
offset = 100/2
dim = (odim - offset*2)/3
pygame.init()
pygame.font.init()
FPS = pygame.time.Clock()
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
backgroundColor = pygame.Color(0,50,0)
class Line:
 def __init__(self,sx,sy,ex,ey):
  self.sx = sx
  self.sy = sy
  self.ex = ex
  self.ey = ey
class field:
 cons  = []

 def __init__(self, pg, surf):
  self.font = pg.font.SysFont('Comic Sans MS', 30)  
  self.cons.append(Line(0,0,0,0))
  self.pg = pg
  self.surf = surf
 def clearMemory(self):
   self.cons.clear() 
   self.cons.append(Line(0,0,0,0))
 def saveToFile(self, filePath):
   file = open(filePath, 'w')
   contents = ''
   for line in self.cons[1:]:
    contents += startTag+': ('+str(line.sx)+', '+str(line.sy)+') '+endTag+': ('+str(line.ex)+', '+str(line.ey)+')\n'
   file.write(contents)
   file.close()
 def mouseClicked(self):
  limit = 15
  match = []
  for y in range(4):
   for x in range(4):
    lastLine = self.cons[len(self.cons)-1]
    if self.pg.mouse.get_pos()[0] > (x*dim+offset-limit) and self.pg.mouse.get_pos()[0] < (x*dim+offset+limit) and self.pg.mouse.get_pos()[1] > y*dim+offset-limit and self.pg.mouse.get_pos()[1] < y*dim+offset+limit:
     self.cons.append(Line(lastLine.ex, lastLine.ey, x, y))
 def draw(self):
  for x in range(4):
   self.surf.blit(self.font.render(str(x), False, (0, 0, 0)), (x*dim+offset-10, 0))
   self.surf.blit(self.font.render(str(x), False, (0, 0, 0)), (10, x*dim+offset-10))
   self.pg.draw.line(self.surf, gridColor,(offset+dim*x,offset), (offset+dim*x, odim-offset))
   self.pg.draw.line(self.surf, gridColor,(offset,dim*x+offset),(odim-offset,offset+dim*x)) 
  for y in range(4):
   for x in range(4):
    self.pg.draw.circle(self.surf, dotColor, (dim*x+offset, dim*y+offset), 10)
  for line in self.cons:
   self.pg.draw.line(self.surf, laidLinesColor, (line.sx*dim+offset, line.sy*dim+offset), (line.ex*dim+offset,line.ey*dim+offset), 4)
  line = self.cons[len(self.cons)-1]
  self.pg.draw.line(self.surf, leaderLineColor, (line.ex*dim+offset, line.ey*dim+offset), self.pg.mouse.get_pos(), 3)
  pos_str = 'x: '+str((self.pg.mouse.get_pos()[0]-offset+dim/2)//dim)+' y: '+str((self.pg.mouse.get_pos()[1]-offset+dim/2)//dim)
  #print(pos_str)
  textsurface = self.font.render(pos_str, False, (0, 0, 0))
  if self.pg.mouse.get_pos()[0] < 350:
   self.surf.blit(textsurface, self.pg.mouse.get_pos())
  else:
   self.surf.blit(textsurface, (self.pg.mouse.get_pos()[0]-150, self.pg.mouse.get_pos()[1]))
  
f = field(pygame, DisplaySurf)
while True:
 pygame.draw.rect(DisplaySurf, backgroundColor, (0,0,odim,odim))
 f.draw()
 pygame.display.update()
 for event in pygame.event.get():
  if event.type == QUIT:
   pygame.quit()
   sys.exit()
  elif event.type == pygame.MOUSEBUTTONUP:
   f.mouseClicked()
  elif event.type == pygame.KEYDOWN:
   if event.key == pygame.K_RETURN: 
    f.saveToFile('algorithm.txt')
   elif event.key == pygame.K_0:
    f.clearMemory()
