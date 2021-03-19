#saveandload
from worldgeneration import generation
from playerdata import data
import os
def SaveSystem(filename):
    check = 0
    x = 0
    badthings = '*."/\\[];:|,'
    namehelp = ""
    linecount = 1
    save = open("saves/savenames.txt","a")
    save.close
    menu = input(str("Welcome to the game\n1) New Game\n2) Continue Game\n"))
    while menu != "1" and menu != "2":
        menu = input(str("Please enter the number corrosponding to your choice\n1) New Game\n2) Continue Game\n"))
    #new game
    if menu == "1":
        save = open("saves/savenames.txt","r")
        for line in save:
            if line != "\n":
                linecount += 1
        save.close
        save = open("saves/savenames.txt","a")
        filename = input("please input the save name: ")
        for temp in badthings:
            filename = filename.translate({ord(temp): None})
            
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
        save.write(str(linecount) + ")" + filename+ "\n")
        save.close
        
        generation(filename)
        data(filename)
#continue
    else:
        print("these are your current saves")
        save = open("saves/savenames.txt","r")
        for line in save:
            print(str(line).translate({ord("\n"): None}))
            if line != "\n":
                linecount += 1
        linecount+=-1
        file = input("please enter which file you wish to open: ").translate({ord(" "): None})
        linecount+=1
        while file != int:
            try:
                file = int(file)
                while file >= linecount or file <= 0:
                    file = input("please enter one of the presented numbers: ").translate({ord(" "): None})
                    file = int(file)
                break
            except:
                file = input("please enter one of the presented numbers: ").translate({ord(" "): None})
            execute
        save.close
        save = open("saves/savenames.txt","r")
        while x != file:
            line = save.readline()
            x+=1
        while line[0]!=")":
            line= line.translate({ord(line[0]): None})
        filename = line.translate({ord(line[0]): None})
        filename = filename.translate({ord("\n"): None})
    return filename
