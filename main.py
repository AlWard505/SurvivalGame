from savesystem import SaveSystem
from load import load
import json
filename = ""
filename = SaveSystem(filename)
stuff ={}
world = []
stuff,world = load(filename,stuff,world)
print(world[stuff["currentlocation"]["x"]][stuff["currentlocation"]["y"]])
input()
