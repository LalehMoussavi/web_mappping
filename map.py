#!/usr/bin/python3
import cgi
import cgitb
import cx_Oracle
import credentials

# This file contains the content of the ‘Charts’ tab.

my_user = credentials.login['user']
my_password = credentials.login['password']

MAX_Y = 16
MAX_X = 16

# Forms a tag for a SVG text.
# This function is responsible for creation of any text (string or number) in the grid tab.
# The inputs are X and Y positions, the text to be shown, amount of shift (x or y) and the font_size
# Using necessary transformations, we mirror the text so it will show well at the end!
def get_text_tagStr(X,Y,text,SHIFT_TEXT_X,SHIFT_TEXT_Y,FONT_SIZE=.3):
    Y = MAX_Y - Y
    ret = '<text x="'+str(X-SHIFT_TEXT_X)+'" y="'+str(Y+SHIFT_TEXT_Y)+'" font-family="Verdana" font-size="'+\
          str(FONT_SIZE)+'" transform=" translate(0,'+str(MAX_Y)+') scale(1,-1)">'+str(text)+'</text>\n'
    return ret

# Forms a tag for a SVG rectangle
# This function creates rectangles with the use of ‘rect’ SVG tag. It draws fields and the container of their id
# numbers in the middle of each field.  get_text_tagStr is also called to fill the container with appropriate id number.
def get_field_tagStr(Field_Id,LOWX,LOWY,HIX,HIY):#TODO: move the attributes to a class
    ret = '<g>\n'
    ret += '<rect x="'+str(LOWX)+'" y="'+str(LOWY)+'" width="'+str(HIX-LOWX)+'" height="'+str(HIY-LOWY)\
           +'" fill="none" stroke="black" stroke-width="0.05" />\n'

    CENTER_X = (LOWX+HIX)/2
    CENTER_Y = (LOWY+HIY)/2

    ret+= '<rect  x="'+str(CENTER_X-.3)+'" y="'+str(CENTER_Y-.3)+\
          '" width="0.6" height=".6" fill="none" stroke="black" stroke-width="0.05"/>'

    text_tag_str = get_text_tagStr(CENTER_X,CENTER_Y,Field_Id,SHIFT_TEXT_X=.15,SHIFT_TEXT_Y=.15,FONT_SIZE=.4)
    ret += text_tag_str
    ret += '</g>\n'

    return ret


# It uses SVG circle tag to point the location of the finds on the grid tab.
# It also calls get_text_tagStr to allocate appropriate id number to each find.
def get_finding_tagStr(FIND_ID,XCOORD,YCOORD,TYPE,DEPTH,FIELD_NOTES,W):
    ret = '<circle style="cursor: pointer;" cx="'+str(XCOORD)+'" cy="'+str(YCOORD)+'" r=".15" stroke="black"'+\
    ' stroke-width="0.05" fill="yellow" onclick="showFindingInfo(event,'+str(FIND_ID)+', '+str(XCOORD)+', '+\
    str(YCOORD)+', '+str(TYPE)+', '+str(DEPTH)+', \''+FIELD_NOTES+'\'' + ', ' + str(W)+')"/>'

    text_tag_str = get_text_tagStr(XCOORD,YCOORD,FIND_ID,SHIFT_TEXT_X=-.2,SHIFT_TEXT_Y=0.15,FONT_SIZE=.4)
    ret += text_tag_str
    return ret

# It uses the rect and circle SVG tag to draw the legend for the map. Also calls get_text_tagStr to enter desired
#  texts to legend section.
def get_legend_tagStr():
    ret = '<g>\n'
    ret += '<rect x="'+str(12.8)+'" y="'+str(.8)+'" width="'+str(3)+'" height="'+str(3)+\
           '" stroke="black" stroke-width="0.05" fill="white" />\n'
    ret +='<circle " cx="'+str(13.5)+'" cy="'+str(1.5)+'" r=".15" stroke="black" stroke-width="0.05" fill="yellow" />\n'
    ret +='<rect x="'+str(13.2)+'" y="'+str(2.2)+\
          '" width="0.6" height=".6" fill="none" stroke="black" stroke-width="0.05"/>'
    text_tag_str1 = get_text_tagStr(13.4,2.3,1,0,0,.4)
    text_tag_str2=get_text_tagStr(13.2,3.1,'Legend',0,0,.4)
    text_tag_str3=get_text_tagStr(14.2,2.3,'Field ID',0,0,.4)
    text_tag_str4=get_text_tagStr(14.2,1.3,'Find ID',0,0,.4)

    ret += text_tag_str1
    ret +=text_tag_str2
    ret +=text_tag_str3
    ret +=text_tag_str4

    ret += '</g>\n'
    return ret



cgitb.enable()
print("Content-Type: text/html\n")
print("<!DOCTYPE html>")

print("<head>")
print("<title>Web Mapping Project</title>")
print("</head>")

print("<body style='background: white'>")
print("<div id='root'>")
print ('<script type="text/javascript" src="../ui.js"></script>')

# Getting the value of the zoom. By default, zoom=1. The size of the original window (iframe) is fixed, but when we
# increase the zoom (always z<=10), we increase the width of the SVG (W). Therefore, it has the effect of zooming in.
arguments = cgi.FieldStorage()
W = int(arguments['zoom'].value) * 200 + 350


# Start the SVG
print('<svg width='+str(W)+' height='+str(W)+' viewBox= "-1 -1 18 18" style= "border: none;">')

print('<g transform="matrix(1,0,0,-1,0,16)">')

# Create the grid
for j in range(17):
    print (get_text_tagStr(-1+.4,j,str(j),0,0,.3))
    print (get_text_tagStr(j,-1+.4,str(j),0,0,.3))
    print('<path stroke="grey" stroke-width="0.025" d="M'+str(j)+' 0 v16"/>')
    print('<path stroke="grey" stroke-width="0.025" d="M0 '+str(j)+' H16"/>')

# Query the database to get the fields and findings
conn = cx_Oracle.connect(my_user+"/"+my_password+"@geosgen")
c = conn.cursor()
c.execute("select * from fields2")
for row in c:
    print(get_field_tagStr(row[0],row[1],row[2],row[3],row[4]))
conn.close()

conn = cx_Oracle.connect(my_user+"/"+my_password+"@geosgen")
c = conn.cursor()
c.execute("select * from finds2")
for row in c:
    s = row[5].lower()
    s = s[0].upper()+s[1:]
    print(get_finding_tagStr(row[0],row[1],row[2],row[3],row[4],s,W))
conn.close()

print(get_legend_tagStr ())

print('</svg>')
print("</div>")
print("</body>")
print("</html>")

