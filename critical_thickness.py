import matplotlib.pyplot as plt
import numpy as np
import math
pi = math.pi
t2 = float(input("Enter Temp T2 : "))
t1 = float(input("enter Temp T1 : "))
k = float(input("Enter Thermal Conductivity (K) of Material : "))
L = float(input("Enter Length : "))
h0 = float(input("Enter Convective Heat transfer coefficient' : "))
r2 = np.linspace(0.1,50*(k/h0),100)
r1 = float(input("Enter Radius 1 : "))
l = []
un = 2*pi*L*abs(t1 - t2)
for ro in r2:
    #ao = 2*pi*ro*L
    d = ro/r1
    j = math.log(ro/r1)/k
    #r = 1/(h0*ro)
    #q = un/(j+r)
    q = -(un/j)
    l.append(q)
print(max(l),min(l),sep='===>')
print(max(r2),min(r2),sep='==>60')
plt.plot(r2,l)
plt.xlabel('Radius')
plt.ylabel('Heat Conduction (Q)')
ma = r2[l.index(max(l))]
plt.title(f"Critical Thickness of Radius for Given Parametr is {ma}")
print(k/h0,r2[l.index(max(l))],sep='--->')
plt.show()

''' Formula for Cylinder is rc = K/ho ===> thermal_conductivity/Heat_transfer_coefficient
    Formula for sphere is rc = 2K/h0 ===> thermal_conductivity/Heat_transfer_coefficient'''
'''wire dia = 6.5 mm ===> 0.0065m
    T1 = 60 C
    K = 0.174 Watt/(Metre*Kelvin)
    ho = 8.722 Watt/((Metre**2)*Kelvin)
    T2 or Ta = 20 C
    critical Thickness ?
    Heat loss per metre length ?
    
    
    rc = K/ho = 0.174/8.722  It's radius. Don't get confuse |
    at rc Q will be Q_max (Watt)                            |
    Thickness of insulation = rc - ro - - - - - - - - - - -<-
    
    Total_Resistance (Kelvin / Watt) = Resistance_conductive + Resistance_convective = [ln(ro/ri)/(2*pi*L*K)] + [1/(ho*ao)] 
    ao = 2*pi*ro*L
    
    
    '''