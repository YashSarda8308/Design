import tkinter as tk
from tkinter import ttk, filedialog, messagebox as mbox
import os, sys,shutil,pdb, datetime
## creaitng main window
main_win=tk.Tk()
main_win.title('Mechanical'.upper())
title = tk.Label(main_win,text='Mechanical Project'.upper(),bg="#074463",fg='white',font=('times new roman',40,'bold'),pady=10).pack(fill='x')
#title.pack(fill='x')
main_win_label = tk.Label(main_win,text=' Please Select topic on which you have to work '.center(60,'*'),bg='black',fg='lightblue',font=('times new roman',30,'bold'))
main_win_label.pack(pady=20)


## Vertical Scroll Bar


def design_button():
    design_ele = {shaft : 'Design of shaft',
        knuckle_pin: 'Design of Knuckle Pin',
        cotter : 'Design of Cotter joint',
        gears : 'Design of Gears',
        lever : 'Design of Lever Arm',
        bearing : 'Design of Bearing'}
    for i in design_ele:
        k = tk.Button(design_topic,text=i,font=('times new roman',15),bg='skyblue',fg='#034217').pack(fill='x',padx=350,pady=3)

def thermo_topic():
    main_win.clipboard_clear()
    #design_topic.pack_forget()
    thermo_ele = ['Laws of Thermodynamics','Heat Transfer','COP of System','RAC','Radiation']
    for i in thermo_ele:
        k = tk.Button(k = tk.Button(design_topic,text=i,font=('times new roman',15,'bold','italic'),bg='red',fg='blue').pack(fill='x',padx=350,pady=3))

##creating topic labelframe
topic=tk.LabelFrame(main_win,text='TOpics',bg='black').pack(side=tk.LEFT,padx=25,pady=25)
design = tk.Button(topic,text='Design Elements',font=('Arial black',20),command=design_button).place(x=25,y=200)
thermodynamics = tk.Button(topic,text='Thermodynamics',font=('Arial black',20),command=thermo_topic).place(x=25,y=300)
materials = tk.Button(topic,text='Materail available',font=('Arial black',20)).place(x=25,y=400)
design_topic=tk.LabelFrame(main_win,text='Design').pack(fill='both',pady=0)
##thermo_topic=ttk.LabelFrame(main_win,text='THERMODYNAMICS').pack(fill='both',padx=300,pady=10)
scroll_bar_v = tk.Scrollbar(design_topic)
###design_topic.focus_set()
##scroll_bar_v.pack(side=tk.RIGHT, fill=tk.Y)
##design_topic.pack(fill='both',padx=300,pady=10)
###scroll_bar_v.config(command=design_topic.YView








main_win.mainloop()
