#!/usr/bin/python3
print ('Content-type: text/html\n')

from os.path import join, abspath
import cgi, sys

#data is local directory, we need to get absolute path of it

BASE_DIR = abspath('data')

form = cgi.FieldStorage()
filename = form.getvalue('filename')
if not filename:
print ('Please enter a file name')
sys.exit()
text = open(join(BASE_DIR, filename)).read()
#transfer POST to save.cgi
#NAME:  filename    password    text    N/A
#TYPE:  hidden      password    N/A     submit
#VALUE: file_name   N/A         t_ext   Save
print ("""
<html>
<head>
<title>Editing...</title>
</head>
<body>
<form action='save.cgi' method='POST'>
<b>file:</b> {0} <br />
<input type='hidden' value='{0}' name='filename' />
<b>Password:</b><br />
<input name='password' type='password' /><br />
<b>Text:</b><br />
<textarea name='text' cols=40 rows='20'>{1}</textarea><br />
<input type='submit' value='Save' />
</form>
</body>
</html>
""".format(filename, text))
