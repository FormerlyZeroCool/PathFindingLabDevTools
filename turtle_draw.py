import os
import sys
from turtle import *
import math
filepath = '.'
if(len(sys.argv)>1):
    filepath = sys.argv[1]
else:
    print("No instructions supplied <(mandatory) file path, (optional) scale>")
    quit(1)

dataArr = []
class Object(object):
    pass
file = open(filepath,'r')
data = file.read()
file.close()
x = 0
arr = []
def absPoint(p):
    #removes incoherent +- values from student work
    p.start.x = abs(p.start.x)
    p.start.y = abs(p.start.y)
    p.end.x = abs(p.end.x)
    p.end.y = abs(p.end.y)
maxWidth = 0
maxHeight = 0
while x < len(data):
    point = Object()
    start = data.find("(",x)
    if start == -1:
        break
    end = data.find(",", start+1)
    start2 = end+1
    end2 = data.find(")", end)
    point.start = Object()
    point.start.x = int(data[start+1 :  end : 1])
    point.start.y = int(data[start2 :  end2 : 1])
    print("(x, y) start: (", point.start.x, ",", point.start.y,") ", sep = "", end = ' ')
    if end2 >= 0:
        x = end2
    else:
        continue
    start = data.find("(",x+1)
    end = data.find(",", start+1)
    point.end = Object()
    point.end.x = int(data[start+1 :  end : 1])
    start = end+1
    end = data.find(")", start)
    point.end.y = int(data[start :  end : 1])
    print("end: (", point.end.x, ",", point.end.y,")", sep = "")
    absPoint(point)
    arr.append(point)
    maxWidth = max(point.start.x,max(point.end.x, maxWidth))
    maxHeight = max(point.start.y,max(point.end.y, maxHeight))
    x = end+1
point = Object()
point.start = Object()
point.end = Object()
point.start.x = 0
point.start.y = 0
point.end.x = arr[0].start.x
point.end.y = arr[0].start.y
sam = Turtle()
jan = Turtle()
sam.pendown()

def moveTurtle(turtle, p, curAngle, scale):
    newAngle = math.atan2(p.end.y - p.start.y, p.end.x - p.start.x)*180/math.pi
    dist = (math.sqrt((p.end.y - p.start.y)**2 + (p.end.x - p.start.x)**2))
    turtle.right(newAngle - curAngle)
    turtle.forward(scale*dist)
    return newAngle


if(len(sys.argv) > 2):
    scale = int(sys.argv[2])
else:
    scale = 20
sam.penup()
sam.setx(scale*-maxWidth)
sam.sety(scale*maxHeight)
curAngle = moveTurtle(sam, point, 0, scale)
sam.pendown()
sam.showturtle()
def drawInstructions(curAngle, sam, scale):
    for p in arr:
        curAngle = moveTurtle(sam, p, curAngle, scale)
        #print("turning to ",curAngle," s: x",p.start.x,"y",p.start.y," e: x",p.end.x,"y",p.end.y)
#while True:
drawInstructions(curAngle, sam, scale)
#    sam.forward(curAngle/5)
    #scale += 1
screen = Screen()
screen.mainloop()

