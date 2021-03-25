from random import randint
import json

player = ""

def data(filename,fog):

    x = randint(484,540)
    y = randint(484,540)
    stuff = {
        "inventory":{
            },
        "spawnlocation": {
            "x": x,
            "y": y
            },
        "currentlocation":{
            "x": x,
            "y": y
            },
        "setspawn":{
            "x": x,
            "y": y
            },
        "discovered":[],
        "generatedbiomes":{
            }
        }
    if fog == 1:
        stuff["fog"] = 1
    else:
        stuff["fog"] = 0
    with open("saves/"+filename+"/"+filename+"data.json", 'w') as outfile:
        json.dump(stuff, outfile)


    
