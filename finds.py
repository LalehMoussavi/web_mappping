#!/usr/bin/python3
import cgi
import cgitb
import cx_Oracle
import credentials

my_user = credentials.login['user']
my_password = credentials.login['password']

# The get_find_row_table function makes one row of the table, using for loop for every column in the finds table
def get_find_row_table(FIND_ID,XCOORD,YCOORD,TYPE,DEPTH,FIELD_NOTES):
    all_cols = [FIND_ID,XCOORD,YCOORD,TYPE,DEPTH,FIELD_NOTES]
    ret="<td style=\"border:none; background-color: white; cursor: pointer\"onclick=\"deleteTable(event,"+str(FIND_ID)+\
        ",'finds')\"> &#x2716 </td>"
    for val in all_cols:
        column='<td>'+str(val)+'</td>'
        ret+= column

    ret2= '<tr>'+ret+'</tr>'
    return ret2

# This function creates the tag for inserting a new row (field). It returns a row which will be added to the main table.
# The types of the fields are taken into account
def get_insert_row():
    ret = "<td class='invis'><input size='8' type='submit' value='Add Find'>  </td><td class='invis'></td>"

    names = 'XCOORD,YCOORD,TYPE,DEPTH,FIELD_NOTES'.split(',')
    types = ['number','number','xxx','xxx','text']

    # XCOORD, YCOORD
    for i in range(2):
        column= '<td class="invis"><input style="width: 100%" type="'+types[i]+'" name="'+names[i]+'" id="'+names[i]+\
                '" placeholder="'+names[i]+'"></td>'
        ret+= column

    i+=1
    # TYPE
    select_str = '<select name="TYPE" id="TYPE"><option value="1">SHARD</option><option value="2">METAL_WORK</option>'+\
                 '<option value="3">FLINT</option><option value="4">BONE</option></select>'

    column= '<td class="invis">'+select_str+'</td>'
    ret += column

    # DEPTH
    i+=1

    column= '<td class="invis"><input style="width: 100%" type="number" min="0" step=".01" name="'+names[i]+'" id="'+\
            names[i]+'" placeholder="'+names[i]+'"></td>'
    ret+= column

    # FIELD_NOTES
    i+=1

    column= '<td class="invis"><input style="width: 100%" type="text"  name="'+names[i]+'" id="'+names[i]+\
            '" placeholder="'+names[i]+'"></td>'
    ret+= column

    ret2= '<tr>'+ret+'</tr>'
    ret2 ='<form action="javascript:insertFind(' \
          'event,XCOORD.value,YCOORD.value,TYPE.value,DEPTH.value,FIELD_NOTES.value)">'+ret2+'</form>'
    return ret2

cgitb.enable()
print("Content-Type: text/html\n")

print("<!DOCTYPE html>")

print('<head>')
print('<style>')
print('table {font-family: arial, sans-serif; border-collapse:collapse; width: 100%; text-align: center;}')
print(' th, td {border: 1px solid black; text-align: left; padding: 8px;}')
print('table tr:nth-child(even) {background-color: #eee;}')
print('table tr:nth-child(odd) {background-color:#fff;}')
print('table th {background-color: black;color: white; font-size:13px}')
print('td.invis { border:none; background-color: white; border-collapse:collapse}')



print('</style>')
print('</head>')
print("<body style='background: white'>")
print('<center>')
print ('<script type="text/javascript" src="../ui.js"></script>')
# The main table
print('<table id = "finds_table"')
# Head of the table
print('<tr>')
print('<th style=\"border:none; background-color: white\"> </th>')
print('<th> FIND ID</th>')
print('<th>XCOORD</th>')
print('<th>YCOORD</th>')
print('<th>TYPE</th>')
print('<th>DEPTH</th>')
print('<th>FIELD NOTES</th>')
print('</tr>')

conn = cx_Oracle.connect(my_user+"/"+my_password+"@geosgen")
c = conn.cursor()

# Querying the finds table to get the find (also joining with class to get the type of the findings)

c.execute("select finds2.FIND_ID,finds2.XCOORD,finds2.YCOORD, gisteach.class.NAME,finds2.DEPTH, finds2.FIELD_NOTES"
          " from finds2, gisteach.class"+ " where finds2.type = gisteach.class.type order by finds2.FIND_ID")

# Adding all the rows the html table
for row in c:

    print(get_find_row_table(row[0],row[1],row[2],row[3],row[4],row [5]))

# Adding the insert portion
print (get_insert_row())

conn.commit()
conn.close()


print('</table>')
print('<br>')
print('<div>')
print("<button type=\"button\" onclick=\"resetTable(event,'finds')\">RESET</button>")
print('</div>')

print('</center>')

print('</body>')
print('</html>')






