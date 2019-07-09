#!/usr/bin/python3
import psycopg
conn = psycopg.connect('user=foo dbname=bar')
curs = conn.cursor()

reply_to = raw_input('Reply to: ')
suject = raw_input('Subject: ')
sender = raw_input('Sender: ')
text = raw_input('Text: ')
if reply_to:
    query = """
    INSERT INTO messages(reply_to, sender, subject, text)
    VALUSE( {0}, '{1}', '{2}', '{3}')""".format(reply_to, sender, subject, text)
else:
    query = """
    INSERT INTO messages(sender, suject, text)
    VALUES('{0}', '{1}', '{2}')""".format(sender, subject, text)

curs.execute(query)
conn.commit()
