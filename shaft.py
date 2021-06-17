import math #module Files 
import tkinter as tk #module for gui(graphical user interface) api
#import os,shutil,datetime
from tkinter import font,ttk,filedialog
from tkinter import messagebox as mbox
from csv import DictWriter
from tkinter.constants import N, SEL_FIRST, W
import pdb
from pyautocad import Autocad, APoint
formulaes = '''
        For Shaft subjected to twisting Moment

        T = Twisting Moment   --- >> unit  N-mm

            Power  =  2 * pi * N * T / 60
            where P = Power = Watt
                  N = Rpm
                  T = N-m
            
            In case of belt drives the twisting moment (T) is given by 

                T = (T1-T2)*R
                where 
                     T1 = Tension in tight side  --->> unit Newton
                     T2 = Tension in slack side  --->> unit Newton
                     R  = Radius of the Pulley  --->> unit meter 
        tau  = Shear Stress  ---->> unit N / mm^2
        
        r = Distance From Neutral AXis to the outer most fibre
         T     tau      G 0
        ---  = ---  =  -----    
         J     d/2       L

        J = Polar Moment Of Inertia

        For Solid Shaft    J = pi/32 * d^4  --->> unit  mm^4

        For Hollow Shaft    J = pi/32 * ( D^4 - d^4 )

        Thus  
            For solid shaft       T = pi/16 * tau * d^3
                                &
            For Hollow Shaft       T = pi/16 * tau * D^3 * (1 - k^4)

            where k = d / D (ratio of inner dia to outer dia)
 
       therefore 
            For solid Shaft d = cuberoot((T * 16) / (tau*pi))
                                &
            For Hollow Shaft D = cuberoot((T * 16) / (tau * pi * (1 - k^4))


    For Bending Moment

         M     sigma_B
        ---  = -------     
         I        y

         M = Bending Moment        --->> unit N-m

            For Solid Shaft     M = pi/32 * sigma_B * d^3

            For Hollow Shaft    M = pi/32 * sigma_B * D^3 (1 - k^4)

            where k = d/D


         I = Moment Of Inertia     --->> unit mm^4

            For Solid Shaft     I = pi/64 * d^4 

            For Hollow Shaft    I = pi/64 * (D^4 - d^4)

        
        sigma_B = Bending Stress    --->> unit N/mm^2

            sigma_B = (32 * M) / (pi * d^3)

            tau = (16 * T) / (pi * d^3)

        y = Distance from neutral axis to the outer most fibre

            y = d/2     --->> unit mm

    If Numerical requires both twisting and bending moment following will be the procedure

    tau_max = 0.5 * sqrt( sigma_B^2 + 4 * tau^2 )

        By Simplifying 

            tau_max = 16 * sqrt[ M^2 + T^2 ] / ( pi * d^3 )

    
    The Twisting Moment due to maximum most shear stress on surface of shaft is known as equivalent twisting moment i.e. Te

        Te = sqrt[ M^2 + T^2 ]

        i.e. Te = pi/16 * tau_max * d^3
        


'''
pi = math.pi
r = round
srt = math.sqrt

#8**(1/3)

def chcek_param(param,i,j):
    if i=='' or i==' 'or i==None or i==0:
        i=float(j)
    else:
        try:
            i = float(i)
        except ValueError:
            mbox.showerror('Invalid Value',f'Please Give valid Value of {param}')
            return False
    return i

class SolidShaft:
    def __init__(self,Power=0,Weight=0,rpm=0,fos=1,T_ratio = 0,shearStress=0,bendingStress=0,Length=1,theta=0,G=0,position=0,Tmax=0,Mmax=0):
        self.P = Power
        self.W = Weight
        self.tau = shearStress
        self.sigma_b = bendingStress
        self.L = Length
        self.N = rpm
        self.fos = fos
        self.theta = theta
        self.G = G
        self.Tratio = T_ratio
        self.position = position.lower()
        self.Tmax = Tmax
        self.Mmax = Mmax
        self.Mmean = None
        self.Tmean = None
        self.TE = 0
        self.ME = 0
        #print(type(self.tau),self.fos,self.P,self.N,self.tau,self.Tratio,sep = ' --- ')
            
        #print('\n\tT ratio = ',self.Tratio)

    
    def validing_param(self):
        self.P = chcek_param('Power',self.P,0)
        self.W = chcek_param('Weight',self.W,0)
        self.Tmax = chcek_param('Twisting Moment',self.Tmax,0)
        self.Mmax = chcek_param('Bending Moment',self.Mmax,0)
        if (self.P == 0 and self.W==0 and self.Tmax==0 and self.Mmax==0):
           mbox.showinfo('\aInvalid Value','Please give valid Loads value correctly')
        
        self.fos = chcek_param('FOS',self.fos,1)
        self.Tratio = chcek_param('Ratio',self.Tratio,0)
        self.theta = math.radians(chcek_param('Theta',self.theta,0))
        self.G = chcek_param('Modulus Of Rigidity',self.G,0) *(10**3)
        self.N = chcek_param('RPM',self.N,0)
        self.tau = chcek_param('Shear Stress',self.tau,0)
        self.sigma_b = chcek_param('Bending Stress',self.sigma_b,0)
        self.L = chcek_param('Length',self.L,100)
        if (self.sigma_b==0 and self.tau==0):
            mbox.showerror('\aInvalid Param','Please Give one of the Stress Value')
        return self.fos,self.Tratio,self.N,self.tau,self.P,self.W,self.L,self.Tmax,self.Mmax,self.sigma_b
    
    def calc_all_moment(self):
        print(type(self.fos),self.fos)
        self.tau = self.tau/self.fos
        self.sigma_b = self.sigma_b/self.fos
        #self.Tratio != None or self.Tratio!=0 or self.Tratio!=' ' or self.Tratio!='': 
        try:
            self.Tmean =  math.ceil((self.P*60)/(2*pi*self.N)) * (10**3)
            print("Tmean --> ",self.Tmean)
        except ZeroDivisionError:
            self.Tmean = 0
        self.Tmax = max(self.Tmax,self.Tmean * (1 + self.Tratio/100))
        print("Tmax --->",self.Tmax)
        if self.position == 'center':
            self.Mmean = self.W * self.L /4 
        else:
            self.Mmean = self.W * self.L #N-mm
        self.Mmax = max(self.Mmax,self.Mmean * (1 + self.Tratio/100))
        print("Mmean --> ",self.Mmean)
        print("Mmax --> ",self.Mmax)
        self.TE = math.sqrt(self.Mmax**2 + self.Tmax**2)
        self.ME = 0.5*(self.Mmax + self.TE)
        print("TE --> ",self.TE)
        print("ME --> ",self.ME)
        return r(self.Tmax,2),r(self.Mmax,2),r(self.Mmean,2),r(self.Tmean,2),r(self.TE,2),r(self.ME,2)
    

    def calc_diameter(self):
##        pdb.set_trace()
        #print(self.Tmax,self.tau,sep='\t\t')
        self.validing_param()
        print('Fos',self.fos,type(self.fos))
        print('tau',self.tau,type(self.tau))
        print('L',self.L,type(self.L))
        print('B',self.sigma_b,type(self.sigma_b))
        print('Ratio',self.Tratio,type(self.Tratio))
        print('P',self.P,type(self.P))
        print('W',self.W,type(self.W))
        print('N',self.N,type(self.N))
        self.calc_all_moment()
        try:
            self.d_t = (self.TE * 16)/(self.tau*pi)
            self.d_t = self.d_t**(1/3)
        except ZeroDivisionError:
            self.d_t=0
        try:
            self.d_m = (self.ME * 32)/(pi * self.sigma_b)
            self.d_m = self.d_m**(1/3)
        except ZeroDivisionError:
            self.d_m=0
        print(math.ceil(self.d_t),math.ceil(self.d_m))
        self.d = max(self.d_t,self.d_m)
        return math.ceil(self.d)
    
    def calc_mass(self):
        r = self.d/2 #smetre
        #mbox.showinfo('\aCalculating Mass','Calculating Mass for length of 100mm')
        self.mass = pi * (r**2) * 100* 0.0079   
        print(self.mass)
        return self.mass
    def draw_drawing(self):
        r = self.d//2 + 1
        acad = Autocad(True)
        circle1 = acad.model.AddCircle(APoint(r,r),r)
        #circle1.Extrude(100,1)
        #acad.best_interface(circle1)
        acad.prompt("Extrude")
        # acad.get_selection(circle1)
        # acad.prompt("100")
        acad.model.AddDimDiametric(APoint(0,r),APoint(r*2,r),1)#,math.radians(45))
        #acad.app.ZoomExtents()
    
class HollowShaft:
    def __init__(self,Power=0,Weight=0,rpm=0,fos=1,T_ratio = 0,shearStress=0,bendingStress=0,Length=1,k=0.5,theta=0,G=0,position="None",Tmax=0,Mmax=0):
        self.P = Power
        self.W = Weight
        self.tau = shearStress
        self.sigma_b = bendingStress
        self.L = Length
        self.N = rpm
        self.fos = fos
        self.theta = theta
        self.G = G
        self.Tratio = T_ratio
        self.k = k
        self.position = position.lower()
        self.Tmax = Tmax
        self.Mmax = Mmax
        self.Tmean = 0
        self.Mmean = 0
        self.TE = 0;self.ME=0

    def validing_param(self):
        print("validing param running....")
        self.P = chcek_param('Power',self.P,0)
        self.W = chcek_param('Weight',self.W,0)
        self.Tmax = chcek_param('Twisting Moment',self.Tmax,0)
        self.Mmax = chcek_param('Bending Moment',self.Mmax,0)
        if (self.P == 0 and self.W==0 and self.TE == 0 and self.ME==0):
           mbox.showinfo('\aInvalid Value','Please give valid Loads value ')
        self.tau = chcek_param('Shear Stress',self.tau,0)
        self.sigma_b = chcek_param('Bending Stress',self.sigma_b,0)
        self.L = chcek_param('Length',self.L,1)*1000
        self.N = chcek_param('RPM',self.N,0)
        self.fos = chcek_param('FOS',self.fos,1)
        self.theta = math.radians(chcek_param('Theta',self.theta,0))
        self.G = chcek_param('Modulus of rigidity',self.G,0) * (10**3)
        self.Tratio = chcek_param('Ratio',self.Tratio,0)
        self.k = chcek_param('Diameter Ratio',self.k,0.5)
        if (self.sigma_b==0 and self.tau==0):
            mbox.showerror('\aInvalid Param','Please Give one of the Stress Value')
        return self.fos,self.Tratio,self.N,self.tau,self.P,self.W,self.L,self.sigma_b,self.k,self.G,self.theta,self.Tmax,self.Mmax
        
    def calc_all_moment(self):
        print("calc all moment running....")
        print(type(self.fos),self.fos)
        self.tau = self.tau/self.fos
        self.sigma_b = self.sigma_b/self.fos
        #self.Tratio != None or self.Tratio!=0 or self.Tratio!=' ' or self.Tratio!='':
        try: 
            self.Tmean =  math.ceil((self.P*60)/(2*pi*self.N) * (10**3))
        except Exception as ex:
            print(ex,"Line NO -> 271",sep="\n")
            self.Tmean=0
        self.Tmax = max(self.Tmax,self.Tmean * (1 + self.Tratio/100))
        if self.position == 'center':
            self.Mmean = self.W * self.L /4 
        else:
            self.Mmean = self.W * self.L #N-mm
        self.Mmax = max(self.Mmax,self.Mmean * (1 + self.Tratio/100))
        print(self.Mmax,"--> Mmax ",self.Mmean,"--> Mmean")
        self.TE = max(self.TE,math.sqrt(self.Mmax**2 + self.Tmax**2))
        self.ME = 0.5*(self.Mmax + math.sqrt(self.Mmax**2 + self.Tmax**2))
        return self.Tmax,self.Mmax,self.Mmean,self.Tmean,self.TE,self.ME
    
        
    def calc_diameter(self):
        print("calc diameter running....")
        self.validing_param()
        self.calc_all_moment()
        print(self.Tmax,self.tau,sep='\t\t')
        # Calcuating by T/J = G0/L
        print(self.TE,self.Tmax,self.ME,self.tau,self.G,self.L,self.theta,sep="  ")
        T_J= ((self.TE*16)/(self.tau*pi)) #equation no. 1 
        #tamx = pi/16  * tau * (D^4 - d^4)/D  
        # thus--->  (D^4 - d^4)/D = (Tmax*16) / (pi*tau) ... eqn_1
        ''' T_J = (D^4 - d^4)/D'''
        try:
            J = (self.TE * self.L)/(self.G * self.theta)  
            # T/J = G0/L thus--->   J = (T*L)/(G*0) 
            print(T_J,"-->T_J\n",J,"-->J")
            ''' J = pi/32 *(D^4 - d^4)'''
            
            #J = pi/32 * (D^4 - d^4) 
            # thus--->    (D^4 - d^4) = J * 32 / pi ... eqn_2
            d1_d2 = J * 32 /pi 
            '''d1_d2 = D^4 - d^4
             T_J = (D^4 - d^4)/D
             i.e.
             d1_d2 / D = T_J
             i.e.
             D = d1_d2 / T_J
             '''
            self.twisiting_OD = r(d1_d2/T_J,3)
            self.twisiting_ID =  max(r((self.twisiting_OD**4 - J)**(1/4),3),self.twisiting_OD*self.k)
            #  (D^4 - d^4)/D = T_J 
            # and from eqn_3 we get (D^4 - d^4) thus solved.... 
            #self.Id_g0 = (self.D**4 - J) ** (1/4)
        except Exception as ex:
            print(ex,"\n\tLine NO -> 326")
            J,self.twisiting_OD,self.twisiting_ID = 0,0,0
        # Thus from equation 1 & 3
        # solving by T/J = tau/r
        try:
            D_T = (self.TE*16)/((self.tau*pi)*(1-(self.k**4)))
            self.bending_OD = D_T**(1/3)
            self.bending_Id = self.bending_OD*self.k
        except Exception as ex:
            print(ex,"\n\tLine No->306")
            self.bending_OD,self.bending_Id=0,0

        self.OD = max(self.bending_OD,self.twisiting_OD)
        self.Id = max(self.bending_Id,self.twisiting_ID) 
        return r(self.OD,2),r(self.Id,2)

    def calc_mass(self):
        R,r = self.OD/20,self.Id/20
        vol = pi * ((R**2) - (r**2)) * 10
        self.mass = vol * 7.9
        return self.mass
    def draw_drawing(self):
        Or = self.OD//2 + 1
        Ir = self.Id//2 + 1
        acad = Autocad(True)
        circle1 = acad.model.AddCircle(APoint(Or,Or),Or)
        circle2 = acad.model.AddCircle(APoint(Or,Or),Ir)
        #circle1.Extrude(100,1)
        #acad.best_interface(circle1)
        acad.prompt("Extrude")
        # acad.get_selection(circle1)
        # acad.prompt("100")
        acad.model.AddDimDiametric(APoint(0,Or),APoint(Or*2,Or),1)#,math.radians(45))
        acad.model.AddDimDiametric(APoint(0,Ir),APoint(Ir*2,Ir),5)#,math.radians(45))
        acad.app.ZoomExtents()
        lo = [circle1,circle2]
        #acad.model.AddRegion(lo)
        #acad.model.Extrude(circle1,100)
        


win = tk.Tk()
color = win.tk_setPalette('#ebc663')
win.geometry('1200x720')
win.title('Design')
tl = tk.Label(text='DESIGN OF SHAFT',relief='flat',fg='white',bg='blue',font=('times new roman',40,'bold'))
tl.pack(fill='x')


#####    CReating labels for the parametrs

########   first have to create lable frame and then in this label frame we will add labels
def TkSolidShaft():
    ss= None
    # win.tk_setPalette('lightblue')
    #swin = tk.Toplevel(win,width=1200,height=720,bd=100)
    swin = tk.Tk()
    tk.Label(text="Design Of Solid Shaft").pack(fill='x')
    lf = tk.LabelFrame(swin,text='\nDesign of Solid Shaft. \nPlese enter following details to get the design of Solid Shaft',font=('italian',18))
    lf.pack()

    ## Labels
    p_l= ttk.Label(lf,text='Power to be Transmitted P',font=(14),foreground='blue')#,background='#ebc663')
    w_l= ttk.Label(lf,text='Load on Shaft W',font=(14),foreground='blue')#,background='#ebc663')
    Rpm_l = ttk.Label(lf,text="Enter Rpm .\nIf you don't know please leave it blank or type 0 ",font=(6),foreground='blue')#,background='#ebc663')
    Len_l = ttk.Label(lf,text="Enter Length .\nIf you don't know please leave it blank or type 0 ",font=(6),foreground='blue')#,background='#ebc663')
    bms_l = ttk.Label(lf,text="Enter Bending Stress .\nIf not applicable please leave it blank or type 0 ",font=(6),foreground='blue')#,background='#ebc663')
    sys_l = ttk.Label(lf,text="Enter Shear Stress Strength of material.\nIf you don't know please leave it blank or type 0 ",font=(6),foreground='blue')#,background='#ebc663')
    Tor_l = ttk.Label(lf,text="Enter Torque excedence %.\nIf you don't know please leave it blank or type 0 ",font=(6),foreground='blue')#,background='#ebc663')
    Fos_l = ttk.Label(lf,text="Enter Faactor of Safety.\nIf you don't know please leave it blank or type 0 ",font=(6),foreground='blue')#,background='#ebc663')
    Pos_l = ttk.Label(lf,text="Enter Position of Load.\nBy default it will be considered as center",font=(6),foreground='blue')#,background='#ebc663')
    G_l = ttk.Label(lf,text="Enter Modulus of rigidity.\nBy default it will be 0",font=(6),foreground='blue')#,background='#ebc663')
    theta_l = ttk.Label(lf,text="Enter Theta (0) \n By default it is 0",font=(6),foreground='blue')#,background='#ebc663')
    Tmax_l = ttk.Label(lf,text="Enter Twisitng Moment if known(0) \n By default it is 0",font=(6),foreground='blue')#,background='#ebc663')
    Mmax_l = ttk.Label(lf,text="Enter Bendnig Moment if Known (0)",font=(6),foreground='blue')#,background='#ebc663')
    

    p_l.grid(row=0,column=0,padx=20,pady=8)
    w_l.grid(row=1,column=0,padx=20,pady=8)
    Rpm_l.grid(row=2,column=0,padx=20,pady=8)
    Len_l.grid(row=3,column=0,padx=20,pady=8)
    Fos_l.grid(row=4,column=0,padx=20,pady=8)
    bms_l.grid(row=5,column=0,padx=20,pady=8)
    sys_l.grid(row=6,column=0,padx=20,pady=8)
    Tor_l.grid(row=7,column=0,padx=20,pady=8)
    G_l.grid(row=8,column=0,padx=20,pady=8)
    theta_l.grid(row=9,column=0,padx=20,pady=8)
    Pos_l.grid(row=10,column=0,padx=20,pady=8)
    Tmax_l.grid(row=11,column=0,padx=20,pady=8)
    Mmax_l.grid(row=12,column=0,padx=20,pady=8)
    ##Entry boxes

    ## Describing variables

    p_v = tk.IntVar()
    w_v = tk.IntVar()
    Rpm_v = tk.IntVar()
    Len_v = tk.IntVar()
    bms_v = tk.IntVar()
    fos_v = tk.IntVar(value=1)
    sys_v = tk.IntVar()
    Tor_v = tk.IntVar()
    Pos_v = tk.StringVar()
    G_v = tk.IntVar()
    Tmax_v = tk.IntVar()
    Mmax_v = tk.IntVar()
    theta_v = tk.IntVar()

    ## Entry boxes created
    pe = tk.Entry(lf,width=20,textvariable = p_v)
    we = tk.Entry(lf,width=20,textvariable = w_v)
    rpme = tk.Entry(lf,width=20,textvariable = Rpm_v)
    Lene = tk.Entry(lf,width=20,textvariable = Len_v)
    fose = tk.Entry(lf,width=20,textvariable = fos_v)
    bmse = tk.Entry(lf,width=20,textvariable = bms_v)
    syse = tk.Entry(lf,width=20,textvariable = sys_v)
    tore =  tk.Entry(lf,width=20,textvariable = Tor_v)
    Ge =  tk.Entry(lf,width=20,textvariable = G_v)
    thetae =  tk.Entry(lf,width=20,textvariable = theta_v)
    pose = ttk.Combobox(lf,values=['Center','End'],textvariable=Pos_v)#,activestyle='dotbox')
    Tmaxe =  tk.Entry(lf,width=20,textvariable = Tmax_v)
    Mmaxe =  tk.Entry(lf,width=20,textvariable = Mmax_v)
    
    ## Griding the entry boxes

    pe.grid(row=0,column=1,padx=25,pady=8)
    we.grid(row=1,column=1,padx=25,pady=8)
    rpme.grid(row=2,column=1,padx=25,pady=8)
    Lene.grid(row=3,column=1,padx=25,pady=8)
    fose.grid(row=4,column=1,padx=25,pady=8)
    bmse.grid(row=5,column=1,padx=25,pady=8)
    syse.grid(row=6,column=1,padx=25,pady=8)
    tore.grid(row=7,column=1,padx=25,pady=8)
    Ge.grid(row=8,column=1,padx=10,pady=8)
    thetae.grid(row=9,column=1,padx=10,pady=8)
    pose.grid(row=10,column=1,padx=10,pady=8)
    Tmaxe.grid(row=11,column=1,padx=10,pady=8)
    Mmaxe.grid(row=12,column=1,padx=10,pady=8)
    ## Submit Buttons
    s_btn = tk.Button(lf,text='\aDesign the Shaft for above parameters')
    s_btn.grid(row=13,columnspan=2,pady=8)

    def submit():
        global ss
        # Getting values of entry boxes and saving variable
        P = pe.get()
        rpm = rpme.get()
        fos = fose.get()
        sys = syse.get()
        t_r = tore.get()
        syb = bmse.get()
        W = we.get()
        G = Ge.get()
        theta = thetae.get()
        L = Lene.get()
        pos = pose.get()
        Tmax = Tmaxe.get()
        Mmax = Mmaxe.get()
        ss = SolidShaft(P,W,rpm,fos,t_r,sys,syb,L,theta,G,pos,Tmax,Mmax)
        dia = ss.calc_diameter()

        deb = tk.Toplevel()
        deb.geometry('720x720')
        lf.pack_forget()
        tl.pack_forget()
        deb.bg='lightblue'
        deb.title('Dimensions of your Design Shaft')    
        ttk.Label(deb,text=f'\n\n\tTorque Ratio given \t{ss.Tratio}% ',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'\tPower Given                           {ss.P} Watt',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'\tLoad Given                           {ss.W}N',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'\tFactor of Safety Given                           {fos}',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'\tTheta Given  0                         {r(ss.theta,2)} ',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'\tModulus of Rigidity                           {r(ss.G,2)}',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'\tRotation / minute (Rpm)                         {rpm}rpm',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'\tMax Twisting Moment                           {r(ss.Tmax,2)} - {r(ss.Tmean,2)} N-mm',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'\tMax Bending Moment                           {ss.Mmax} - {ss.Mmean} N-mm',font=('italian',17,'bold')).pack(fill='x')
        if ss.fos!=1:
            ttk.Label(deb,text=f'\tULtimate Shear stress given                           {sys} N/mm^2',font=('italian',17,'bold')).pack(fill='x')
            ttk.Label(deb,text=f'\tULtimate Bending stress given                           {syb} N/mm^2',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'\tShear Stress considered                           {ss.tau}N/mm^2',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'\tBending Stress considered                           {ss.sigma_b}N/mm^2',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'\tDiameter of Bending Shaft                      {r(ss.d_m,2)}mm',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'\tDiameter of Twsiting Shaft                      {r(ss.d_t,2)}mm',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'\tDiameter of Shaft                      {dia}mm',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'\tTwisitng Moment  TE                      {ss.TE}N-mm',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'\tBending Moment  ME                    {ss.ME}N-mm',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'\tpostition Given                 {ss.position}',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'\tMass of Cylinder for 1 m length                 {r(ss.calc_mass(),2)} g',font=('italian',17,'bold')).pack(fill='x')
        
        ttk.Label(deb,text='Do you want this dimension in word file or pdf file. Then press the below button to get data',font=('italian',14,'bold')).pack(fill='x')
        
        def get_btn(e=None):
            url = ''
            url = filedialog.asksaveasfile(mode = 'w',defaultextension='.pdf',filetypes = (('Text Files','*.txt'),('Word File','*.word'),('PDF File','*.pdf'),('CSv File','*.csv'),('All Files','*.*')))       
            if url:
                url.write(f'Given Parameters \n\n Power Given\t:{P}N\ntWISTING Moment\t:{t_r}\n\n\nShear Stress given\t-->{sys}N\nDiameter of Shaft\t: {dia}mm\nRotation Per Minute\t : {rpm}')
                url.close()
            else:
                return
            
        get_btn = ttk.Button(deb,text='Get Dimension to the file',command=get_btn)
        get_btn.pack(pady = 20)
        draw_btn = ttk.Button(deb,text="Design 2D drawing in AutoCAD",command=ss.draw_drawing)
        draw_btn.pack(pady=20)
        return ss

    s_btn.config(command=submit)
    swin.mainloop()
    return ss
    


def TK_HS():
    hs = None
    hwin = tk.Tk()
    lf = tk.LabelFrame(hwin,text='\n Plese enter following details to get the design of HOllow Shaft',font=('italian',18))
    lf.pack(pady=10)

    ## Labels
    k_l = ttk.Label(lf,text="Enter k .\nIf you don't know please leave it blank or type 0 ",font=(6),foreground='blue')#background='#ebc663')
    p_l= ttk.Label(lf,text='Power to be Transmitted P in KW',font=(14),foreground='blue')#,background='#ebc663')
    w_l= ttk.Label(lf,text='Load on Shaft W',font=(14),foreground='blue')#,background='#ebc663')
    Rpm_l = ttk.Label(lf,text="Enter Rpm .\nIf you don't know please leave it blank or type 0 ",font=(6),foreground='blue')#,background='#ebc663')
    Len_l = ttk.Label(lf,text="Enter Length in m.\nIf you don't know please leave it blank or type 0 ",font=(6),foreground='blue')#,background='#ebc663')
    bms_l = ttk.Label(lf,text="Enter Bending Stress in N/mm2 .\nIf not applicable please leave it blank or type 0 ",font=(6),foreground='blue')#,background='#ebc663')
    sys_l = ttk.Label(lf,text="Enter Shear Stress Strength of material in N/mm2.\nIf you don't know please leave it blank or type 0 ",font=(6),foreground='blue')#,background='#ebc663')
    Tor_l = ttk.Label(lf,text="Enter Torque excedence in %.\nIf you don't know please leave it blank or type 0 ",font=(6),foreground='blue')#,background='#ebc663')
    Fos_l = ttk.Label(lf,text="Enter Factor of Safety.\nIf you don't know please leave it blank or type 1 ",font=(6),foreground='blue')#,background='#ebc663')
    Pos_l = ttk.Label(lf,text="Select Position of Load.\nBy default it will be considered as center",font=(6),foreground='blue')#,background='#ebc663')
    G_l = ttk.Label(lf,text="Enter Modulus of rigidity in GN/m2.\nBy default it will be 0",font=(6),foreground='blue')#,background='#ebc663')
    theta_l = ttk.Label(lf,text="Enter Theta (0) in degrees \n By default it is 0",font=(6),foreground='blue')#,background='#ebc663')
    Tmax_l = ttk.Label(lf,text="Enter Bending Moment if known(0) \n By default it is 0",font=(6),foreground='blue')#,background='#ebc663')
    Mmax_l = ttk.Label(lf,text="Enter Twisting Moment if Known (0)",font=(6),foreground='blue')#,background='#ebc663')
    

    p_l.grid(row=0,column=0,padx=20,pady=8)
    w_l.grid(row=1,column=0,padx=20,pady=8)
    Rpm_l.grid(row=2,column=0,padx=20,pady=8)
    Len_l.grid(row=3,column=0,padx=20,pady=8)
    Fos_l.grid(row=4,column=0,padx=20,pady=8)
    bms_l.grid(row=5,column=0,padx=20,pady=8)
    sys_l.grid(row=6,column=0,padx=20,pady=8)
    k_l.grid(row=7,column=0,padx=20,pady=8)
    Tor_l.grid(row=8,column=0,padx=20,pady=8)
    G_l.grid(row=9,column=0,padx=20,pady=8)
    theta_l.grid(row=10,column=0,padx=20,pady=8)
    Pos_l.grid(row=11,column=0,padx=20,pady=8)
    Tmax_l.grid(row=12,column=0,padx=20,pady=8)
    Mmax_l.grid(row=13,column=0,padx=20,pady=8)
    
    
    ##Entry boxes

    ## Describing variables

    p_v = tk.IntVar()
    w_v = tk.IntVar()
    Rpm_v = tk.IntVar()
    Len_v = tk.IntVar()
    bms_v = tk.IntVar()
    fos_v = tk.IntVar(value=1)
    sys_v = tk.IntVar()
    Tor_v = tk.IntVar()
    Pos_v = tk.StringVar()
    G_v = tk.IntVar()
    k_v = tk.IntVar()
    Tmax_v = tk.IntVar()
    Mmax_v = tk.IntVar()
    theta_v = tk.IntVar()
    ## Entry boxes created

    pe = tk.Entry(lf,width=20,textvariable = p_v)
    we = tk.Entry(lf,width=20,textvariable = w_v)
    rpme = tk.Entry(lf,width=20,textvariable = Rpm_v)
    Lene = tk.Entry(lf,width=20,textvariable = Len_v)
    fose = tk.Entry(lf,width=20,textvariable = fos_v)
    bmse = tk.Entry(lf,width=20,textvariable = bms_v)
    syse = tk.Entry(lf,width=20,textvariable = sys_v)
    ke =  tk.Entry(lf,width=20,textvariable = k_v)
    tore =  tk.Entry(lf,width=20,textvariable = Tor_v)
    Ge =  tk.Entry(lf,width=20,textvariable = G_v)
    thetae =  tk.Entry(lf,width=20,textvariable = theta_v)
    pose = ttk.Combobox(lf,values=['Center','End'],textvariable=Pos_v)#,activestyle='dotbox')
    Tmaxe =  tk.Entry(lf,width=20,textvariable = Tmax_v)
    Mmaxe =  tk.Entry(lf,width=20,textvariable = Mmax_v)
    ## Griding the entry boxes

    pe.grid(row=0,column=1,padx=25,pady=8)
    we.grid(row=1,column=1,padx=25,pady=8)
    rpme.grid(row=2,column=1,padx=25,pady=8)
    Lene.grid(row=3,column=1,padx=25,pady=8)
    fose.grid(row=4,column=1,padx=25,pady=8)
    bmse.grid(row=5,column=1,padx=25,pady=8)
    syse.grid(row=6,column=1,padx=25,pady=8)
    ke.grid(row=7,column=1,padx=25,pady=8)
    tore.grid(row=8,column=1,padx=25,pady=8)
    Ge.grid(row=9,column=1,padx=10,pady=8)
    thetae.grid(row=10,column=1,padx=25,pady=8)
    pose.grid(row=11,column=1,padx=10,pady=8)
    Tmaxe.grid(row=12,column=1,padx=25,pady=8)
    Mmaxe.grid(row=13,column=1,padx=25,pady=8)
    ## Submit Buttons
    s_btn = ttk.Button(lf,text='Design the Shaft for above parameters')
    s_btn.grid(row=14,columnspan=2,pady=20)


    def submit_HS():
        global hs
        P = pe.get()
        rpm = rpme.get()
        fos = fose.get()
        sys = syse.get()
        t_r = tore.get()
        syb = bmse.get()
        W = we.get()
        G = Ge.get()
        theta = thetae.get()
        L = Lene.get()
        pos = pose.get()
        k = ke.get()
        Tmax = Tmaxe.get()
        Mmax = Mmaxe.get()
        hs = HollowShaft(P,W,rpm,fos,t_r,sys,syb,L,k,theta,G,pos,Tmax,Mmax)
        #if tor==0:
        #tor = hs.calc_twisting_moment()
        dia1,dia2 = hs.calc_diameter()
        # elif tor!=0:
        #     dia1,dia2 = hs.calc_diameter()
        deb = tk.Toplevel()
        deb.geometry('720x720')
        lf.pack_forget()
        tl.pack_forget()
        deb.bg='white'
        deb.title('Dimensions of your Design Shaft')    
        ttk.Label(deb,text=f'\n\n\tTorque Ratio given \t{hs.Tratio}% ',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'\tPower Given                           {P} KW',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'\tLoad Given                           {W}N',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'\tFactor of Safety Given                           {fos}',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'\tTheta Given  0                         {r(hs.theta,2)} - {r(hs.Tmean,2)} N-m',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'\tModulus of Rigidity                           {r(hs.G,2)} - {r(hs.Tmean,2)} N-m',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'\tRotation / minute (Rpm)                         {rpm}rpm',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'\tMax Twisting Moment                           {r(hs.Tmax,2)} - {r(hs.Tmean,2)} N-m',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'\tMax Bending Moment                           {hs.Mmax} - {hs.Mmean} N-mm',font=('italian',17,'bold')).pack(fill='x')
        if hs.fos!=1:
            ttk.Label(deb,text=f'\tULtimate Shear stress given                           {sys} N/mm^2',font=('italian',17,'bold')).pack(fill='x')
            ttk.Label(deb,text=f'\tULtimate Bending stress given                           {syb} N/mm^2',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'\tBending Stress considered                           {hs.sigma_b}N/mm^2',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'\tOuter Diameter of Bending Shaft                      {hs.bending_OD}mm',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'\tInner Diameter of Bending Shaft                     {hs.bending_Id}mm',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'\tShear Stress considered                           {hs.tau}N/mm^2',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'\tOuter Diameter of Twsiting Shaft                     {hs.twisiting_OD}mm',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'\tInner Diameter of Twisting Shaft                     {hs.twisiting_ID}mm',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'\tSafe Outer Diameter for Shaft                     {hs.OD}mm',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'\tSafe Inner Diameter for Shaft                   {hs.Id}mm',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'\tTwisitng Moment  TE                      {hs.TE}N-mm',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'\tBending Moment  ME                    {hs.ME}N-mm',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'\tpostition Given                 {hs.position}',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'\tMass of Cylinder for 1 m length                 {r(hs.calc_mass(),2)} g',font=('italian',17,'bold')).pack(fill='x')
        
        def get_btn(e=None):
            url = ''
            url = filedialog.asksaveasfile(mode = 'w',defaultextension='.pdf',filetypes = (('Text Files','*.txt'),('Word File','*.word'),('PDF File','*.pdf'),('CSv File','*.csv'),('All Files','*.*')))           
            if url:
                url.write(f'Given Parameters \n\n Power Given\t:{P}N\nTorque / Twisting Moment\t:{hs.TE}\n\n\nShear Stress given\t-->\t:{sys}N\nRotation/Minute (Rpm)\t-->\t{rpm}\nOuter Diameter of Shaft\t-->\t{dia1}mm\nInner Diameter of Shaft\t-->\t{dia2}mm')
                url.close()
            else:
                return
        get_btn = ttk.Button(deb,text='Get Dimension to the file',command=get_btn)
        get_btn.pack(pady = 20)
        draw_btn = ttk.Button(deb,text="Design 2D drawing in AutoCAD",command=hs.draw_drawing)
        draw_btn.pack(pady = 20)
        return hs

    s_btn.config(command=submit_HS)
    hwin.mainloop()
    return hs

def TK_CS():
    
    cswin = tk.Tk()
    lf = tk.LabelFrame(cswin,text='\n Plese enter following details to get the design of HOllow Shaft',font=('italian',18))
    lf.pack(pady=10)

    ## Labels
    p_l= ttk.Label(lf,text='Power to be Transmitted\n',font=(14),foreground='blue',background='#ebc663')
    fos_l = ttk.Label(lf,text="Enter Fos .\nIf you don't know please leave it blank or type 0 ",font=(6),foreground='blue',background='#ebc663')
    Rpm_l = ttk.Label(lf,text="Enter Rpm .\nIf you don't know please leave it blank or type 0 ",font=(6),foreground='blue',background='#ebc663')
    sys_l = ttk.Label(lf,text="Enter Shear Stress Strength of material.\nIf you don't know please leave it blank or type 0 ",font=(6),foreground='blue',background='#ebc663')
    k_l = ttk.Label(lf,text="Enter k .\nIf you don't know please leave it blank or type 0 ",font=(6),foreground='blue',background='#ebc663')
    Tor_l = ttk.Label(lf,text="Enter Torque excedence %.\nIf you don't know please leave it blank or type 0 ",font=(6),foreground='blue',background='#ebc663')

    p_l.grid(row=1,column=0,pady=10,padx=25)
    fos_l.grid(row=2,column=0,pady=10,padx=25)
    Rpm_l.grid(row=3,column=0,pady=10,padx=25)
    sys_l.grid(row=4,column=0,pady=10,padx=25)
    k_l.grid(row=5,column=0,pady=10,padx=25)
    Tor_l.grid(row=6,column=0,pady=10,padx=25)
    
    p_v = tk.IntVar()
    fos_v = tk.IntVar()
    Rpm_v = tk.IntVar()
    sys_v = tk.IntVar()
    k_v = tk.IntVar()
    tor_v = tk.IntVar()
    ## Entry boxes created

    pe = tk.Entry(lf,width=20,textvariable = p_v)
    fose =  tk.Entry(lf,width=20,textvariable = fos_v)
    rpme = tk.Entry(lf,width=20,textvariable = Rpm_v)
    syse = tk.Entry(lf,width=20,textvariable = sys_v)
    ke = tk.Entry(lf,width=20,textvariable = k_v)
    tore = tk.Entry(lf,width=20,textvariable = tor_v)
    ## Griding the entry boxes

    pe.grid(row=1,column=1,padx=15,pady=30)
    fose.grid(row=2,column=1,padx=15,pady=30)
    rpme.grid(row=3,column=1,padx=15,pady=30)
    syse.grid(row=4,column=1,padx=15,pady=30)
    ke.grid(row=5,column=1,padx=15,pady=30)
    tore.grid(row=6,column=1,padx=15,pady=30)

      ## Submit Buttons
    s_btn = ttk.Button(lf,text='Comparison of the Hollow and Solid Shaft for above parameters')
    s_btn.grid(row=6,columnspan=2,pady=20)


    def submit_HS():
        P = pe.get()
        fos = fose.get()
        rpm = rpme.get()
        sys = syse.get()
        k = ke.get()
        t_r = tore.get()

        hs = HollowShaft(P,shearStress=sys,rpm=rpm,k=k,fos=fos,position='center',T_ratio=t_r)
        ss = SolidShaft(P,shearStress=sys,rpm=rpm,fos=fos,position='center',T_ratio=t_r)
        #if tor==0:
        dia = ss.calc_diameter()
        dia1,dia2 = hs.calc_diameter()
        # elif tor!=0:
        #     dia1,dia2 = hs.calc_diameter()
        deb = tk.Toplevel()
        deb.geometry('360x720')
        lf.pack_forget()
        tl.pack_forget()

        deb.title('Comparison of Shafts')
        ttk.Label(deb,text=f'Power Given                           {P} W',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'Twisting Moment\'s for\n \t Hollow one\t{hs.Tmax}N-m\n\tSolid one\t {ss.Tmax} N-m',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'Factor of Safety                           {hs.fos}',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'Rotation / minute (Rpm)                         {rpm}rpm',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'Shear Stress given                           {sys}N/mm^2',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'Outer Diameter of Shaft                      {dia1}mm',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'Diameter of solid Shaft                 {dia}mm',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'Diameter ratio given                     {hs.k}',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'Inner Diameter of Shaft                      {dia2}mm',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'\nMass of Solid Shaft                      {r(ss.calc_mass(),2)}g',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text=f'Position Given                      {hs.position}',font=('italian',17,'bold')).pack(fill='x')
        ttk.Label(deb,text='Do you want this dimension in word file or pdf file. Then press the below button to get data',font=('italian',14,'bold')).pack(fill='x')
        def get_btn(e=None):
            url = ''
            url = filedialog.asksaveasfile(mode = 'w',defaultextension='.pdf',filetypes = (('Text Files','*.txt'),('Word File','*.word'),('PDF File','*.pdf'),('CSv File','*.csv'),('All Files','*.*')))           
            if url:
                url.write(f'Given Parameters \n\n Power Given\t:{P} Watts\nTorque / Twisting Moment\t:{ss.Tmax}\n\n\nShear Stress given\t-->\t:{sys}N\nRotation/Minute (Rpm)\t-->\t{rpm}rpm\nOuter Diameter of Shaft\t-->\t{dia1}mm\nInner Diameter of Shaft\t-->\t{dia2}mm\nDiameter of Solid Shaft {dia}mm')
                url.close()
            else:
                return
        get_btn = ttk.Button(deb,text='Get Dimension to the file',command=get_btn)
        get_btn.pack(pady = 20)
        return 0

    s_btn.config(command=submit_HS)
    cswin.mainloop()
    




ss_btn = tk.Button(win,text='\aDesign Solid Shaft',width=100,height=5,bg='lightblue',border=35)
ss_btn.pack(padx=50,pady = 50)
ss_btn.config(command=TkSolidShaft)
hs_btn = tk.Button(win,text='\aDesign Hollow Shaft',width=100,height=5,bd=25)
hs_btn.pack(padx=50,pady = 50)
hs_btn.config(command=TK_HS)
cs_btn = tk.Button(win,text='\aCompare Hollow & Solid Shaft for Same parameters',width=100,height=5,bd=15)
cs_btn.pack(padx=50,pady = 50)
cs_btn.config(command=TK_CS)
win.mainloop()
