import cx_Freeze, sys, os
base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

os.environ['TCL_LIBRARY'] = r'C:\Python\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Python\tcl\tk8.6'

excecutables = [cx_Freeze.Executable('tkinter_design_of_Knuckle_Pin.py',base=base)]

cx_Freeze.setup(
    name = 'Design of Knuckle Pin',
    options = {'build_exe':{'packages':['tkinter','os'],'include_files':['tcl86t.dll','tk86t.dll']}},
    version = '0.0.1',
    description = '* Design Software *',
    executables = excecutables)
