import tkinter as tk
import os,shutil,datetime
from tkinter import font,ttk,filedialog
from tkinter import messagebox as mbox
import math
from csv import DictWriter 
pi = math.pi
win = tk.Tk()
color = win.tk_setPalette('#ebc663')
##win.geometry('1200x720')
win.title('Design')
tl = tk.Label(text='DESIGN OF KNUCKLE PIN',relief='flat',fg='white',bg='blue',font=('times new roman',40,'bold'))
tl.pack(fill='x')


#####    CReating labels for the parametrs

########   first have to create lable frame and then in this label frame we will add labels

lf = tk.LabelFrame(win,text='\nWelcome to design of Knuckle Pin. Plese enter following details to get the design of Knuckle pin',font=('italian',18))
lf.pack(pady=10)

## Labels
fos = ttk.Label(lf,text='Factor Of Safety\n',foreground='blue',background='#ebc663',font=(14))
p = ttk.Label(lf,text='Power to be Transmitted\n',font=(14),foreground='blue',background='#ebc663')
sytl = ttk.Label(lf,text="Enter Shear Strength of material.\nIf you don't know please leave it blank or type 0 ",font=(6),foreground='blue',background='#ebc663')
sycl = ttk.Label(lf,text="Enter Compress Shear Strength of material.\nIf you don't know please leave it blank or type 0 ",font=(6),foreground='blue',background='#ebc663')
sysl = ttk.Label(lf,text="Enter Shear Stress Strength of material.\nIf you don't know please leave it blank or type 0 ",font=(6),foreground='blue',background='#ebc663')

fos.grid(row=0,column=0,pady=10)
p.grid(row=1,column=0,pady=10)
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


syt =  tk.Entry(lf,width=20,textvariable = syt_e)
syc = tk.Entry(lf,width=20,textvariable = syc_e)
sys = tk.Entry(lf,width=20,textvariable = sys_e)

    

## Griding the entry boxes
fose.grid(row=0,column=1,padx=15,pady=30)
pe.grid(row=1,column=1,padx=15,pady=30)
syt.grid(row=2,column=1,padx=15,pady=30)
syc.grid(row=3,column=1,padx=15,pady=30)
sys.grid(row=4,column=1,padx=15,pady=30)

## Submit Buttons
s_btn = ttk.Button(lf,text='Design the knuckle pin for above parameters')
s_btn.grid(row=5,columnspan=2)



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



##   Defining Function for the calculation
def submit():
    Fos = fose.get()
    P = pe.get()
    Syt = syt.get()
    Syc = syc.get()
    Sys = sys.get()
    try:
        Fos = float(Fos)
        if Fos == 0:
           Fos = 1
    except ValueError:
        mbox.showerror('Invalid Value','Plesae Enter Fos correctly')
    try:
        P = float(P)
        if P == 0:
           mbox.showinfo('Invalid Value','Please enter Power value correctly')
##        elif P != 0:
##            force = {'KN':10**3,'MN':10**6,'GN':10**9}
##            for i in force:
##                lf.add_radiobutton(label=i,variable=P*force.get(i))
                
    except ValueError:
        mbox.showerror('Invalid Value','Plesae Enter Power correctly')
    ## Now Getting Forces Correctly    
    else:
        try:
            Syt = float(Syt)
            Syc = float(Syc)
            Sys = float(Sys)
        except ValueError:
            mbox.showerror('Invalid Value','Please Enter correct forces')
        else:
            if Syt == 0 and Sys == 0 and Syc == 0:
                mbox.showinfo('Strength 0 !','All strength are 0 ?. Please Enter Valid Forces')
            else:
                if Syt != 0 and Syc != 0 :
                    if Sys == 0:
                        Sys = Syc
                    Sys = Sys
                    st = round(Syt/Fos , 3)
                    sc = round(Syc/Fos , 3)
                    tau = round(Sys/Fos , 3)
                elif Syt == 0 and Syc!=0:
                    if Sys == 0:
                        Sys = Syc
                    Sys = Sys
                    st = round(Syc/Fos , 3)
                    sc = round(Syc/Fos , 3)
                    tau = round(Sys/Fos , 3)
                        
                elif Syt!=0 and Syc==0:
                    Syc = 1.2*Syt
                    if Sys == 0:
                        Sys = 0.5*Syt
                    Sys = Sys
                    st = round(Syt/Fos , 3)
                    sc = round(Syc/Fos , 3)
                    tau = round(Sys/Fos , 3)
                elif Syt==0 and Syc == 0 and Sys!=0:
                    Syc = Sys
                    st = round(Syc/Fos , 3)
                    sc = round(Syc/Fos , 3)
                    tau = round(Sys/Fos , 3)
                
                else:
                    pass                
                    
                    
    ## Diameter of rod             
    a1 = st*pi/4
    d = round(((P/a1)**0.5 + 1),2)

    ## Diameter of Knuckle Pin
    a2 = 2*pi*tau/4
    Dp = round((P/a2)**0.5) + 1

    ## Thickness of Single Eye
    t1 = round((1.25*d + 1),2)
    t2 = round((P/(sc*Dp) + 1),2)
    if t1>t2:
        t = t1
    elif t1<t2:
        t = t2

    ## Thickness of Fork
    t3 = round(((0.75*d) + 1),2)
    t4 = round(((P/(sc*Dp*2)) + 1),2)
    if t3>t4 :
        T1 = t3
    else :
        T1 = t4

    ## Diameter
    a5 = P/(tau*t)
    D = round((a5+Dp+1),2)
    
    

    ## Analysis of Fork end in Tension failure
    a6 = 2*T1*(D-Dp)
    st1 = round((P/a6),2)

    ## Analysis of Fork end in shear
    a7 = 2*T1*(D-Dp)
    tau1 = round((P/a7),2)

##    print(d,Dp,st1,tau1,t,T1,end='\n',sep=' ')

##    ## Dialogue Box
    deb = tk.Toplevel()
    deb.geometry('1200x1200')
    lf.pack_forget()
    tl.pack_forget()
    
    deb.title('Dimensions of your Design Pin')
    ttk.Label(deb,text=f'Power Given                           {P}N',font=('italian',17,'bold')).pack(fill='x')
    ttk.Label(deb,text=f'Factor of Safety Selected             {Fos}',font=('italian',17,'bold')).pack(fill='x')
    ttk.Label(deb,text=f'\n\nForces given\nShear Yield Strengrth:\t{Syt}N\nShear compression Strengrth:\t{Syc}N\nShear Stress:\t{Sys}N',font=('italian',15,'bold')).pack(fill='x')
    ttk.Label(deb,text=f'Diameter of rod                      {d}mm',font=('italian',17,'bold')).pack(fill='x')
    ttk.Label(deb,text=f'Diameter of Knuckle Pin             {Dp}mm',font=('italian',17,'bold')).pack(fill='x')
    ttk.Label(deb,text=f'Thickness of single eye             {t}mm',font=('italian',17,'bold')).pack(fill='x')
    ttk.Label(deb,text=f'Thickness of Fork                   {T1}mm',font=('italian',17,'bold')).pack(fill='x')#,font=('italian',20,'bold'))
    ttk.Label(deb,text=f'Outside Diameter of Eye             {D}mm',font=('italian',17,'bold')).pack(fill='x')#,font=('italian',20,'bold'))
    ttk.Label(deb,text='Analysis of failure of fork end in tension and shear',font=('italian',17,'bold')).pack(fill='x')#,font=('italian',20,'bold'))
    ttk.Label(deb,text='Analysis of failure of fork end in tension',font=('italian',17,'bold')).pack(fill='x')#,font=('italian',20,'bold'))
    if st1<st:
        ttk.Label(deb,text=f"Since st = {st1}N/mm2  <  {st}N/mm2 \n\t\tHence Fork End is safe against Tensile Failure",font=('italian',14,'bold')).pack(fill='x')#,font=('italian',20,'bold'))
    else:
        ttk.Label(deb,text=f"Since st = {st1}N/mm2  >  {st}N/mm2 \nHence Fork End is not safe against Tensile Failure\nYou have to change parameters to design the Safe Knuckle Pin").pack(fill='x')#,font=(20,'bold'))
    ttk.Label(deb,text='\nNow analysis of Fork End in Shear',font=('italian',17,'bold')).pack(fill='x')#,font=('italian',20,'bold'))
    if tau1<tau:
        ttk.Label(deb,text=f"\nSince st = {tau1}N/mm2  <  {tau}N/mm2 \n\t\tHence Fork End is safe against Shear Failure",font=('italian',14,'bold')).pack(fill='x')#,font=('italian',20,'bold'))
    else:
        ttk.Label(deb,text=f"Since st = {tau1}N/mm2  >  {tau}N/mm2 \nHence Fork End is not safe against Shear Failure\nYou have to change parameters to design the Safe Knuckle Pin").pack(fill='x')#,font=(20,'bold'))
    ttk.Label(deb,text='Do you want this dimension in word file or pdf file. Then press the below button to get data',font=('italian',14,'bold')).pack(fill='x')#,font=('italian',20,'bold'))
    def get_btn(e=None):
        url = ''
        url = filedialog.asksaveasfile(mode = 'w',defaultextension='.pdf',filetypes = (('Text Files','*.txt'),('Word File','*.word'),('PDF File','*.pdf'),('CSv File','*.csv'),('All Files','*.*')))
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
               
        if url:
            url.write(f'Given Parameters \n\n Power Given\t:{P}N\nFactor of Safety Selected\t:{Fos}\n\n\nForces given\t-->\nShear Yield Strengrth:{Syt}N\nShear compression Strengrth:{Syc}N\nShear Stress:{Sys}N\nDimensions of your Design Pin\n\nDiameter of rod\t: {d}mm\nDiameter of Knuckle Pin\t: {Dp}mm\nThickness of single eye\t: {t}mm\nThickness of Fork\t: {T1}mm\nOutside Diameter of Eye\t: {D}mm')
            url.close()
        else:
            return
        
    

        
    get_btn = ttk.Button(deb,text='Get Dimension to the file',command=get_btn)
    get_btn.pack(pady = 20)


s_btn.config(command=submit)

win.mainloop()
