from savesystem import *
from load import load
import json
import os
from tkinter import *
from worldgeneration import *
from game import *


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
        mapwindow.destroy()
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
        mapwindow.destroy()
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
    global border,mapzoom,mapwindow,mapframe,maorange,zoomframe,OldWidth,ChunkInfo
    
    mapwindow = PanedWindow(main,orient=VERTICAL)
    mainwin.add(mapwindow) 
    mapwindow.update_idletasks()
    
    main.update_idletasks()
    if mapwindow.winfo_width() <= main.winfo_height()-30:
        mapframe = Frame(mapwindow,bg="black",height = mapwindow.winfo_width())
    else:
        mapframe = Frame(mapwindow,bg="black",height = main.winfo_height()-30,width =main.winfo_height()-30)

    Grid.rowconfigure(mapframe, 0, weight=1)
    Grid.columnconfigure(mapframe, 0, weight=1)
    x=0
    y=0
    
    
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
        Grid.rowconfigure(mapframe, y-1, weight=1)
        while x-mapzoom-1 != mapzoom:
            x+=1
            Grid.columnconfigure(mapframe, x-1, weight=1)

            check = False
            count = 0
            if str(stuff["currentlocation"]["x"]+x-mapzoom-1) +","+ str(stuff["currentlocation"]["y"]+y-mapzoom-1) in stuff["discovered"] or stuff["fog"] == 0:
                button = Button(mapframe,
                                bg = colours[world[stuff["currentlocation"]["y"]+y-mapzoom-1][stuff["currentlocation"]["x"]+x-mapzoom-1]-1],
                                command = lambda movx = stuff["currentlocation"]["x"]+x-mapzoom-1,
                                movy =stuff["currentlocation"]["y"]+y-mapzoom-1: MapMove(movx,movy,biome))
                
                button.grid(column = y-1, row = x-1,sticky=N+S+E+W)
            else:
                for amount in border:
                    
                    if str(stuff["currentlocation"]["x"]+x-mapzoom-1+int(border[count][0])) +","+ str(stuff["currentlocation"]["y"]+y-mapzoom-1+int(border[count][1])) in stuff["discovered"]:
                        button = Button(mapframe,
                                        bg = "#999999",command = lambda movx = stuff["currentlocation"]["x"]+x-mapzoom-1,
                                        movy =stuff["currentlocation"]["y"]+y-mapzoom-1: MapMove(movx,movy,biome))
                        button.grid(column = y-1, row = x-1,sticky=N+S+E+W)
                        check = True
                        pass
                    count +=1
                if check == False:
                    button = Button(mapframe,bg = "#737373")
                
                    button.grid(column = y-1, row = x-1,sticky=N+S+E+W)
            
        x = 0
        
    zoomframe = Frame(mapwindow,bg="black")
    button = Button(zoomframe,text = "+",height=1, width = 2,command= lambda:zoomin())
    button.grid(row = mapzoom*2+2,column = mapzoom+2)
    
    button = Button(zoomframe,text = "-",height=1, width = 2,command= lambda:zoomout())
    button.grid(row = mapzoom*2+2,column = mapzoom)
    
    if mapwindow.winfo_width() <= main.winfo_height()-30:
        mapwindow.add(mapframe)
    else:
        mapwindow.paneconfig(mapframe, width =main.winfo_height()-30)
        
    mapwindow.paneconfig(zoomframe,sticky = N)
    zoomframe.update_idletasks()
    mapframe.update_idletasks()
    OldWidth = mapwindow.winfo_width()
    ChunkInfo.set("x:"+str(stuff["currentlocation"]["y"])+"\ny:"+str(1024-stuff["currentlocation"]["x"]))
    
#moves the button clicked to the center of the grid
def MapMove(movx,movy,biome):
    global ChunkInfo
    stuff["currentlocation"]["x"] = movx
    stuff["currentlocation"]["y"] = movy
    mapwindow.destroy()
    Map(stuff,world)

    
#expands the radius of the grid by 1
def zoomin():
    global mapzoom
    if mapzoom != 8:
        mapzoom+=1
        
        mapwindow.destroy()
        Map(stuff,world)

#decreases the raidus of the grid by one
def zoomout():
    global mapzoom
    if mapzoom != 2:
        mapzoom+=-1
        
        mapwindow.destroy()
        Map(stuff,world)


def OnChange(self):
    global mapwindow
    global mapframe
    global OldWidth
    global GUI
    mapwindow.update_idletasks()
    mapframe.update_idletasks()
    main.update_idletasks()

    if mapwindow.winfo_width() != OldWidth:
        mapwindow.remove(mapframe)

        if mapwindow.winfo_width() <= main.winfo_height()-30:
            mapwindow.paneconfig(mapframe,before = zoomframe,height = mapwindow.winfo_width())

        else:
            mapwindow.paneconfig(mapframe, width =main.winfo_height()-30,before = zoomframe,height = mapwindow.winfo_height()-30)
            mapwindow.width = main.winfo_height()-30
        OldWidth = mapwindow.winfo_width()
        
#sets up the game window
def GameSetUp(stuff,world):
    global GUI
    global gamewindow
    GUI = Frame(gamewindow,bg="white")
    for children in gamewindow.panes():
        gamewindow.forget(children)
    #game options
    optionsframe = Frame(gamewindow,bg="black")
    BuildButton = Button(optionsframe,text = "Build",height = 1)
    BuildButton.pack(side = LEFT)
    LogButton = Button(optionsframe,text = "Log",height = 1)
    LogButton.pack(side = LEFT)
    MineButton = Button(optionsframe,text = "Mine",height = 1)
    MineButton.pack(side = LEFT)
    MineButton = Button(optionsframe,text = "Inventory",height = 1,command = Inventory)
    MineButton.pack(side = LEFT)
    
    gamewindow.paneconfig(optionsframe,sticky = S, height = 30)
    
    #info
    main.update_idletasks()
    gamewindow.paneconfig(GUI,sticky = N+E+W, before = optionsframe,height = main.winfo_height()-30)
    MainScreen()
    Map(stuff,world)

#opens inventory
def Inventory():
    inventory = Toplevel(main)
    label = Label(inventory)
    for x in stuff["inventory"]:
        label.text += str(stuff["inventory"][x])
    label.pack(side = LEFT)
    
def MainScreen():
    global GUI, ChunkInfo
    ChunkInfo = StringVar()

    info = Label(GUI, textvariable = ChunkInfo)
    info.pack(anchor = NW)

def upmaprange():

    global maprange

    maprange += 1

            
def lowermaprange():
    global border
    global maprange

    maprange += -1

    
#Window Setup        
main = Tk()
global mainheight, mainwidth 
mainheight = main.winfo_screenheight()-200
mainwidth = main.winfo_screenwidth()-200
main.fullScreenState = True
mainwin = PanedWindow(height = mainheight, width = mainwidth)
mainwin.pack(fill=BOTH, expand=1,side = LEFT)



#varibles
mapzoom=2
maprange = 1
border=[]
for z in range(2*1+1):
    for c in range(2*1+1):
        border+=[[z-1,c-1]]
#Game Content
global gamewindow
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
debugmenu.add_command(label="increase maprange", command=upmaprange)
debugmenu.add_command(label="decrease maprange", command=lowermaprange)
menubar.add_cascade(label="Debug", menu=debugmenu)

editmenu = Menu(menubar, tearoff=0)

main.config(menu=menubar)

main.bind('<ButtonRelease>',OnChange)

main.mainloop()
