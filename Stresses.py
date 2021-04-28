'''    Bending Stresses '''
import matplotlib.pyplot as plt
import shaft
import numpy as np
import math
pi = math.pi
p4 = pi/4
r = round
class RectangleStress:
    def __init__(self,width,thickness,bending_moment,shear_stress):
        self.w = width
        self.t = thickness
        self.bm = bending_moment
        self.tau = shear_stress
    a = None
    mi = None
    ss = None
    ms = None
    def Area(self):
        global a
        a = self.w * self.t
        return a
    def MomentOfInertia(self):
        global mi
        mi = (1/12) * (self.w * (self.t**3))
        return mi
    def ShearStress(self):
        global ss
        ss = 3/2 * (self.tau/self.Area())
        return ss
    def MaxBendingStress(self):
        global ms
        ms = (self.bm *(self.t/2))/self.MomentOfInertia()
        return ms
    def plotting(self):
        global a,mi,ss,ms
        x = range(0,3,1)
        y = a, ss, ms
        plt.plot(x,y,'g+',marker='o',linestyle=' ',markersize=12)
        plt.title('Stresses')
        plt.xlabel('Area - Mi - SS - MS')
        plt.ylabel('VALUES')
        return plt.show()
    def __repr__(self):
        print("\t\tArea\t",r(self.Area(),2),sep='--->'.center(20))
        print("\tMoment Of Inertia",r(self.MomentOfInertia(),2),sep='--->'.center(15))
        print("\t   Shear Stress",r(self.ShearStress(),2),sep='--->'.center(20))
        print("\tMax Bending Stress",r(self.MaxBendingStress(),5),sep='--->'.center(15))
        self.plotting()
        return ''
        

class CircularStress:
    def __init__(self,OD,bending_moment,shear_stress):
        self.bm = bending_moment
        self.tau = shear_stress
        self.o = OD
    a = None
    mi = None
    ss = None
    ms = None
    def Area(self):
        global a
        a = (self.o**2) * p4
        return a
    def MomentOfInertia(self):
        global mi
        mi = (1/64) * pi * self.o**4
        return mi
    def ShearStress(self):
        global ss
        ss = 4/3 * (self.tau/self.Area())
        return ss
    def MaxBendingStress(self):
        global ms
        ms = ((self.bm *(self.o/2)))/self.MomentOfInertia()
        return ms
    def plotting(self):
        return RectangleStress.plotting(self)
    def __repr__(self):
        RectangleStress.__repr__(self)
        return ''
            

class CircularTube:
    def __init__(self,OD,ID,bending_moment,shear_stress):
        self.bm = bending_moment
        self.tau = shear_stress
        self.o = OD
        self.i = ID
    a = None
    mi = None
    ss = None
    ms = None
    def Area(self):
        global a
        a = ((self.o**2) - (self.i**2)) * p4
        return a
    def MomentOfInertia(self):
        global mi
        mi = ((self.o**4) - (self.i**4)) / (pi/64)
        return mi
    def ShearStress(self):
        global ss
        d2 = (self.i/2)**2 + (self.o/2)**2
        d =  (0.25*self.o * self.i) + d2
        fd = d/d2
        ss = CircularStress.ShearStress(self) * fd
        return ss
    def MaxBendingStress(self):
        global ms
        ms = CircularStress.MaxBendingStress(self)
        return ms
    def plotting(self):
        return RectangleStress.plotting(self)
    def __repr__(self):
        CircularStress.__repr__(self)
        return ''
        

        
##re = RectangleStress(5,10,1000,100)
##print(re)
##c = CircularStress(20,50,50)
##print(c)
t = CircularTube(5,3,20,6)
print(t)
