#!/usr/bin/python3

import cgi
form = cgi.FieldStorage()

text = form.getvalue('text', open('simple_edit.dat').read())
f = open('simple_edit.dat', 'w')
f.write(text)
f.close()
#the below code just change the display of current text box to the box you modified before. 
#when you submit you just POST the text in the box into text and write it into simple_edit.dat
print ("""Content-type: text/html

<html>
	<head>
	<title>A Simple Editor</title>
	</head>
<body>
	<form action='simple_edit.cgi' method='POST'>
	<textarea rows='10' cols='20' name='text'>{}</textarea><br />
	<input type='submit' />
	</form>
</body>
</html>
""".format(text))
