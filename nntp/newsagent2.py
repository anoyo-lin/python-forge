#!/usr/bin/python3
from nntplib import NNTP
from time import strftime, time, localtime
from email import message_from_string
from urllib.request import urlopen
import textwrap
import re

#class1: src=>dest broadcast
#class2: newsitem contains title and body
#class3/4: src thru regex and NNTP server
#class5/6: dest print to plain text AND html format
day = 24 * 60 * 60
def wrap(string, max=70):
    return '\n'.join(textwrap.wrap(string)) + '\n'

class NewsAgent:
    def __init__(self):
        self.sources = []
        self.destinations = []
    def addSource(self, source):
        self.sources.append(source)
    def addDestination(self, destination):
        self.destinations.append(destination)

    def distribute(self):
        
        news_items = []
        for source in self.sources:
            news_items.extend(source.getItems())
            #grasp all items from different sources
        for dest in self.destinations:
            dest.receiveItems(news_items) 
            #both print plain text and wirte into html files

class NewsItem:
    def __init__(self, title, body):
        self.title = title
        self.body = body

class NNTPSource:
    def __init__(self, servername, group, window):
        self.servername = servername
        self.group = group
        self.window = window

    def getItems(self):
        start = localtime(time() - self.window*day)
        date = strftime('%y%m%d', start)
        hour = strftime('%H%M$S', start)

        server = NNTP(self.servername)

        ids = server.newnews(self.group, date, hour)[1]

        for id in ids:
            lines=server.article(id)[3]
            message = message_from_string('\n'.join(lines))

            title = message['subject']
            body = message.get_payload()
            if message.is_multipart():
                body = body[0]
                #body is a list if is a multipart body

            yield NewsItem(title, body)

        server.quit()

class SimpleWebSource:
    def __init__(self, url, titlePattern, bodyPattern):
        self.url = url
        self.titlePattern = re.compile(titlePattern)
        self.bodyPattern = re.compile(bodyPattern)
    def getItems(self):
        text = urlopen(self.url).read().decode('utf-8')
        #bytes type needs to decode as utf-8
        titles = self.titlePattern.findall(text)
        bodys = self.bodyPattern.findall(text)
        for title, body in zip(titles, bodys):
            yield NewsItem(title, wrap(body))

class PlainDestination:
    def receiveItems(self, items):
        for item in items:
            print (item.title)
            print ('_'*len(item.title))
            print (item.body)

class HTMLDestination:
    def __init__(self, filename):
        self.filename = filename
    def receiveItems(self, items):
        out = open(self.filename, 'w')
        #print using the python3 style function
        print ("""
        <html>
            <head>
                <title>Today's News</title>
            </head>
            <body>
            <h1>Today's News</h1>
            """, file=out)
        print ('<ul>', file=out)
        id = 0
        for item in items:
            id +=1
            print ('<li><a href="#%i">%s</a><li>' % (id, item.title), file=out)
        print ('<ul>', file=out)

        id = 0
        for item in items:
            id += 1
            print ('<h2><a name="%i">%s</a><h2>' % (id, item.title), file=out)
            print ('<pre>%s</pre>' % item.body, file=out)
        print ("""
            </body>
        </html>
        """, file=out)
def runDefaultSetup():
    agent = NewsAgent()
    bbc_url = 'http://www.sina.com.cn'
    bbc_title = r'.*a href="([^"]*?)".*'
    #end till first " occured, not greedy behavior.
    #Note that the (?x) flag changes how the expression is parsed. It should be used first in the expression string, or after one or more whitespace characters. If there are non-whitespace characters before the flag, the results are undefined.
    #(?s) meas match multiple result in one line.
    bbc_body = r'.*a href="([^"]*)".*'
    bbc = SimpleWebSource(bbc_url, bbc_title, bbc_body)

    agent.addSource(bbc)
    agent.addDestination(PlainDestination())
    agent.addDestination(HTMLDestination('news.html'))

    agent.distribute()

if __name__ == '__main__': runDefaultSetup()

