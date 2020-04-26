# -*- coding: utf-8 -*-
"""
This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/ or send a letter to Creative Commons,
PO Box 1866, Mountain View, CA 94042, USA.
"""
from gturtle import *
import math

class myLSystem:
	alpha=90
	axiom=""
	regeln = []

	debug=False
	code=[]
	length=100;

	def __init__(self):
		pass

	def output(self, msg):
		if self.debug==True:
			print msg

	''' Eine Regel wird zum Regelwerk aufgenommen '''
	def addRegel(self, regel):
		self.regeln.append(regel)

	''' Die Iterationen werden durchgeführt '''
	def iterate(self, iterationen):
		ht()
		code = self.axiom
		for i in range(iterationen+1):
			#arbeite alle Regeln durch
			for k in range(len(self.regeln)):
				item = self.regeln[k]
				code = code.replace(item[0], item[1])
				self.output(code)
		print "Fertiger Code: %s" % (code)
		self.code = code
		st()

	''' zeichnet das L System '''
	def draw(self, Tool):
		for char in self.code:
			if char=="F":
				forward(self.length)
				Tool.SVG_DrawTo(getX(), getY())
				#self.output("F: %s" % self.length)

			elif char=="+":
				left(self.alpha)
				#self.output("+: %s" % self.alpha)

			elif char=="-":
				right(self.alpha)
				#self.output("-: %s" % self.alpha)

			elif char=="f":
				pu()
				forward(self.length)
				pd()
				Tool.SVG_MoveTo(getX(), getY())
				#self.output("f: %s" % self.length)
			else:
				#default
				#self.output("Konstante: %s" % char)
				forward(self.length)
				Tool.SVG_DrawTo(getX(), getY())
