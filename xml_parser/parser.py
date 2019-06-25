#!/usr/bin/python3
from xml.sax.handler import ContentHandler
from xml.sax import parse

class HeadlineHandler(ContentHandler):
        in_headline = False
        def __init__(self, headlines):
            ContentHandler.__init__(self)
            self.headlines = headlines
            self.data = []
        def startElement(self, name, attrs):
            if name == 'hl':
                self.in_headline = True
        def endElement(self, name):
            if name == 'hl':
                text = ''.join(self.data)
                self.data = []
                self.headlines.append(text)
                self.in_headline = False
        def characters(self, string):
            if self.in_headline:
                self.data.append(string)
headlines = []
parse('website.xml', HeadlineHandler(headlines))

print ('the following <hl> elements were found:')
for h in headlines:
    print (h)

