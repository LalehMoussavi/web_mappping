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


# Retrieving the table name (fields or finds)
tab = arguments['tab'].value

# The argument keys we're looking for based on the table

if tab=='fields':
    keys = 'LOWX,LOWY,HIX,HIY,AREA,OWNER,CROP'.split(",")
else:
    keys = 'XCOORD,YCOORD,TYPE,DEPTH,FIELD_NOTES'.split(",")

# Retrieving the values of columns
values = []
for k in keys:
    print ("k: ",k)
    values.append(str(arguments[k].value))

# Getting the max_id of the table
if tab=='fields':
    rows = c.execute("select max(field_id) from fields2")
elif tab=='finds':
    rows = c.execute("select max(find_id) from finds2")

for row in rows:
    max_id = row[0]

# new_id is max_id+1
max_id += 1

# Inserting into the table
if tab=='fields':
    c.execute("INSERT INTO fields2 VALUES ("+ str(max_id)+","+  values[0]+","+ values[1]+","+ values[2]+","+
              values[3]+","+ values[4]+",'"+ values[5]+"'," + values[6]+ ")")
elif tab=='finds':
    c.execute("INSERT INTO finds2 VALUES ("+ str(max_id)+","+  values[0]+","+
              values[1]+",'"+ values[2]+"',"+ values[3]+",'"+ values[4]+"')")

conn.commit()
conn.close()
