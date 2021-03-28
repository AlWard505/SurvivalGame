from savesystem import *
from load import load
import json
import os
from tkinter import *
from worldgeneration import *
from game import *
mapzoom=2

#Generates and gets the contents of th ~playerdata and ~worlddata json files
def GetNew(entry,filewin,fog):
    global filename
    global stuff
    global world
    fog = fog.get()
    filename = ""
    stuff ={}
    world = []
    filename3=""
    stuff3 ={}
    world3 = []
    filename3 = entry.get()
    
    filename = New(filename3,fog)
    stuff, world = load(filename,stuff3,world3)
    
    try:
        mapframe.destroy()
    except:
        pass
    GameSetUp(stuff,world)
    filewin.destroy()

#creates the page that lets you enter your new world name
def DoNew():
    try:
        filewin.destroy()
    except:
        pass
    
    filewin = Toplevel(main)
    enterframe = Frame(filewin)
    fog = IntVar()
    
    label = Label(enterframe, text="Enter world name:")
    label.pack( side = LEFT)
    
    entry = Entry(enterframe, bd =5)
    entry.focus_set()
    
    entry.pack(side = LEFT)
    button = Button(enterframe, text="OK",command = lambda:GetNew(entry,filewin,fog))
    
    button.pack(side = LEFT)
    
    enterframe.pack(anchor = NW)
    
    FogCheck = Checkbutton(filewin,text = "Fog of War",variable = fog, onvalue = 1, offvalue = 0)
    FogCheck.pack(anchor = SW)

#warns you if you have any unsaved data
def SaveWarNew():
    try:
        filename
    except:
        DoNew()
    else:
        try:
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
        except:
            DoNew()
            
#warns you if you have any unsaved data     
def SaveWarCon():
    try:
        filename
    except:
        DoContinue()
    else:
        try:
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
        except:
            DoContinue()

#will create a new file if there is unsaved data           
def DoNewNoSave(filewin):
    filewin.destroy()
    DoNew()

#will load an old file if there is unsaved data  
def DoConNoSave(filewin):
    filewin.destroy()
    DoContinue()

#creates the window that lets you choose what file to open
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

#loads the file that has been selected by the DoContinue() function
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
    try:
        mapframe.destroy()
    except:
        pass
    GameSetUp(stuff,world)
    filewin.destroy()

#changes a value for debug
def alter():
    print (stuff)
    stuff["inventory"]["pie"]=69
    print (stuff)

#saves data then quits the file
def SaveQuit():
    try:
        Save(filename,stuff,world)
    except:
        pass
    exitsavwar()

#warns you if you have any unsaved data when trying to quit
def exitsavwar():
    try:
        filename
    except:
        exit()
    else:
        try:
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
        except:
            exit()
            
# generates the map of the world and allows you to click a square and move to it
# contains the system that generates the fog of war
def Map(stuff,world):
    global mapzoom
    global mapframe
    mapframe = Frame(main,bd=2,bg="black")
    x=0
    y=0
    maprange = 1
    biome = world[stuff["currentlocation"]["y"]][stuff["currentlocation"]["x"]]
    if str(stuff["currentlocation"]["x"]) +","+ str(stuff["currentlocation"]["y"]) not in stuff["generatedbiomes"]:
        BiomeGeneration(biome,stuff)
    #fog of war
    while y-maprange-1!=maprange and stuff["fog"]==1:
        y+=1
        
        while x-maprange-1 != maprange:
            x+=1
            
            if str(stuff["currentlocation"]["x"]+x-maprange-1) +","+ str(stuff["currentlocation"]["y"]+y-maprange-1) not in stuff["discovered"]:
                stuff["discovered"]+= [str(stuff["currentlocation"]["x"]+x-maprange-1) +","+ str(stuff["currentlocation"]["y"]+y-maprange-1)]
        x=0
    stuff["discovered"]
    x=0
    y=0
    tempx=0
    tempy=0
    biome = 0
    movx = 0
    movy = 0
    
    #display
    while y-mapzoom-1 != mapzoom:
        y+=1
        colours=["#A1EC4B","#478301","#D8DD28","#1D4CC5","#B8B8B8","red"]
        
        while x-mapzoom-1 != mapzoom:
            x+=1
            
            if str(stuff["currentlocation"]["x"]+x-mapzoom-1) +","+ str(stuff["currentlocation"]["y"]+y-mapzoom-1) in stuff["discovered"] or stuff["fog"] == 0:
                button = Button(mapframe,bg = colours[world[stuff["currentlocation"]["y"]+y-mapzoom-1][stuff["currentlocation"]["x"]+x-mapzoom-1]-1],height=1, width = 2,command = lambda movx = stuff["currentlocation"]["x"]+x-mapzoom-1,movy =stuff["currentlocation"]["y"]+y-mapzoom-1: MapMove(movx,movy,biome))
                button.grid(column = y, row = x)
                
            else:
                button = Button(mapframe,bg = "grey",height=1, width = 2,command = lambda  movx = stuff["currentlocation"]["x"]+x-mapzoom-1,movy =stuff["currentlocation"]["y"]+y-mapzoom-1: MapMove(movx,movy,biome))
                button.grid(column = y, row = x)
    
        x = 0
    button = Button(mapframe,text = "+",height=1, width = 2,command= lambda:zoomin())
    button.grid(row = mapzoom*2+2,column = mapzoom+2)
    
    button = Button(mapframe,text = "-",height=1, width = 2,command= lambda:zoomout())
    button.grid(row = mapzoom*2+2,column = mapzoom)
    
    mainwin.add(mapframe)

#moves the button clicked to the center of the grid
def MapMove(movx,movy,biome):
    stuff["currentlocation"]["x"] = movx
    stuff["currentlocation"]["y"] = movy
    mapframe.destroy()
    Map(stuff,world)

#expands the radius of the grid by 1
def zoomin():
    global mapzoom
    if mapzoom != 10:
        mapzoom+=1
        
        mapframe.destroy()
        Map(stuff,world)

#decreases the raidus of the grid by one
def zoomout():
    global mapzoom
    if mapzoom != 2:
        mapzoom+=-1
        
        mapframe.destroy()
        Map(stuff,world)

def GameSetUp(stuff,world):
    optionsframe = Frame(gamewindow,bd=2,bg="black")
    BuildButton = Button(optionsframe,text = "Build")
    BuildButton.pack(side = LEFT)
    LogButton = Button(optionsframe,text = "Log")
    LogButton.pack(side = LEFT)
    MineButton = Button(optionsframe,text = "Mine")
    MineButton.pack(side = LEFT)
    gamewindow.add(optionsframe)
    
    Map(stuff,world)
    
#Window Setup        
main = Tk()

mainheight = main.winfo_screenheight()-200
mainwidth = main.winfo_screenwidth()-200
main.fullScreenState = True
mainwin = PanedWindow(height = mainheight, width = mainwidth)
mainwin.pack(fill=BOTH, expand=1,side = LEFT)

#Game Content

gamewindow = PanedWindow(mainwin, orient=VERTICAL,bg = "black", height = mainheight, width = mainwidth/2)
mainwin.add(gamewindow)


#creates the menu bar at the top of the window
menubar = Menu(main)

#file section of the menu bar, allows for a new game, continued game, save and quit
filemenu = Menu(menubar, tearoff=0)

filemenu.add_command(label="New", command=lambda:SaveWarNew())
filemenu.add_command(label="Continue", command=lambda:SaveWarCon())
filemenu.add_command(label="Save", command=lambda:Save(filename,stuff,world))
filemenu.add_command(label="Save&Quit", command=lambda:SaveQuit())
filemenu.add_command(label="Quit", command=lambda:exitsavwar())

menubar.add_cascade(label="File", menu=filemenu)

#debug section of the menu bar, allows for elements to be changed during testing
debugmenu = Menu(menubar, tearoff=0)

debugmenu.add_command(label="filename", command=lambda:print(filename))
debugmenu.add_command(label="stuff", command=lambda:print(stuff))
debugmenu.add_command(label="change", command=lambda:alter())
menubar.add_cascade(label="Debug", menu=debugmenu)

editmenu = Menu(menubar, tearoff=0)

main.config(menu=menubar)
main.mainloop()
