# Tigerjython
a library to use with Tigerjython

## Usage
### How to include the Library

Change the Python Path, in order to fins your Library
```
import os
rootPath = os.path.abspath(os.path.join(os.path.dirname(__file__)))
#subdirs?
libPath = os.path.join(rootPath, "")
#add libPath to SystemPath
sys.path.insert(0, libPath)
```

### Inside the Code
```
#init the Library
Tool = myTurtle(800)
Tool.makePlayground()

#während des Zeichnes, musst du die SVG Elemente abspeichern
#diese Befehle gibt es momentan

Tool.SVG_Move(x, y)
Tool.SVG_DrawTo(x, y)
Tool.SVG_Circle(x, y, radius)


#am Ende deiner Zeichnung wird die Datei erstellt        
#Ausgabe nach SVG ==================================
fh = Tool.open_file("MeineZeichnung.svg")
css = "stroke:#000000;stroke-width:3px;fill:none;stroke-opacity:1"
Tool.write_file_path(fh, css)
Tool.close_file(fh)
```
