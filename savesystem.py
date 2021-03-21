#saveandload
from worldgeneration import generation
from playerdata import data
import os
from json import *
from tkinter import *
def New(filename):
    check = 0
    x = 0
    badthings = '*."/\\[];:|,'
    namehelp = ""
    linecount = 1



    for temp in badthings:
        filename = filename.translate({ord(temp): None})
    if filename == "":
        filename = "New World"
    while check != 1:
        if os.path.exists("saves/"+filename+str(namehelp)):
            if namehelp == "":
                namehelp = 1
            else:
                namehelp += 1
        else:
            os.makedirs("saves/"+filename+str(namehelp))
            check = 1
            filename = filename+str(namehelp)

    
    generation(filename)
    data(filename)
    return filename
#continue
def Save(filename,stuff,world):
    with open("saves/"+filename+"/"+filename+"data.json", 'w') as outfile:
        dump(stuff, outfile)
    with open("saves/"+filename+"/"+filename+"worlddata.json", 'w') as outfile:
        dump(world, outfile)
    
