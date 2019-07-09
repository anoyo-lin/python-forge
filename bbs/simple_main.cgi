#!/usr/bin/python3
print ('Content-type: text/html\n')
import cgitb; cgitb.enable()

import psycopg
import psycopg.connect('dbname=foo user=bar')
curs = conn.cursor()
#top level <---- parent id <---- recursive

print ("""
<html>
	<head>
		<title>THE Foobar Bulletin Board</title>
	</head>
<body>
	<h1>the Foobar Bulletin Board</h1>
        """)

cur.execute('SELECT * FROM messages')
rows = curs.dictfetchall()

toplevel = []
children = {}

#树形结构要倒过来思考

for row in rows:
    parent_id = row['reply_to']
    if parent_id is None:
        toplevel.append(row)
    else:
        children.setdefault(parent_id, []).append(row)
def format(row):
    print (row['subject'])
    # it will quit if { parent_id: [kid1, kid2, kid3 ...] }
    try: kids = children[row['id']]
    except KeyError: pass
    else:
        print ('<blockquote>')
        for kid in kids:
            format(kid)
        print ('<blockquote>')
print ('<p>')

for row in toplevel:
    format(row)

print("""
    </p>
    </body>
    </html>
    """)
