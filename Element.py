import pygame
import math
import copy

PI=3.1415926535
EPS=0.00001

class vec2D():
    def __init__(self,dx=0,dy=0):
        self.x = dx
        self.y = dy
    def __deepcopy__(self,memo):
        return vec2D(copy.deepcopy(self._x,memo), copy.deepcopy(self._y,memo))
    def set(self,dx,dy,length=0):
        l,r = 0.0,1e6
        for i in range(100):
            mid=(l+r)/2
            if (mid*dx)**2+(mid*dy)**2 < length**2:
                l=mid
            else:
                r=mid
        self.x=l*dx
        self.y=l*dy
    
    def set_angle(self,a,length=0):
        self._x = length*math.cos(a/180*PI)
        self._y = length*math.sin(a/180*PI)

    def __iadd__(self,other):
        self.x+=other.x
        self.y+=other.y
        return self
    def __isub__(self,other):
        self.x-=other.x
        self.y-=other.y
        return self
    def __imul__(self,other):
        self.x*=other
        self.y*=other
        return self
    def __add__(a,b):
        ret=vec2D(float(a.x),float(a.y))
        ret.x+=b.x
        ret.x+=b.y
        return ret
    def __sub__(a,b):
        ret=vec2D(float(a.x),float(a.y))
        ret.x-=b.x
        ret.x-=b.y
        return ret
    def __mul__(a,b):
        ret=vec2D(float(a.x),float(a.y))
        ret.x*=b
        ret.y*=b
        return ret
    def __eq__(self,other):
        return self.x==other.x and self.y==other.y
    def __ne__(self,other):
        return ~(self==other)
    def get_tuple(self):
        return (self.x,self.y)

def dis(a, b):
    return math.sqrt((a.x-b.x)**2+(a.y-b.y)**2)

class Button:
    def __init__(self,text="click me",pos=vec2D(0,0)):
        self.text=text
        self.pos=pos

class Element:
    def __init__(self,pos=vec2D(0,0)):
        self.text="Mg"
        self.pos=pos
        self.left=False
        self.right=False
        self.up=False
        self.down=False
        self.selected=0
        self.highlight=False
    def detect_mouse(self,pos=vec2D(0,0)):
        # 
        # 0 2 1
        # left -20,-40,+25,-20
        if pos.x<self.pos.x-20 and pos.x>self.pos.x-40 and pos.y<self.pos.y+25 and pos.y>self.pos.y-20:
            # left
            return 1
        elif pos.x<self.pos.x+45 and pos.x>self.pos.x+25 and pos.y<self.pos.y+25 and pos.y>self.pos.y-20:
            # right
            return 2
        elif pos.x<self.pos.x+25 and pos.x>self.pos.x-20 and pos.y<self.pos.y-20 and pos.y>self.pos.y-40:
            # up
            return 3
        elif pos.x<self.pos.x+25 and pos.x>self.pos.x-20 and pos.y<self.pos.y+45 and pos.y>self.pos.y+25:
            # down
            return 4
        elif pos.x<self.pos.x+25 and pos.x>self.pos.x-20 and pos.y<self.pos.y+25 and pos.y>self.pos.y-20:
            # middle
            return 5
        return 0

class Bond:
    def __init__(self,ste=Element(vec2D(0,0)),ede=Element(vec2D(0,0))):
        self.ste=ste
        self.ede=ede
        self.type=1