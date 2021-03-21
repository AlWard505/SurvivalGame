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
    try:
        filewin.destroy()
    except:
        pass
    filewin = Toplevel(main)
    label = Label(filewin, text="Enter world name:")
    label.pack( side = LEFT)
    entry = Entry(filewin, bd =5)
    entry.focus_set()
    entry.pack(side = LEFT)
    button = Button(filewin, text="OK",command = lambda:GetNew(entry,filewin))
    button.pack(side = LEFT)
def SaveWarNew():
    try:
        filename
    except:
        DoNew()
    else:
        stufftemp = {}
        worldtemp = []
        stufftemp, worldtemp = load(filename,stufftemp,worldtemp)
        if stufftemp != stuff or worldtemp!= world:
            filewin = Toplevel(main)
            label = Label(filewin, text="You have unsaved data, are you sure you want to continue?")
            label.grid(row = 0,columnspan = 30,column = 0)
            dont = Button(filewin, text = "yes", command = lambda:DoNewNoSave(filewin))
            dont.grid(column = 14,row = 1)
            yeah = Button(filewin, text = "no", command = lambda:filewin.destroy())
            yeah.grid(column = 15,row = 1)
        else:
            DoNew()
def SaveWarCon():
    try:
        filename
    except:
        DoContinue()
    else:
        stufftemp = {}
        worldtemp = []
        stufftemp, worldtemp = load(filename,stufftemp,worldtemp)
        if stufftemp != stuff or worldtemp!= world:
            filewin = Toplevel(main)
            label = Label(filewin, text="You have unsaved data, are you sure you want to continue?")
            label.grid(row = 0,columnspan = 30,column = 0)
            dont = Button(filewin, text = "yes", command = lambda:DoConNoSave(filewin))
            dont.grid(column = 14,row = 1)
            yeah = Button(filewin, text = "no", command = lambda:filewin.destroy())
            yeah.grid(column = 15,row = 1)
        else:
            DoContinue()
def DoNewNoSave(filewin):
    filewin.destroy()
    DoNew()
def DoConNoSave(filewin):
    filewin.destroy()
    DoContinue()
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
def alter():
    print (stuff)
    stuff["inventory"]["pie"]=69
    print (stuff)
def SaveQuit():
    try:
        Save(filename,stuff,world)
    except:
        pass
    exitsavwar()
def exitsavwar():
    try:
        filename
    except:
        exit()
    else:
        stufftemp = {}
        worldtemp = []
        stufftemp, worldtemp = load(filename,stufftemp,worldtemp)
        if stufftemp != stuff or worldtemp!= world:
            filewin = Toplevel(main)
            label = Label(filewin, text="You have unsaved data, are you sure you want to continue?")
            label.grid(row = 0,columnspan = 30,column = 0)
            dont = Button(filewin, text = "yes", command = lambda:exit())
            dont.grid(column = 14,row = 1)
            yeah = Button(filewin, text = "no", command = lambda:filewin.destroy())
            yeah.grid(column = 15,row = 1)
        else:
            exit()
main = Tk()
menubar = Menu(main)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=lambda:SaveWarNew())
filemenu.add_command(label="Continue", command=lambda:SaveWarCon())
filemenu.add_command(label="Save", command=lambda:Save(filename,stuff,world))
filemenu.add_command(label="Save&Quit", command=lambda:SaveQuit())
filemenu.add_command(label="Quit", command=lambda:exitsavwar())
filemenu.add_command(label="filename", command=lambda:print(filename))
filemenu.add_command(label="stuff", command=lambda:print(stuff))
filemenu.add_command(label="change", command=lambda:alter())
menubar.add_cascade(label="File", menu=filemenu)
editmenu = Menu(menubar, tearoff=0)

main.config(menu=menubar)
main.mainloop()
