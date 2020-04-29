# -*- coding: utf-8 -*-
import math
"""
Mag. Stefan Hagmann 2020
This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/ or send a letter to Creative Commons,
PO Box 1866, Mountain View, CA 94042, USA.
"""

''' defines a vector '''
class Vector(object):
    #hier werden Classen Attribute erstellt

    #imKonstruktor werden Instanz Attribute erstellt
    def __init__(self, x, y, z):
        #A double underscore: Private variable
        #A single underscore: Protected variable
        self._koord = [x,y,z]
        self._name = "vec"

    def _getX(self):
        return self._koord[0]

    def _getY(self):
        return self._koord[1]

    def _getZ(self):
        return self._koord[2]

    def _setX(self, x):
        self._koord[0] = x

    def _setY(self, y):
        self._koord[1] = y

    def _setZ(self, z):
        self._koord[2] = z

    def _setName(self, name):
        self._name = name

    def _getName(self):
        return self._name

    ''' print out the Vector '''
    def print(self, dim):
        str=""
        for i in range(0, dim):
            str += "%s, " % self._koord[i]
        #Delete last Char
        str = str[:-2]
        print("%s > [%s]" % (self._name, str))

    ''' length of the vector '''
    def length(self):
        return math.sqrt(
            self._koord[0]*self._koord[0] +
            self._koord[1]*self._koord[1] +
            self._koord[2]*self._koord[2]
            )

#-------------------------------------------------------------------------------

''' represents a 3D Vector '''
class Vector3D(Vector):
    def __init__(self, x, y, z):
        self._koord = [x,y,z]
        self._name = "vec"

    def print(self):
        ''' print out the Vector '''
        super().print(3)

    def add(self, v2):
        """ 3D Vector Add """
        self._koord[0] += v2._getX()
        self._koord[1] += v2._getY()
        self._koord[2] += v2._getZ()

#-------------------------------------------------------------------------------

''' represents a 2D Vector '''
class Vector2D(Vector):
    def __init__(self, x, y):
        self._koord = [x,y,0]
        self._name = "vec"

    def print(self):
        ''' print out the Vector '''
        super().print(2)

    def add(self, v2):
        """ 2D Vector Add """
        self._koord[0] += v2._getX()
        self._koord[1] += v2._getY()

    def sub(self, v2):
        """ 2D Vector Sub """
        self._koord[0] -= v2._getX()
        self._koord[1] -= v2._getY()

    def scalar(self, k):
        """ 2D Vector multiply with scalar """
        self._koord[0] *= k
        self._koord[1] *= k

    def length(self):
        """ get length of vector """
        return super().length()

    def unit(self):
        """ make vector length 1 """
        l = self.length()
        self.scalar(1/l)

    def scalarProduct(self, v):
        """ calculate the scalar Product """
        return self._koord[0] * v._getX() + self._koord[1] * v._getY()


    def getAngle(self, v):
        """ get the angle from vector between self and v """
        c = self.scalarProduct(v) / self.length() / v.length()
        return math.acos(c)*180/math.pi
