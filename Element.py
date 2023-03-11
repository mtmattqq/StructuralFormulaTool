import pygame
import math
import copy

PI=3.1415926535
EPS=0.00001

class vec2D():
    def __init__(self,dx=0,dy=0):
        self._x = dx
        self._y = dy
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
        self._x=l*dx
        self._y=l*dy
    
    def set_angle(self,a,length=0):
        self._x = length*math.cos(a/180*PI)
        self._y = length*math.sin(a/180*PI)

    def __iadd__(self,other):
        self._x+=other.x
        self._y+=other.y
        return self
    def __isub__(self,other):
        self._x-=other.x
        self._y-=other.y
        return self
    def __imul__(self,other):
        self._x*=other
        self._y*=other
        return self
    def __add__(a,b):
        ret=vec2D(float(a.x),float(a.y))
        ret._x+=b.x
        ret._x+=b.y
        return ret
    def __sub__(a,b):
        ret=vec2D(float(a.x),float(a.y))
        ret._x-=b.x
        ret._x-=b.y
        return ret
    def __mul__(a,b):
        ret=vec2D(float(a.x),float(a.y))
        ret._x*=b
        ret._y*=b
        return ret
    def __eq__(self,other):
        return self.x==other.x and self.y==other.y
    def __ne__(self,other):
        return ~(self==other)
    def get_tuple(self):
        return (self.x,self.y)
    
    # 讀取
    @property
    def x(self):
        return self._x
    @property
    def y(self):
        return self._y

    # 寫入
    @x.setter
    def x(self,num):
        self._x = num
    @y.setter
    def y(self,num):
        self._y = num

def dis(a, b):
    return math.sqrt((a.x-b.x)**2+(a.y-b.y)**2)

class Element:
    def __init__(self):
        text="C"