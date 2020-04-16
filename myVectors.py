# -*- coding: utf-8 -*-
import math

class myVectors:    
    def __init__(self):
        pass
        
    def add(self, v1, v2):
        """ 2D Vector Add """
        return [v1[0]+v2[0], v1[1]+v2[1]]

    def sub(self, v1, v2):
        """ 2D Vector Sub """
        return [v1[0]-v2[0], v1[1]-v2[1]]

    def scalar(self, k, v1):
        """ 2D Vector multiply with scalar """
        return [k*v1[0], k*v1[1]]
    
    def length(self, v):
        """ get length of vector """
        return math.sqrt(v[0]*v[0], v[1]*v[1])
    
    def unit(self, v):
        """ make vectoe length 1 """
        l = self.length(v)
        return self.scalar(1/l, v)
    
    def scalarProduct(self, a, b):
        """ calculate the scalar Product """
        return a[0]*b[0]+a[1]*b[1]
    
    def getAngle(self, p1, p2):
        """ get the angle from vector between p1, p2 """
        a = self.sub(p2, p1)
        #x axis
        b = [10, 0]
        
        c = self.scalarProduct(a, b) / self.length(a) / self.length(b)
        return math.acos(c)*180/math.pi
        

