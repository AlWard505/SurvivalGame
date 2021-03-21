from savesystem import *
from load import load
import json
import os
from tkinter import *
def GetNew(entry,filewin):
    global filename
    global stuff
    global world
    filename = ""
    stuff ={}
    world = []
    filename3=""
    stuff3 ={}
    world3 = []
    filename3 = entry.get()
    filename = New(filename3)
    stuff, world = load(filename,stuff3,world3)
    filewin.destroy()
def DoNew():
    filewin = Toplevel(main)
    label = Label(filewin, text="Enter world name:")
    label.pack( side = LEFT)
    entry = Entry(filewin, bd =5)
    entry.focus_set()
    entry.pack(side = LEFT)
    button = Button(filewin, text="OK",command = lambda:GetNew(entry,filewin))
    button.pack(side = LEFT)
def DoContinue():
    filewin = Toplevel(main)
    x=0
    saves = os.listdir("saves")
    List = Listbox(filewin,selectmode = SINGLE)
    scroll = Scrollbar(filewin)
    scroll.pack(side=RIGHT,fill = BOTH)
    while x != len(saves):
        List.insert(x,saves[x])
        List.pack()
        x+=1
    List.config(yscrollcommand = scroll.set)
    scroll.config(command = List.yview)
    button = Button(filewin, text = "load",command =lambda:GetContinue(List,filewin,saves))
    button.pack()
def GetContinue(List,filewin,saves):
    global filename
    global stuff
    global world
    filename = ""
    stuff ={}
    world = []
    stuff3 ={}
    world3 = []
    check = List.curselection()
    check = str(check)
    check = check.translate({ord(","): None})
    check = check.translate({ord("("): None})
    check = check.translate({ord(")"): None})
    filename = saves[int(check)]
    stuff, world = load(filename,stuff3,world3)
    filewin.destroy()
main = Tk()
menubar = Menu(main)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=lambda:DoNew())
filemenu.add_command(label="Continue", command=lambda:DoContinue())
filemenu.add_command(label="filename", command=lambda:print(filename))
filemenu.add_command(label="stuff", command=lambda:print(stuff))
menubar.add_cascade(label="File", menu=filemenu)
editmenu = Menu(menubar, tearoff=0)

main.config(menu=menubar)
main.mainloop()
