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

# Retrieving the table and id arguments
arguments = cgi.FieldStorage()
fid = arguments['fid'].value
tab = arguments['tab'].value

# Deleting from the table
if tab=="fields":
    c.execute("delete from fields2 where field_id="+str(fid))
elif tab=="finds":
    c.execute("delete from finds2 where find_id="+str(fid))

conn.commit()
conn.close()
