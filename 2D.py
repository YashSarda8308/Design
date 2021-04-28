from tkinter import ttk
from tkinter.constants import CENTER, LEFT, RIGHT
import turtle,tkinter
t = turtle.Turtle()
t.fd(50)
t.onclick(20,5)

win = tkinter.Tk("WELCOME")
win.title("DESIGN SOFTWARE")
draw = ttk.LabelFrame(win,border=0,height=500)
draw.pack(side=LEFT)

npad = tkinter.Canvas(win).pack(fill='x')
'''CIRCLE BUTTON'''
circle_button = ttk.Button(draw,text="Circle").grid(row=0,column=0)
rectangle_button = ttk.Button(draw,text="Rectangle").grid(row=1,column=0)
square_button = ttk.Button(draw,text="Sqaure").grid(row=2,column=0)


    


win.mainloop()