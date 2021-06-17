import win32com.client as cl
import pythoncom as pc
acad = cl.Dispatch("AutoCAD.Application")
acadModel = acad.ActiveDocument.ModelSpace

def aPoint(x=0,y=0,z=0):
    return cl.VARIANT(pc.VT_ARRAY | pc.VT_R8,(x,y,z))
def aDouble(xyz):
    return cl.VARIANT(pc.VT_ARRAY | pc.VT_R8,(xyz))
def aVariant(vObject):
    return cl.VARIANT(pc.VT_ARRAY | pc.VT_DISPATCH,(vObject))

