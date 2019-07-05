#!/usr/bin/env python

import cgi
form = cgi.FieldStorage()

name = form.getvalue('name', 'world')

print ("""Content-type: text/html

<html>
	<head>
		<title>Greeting Page</title>
	</head>
	<body>
		<h1>Hello, %s!</h1>

		<form action='simple3.cgi'>
		Change name <input type='text' name='name' />
		<input type='submit' />
		</form>
	</body>
</html>
""" % name)


text = form.getvalue('text', open('simple_edit.dat').read())
f = open('simple_edit.dat', 'w')
f.write(text)
f.close()
print ("""Content-type: text/html

        <html>
            <head>
                <title>A Simple Editor</title>
            </head>
            <body>
                <form action='simple_edit.cgi' method='POST'>
                <textarea rows='10' cols='20' name='text'>%s </textarea><br />
                <input type='submit' />
                </form>
            </body>
        </html>
    """ % text)
