import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox as mbox
import os, sys,shutil,pdb

dm = tk.Tk()
dm.geometry('1280x1080')
dm.title('Design software')
title = tk.Label(dm,text='Design Software Automated',bg="#074463",fg='white',font=('times new roman',40,'bold'),pady=10).pack(fill='x')


dmlf = tk.LabelFrame(dm,text = 'Select the design material',font=('times new roman',25,'bold'),bg='black',fg='white')

## scroll bar
scroll_bar = tk.Scrollbar(dmlf)
scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
dmlf.pack(fill=tk.BOTH,expand=True)
##scroll_bar.config(command=dmlf.yview)

## buttons
shaft = tk.Button(dmlf,text='Design a shaft',font=('times new roman',20,'bold'),bg='blue',fg='white',pady=50)#.grid(row=1,column=1,padx=20,pady=20)
knuckle_pin = tk.Button(dmlf,text='Design a knuckle pin',font=('times new roman',20,'bold'),bg='white',fg='blue',pady=50)
cotter = tk.Button(dmlf,text='Design a Cotter pin',font=('times new roman',20,'bold'),bg='red',fg='yellow',pady=50)


''' defining function'''

def knucklepin():
    try:
        import tkinter_design_of_Knuckle_Pin.py 
    except ModuleNotFoundError:
        mbox.showerror('file not exist','your design file for shaft does not exist')
def dshaft():
    try:
        import shaft.py
    except ModuleNotFoundError:
        mbox.showerror('file not exist','your design file for shaft does not exist')
def dcotterpin():
    try:
        import tkinter_design_of_cotter_pin.py
    except ModuleNotFoundError:
        mbox.showerror('file not exist','your design file for cotter pin does not exist')


shaft.pack(fill='x')
knuckle_pin.pack(fill='x')
cotter.pack(fill='x')

knuckle_pin.config(command = knucklepin)
shaft.config(command=dshaft)
cotter.config(command=dcotterpin)

dm.mainloop()
