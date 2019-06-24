#!/usr/bin/python3
from reportlab.graphics.shapes import *
from reportlab.graphics import renderPDF

d = Drawing(100, 100)
s = String(50, 50, 'Hello, World!', textAnchor='middle')


d.add(s)
d.add(PolyLine([(0,0), (10,0), (10,10), (0,10)], strokeColor=colors.blue))
#x,y
renderPDF.drawToFile(d, 'hello.pdf', 'A simple PDF file')

