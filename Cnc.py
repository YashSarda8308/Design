import turtle
t = turtle.Turtle()
import sys
t.degrees()
t.pd()
while True:
    l = input().split()
    if not l:
        break    
    else:
        if len(l)==1:
            if 'p' in l[0].upper():
                t.pu()
            elif 'd' in l[0].upper():
                t.pd()
        elif len(l) == 3 : #'X' in l[0] and 'Y' in l[1] and 'R' in l[2]: ====> X100 Y100 Z5
            x = float(l[0][1:])
            y = float(l[1][1:])
            if 'Z' in l[2].upper():
                if float(l[2][1:])>0:
                    t.pu()
                else:   t.pd()
                t.goto(x,y)
            elif 'R' in l[2].upper():
                t.pu()
                r = float(l[2][1:])
                t.goto(x,y-r)
                t.pd()
                t.circle(r)

        else:
            x = float(l[0][1:])
            y = float(l[1][1:])
            t.goto(x,y)
        