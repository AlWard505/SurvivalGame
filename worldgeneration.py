#World Generation
import os
import random
import json
filename=""
namehelp=""
world = ""
def generation(filename):
    arr=[[]]
    x=0
    y=0
    n=0
    worldsize = 1024
    amunt = 0
    based = 0
    finche = 0
    while y != worldsize:
        while x!=worldsize:
            che = []
            try:
                che += [arr[y-1][x]]
            except:
                che += [0]
            try:
                che += [arr[y][x-1]]*2
            except:
                che += [0]*2
            try:
                che += [arr[y-1][x-1]]
            except:
                che += [0]
            try:
                che += [arr[y-1][x+1]]
            except:
                che += [0]
            check = [1,2,3,4,5]
            while n!= len(check):
                n+=1
                quan = che.count(n)
                check += [n]*quan**4
            while amunt != len(che):
                check += [che[amunt]]
                amunt +=1
            while based == 0:
                finche = random.randint(0,len(check)-1)
                based = check[finche]
            arr[y]+=[based]
            based = 0
            finche=0
            amunt = 0
            x+=1
        arr+=[[]]
        y+=1
        x=0
    with open("saves/"+filename+"/"+filename+"worlddata.json", 'w') as outfile:
        json.dump(arr, outfile)
def BiomeGeneration(biome,stuff):
    biomelist = ["planes","forest","desert","ocean","mountains"]
    loaddata = open("biomes/biomeStats.json", "r")
    biomeStats = json.load(loaddata)
    print (biomeStats)
    stuff["generatedbiomes"][str(stuff["currentlocation"]["x"]) +","+ str(stuff["currentlocation"]["y"])] = {}
    stuff["generatedbiomes"][str(stuff["currentlocation"]["x"]) +","+ str(stuff["currentlocation"]["y"])]["ores"] = {}
    for x in biomeStats[biomelist[biome-1]]["ores"]:

        stuff["generatedbiomes"][str(stuff["currentlocation"]["x"]) +","+ str(stuff["currentlocation"]["y"])]["ores"][x]= {}
        stuff["generatedbiomes"][str(stuff["currentlocation"]["x"]) +","+ str(stuff["currentlocation"]["y"])]["ores"][x]["quantity"] = random.randint(biomeStats[biomelist[biome-1]]["ores"][x]["quantity"][0],biomeStats[biomelist[biome-1]]["ores"][x]["quantity"][1])

