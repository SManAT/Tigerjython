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
    debug = False
    
    normal, fast, ultra = 100, 1000, 10000
    width, height = 0, 0
    frame = None
    Pkt = []
    extra_svg_shapes = []
    defaultstyle = "fill:none;stroke:rgb(0,0,0);stroke-width:2"

    def __init__(self, size=400):
        self.size = size
        self.makePlayground()
        self.frame = TurtleFrame()
        makeTurtle()
        setColor(makeColor(0x666666))
        setLineWidth(2)
        print "Aufloesung %s x %s" % (self.width, self.height)

        # SVG Punkte
        self.initPktArray(0, 0)

    # def __del__(self):
    #    print "Destructor started"

    def setDefaultStyle(self, str):
      self.defaultstyle = str

    def getFrame(self):
        return self.frame

    def getSpeed(self, name):
        if name == "normal":
            return self.normal
        if name == "fast":
            return self.fast
        if name == "ultra":
            return self.ultra
        if name == "lightspeed":
            return -1
        return self.normal

    # mit 4:3 Auflösung
    def makePlayground(self):
        self.height = self.size
        self.width = int(self.size/3*4)
        setPlaygroundSize(self.width, self.height)
        setFramePositionCenter()

    def drawBorders(self):
        # hideturtle()
        ht()
        margin = 5
        backup_col = getPenColor()
        setLineWidth(1)

        backup_direction = heading()
        backup_xpos = getX()
        backup_ypos = getY()
        setPenColor(makeColor("000000"))
        setPos(-self.width/2+margin, self.height/2-margin)

        for x in range(0, 2):
            right(90)
            forward(self.width-2*margin)
            right(90)
            forward(self.height-2*margin)

        setPos(backup_xpos, backup_ypos)
        heading(backup_direction)
        setPenColor(backup_col)
        st()

    def speed(self, name):
        if name == "lightspeed":
            hideTurtle()
        else:
            return speed(self.getSpeed(name))

    # File Stuff ========================================================================
    # https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Basic_Shapes
    def write_SVG_header(self, handle):
        self.write_file(
            handle, '<?xml version="1.0" encoding="UTF-8" standalone="no"?>')
        self.write_file(handle, '<svg')
        self.write_file(handle, 'xmlns:dc="http://purl.org/dc/elements/1.1/"')
        self.write_file(handle, 'xmlns:cc="http://creativecommons.org/ns#"')
        self.write_file(
            handle, 'xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"')
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
        fh = open(name, "w")
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

    def SplitPoints(self, data):
        """ 
        splitte Points 
        828.442325904,452.0944533##fill:none;fill-opacity:1;stroke:rgb(255,0,0);stroke-width:2 23,12## 23,23....
        M533.0,400.0 [stroke:#4567AE,stroke-width:2]733.0,500.0 -->
        M533.0,400.0, [stroke:#4567AE,stroke-width:2], 733.0,500.0
        """
        erg = []
        if len(data) > 0:
            items = data.split(" ")
            first = True
            for item in items:
              # try split on ]
              part = item.split("]")
              if len(part)>1:
                # hat style
                erg.append("%s]" % part[0])
                erg.append(part[1])
              else:
                erg.append(item)
        return erg

    def getStyles(self, txt):
        """ extract from '633.0,400.0##stroke:rgb(255,0,0);stroke-width:2' styles and coordinates """
        parts = txt.split("##")
        # gibt es immer
        coordinates = parts[0]
        # muss es nicht geben
        try:
          styles = parts[1]
        except:
          styles = ""
        return [coordinates, styles]

    def clearStyleSeperator(self, pt):
      """ 230,456## zu 230,456 """
      data = pt.split('##')
      return data[0]

    def parsePktStr(self, data):
        """extract attributes and create SVG Lines"""
        # Data sieht so aus 
        # M533.0,400.0## M533.0,400.0## 633.0,400.0##stroke:rgb(255,0,0);stroke-width:2 633.0,500.0##stroke:rgb(255,0,0);stroke-width:2

        # Split am Leerzeichen
        newdata = self.SplitPoints(data)

        # Erstelle die SVG Linien
        data = []
        style = ""
        # ['M533.0,400.0##', 'M533.0,400.0##', '633.0,400.0##stroke:rgb(255,0,0);stroke-width:2', '633.0,500.0##stroke:rgb(255,0,0);stroke-width:2']
        if self.debug:
          print("Newdata: %s" % newdata)

        # we draw allwasy lines from startPt to endPt
        startPt = ""
        endPt = ""
        for item in newdata:
            if len(item) > 0:
                # print("Item: %s" % item)
                new_item = self.getStyles(item)
                if new_item[0][0] == "M":
                    # Move To Command
                    startPt = self.clearStyleSeperator(item[1:])  # ohne M                
                else:
                    # Start und Endpoint the same?
                    endPt = self.clearStyleSeperator(new_item[0])
                    style = new_item[1]

                    if self.getX(startPt) != self.getX(endPt) or self.getY(startPt) != self.getY(endPt):
                        if len(style) == 0:
                            style = self.defaultstyle
                        if self.debug:
                          print("Line:  %s, %s -> %s, %s" % (self.getX(startPt), self.getY(startPt), self.getX(endPt), self.getY(endPt)))    
                        print("Line:  %s, %s -> %s, %s" % (self.getX(startPt), self.getY(startPt), self.getX(endPt), self.getY(endPt)))    
                        line = '<line x1="%s" y1="%s" x2="%s" y2="%s" style="%s" />' % (self.getX(startPt), self.getY(startPt), self.getX(endPt), self.getY(endPt), style)
                        data.append(line)
                    else:
                        pass
                    startPt = endPt
        return data

    def write_file_path(self, handle):
        """create SVG Data, color and width are in front within []"""
        pktstr = self.array_to_SVG()
        paths = self.parsePktStr(pktstr)

        for p in paths:
            self.write_file(handle, p)

        # extra shapes
        for i in range(len(self.extra_svg_shapes)):
            item = self.extra_svg_shapes[i]
            # css einsetzen
            item = item[:-2]
            erg = '%s />' % (item)
            self.write_file(handle, erg)

    def handle_Styles(self, kwargs):
      styles = ""
      if "fill" in kwargs:
            w = kwargs.get("fill")
            styles += ';fill:%s;fill-opacity:1' % w
      if "stroke" in kwargs:
          w = kwargs.get("stroke")
          styles += ";stroke:%s" % w
      if "stroke_width" in kwargs:
          w = kwargs.get("stroke_width")
          styles += ";stroke-width:%s" % w
      # dont start with ,
      if styles != "":
        if styles[:1]==";":
          styles = styles[1:]
      return styles

    def SVG_MoveTo(self, x, y, **kwargs):
        """ move to Coordinates """
        erg = "M%s,%s"
        # Move to hat keine Styles!
        self.Pkt.append([erg % (x, y)])

    def SVG_DrawTo(self, x, y, **kwargs):
        """ move to Coordinates """
        erg = "%s,%s"
        if len(kwargs.items()) != 0:
          styles = self.handle_Styles(kwargs)
        else:
          styles = self.defaultstyle
        # Styles werden von den Koordinaten mit ## getrennt
        erg += "##%s" % styles
        self.Pkt.append([erg % (x, y)])

    def SVG_Circle(self, x, y, radius, **kwargs):
        """ draws a circle, non filled """
        # Transformation to center
        x = x + self.width/2
        y = y + self.height/2

        if len(kwargs.items()) != 0:
          styles = self.handle_Styles(kwargs)
        else:
          styles = self.defaultstyle

        self.extra_svg_shapes.append(
            '<circle cx="%s" cy="%s" r="%s" style="%s" />' % (x, y, radius, styles))

    def initPktArray(self, x, y):
        self.Pkt = []
        self.Pkt.append(["M%s,%s" % (x, y)])

    def getColor(self, data):
        """create Color for SVG Output"""
        return 'stroke:%s' % data.strip()

    def getWidth(self, data):
        """create Width for SVG Output"""
        return 'stroke-width:%s' % data.strip()

    # Übergeben wird ein Array aus Arrays bestehenden aus Punkten mit x,y Koordinaten
    # Erstellt wird ein  String Array aus Punkten im SVG Style
    # [M 130,10], [M 180,20], [170,10] ...
    # Pkt1x, Pkt1y Pkt2x, Pkt2y ...
    # M ... move to
    # Uppercase ... absolute Koordinaten
    # Lowercase ... relative Koordinaten
    def array_to_SVG(self):
        # Alle Koordinaten auf Mitte Ausgabe beziehen
        TransformedPkt = []
        if self.debug:
          print("Original Data: %s" % self.Pkt)

        for i in range(len(self.Pkt)):
            data = self.Pkt[i]

            prefix = ""
            # extract "M "
            content = data[0]
            if(content[0] == "M"):
                content = content[1:len(content)]
                prefix = "M"

            # are there Styles [3,5##color: rgb... ]?
            parts = content.split("##")
            coordinates = parts[0]
            items = coordinates.split(",")
            
            # muss es nicht geben
            try:
              styles = parts[1]
            except:
              styles = ""
            
            if items[0]:
                x = float(items[0]) + self.width/2
            if items[1]:
                y = float(items[1]) + self.height/2

            data_str = "%s%s,%s##%s" % (prefix, x, y, styles)
            TransformedPkt.append(data_str)

        erg = ""
        for i in range(0, len(TransformedPkt)):
            erg += TransformedPkt[i]
            if i != (len(TransformedPkt)-1):
                erg += " "
        if self.debug:
          print("Transformed Data: %s" % erg)
        return erg
