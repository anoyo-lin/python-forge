#!/usr/bin/python3

print ('Content-type: text/html\n')

import cgitb: cgitb.enable()

import psycopg
conn = psycopg.connect('dbname=foo user=bar')
curs = conn.cursor()

print ("""
        <html>
        <head>
            <title>The FooBar Bulletin Board</title>
        </head>
        <body>
            <h1>The Foobar Bulletin Board</h1>
            """)

curs.execute('SELECT * FROM messages')
rows = curs.dictfetchall()

toplevel = []
children = {}
for row in rows:
    if row['reply_to'] == None:
        toplevel.append(row)
    else:
        children.setdefault(row['reply_to'], []).append(row)

def explore(row):
    print (row['subject'])
    print ('<p><a href="view.cgi?id=%(id)i">%(subject)s</a></p>' % row)
    try:
        have_children = children[row['id']]
    except KeyError:
        pass
    else:
        print ('<blockquote>')
        for child in have_children:
            explore(child)
        print ('<blockquote>')
print ('<p>')

for row in toplevel:
    explore(row)

print ("""
        </p>
        <hr />
        <p><a href="edit.cgi">Post message</a></p>
        </body>
    </html>
""")

