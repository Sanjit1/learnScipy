import numpy as numpy
import matplotlib.pyplot as plt
from scipy import linalg, optimize
from sympy import *
from Tkinter import *
from Tkinter.filedialog import askopenfilename


class regData():
    def __init_(self, information):
        



def new_file():




master = Tk()
mainMenu = Menu(master)
master.config(menu=menu)
file = Menu(mainMenu)
menu.add_cascade(label="File", menu=file)
file.add_command(label="New", command=new_file)
file.add_command(label='Open', command=open_file)
file.add_command(label='Exite', command=master.quit)