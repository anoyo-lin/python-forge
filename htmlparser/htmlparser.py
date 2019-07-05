#!/usr/bin/python3

from urllib.request import urlopen
from html.parser import HTMLParser
#structure
#h3
#a
#
#/a
#/h3

class Scrapper(HTMLParser):

    in_h3 = False
    in_link = False
    #xml tag, attributes in tag
    #attrs can convert into dictionary
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'li':
            self.in_h3 = True

        if tag == 'a' and 'href' in attrs:
            self.in_link = True
            #create a list of chunks
            self.chunks = []
            self.url = attrs['href']
    def handle_data(self, data):
        if self.in_link:
            self.chunks.append(data)

    def handle_endtag(self, tag):
        if tag == 'h3':
            self.in_h3 = False
        if tag == 'a':
            if self.in_h3 and self.in_link:
                print ('%s (%s)' % ( ''.join(self.chunks), self.url))
            self.in_link = False

text = urlopen('http://python.org/community/jobs').read().decode('utf-8')
print (text); input()
parser = Scrapper()
#inherited method
parser.feed(text)
parser.close()
