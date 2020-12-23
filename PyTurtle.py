# -*- coding: utf-8 -*-
"""
Mag. Stefan Hagmann 2020
This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/ or send a letter to Creative Commons,
PO Box 1866, Mountain View, CA 94042, USA.
"""
from gturtle import *
from tjaddons import makeRainbowColor
import math

class PyTurtle:
    normal, fast, ultra = 100, 1000, 10000
    width, height = 0,0
    frame = None
    Pkt = []
    extra_svg_shapes = []

    def __init__(self, size=400):
        self.size = size
        self.makePlayground()
        self.frame = TurtleFrame()
        makeTurtle()
        setColor(makeColor(0x666666))
        setLineWidth(2)
        print "Aufloesung %s x %s" % (self.width,self.height)

        #SVG Punkte
        self.initPktArray(0,0)


    #def __del__(self):
    #    print "Destructor started"

    def getFrame(self):
        return self.frame

    def getSpeed(self, name):
        if name=="normal": return self.normal
        if name=="fast": return self.fast
        if name=="ultra": return self.ultra
        if name=="lightspeed": return -1
        return self.normal

    #mit 4:3 Auflösung
    def makePlayground(self):
        self.height = self.size
        self.width = int (self.size/3*4)
        setPlaygroundSize(self.width, self.height)
        setFramePositionCenter()

    def drawBorders(self):
        #hideturtle()
        ht()
        margin=5
        backup_col = getPenColor()
        setLineWidth(1)

        backup_direction = heading()
        backup_xpos = getX()
        backup_ypos = getY()
        setPenColor(makeColor("000000"))
        setPos(-self.width/2+margin,self.height/2-margin)

        for x in range(0, 2):
            right(90)
            forward(self.width-2*margin)
            right(90)
            forward(self.height-2*margin)

        setPos(backup_xpos,backup_ypos)
        heading(backup_direction)
        setPenColor(backup_col)
        st()

    def speed(self, name):
        if name=="lightspeed":
            hideTurtle()
        else:
            return speed(self.getSpeed(name))

    #File Stuff ========================================================================
    #https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Basic_Shapes
    def write_SVG_header(self, handle):
        self.write_file(handle, '<?xml version="1.0" encoding="UTF-8" standalone="no"?>')
        self.write_file(handle, '<svg')
        self.write_file(handle, 'xmlns:dc="http://purl.org/dc/elements/1.1/"')
        self.write_file(handle, 'xmlns:cc="http://creativecommons.org/ns#"')
        self.write_file(handle, 'xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"')
        self.write_file(handle, 'xmlns:svg="http://www.w3.org/2000/svg"')
        self.write_file(handle, 'xmlns="http://www.w3.org/2000/svg"')
        self.write_file(handle, 'height="%s"' % (self.height))
        self.write_file(handle, 'width="%s"' % (self.width))
        self.write_file(handle, 'version="1.1">')
        self.write_file(handle, '<title>Tigerjython SVG</title>')
        self.write_file(handle, '<desc>Tigerjython SVG</desc>')

    def write_SVG_footer(self, handle):
        self.write_file(handle, '</svg>')

    def open_file(self, name):
        fh = open(name,"w")
        self.write_SVG_header(fh)
        return fh

    def close_file(self, handle):
        self.write_SVG_footer(handle)
        handle.close()

    def write_file(self, handle, data):
        handle.write(data+"\n")
    
    def getX(self, data):
        """extract X from e.g. 200,345"""
        items = data.split(",")
        return items[0].strip()
    
    def getY(self, data):
        """extract Y from e.g. 200,345"""
        items = data.split(",")
        return items[1].strip()  
    
    def getLastMovePoint(self, data):
        """extract the last Move point if there are more of them"""
        # M 266.5,200.0 M 66.5,400.0 
        pts = data.split("M")        
        return pts[len(pts)-1].strip()

        
    def parsePktStr(self, data):
        """extract attributes and create SVG Lines"""
        # clear Empty Attributes []
        pattern = '[]'
        replaceWith = ''
        data = data.replace(pattern, replaceWith)
        
        # break data at Atributes [xxxxx]
        erg = ""
        newdata = []
        for char in data:
            if char != "[" and char != "]" and char != "M":
                erg += char
            else:
                if char == "M":
                    # beginning Move Point
                    newdata.append(erg)
                    erg = "M "
                if char == "[":
                    # beginnender Atrribut Block
                    newdata.append(erg)
                    erg = ""
                if char == "]":
                    # Ende Atrribut Block
                    newdata.append("[%s]" % erg)
                    erg = ""
        newdata.append(erg)
        
        # Erstelle die SVGgetLastMovePoint Paths
        data = []
        style = ""
        for item in newdata:
            if len(item)>0:
                if item[0] == "M":
                    # Move To Command
                    last_item = self.getLastMovePoint(item)
                else:
                    if item[0] == "[":
                        # Attribut
                        style = item[1:-1]  # ohne []
                        pattern = ','
                        replaceWith = ' '
                        style = style.replace(pattern, replaceWith)
                    else:
                        line = '<line x1="%s" y1="%s" x2="%s" y2="%s" %s />' % (self.getX(last_item), self.getY(last_item), self.getX(item), self.getY(item), style)
                        style = ""
                        data.append(line)        
                        last_item = item
        return data

    def write_file_path(self, handle):
        """create SVG Data, color and width are in front within []"""
        pktstr = self.array_to_SVG()
        paths = self.parsePktStr(pktstr)
        
        
        for p in paths:
            self.write_file(handle, p)

        #extra shapes
        for i in range(len(self.extra_svg_shapes)):
            item = self.extra_svg_shapes[i]
            #css einsetzen
            item = item[:-2]
            erg = '%s />' % (item)
            self.write_file(handle, erg)


    def SVG_MoveTo(self, x, y, **kwargs):
        """ move to Coordinates """
        erg = "M %s,%s"
        if "color" in kwargs:
			c = kwargs.get("color")
			erg += ", %s" % c
        if "width" in kwargs:
			w = kwargs.get("width")
			erg += ", %s" % w
        self.Pkt.append([erg % (x, y)])

    def SVG_DrawTo(self, x, y, **kwargs):
		"""
		move to Coordinates
		kwargs > color='#4567AE', width=2
		"""
		erg = "%s,%s"
		if "color" in kwargs:
			c = kwargs.get("color")
			erg += ", %s" % c
		if "width" in kwargs:
			w = kwargs.get("width")
			erg += ", %s" % w
			
		self.Pkt.append([erg % (x, y)])

    def SVG_Circle(self, x, y, radius, **kwargs):
        """ draws a circle, non filled """
        #Transformation to center
        x = x + self.width/2
        y = y + self.height/2
        
        style=""
        if "color" in kwargs:
			c = kwargs.get("color")
			style += 'stroke="%s"' % c
        if "width" in kwargs:
			w = kwargs.get("width")
			style += ' stroke-width="%s"' % w
        self.extra_svg_shapes.append('<circle cx="%s" cy="%s" r="%s" %s fill="transparent" style="fill:none" />' % (x,y,radius, style))

    def initPktArray(self, x, y):
        self.Pkt=[]
        self.Pkt.append(["M %s,%s" % (x,y)])
        
    def getColor(self, data):
        """create Color for SVG Output"""
        return 'stroke="%s"' % data.strip()

    def getWidth(self, data):
        """create Width for SVG Output"""
        return 'stroke-width="%s"' % data.strip()

    #Übergeben wird ein Array aus Array bestehenden aus Punkten mit x,y Koordinaten
    #Erstellt wird ein  String Array aus Punkten im SVG Style
    #[M 130,10], [180,20], [170,10] ...
    # Pkt1x, Pkt1y Pkt2x, Pkt2y ...
    # M ... move to
    # Uppercase ... absolute Koordinaten
    # Lowercase ... relative Koordinaten
    def array_to_SVG(self):
        #Alle Koordinaten auf Mitte Ausgabe beziehen
        TransformedPkt=[]
        for i in range(len(self.Pkt)):
            data = self.Pkt[i]

            prefix=""
            #erster Punkt "M " > für Berechnung herausnehmen
            content = data[0]
            if(content[0:2] == "M "):
                content = content[2:len(content)]
                prefix="M "
            items = content.split(",")
            
            if items[0]:
				x = float(items[0]) + self.width/2
            if items[1]:
				y = float(items[1]) + self.height/2
            
            # Attribute String for Lines
            attrib = "["
            try:
                # color
                color = self.getColor(items[2])
                attrib += "%s," % color
            except Exception as e: 
				pass
				
            try:
                # width
                width = self.getWidth(items[3])
                attrib += "%s" % width
            except Exception as e: 
				pass
            attrib += "]"
            data_str = "%s%s%s,%s" % (attrib, prefix, x, y)

            TransformedPkt.append(data_str)
        erg=""
        
        for i in range(0, len(TransformedPkt)):
            erg += TransformedPkt[i]
            if i!=(len(TransformedPkt)-1):
                erg += " "
        return erg
