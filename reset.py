#!/usr/bin/python3
import cx_Oracle
import cgi
import cgitb
import credentials

my_user = credentials.login['user']
my_password = credentials.login['password']

cgitb.enable()
print("Content-Type: application\n")
conn = cx_Oracle.connect(my_user+"/"+my_password+"@geosgen")
c = conn.cursor()

arguments = cgi.FieldStorage()
tab = arguments['tab'].value

# We reset by reading from the original tables gisteach.fields or gisteach.finds

if tab=="fields":
    c.execute("delete from fields2 where 1=1")
    c.execute("insert into fields2 (select * from gisteach.fields)")

elif tab=="finds":
    c.execute("delete from finds2 where 1=1")
    c.execute("insert into finds2 (select * from gisteach.finds)")

# c.execute("insert into fields2 (select * from gisteach.fields)")

conn.commit()
conn.close()


