#!/usr/bin/python3
from urllib.request import urlopen
from reportlab.graphics.shapes import *
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.textlabels import Label
from reportlab.graphics import renderPDF

#URL = 'http://www.swpc.noaa.goc/ftpdir/weekly/Perdict.txt'
URL = 'https://services.swpc.noaa.gov/text/predicted-sunspot-radio-flux.txt'
COMMENT_CHARS = '#:' 

drawing = Drawing(400, 200)
data = []
for line in urlopen(URL).readlines():
    if not line.isspace() and not line.decode('ascii')[0] in COMMENT_CHARS:
        data.append([float(n) for n in line.split()])

nr_pred = [row[2] for row in data]
nr_high = [row[3] for row in data]
nr_low = [row[4] for row in data]
flux_pred = [row[5] for row in data]
flux_high = [row[6] for row in data]
flux_low = [row[7] for row in data]
times = [row[0] + row[1]/12.0 for row in data]

lp=LinePlot()
lp.x = 50
lp.y = 50
lp.height = 125
lp.width = 300
lp.data = [list(zip(times, nr_pred)), list(zip(times, nr_high)), list(zip(times, nr_low)), list(zip(times, flux_pred)), list(zip(times, flux_high)), list(zip(times, flux_low))]
lp.lines[0].strokeColor = colors.blue
lp.lines[1].strokeColor = colors.red
lp.lines[2].strokeColor = colors.green
lp.lines[3].strokeColor = colors.blue
lp.lines[4].strokeColor = colors.red
lp.lines[5].strokeColor = colors.green

drawing.add(lp)

drawing.add(String(250, 150, 'Sunspots', fontSize=14, fillColor=colors.red))

renderPDF.drawToFile(drawing, 'report2.pdf', 'Sunspots')
