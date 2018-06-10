#!/usr/bin/python3
import cgi
import cgitb
import cx_Oracle
import credentials

my_user = credentials.login['user']
my_password = credentials.login['password']

# The get_field_row_table function makes one row of the html table, using for loop for every column in the fields table
def get_field_row_table(Field_Id,LOWX,LOWY,HIX,HIY,AREA,OWNER,CROP):
    all_cols = [Field_Id,LOWX,LOWY,HIX,HIY,AREA,OWNER,CROP]
    ret="<td id=\""+str(Field_Id)+"\" style=\"border:none; background-color: white; cursor: pointer\" " \
                                  "onclick=\"deleteTable(event,"+str(Field_Id)+",'fields')\"> &#x2716 </td>"
    for val in all_cols:
        column='<td>'+str(val)+'</td>'
        ret+= column

    ret2= '<tr>'+ret+'</tr>'
    return ret2

# This function creates the tag for inserting a new row (field). It returns a row which will be added to the main table.
# The types of the fields are taken into account
def get_insert_row():
    ret = "<td class='invis'><input size='8' type='submit' value='Add Field'>  </td><td class='invis'></td>"

    names = 'LOWX,LOWY,HIX,HIY,OWNER'.split(',')
    types = ['number','number','number','number','text']


    for i in range(4):
        column= '<td class="invis"><input style="width: 100%" type="'+types[i]+'" name="'+names[i]+'" id="'\
                +names[i]+'" placeholder="'+names[i]+'"></td>'
        ret+= column

    ret+="<td class='invis'></td>"

    i=4
    column= '<td class="invis"><input style="width: 100%" type="'+types[i]+'" name="'+names[i]+\
            '" id="'+names[i]+'" placeholder="'+names[i]+'"></td>'
    ret+= column


    select_str = \
        '<select name="CROP" id="CROP"><option value="1">TURNIPS</option><option value="2">OIL SEED RAPE</option>'+\
                 '<option value="3">STRAWBERRIES</option>' \
                 '<option value="4">PEAS</option><option value="5">POTATOES</option></select>'



    column= '<td class="invis">'+select_str+'</td>'
    ret+=column

    ret2= '<tr>'+ret+'</tr>'
    ret2 ='<form action="' \
          'javascript:insertField(event,LOWX.value,LOWY.value,HIX.value,HIY.value,OWNER.value,CROP.value)">'\
          +ret2+'</form>'
    return ret2

cgitb.enable()
print("Content-Type: text/html\n")

print("<!DOCTYPE html>")

print('<head>')

print('<style>')
print('table {font-family: arial, sans-serif; border-collapse:collapse; width: 100%; text-align: center;}')
print(' th,td {border: 1px solid black; text-align: left; padding: 8px;}')
print('table tr:nth-child(even) {background-color: #eee;}')
print('table tr:nth-child(odd) {background-color:#fff;}')
print('table th {background-color: black;color: white;}')
print('td.invis { border:none; background-color: white; border-collapse:collapse}')
print('</style>')

print('</head>')

print("<body style='background: white'>")
print('<center>')
print ('<script type="text/javascript" src="../ui.js"></script>')
# The main table
print('<table id="field_table">')
# Head of the table
print('<tr>')
print('<th style=\"border:none; background-color: white;\"></th>')
print('<th>FIELD ID</th>')
print('<th>LOWX</th>')
print('<th>LOWY</th>')
print('<th>HIX</th>')
print('<th>HIY</th>')
print('<th>AREA</th>')
print('<th>OWNER</th>')
print('<th>CROP</th>')
print('</tr>')

conn = cx_Oracle.connect(my_user+"/"+my_password+"@geosgen")
c = conn.cursor()

# Querying the fields table to get the fields (also joining with crops to get the name of the crops)

c.execute("select fields2.Field_Id,fields2.LOWX,fields2.LOWY,fields2.HIX,fields2.HIY,fields2.AREA,fields2.OWNER"+
          ",gisteach.crops.name from fields2, gisteach.crops where"+
          " fields2.crop = gisteach.crops.crop order by fields2.field_id")

# Adding all the rows the html table
for row in c:
    area = row[5]
    area = round (float (area),2)
    print(get_field_row_table(row[0],row[1],row[2],row[3],row[4],area,row[6],row[7]))

# Adding the insert portion
print(get_insert_row())

conn.commit()
conn.close()

print('</table>')
print('<br>')
print('<div>')
print("<button type=\"button\" onclick=\"resetTable(event,'fields')\">RESET</button>")
print('</div>')
print('</body>')
print('</center>')

print('</html>')






