#!/usr/bin/python3
from xml.sax.handler import ContentHandler
from xml.sax import parse
import os
#mix-in method
#use start/end element method to redirect to the dedicate method you wants, avoiding to write too many if to filter you action to desired method,
#it will provide you capacity to parse different kind of element in the xml files.
class Dispatcher:
    #prefix= start/end, name= page/directory
    def dispatch(self, prefix, name, attrs=None):
        mname = prefix + name.capitalize()
        dname = 'default' + prefix.capitalize()
        method = getattr(self, mname, None)
        #init empty args tuple
        if callable(method): args = ()
        else:
            #put name in tuple arg
            method = getattr(self, dname, None)
            #, change the str to dedicate type
            args = name,
        #if prefix is start put attrs in args
        if prefix == 'start' : args += attrs,
        #return the method
        if callable(method): method(*args)
    def startElement(self, name, attrs):
        self.dispatch('start', name, attrs)
    def endElement(self, name):
        self.dispatch('end', name)
class WebsiteConstructor(Dispatcher, ContentHandler):
    passthrough = False
    def __init__(self, directory):
        self.directory = [directory]
        self.ensureDirectory()
    def ensureDirectory(self):
        path = os.path.join(*self.directory)
        if not os.path.isdir(path): os.makedirs(path)

    def characters(self, chars):
        if self.passthrough: self.out.write(chars)

    def defaultStart(self, name, attrs):
        if self.passthrough:
            self.out.write('<' + name)
            if name == 'a':
                self.out.write(' ')
            for key, val in attrs.items():
                self.out.write('%s="%s"' % (key, val))
            self.out.write('>')
    def defaultEnd(self, name):
        if self.passthrough:
            self.out.write('</%s>' % name)


    def startDirectory(self, attrs):
        self.directory.append(attrs['name'])
        self.ensureDirectory()
    def endDirectory(self):
        self.directory.pop()

    def startPage(self, attrs):
        filename = os.path.join(*self.directory + [attrs['name'] + '.html'])
        self.out = open(filename, 'w')
        self.writeHeader(attrs['title'])
        self.passthrough = True
    def endPage(self):
        self.passthrough = False
        self.writeFooter()
        self.out.close()

    def writeHeader(self, title):
        self.out.write('<html>\n<head>\n    <title>')
        self.out.write(title)
        self.out.write('</title>\n</head>\n     <body>\n')
    def writeFooter(self):
        self.out.write('\n</body>\n</html>\n')
parse('website.xml', WebsiteConstructor('public_html'))
