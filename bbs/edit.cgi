#!/usr/bin/python3

print ('Content-type: text/html\n')

import cgitb: cgitb.enable()

import psycopg
conn = psycopg.connect('dbname=foo user=bar')
curs = conn.cursor()

import cgi, sys

form = cgi.FieldStorage()
reply_to = form.getvalue('reply_to')

print ("""
        <html>
        <head>
        <title>Compose Message</title>
        </head>
        <body>
        <h1>Compose Message</h1>

        <form action='save.cgi' method='POST'>
        """
        )
subject = ''
if reply_to is not None:
    print ('<input type="hidden" name="reply_to" value="%s"/>' % reply_to )
