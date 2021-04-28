import numpy as np
import matplotlib.pyplot as plt
import pdb

from numpy.lib.shape_base import expand_dims

def sfd_bmd():
    L = int(input()) #Length of beam
    P = int(input()) # Load in N
    a = int(input()) # distance of load

    # Sum of all forces Sx =

    # Reactions
    R1 = (P*(L-a))/L
    R2 = P*a/L

    # Moments
    l = np.linspace(0,L,200)
    X = [] # Distances
    SF = [] #Shear Force
    M = [] # Moment
    
    for x in l:
        if x<=a:
            m=R1*x #Moment
            sf = R1 #Shear force
        elif x>a:
            m=(R1*x) - (P*(x-a))
            sf = R1-P
        M.append(m)
        X.append(x)
        SF.append(sf)

    plt.subplot(2,1,1)
    plt.title('Shear Force Diagram')
    plt.plot(X,SF)
    plt.plot([0,L],[0,0])
    plt.xlabel('Length in m')
    plt.ylabel('Shear forces in N')

    plt.subplot(2,1,2)
    plt.plot(X,M)
    plt.xlabel('Length in m')
    plt.ylabel('Bending Moment in Nm')
    plt.plot([0,L],[0,0])

    #print(f'R1 --> {R1}\nR2-->{R2}\nmax bending moment -->{max(M)} at point {X[max(M).index()]}')

    plt.show()
    return 0

#sfd_bmd()

'''Another Approach'''


def sfd_bmd_scipy():
    from sympy.physics.continuum_mechanics.beam import Beam
    import sympy

    E,I = sympy.symbols('E,I') #E = modulus of elasticity , I = Moment of Inertia
    L = int(input())
    b = Beam(L,E,I)
    loads = []
    b.apply_load(-12,L,-1)
    b.apply_load(50,5,-2)
    b.apply_load(-8,0,0,end=5)
    b.bc_deflection.append((0,0))
    b.bc_slope.append((0,0))
    #These boundary conditions introduces an unknown reaction force and moment which need to be applied to the beam to maintain static equilibrium
    R,M = sympy.symbols('R,M') #R-> Reaction , M-> Moment
    b.apply_load(R,0,-1)
    b.apply_load(M,0,-2)
    b.load
    b.solve_for_reaction_loads(R,M)
    b.reaction_loads
    b.plot_shear_force()
    b.plot_bending_moment()
    b.plot_slope(subs={E:20E9 , I:3.25E-6})
    b.plot_deflection(subs={E:20E9, I:3.25E-6})
    b.plot_loading_results()
    return 0

sfd_bmd_scipy()



def my_func_sfd_bmd():
    
    Length = float(input('Length of beam : '))
    no_of_forces = int(input('Number of forces acting : '))
    forces_list = []
    n = no_of_forces
    while n:
        i,j = map(float,input('Enter load and distn from left side ex: load is 10N at 5m, enter 10 5\n').split())
        forces_list.append([i,j])
        n-=1
    del n
    X = [] # Distances
    SF = [] # Shear Forces
    M = [] # Moments

    R1,R2,S = 0,0,0
    '''Calculating Shear Force Summation'''
    for i in forces_list:
        S += i[0] 
    print("S \t-- >\t",S)
    '''Calculating Moment Summation'''
    Mm = 0
    for i in forces_list:
        Mm += float(i[0])*float(i[1])

    R2 = (Mm/Length)
    R1 = (S-R2)
    print(f'\t\tR1==>{R1} N\n\t\tR2==>{R2} N')
    forces_list.insert(0,[-R1,0])
    forces_list.append([-R2,Length])
    print(forces_list)
    lp = np.linspace(0,Length,int(Length*2))
    
    '''Plotting'''
    i = 0
    sf,bm = 0,0
    # for x in lp:
    #     if x<=float(forces_list[i][1]):
    #         sf += float(forces_list[i][0])*(-1)
    #         #print(x,sf,forces_list[i][0],sep='\t')
    #         bm += float(forces_list[i][0]) * float(forces_list[i][1]) *(-1)
    #         # elif l[i][2]=='U':
    #         #     bm+= float(l[i][0])*float(l[i][1])*(L - float(l[i][1]/2)) *(-1)
    #         SF.append(sf)
    #         M.append(bm)
    #         X.append(x)
    #     else:
    #         i+=1
    # for j in range(1,(len(forces_list)*2)+1):
    #     if j%2==0:
    #         sf = float(forces_list[i][0]*(-1))
    #         i+=1
    #         SF.append(sf)
    #     else:    
    #         SF.append(sf)
    for x in lp:
        if x<=forces_list[i][1]:
            bm=forces_list[i][0] *x #Moment
            sf = forces_list[i][0]*(-1) #Shear force
        else:
            i+=1
        M.append(bm)
        X.append(x)
        SF.append(sf)
    print(k for k in X)
    plt.subplot(2,1,1)
    plt.title('Shear Force Diag')
    plt.plot(X,SF)
    plt.plot([0,Length],[0,0])
    plt.xlabel('Length in m')
    plt.ylabel('Shear forces in N')
    
    plt.subplot(2,1,2)
    plt.plot(X,M)
    plt.xlabel('Length in m')
    plt.ylabel('Bending Moment in Nm')
    plt.plot([0,Length],[0,0])
    plt.show()


my_func_sfd_bmd()













