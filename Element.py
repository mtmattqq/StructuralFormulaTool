import pygame
import math
import copy
import cmath

PI=3.1415926535
EPS=0.00001
id=0
bid=0
bbid=1000000010
programIcon=pygame.image.load('icon.jpg')

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

def dis(a,b):
    return math.sqrt((a.x-b.x)**2+(a.y-b.y)**2)

def dot(a,b):
    return a.x*b.x+a.y*b.y

class Element:
    def __init__(self,pos=vec2D(0,0)):
        global id
        self.text="C"
        self.pos=pos
        self.left=False
        self.right=False
        self.up=False
        self.down=False
        self.selected=0
        self.highlight=False
        self.isDefault=False
        self.id=id
        id+=1
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
        elif pos.x<self.pos.x+45 and pos.x>self.pos.x+25 and pos.y<self.pos.y-20 and pos.y>self.pos.y-40:
            # right up
            return 6
        return 0

class Bond:
    def __init__(self,ste=Element(vec2D(0,0)),ede=Element(vec2D(0,0))):
        global bid
        self.ste=ste
        self.ede=ede
        self.type=1
        self.id=bid
        bid+=1
    def detect_mouse(self,pos=vec2D(0,0)):
        # return True or False
        f1=self.ste.pos.y-self.ede.pos.y
        f2=-(self.ste.pos.x-self.ede.pos.x)
        f3=-(self.ste.pos.x*f1+self.ste.pos.y*f2)
        if (pos.x*f1+pos.y*f2+f3)**2<(20**2)*(f1**2+f2**2):
            pb=vec2D(self.ede.pos.x-pos.x,self.ede.pos.y-pos.y)
            pa=vec2D(self.ste.pos.x-pos.x,self.ste.pos.y-pos.y)
            if dot(pa,pb)<=0:
                return True
        return False
    
class Button:
    def __init__(self,text="click me",pos=vec2D(0,0),color=[0,0,0],bd=Bond()):
        self.text=text
        self.pos=pos
        self.color=color
        self.type=1
        self.bond=bd
    def detect_mouse(self,pos=vec2D(0,0)):
        if pos.x<self.pos.x+20 and pos.x>self.pos.x and pos.y<self.pos.y+20 and pos.y>self.pos.y:
            return True
        return False

# not finishe yet
rotate=complex(0.5,0.866025404)
benzene_size=50
class Benzene:
    def __init__(self,pos=vec2D(0,0)):
        global bid
        self.pos=pos
        self.elements=[Element(vec2D(pos.x+benzene_size,pos.y))]
        self.elements[0].id+=bbid
        self.id=bid
        self.highlight=False
        bid+=1
        tp=complex(benzene_size,0)
        for i in range(5):
            tp*=rotate
            newElement=Element(vec2D(tp.real+pos.x,tp.imag+pos.y))
            newElement.id+=bbid
            self.elements.append(newElement)
    def set(self):
        self.elements[0].pos=vec2D(self.pos.x+benzene_size,self.pos.y)
        tp=complex(benzene_size,0)
        for i in range(1,6):
            tp*=rotate
            self.elements[i].pos=vec2D(tp.real+self.pos.x,tp.imag+self.pos.y)
    def detect_mouse(self,pos=vec2D(0,0)):
        idx=0
        # select the certain element
        for element in self.elements:
            if dis(vec2D(element.pos.x,element.pos.y),pos)<15:
                return idx
            idx+=1
        # select main part
        if dis(self.pos,pos)<50:
            return 6
        if dis(vec2D(self.pos.x+50,self.pos.y-50),pos)<10:
            return 7
        # not being selected
        return -1