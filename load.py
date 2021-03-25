import json

def load(filename, stuff, world):

    loaddata = open("saves/" + filename + "/"+ filename + "data.json", "r")
    stuff = json.load(loaddata)
    
    loaddata = open("saves/" + filename + "/" + filename + "worlddata.json", "r")
    world = json.load(loaddata)

    return stuff, world
