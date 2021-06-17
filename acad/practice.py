from array import array
from math import radians

import pyautocad as pa
from pyautocad.api import Autocad
from pyautocad.types import APoint, aDouble
acad = Autocad(create_if_not_exists=True)
#acad.prompt("units")
#print(acad.doc.Name)
#doc.Name --> Return the name of the active document
#print(acad.doc.FullName)
#doc.FullName --> Return the path of active document. If the file is not saved it will return an empty String

'''The following method < acad.app.Documents >will givw list of all active documents'''
# activeDocumentList = []
# for i in acad.app.Documents:
#     activeDocumentList.append(i)
# print(activeDocumentList)

''' The following method acad.app.ActiveDocument = filename will change the active document to filename'''
# acad.app.ActiveDocument = activeDocumentList[0]

'''Zoom Method'''
acad.app.ZoomAll()
acad.app.ZoomExtents()

'''Points Methods'''
ap = pa.APoint(20,50,60) #x,y,z points resp. if you dont set any point it will bw zero
ad = pa.APoint([10,50,40])
print(ap.x,ap.y,ap.z) # return x,y,z pint resp.
ap.x = 55.21 #could also change point in this way
ap.z = 25.21
print(ap.x,ap.y,ap.z)
origin = pa.APoint(0,0,0)
print(ap.distance_to(origin)) # returns the distanc of first point to second point
print(pa.APoint(1,1,0).distance_to(origin))

''' The Apoint() supports all the arithmetic operator'''
ap += 1
ap-=1
ap*=2
ap/=2 #They will add this arguments to each parameter i.e x,y,z
pd = origin + 2
print(pd)
pd = origin - 2
print(pd)
pd = ap * 2
print(pd)
pd = origin / 2 # does not produce zerodivision Error as it is handled
print(pd)
pd = origin - ap

'''Add Line in autoCad'''

p0 = pa.APoint(0,0)
p1 = pa.APoint(5,5)
p2 = pa.APoint(-5,5)
acad.model.AddLine(p0,p1)
#acad.model.AddLine([0,0][3,6]) becoz addline takes instance of Apoint()
acad.model.AddLine(pa.APoint(0,0),pa.APoint(3,6))
acad.model.AddLine(p0,p2)
# it's better to store the model in variable so in future if we want to modify it we could do easily
line1 = acad.model.AddLine(p0,pa.APoint(20,-20))
line1.Move(p0,pa.APoint(20,20))

''' To draw Poly Lines'''
points = pa.aDouble(0,0,0,1,2,0,3,4,0,2,5,0,6,1,1) # here we have to specify points as (x1,y1,z1,x2,y2,z2,x3,y3,z3)
acad.model.AddPolyline(points)
# we can also define points in terms of array of double 's as follow
# ar = array("d",[0,0,0-1,1,0,-2,2,0,-3,0,0])
# acad.model.AddPolyLine(ar)
''' To add / graph Point in AutoCad'''
p0 =  APoint(2,2)
point0 = acad.model.AddPoint(p0)
''' To get variables or propertires'''
print(acad.doc.GetVariable("PDMODE"))
acad.doc.SetVariable("PDMODE",66)
print(acad.doc.GetVariable("PDMODE"))
print(acad.doc.GetVariable("PDSIZE"))
acad.doc.SetVariable("PDSIZE",1)
print(acad.doc.GetVariable("PDSIZE"))


'''To add circle or arc'''
# to add a circle acad.model.AddCircle(base_point of circle or centre of circle,radius of circle)
#It takes two arguments first is center of circle second is radius of circle
p0 = APoint(10,10)
acad.model.AddCircle(p0,3)

#Similarly to arc it takes 4 arguments 
# first and second same as circle i.e. cetre point and radius
# 3rd and 4th are the initial starting and ending angle of arc in radians
p0 = APoint(10,10)
acad.model.AddArc(p0,5,0,45/180*3.1415)
acad.model.AddArc(p0,5,270/180*3.1415,1)

'''To add Ellipse'''
#acad.model.AddEllipse(center point of ellipse,point of largest radius of ellipse,ratio of radius)
p0 = APoint(6,4)
radius = APoint(3,2)
acad.model.AddEllipse(p0,radius,0.5)

''' To add text to autocad file'''
#acad.model.AddText(Text to be added, insertion/base point, height of the text)
p0 = APoint(-1,-1)
acad.model.AddText("Welcome to autocad ",p0,0.5)
p0+=5
#For multiline text acad.model.AddMText(insertion/base point, width of box, Text to be added)
acad.model.AddMText(p0,15,"This is from Python")

''' To create dimensions in autocad'''
# lets draw a rectangle first
p0 = aDouble(10,0,10,12,0,10,12,4,10,10,4,10,10,0,10)
rec = acad.model.AddPolyLine(p0)
#acad.model.AddDimAligned(start of dimendion, end of dimension, position of dimension text)
acad.model.AddDimAligned(APoint(10,0),APoint(10,4),APoint(9.5,2))
acad.model.AddDimAligned(APoint(10,4),APoint(12,4),APoint(11,4.5))
#acad.model.AddDimAngular(vertex of angle, point beginnig of angle , end point of angle, and point where we want to place)
# for angular dimension
acad.model.AddDimAngular(APoint(10,0),APoint(10,2),APoint(11,0),APoint(11,11))
#Dimension to cirle
#acad.model.AddDimDiametric(starting point, ending point, position)
acad.model.AddCircle(APoint(-10,-10),5)
acad.model.AddDimDiametric(APoint(-15,-10),APoint(-5,-10),1)
acad.model.AddDimRadial(APoint(-10,-10),APoint(-5,-10),1)
#to add dimension rotated
#acad.model.AddDimRotated(start point, end point, location point of text, angle in radians)
acad.model.AddDimRotated(APoint(-10,-10),APoint(-5,-10),APoint(-5,-10),radians(30))


'''To add region'''
#we have to specify an empty list of objects to define region so we could define the objects in list as region
listOfObjects = []
# listOfObjects.append(acad.model.AddArc(APoint(-40,50),25,radians(45),radians(180)))
# listOfObjects.append(acad.model.AddPolyLine(aDouble(-40,50,0,-40,75,0,75,-40,0,50,-40,0,-40,50,0)))


#acad.model.AddRegion(listOfObjects)
acad.app.ZoomExtents()
print("done")
