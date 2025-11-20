from tkinter import *

import tkinter.messagebox as mb

import tkinter.ttk as ttk

from gui_final_project_create_db import DB

path= "final_project_db.db"

db = Database(path)

#create a window object
root = tk()

root.title("Final Project GUI")
#set the geometry of the window
root.geometry("800x600+351+174")

#create a label widget for the title 
title_label = Label(root, text="Final Project GUI Application", font=("Helvetica", 16))

#declare the functions that will be called in the commands of the different buttons