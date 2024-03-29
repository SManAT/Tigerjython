# Tigerjython
a library to use with Tigerjython

## Usage
### How to include the Library

Change the Python Path, in order to find your Library
```
import os
rootPath = os.path.abspath(os.path.join(os.path.dirname(__file__)))
#subdirs?
libPath = os.path.join(rootPath, "")
#add libPath to SystemPath
sys.path.insert(0, libPath)

# e.g.
from PyTurtle import PyTurtle
```

### Inside the Code
```python
#init the Library
Tool = PyTurtle(800)
Tool.makePlayground()

#during the drawing you have to write also to SVG
#these commands exists up to now
Tool.SVG_Move(x, y)
Tool.SVG_DrawTo(x, y)
Tool.SVG_Circle(x, y, radius)

#write to SVG ==================================
fh = Tool.open_file("MeineZeichnung.svg")
Tool.write_file_path(fh, css)
Tool.close_file(fh)
```
You can use some CCS Styles for the shapes
There is an Default Style for all Shapes. You can change it with
```
Tool.setDefaultStyle(fill="none", stroke="rgb(0,0,0)", stroke_width="2")
```
Also you can specify Styles for each Methode
```
Tool.SVG_DrawTo(x, y, stroke="rgb(255,0,0)", stroke_width="2")
Tool.SVG_Circle(x, y, radius, fill="none", stroke="rgb(0,0,0)", stroke_width="2")
```

### Lindenmayer System
```python
LSystem = PyLSystem()
LSystem.length = 100
LSystem.alpha = 120
LSystem.axiom = "F-G-G"

#Rules
regel = ["G", "GG"]
regel_1 = ["F", "F-G+F+G-F"]
#add the rules
LSystem.addRegel(regel)
LSystem.addRegel(regel_1)
print "Axiom: %s" % (LSystem.axiom)

#iterate
LSystem.debug = True;
LSystem.iterate(iterationen)

#draw
LSystem.draw(Tool)
```
### Vectors
```python
v1 = Vector2D(1,2)
v2 = Vector2D(3,3)
v1.output()
v2.output()

v1.add(v2)
v1.output()
v1.sub(v2)
v1.output()

v1.unit()
v1.output()

print(v1.getAngle(v2))
```
