## importing Packages
import math,time
import tkinter as tk
import os,shutil,datetime
from tkinter import font,ttk,filedialog
from tkinter import messagebox as mbox
from csv import DictWriter as Dw 
import numpy as np
t = time.time()
pi = math.pi 
srt = math.sqrt 
p4 = round(pi/4,3)

'''   Functions to solve quadratic equations   '''
def solve_poly(a,b,c):
    p = np.poly1d([a,b,c])
    roots = p.r
    print(roots)
    r = float(max(roots))
    return r
def solve_quadra(a,b,c):
    d = (b**2)-(4*a*c)
    sol1 = (-b-srt(d))/(2*a)
    sol2 = (-b+srt(d))/(2*a)
    print(sol1,sol2,sep = ' ---> ')
    r = max(sol1,sol2)
    return r

'''Creating Class Cotter pin '''
#print(solve_poly(2,-5,3))
#print(solve_quadra(2,-5,3))
class CotterPin:
    IV = "Invalid Value"
    def __init__(self,Power,Fos=1,Syt=None,Syc=None,Sys=None):
        self.Power = Power
        self.Fos = Fos
        self.Syt = Syt
        self.Syc = Syc
        self.Sys = Sys

    ## Setting Variables
    fos = None
    P = None 
    #Efos = None
    #EP = None
    ''' Checking Fos '''
    def check_fos(self):
        global fos
        try:
            fos = float(self.Fos)
            if fos <= 0:
                mbox.showerror('Invalid Value','Setting FOS to 1.5')
                fos = 1.5
                print(CotterPin.IV)
            print('\t',fos,'    --->'.center(25," "),'FOS')
        except ValueError:
            mbox.showerror('Invalid Value','Plesae Enter fos correctly')
            print(CotterPin.IV)
        else:
            return fos
    '''Checking Power '''        
    def check_Power(self):
        global P
        try:
            P = float(self.Power) 
            if P <= 0:
                mbox.showinfo('Invalid Value','Please enter Power value correctly')
                print(CotterPin.IV)
            print('\t',P , ' ---> '.center(20," "),'Power')              
        except ValueError:
            mbox.showerror('Invalid Value','Plesae Enter fos correctly')
            print(CotterPin.IV)
        ## Now Getting Forces Correctly 
        else: 
            return P
 
    ''' Checking Forces '''
    sc = None
    st = None
    tau = None 
    def check_forces(self):
        global st, tau, sc
        try:
            Syt = float(self.Syt)
            Syc = float(self.Syc)
            Sys = float(self.Sys)
        except ValueError:
            mbox.showerror('Invalid Value','Please Enter correct forces')
            print(CotterPin.IV)
        else:
            #print(f"sc: {st}")
            if Syt <= 0 and Sys <= 0 and Syc <= 0:
                mbox.showinfo('Strength 0 !','All strength are 0 ?. Please Enter Valid Forces')
                print(CotterPin.IV)
            elif Syt > 0 and Sys >0 and Syc > 0:
                st = round(Syt/fos , 3)
                sc = round(Syc/fos , 3)
                tau = round(Sys/fos , 3)
            else:
                if Syt > 0 and Syc > 0:
                    if Sys <= 0:
                        Sys = Syc
                        #Sys = Sys
                        st = round(Syt/fos , 3)
                        sc = round(Syc/fos , 3)
                        tau = round(Sys/fos , 3)
                    elif Syt <= 0 and Syc>0:
                        if Sys <=0:
                            Sys = Syc
                        Sys = Sys
                        st = round(Syc/fos , 3)
                        sc = round(Syc/fos , 3)
                        tau = round(Sys/fos , 3)           
                    elif Syt>0 and Syc<=0:
                        Syc = 1.2*Syt
                        if Sys <= 0:
                                Sys = 0.5*Syt
                        Sys = Sys
                        st = round(Syt/fos , 3)
                        sc = round(Syc/fos , 3)
                        tau = round(Sys/fos , 3)
                    elif Syt<=0 and Syc <= 0 and Sys>0:
                        Syc = Sys
                        st = round(Syc/fos , 3)
                        #Syt = st*fos
                        sc = round(Syc/fos , 3)
                        tau = round(Sys/fos , 3)
            return Syt, Sys, Syc
        print(st, sc, tau, P, fos, Syt, Syc, Sys, sep="\n")
        return st, sc, tau, P, fos, Syt, Syc, Sys

    def check_all_variables(self):
        global fos, P, st, sc, tau
        self.check_fos()
        self.check_Power()
        self.check_forces()           
        return P, fos, st, sc, tau  
    ## Doing Calculations                              
    d = None  ## Diameter of rod
    t = None  ## Thickness of rod
    d2 = None
    a = None
    t1 = None
    d1 = None
    d4 = None
    b = None
    L = None  ## Length Of Cotter
    e = None

    ## Defining Function
    def design_of_rod_under_tension(self):
        global d
        d = math.ceil(srt(P/(st*p4)))
        print('\t ',round(d,2),'mm',' ---> '.center(23," "),'d')
        return d 
    
    def design_of_spigot_end_tensile(self):
        global d2, t
        d2 = srt(P/((p4-0.25)*st))
        t = d2/4
        print('\t',round(d2,2),'mm',' ---> '.center(20," "),'d2')
        print('\t',round(t,2),'mm',' ---> '.center(20," "),'t')
        return d2 , t
    def design_of_spigot_considering_crushing(self):
        global d2,t
        d2 = math.ceil(srt((P*4)/sc))
        t = math.ceil(d2/4)
        print('\t',round(d2,2),'mm',' ---> '.center(20," "),'d2')
        print('\t',round(t,2),'mm',' ---> '.center(20," "),'t') 
        return d2,t, True
    
    def shearing_failure_of_spigot(self):
        global a
        a = math.ceil(P/(tau*d2*2))
        print('\t',a ,'mm','---> '.center(20," "),'a')
        return a
    
    def my_change_fos(self):
        global fos,P
        f = float(input('Please Enter Your Choice for Fos : '))
        d = CotterPin(P,f,self.Syt,self.Syc,self.Sys)
        d.run_all()
    def change_parameters(self):
        global fos,P
        d = input("Please change Parameters or increase fos 'Y' add your choice of fos 'N' to change parameters by going out of program ")
        if d.lower()=='y':
            self.my_change_fos()        
        else:
           print("Change Parameters ")
           mbox.showerror('Invalid Parameters','Please Enter parameters by retartiung program')
           

           
    def crushing_of_spigot_end(self):
        sc = P / (d2*t)
        if int(sc) == int(self.Syc):
            return sc
        if int(sc) < int(self.Syc):
            print(f"\n\tDesign is safe upto this point as {sc} < {self.Syc}\n")
        elif int(sc) > int(self.Syc):
             print(f"\n\tDesign is not safe upto this point as {sc} >> {self.Syc}\n")
             self.design_of_spigot_considering_crushing()
             if self.crushing_of_spigot_end()==False:
                 self.my_change_fos()
             else:
                 self.crushing_of_spigot_end()
        return 
    o = None
    def spigot_end(self):
        return self.design_of_spigot_end_tensile(), self.crushing_of_spigot_end()
        
    def design_of_spigot_collar(self):
        t1 = math.ceil(P/(tau*pi*d2))
        print('\t',t1,'mm',' ---> '.center(20," "),'t1')
        return t1
    
    def design_of_socket_under_tension(self):
        global o,d1,t,p4
        A = P/st
        o = A+(p4*(d2**2)-(d2*t))
        print('\t\t',o)
        D1 = solve_quadra(p4,-t,-o)
        D2 = solve_poly(p4,-t,-o)
        d1 = math.ceil(max(D1,D2))
        print('\t',d1,'mm',' ---> '.center(20," "),'d1')
        return d1
    
    def design_of_socket_in_crushing_failure(self):
        global d4
        d4 = (P/(sc*t))+d2
        print('\t',math.ceil(d4),'mm',' ---> '.center(20," "),'d4')
        return d4
    
    def design_of_socket_in_shearing_failure(self):
        global d4
        c =  math.ceil(P/(2*tau*(d4-d2)))
        print('\t ',c,'mm',' ---> '.center(20," "),'c')
        return c
    
    def design_of_cotter_considering_shearing_failure(self):
        global L,e,d,t,b
        b = math.ceil(P/(tau*2*t))
        L = math.ceil(4*d)
        e = math.ceil(1.2*d)
        print('\t ',b,'mm',' ---> '.center(20," "),'b')
        print('\t',L,'mm',' ---> '.center(20," "),'L')
        print('\t',e,'mm',' ---> '.center(20," "),'e')
        return b,L,e
    
    def bending_of_cotter(self):
        global b,t,P,d4,d2
        z = (t*(b**2))/6
        m = (P/2)*((d4/6) + (d2/12))
        sb = math.ceil(m/z)
        q = float(self.Syc)*t  ## Because Tkinter takes input in string format so instead of declareing new varialble to forces i directly converted it into float to save memory
        s = print(f'MAx Bending Movement ----->  {m}')
        s
        print(s)
        if float(sb) > float(self.Syc):
            print(f'sb is greater than Syc {sb} >> {self.Syc}')
            b = math.ceil(srt((m*6)/(q)))
            print('\t',b,' ---> '.center(20," "),'b')
            self.bending_of_cotter()
        else:
            print(f'sb is less than Syc {sb} << {self.Syc}')
    def run_all(self):
        self.check_all_variables()
        self.design_of_rod_under_tension()
        self.spigot_end()
        self.shearing_failure_of_spigot()
        self.design_of_spigot_collar()
        self.design_of_socket_under_tension()
        self.design_of_socket_in_crushing_failure()
        self.design_of_socket_in_shearing_failure()
        self.design_of_cotter_considering_shearing_failure()
        self.bending_of_cotter()

c = CotterPin("200000",1,80,60,0)
c.run_all()





''' **************    DESIGNING GUI FOR COTTER PIN   *************   '''
win = tk.Tk()
color = win.tk_setPalette('#ecb663')
##win.geometry('1200x720')
win.title('Design')
tl = tk.Label(win,text='DESIGN OF KNUCKLE PIN',relief='flat',fg='white',bg='blue',font=('times new roman',40,'bold'))
tl.pack(fill='x')



#####    CReating labels for the parametrs

########   first have to create lable frame and then in this label frame we will add labels

lf = tk.LabelFrame(win,text='\nWelcome to design of Cotter Pin. Plese enter following details to get the design of Knuckle pin',font=('italian',18))
lf.pack(pady=10)

## Labels
fosk = ttk.Label(lf,text='Factor Of Safety\n',foreground='blue',background='#ebc663',font=(14))
pk = ttk.Label(lf,text='Power to be Transmitted\n',font=(14),foreground='blue',background='#ebc663')
sytl = ttk.Label(lf,text="Enter Tensile Stress of material.\nIf you don't know please leave it blank or type 0 ",font=(6),foreground='blue',background='#ebc663')
sycl = ttk.Label(lf,text="Enter Compress Stress of material.\nIf you don't know please leave it blank or type 0 ",font=(6),foreground='blue',background='#ebc663')
sysl = ttk.Label(lf,text="Enter Shear Stress of material.\nIf you don't know please leave it blank or type 0 ",font=(6),foreground='blue',background='#ebc663')

fosk.grid(row=0,column=0,pady=10)
pk.grid(row=1,column=0,pady=10)
sytl.grid(row=2,column=0,padx=25,pady=10)
sycl.grid(row=3,column=0,pady=10)
sysl.grid(row=4,column=0,pady=10)

##Entry boxes

## Describing variables
fos_e = tk.IntVar()
p_e = tk.IntVar()
syt_e = tk.IntVar()
syc_e = tk.IntVar()
sys_e = tk.IntVar()

## Entry boxes created
fose = tk.Entry(lf,width=20,textvariable = fos_e)

pe = tk.Entry(lf,width=20,textvariable = p_e)
## Radio Buttons for POwer
##kpa = tk.Radiobutton(lf,text='KN').grid(row=1,column=2,padx=15,pady=30)
##mpa = tk.Radiobutton(lf,text='MN').grid(row=1,column=3,padx=15,pady=30)
##gpa = tk.Radiobutton(lf,text='GN').grid(row=1,column=4,padx=15,pady=30)

syte =  tk.Entry(lf,width=20,textvariable = syt_e)
syce = tk.Entry(lf,width=20,textvariable = syc_e)
syse = tk.Entry(lf,width=20,textvariable = sys_e)

    

## Griding the entry boxes
fose.grid(row=0,column=1,padx=15,pady=30)
pe.grid(row=1,column=1,padx=15,pady=30)
syte.grid(row=2,column=1,padx=15,pady=30)
syce.grid(row=3,column=1,padx=15,pady=30)
syse.grid(row=4,column=1,padx=15,pady=30)

## Submit Buttons
s_btn = ttk.Button(lf,text='Design the Cotter pin for above parameters')
s_btn.grid(row=5,columnspan=2)

## Defining Submit Process in Tkinter
def soln_label_frame():
    deb = tk.Toplevel()
    deb.geometry('1200x1200')
    lf.pack_forget()
    tl.pack_forget()
    
    deb.title('Dimensions of your Design Pin')
    ttk.Label(deb,text=f'Power Given                           {c.P}N',font=('italian',17,'bold')).pack(fill='x')
    ttk.Label(deb,text=f'Factor of Safety Selected             {c.fos}',font=('italian',17,'bold')).pack(fill='x')
    ttk.Label(deb,text=f'\n\nForces given\nShear Yield Strengrth:\t{c.Syt}N\nShear compression Strengrth:\t{c.Syc}N\nShear Stress:\t{c.Sys}N',font=('italian',15,'bold')).pack(fill='x')
    ttk.Label(deb,text=f'Diameter of rod                      {c.d}mm',font=('italian',17,'bold')).pack(fill='x')
    ttk.Label(deb,text=f'Diameter of Knuckle Pin             {c.d1}mm',font=('italian',17,'bold')).pack(fill='x')
    ttk.Label(deb,text=f'Thickness of single eye             {c.t}mm',font=('italian',17,'bold')).pack(fill='x')
    ttk.Label(deb,text=f'Thickness of Fork                   {c.d2}mm',font=('italian',17,'bold')).pack(fill='x')#,font=('italian',20,'bold'))
    ttk.Label(deb,text=f'Outside Diameter of Eye             {c.d4}mm',font=('italian',17,'bold')).pack(fill='x')#,font=('italian',20,'bold'))
    ttk.Label(deb,text='Analysis of failure of fork end in tension and shear',font=('italian',17,'bold')).pack(fill='x')#,font=('italian',20,'bold'))
    ttk.Label(deb,text='Analysis of failure of fork end in tension',font=('italian',17,'bold')).pack(fill='x')#,font=('italian',20,'bold'))
##    if st1<st:
##        ttk.Label(deb,text=f"Since st = {st1}N/mm2  <  {st}N/mm2 \n\t\tHence Fork End is safe against Tensile Failure",font=('italian',14,'bold')).pack(fill='x')#,font=('italian',20,'bold'))
##    else:
##        ttk.Label(deb,text=f"Since st = {st1}N/mm2  >  {st}N/mm2 \nHence Fork End is not safe against Tensile Failure\nYou have to change parameters to design the Safe Knuckle Pin").pack(fill='x')#,font=(20,'bold'))
##    ttk.Label(deb,text='\nNow analysis of Fork End in Shear',font=('italian',17,'bold')).pack(fill='x')#,font=('italian',20,'bold'))
##    if tau1<tau:
##        ttk.Label(deb,text=f"\nSince st = {tau1}N/mm2  <  {tau}N/mm2 \n\t\tHence Fork End is safe against Shear Failure",font=('italian',14,'bold')).pack(fill='x')#,font=('italian',20,'bold'))
##    else:
##        ttk.Label(deb,text=f"Since st = {tau1}N/mm2  >  {tau}N/mm2 \nHence Fork End is not safe against Shear Failure\nYou have to change parameters to design the Safe Knuckle Pin").pack(fill='x')#,font=(20,'bold'))
##    ttk.Label(deb,text='Do you want this dimension in word file or pdf file. Then press the below button to get data',font=('italian',14,'bold')).pack(fill='x')#,font=('italian',20,'bold'))
##    def get_btn(e=None):
##        url = ''
##        url = filedialog.asksaveasfile(mode = 'w',defaultextension='.pdf',filetypes = (('Text Files','*.txt'),('Word File','*.word'),('PDF File','*.pdf'),('CSv File','*.csv'),('All Files','*.*')))
##        if filetypes in url == filetypes.index[3]:
##               with open(url,'w') as f:
##                   d = DictWriter
##                   d.writeheader(f,fieldnames=['Name of Part','Dimensions in mm'])
##                   d.writerow({f'Diameter of rod': '{d}mm',
##                               f'Diameter of Knuckle Pin': '{Dp}mm',
##                               f'Thickness of single eye' : '{t}mm',
##                               f'Thickness of Fork' : '{T1}mm',
##                               f'Outside Diameter of Eye' : '{D}mm'})
##                   f.close()
##                   
##               
##        if url:
##            url.write(f'Given Parameters \n\n Power Given\t:{P}N\nFactor of Safety Selected\t:{Fos}\n\n\nForces given\t-->\nShear Yield Strengrth:{Syt}N\nShear compression Strengrth:{Syc}N\nShear Stress:{Sys}N\nDimensions of your Design Pin\n\nDiameter of rod\t: {d}mm\nDiameter of Knuckle Pin\t: {Dp}mm\nThickness of single eye\t: {t}mm\nThickness of Fork\t: {T1}mm\nOutside Diameter of Eye\t: {D}mm')
##            url.close()
##        else:
##            return
##        
    

        
    get_btn = ttk.Button(deb,text='Get Dimension to the file',command=get_btn)
    get_btn.pack(pady = 20)

def submit():
    print("None")
    PO = pe.get()
    FOS = fose.get()
    SYT = syte.get()
    SYC = syce.get()
    SYS = syse.get()
    c = CotterPin(PO,FOS,SYT,SYC,SYS)
    print(c.P,c.Syt,c.Syc,c.Sys,c.Fos,sep='\n')
    c.run_all()
    lf.pack_forget()
    sf = tk.LabelFrame(win,text = 'YOUR DIMENSIONS')
    soln_label_frame()
s_btn.config(command=submit)


## creating buttons for strength option

'''blf = ttk.LabelFrame(lf)
blf.grid(row=2,column=1)
syt_btn = ttk.Button(blf,text='Syt')
sct_btn = ttk.Button(blf,text='Sct')
sys_btn = ttk.Button(blf,text='Sys')


syt_btn.grid(row=0,column=0,padx=5)
syt_btn.grid(row=0,column=1,padx=5)
syt_btn.grid(row=0,column=2,padx=5)


## creating buttons for strength option
syt_btn = ttk.Button(lf,text='Syt')
sct_btn = ttk.Button(lf,text='Sct')
sys_btn = ttk.Button(lf,text='Sys')
'''

win.mainloop()
