import exerciseList;
import dataLocation;
import PySimpleGUI as sg;


def toVisual(fL): #builds heatmap
    buildRecord = []
    for record in fL:
        if record == "Y":
            buildRecord.append("🟩Y")
        elif record == "H":
            buildRecord.append("🟨H")
        else:
            buildRecord.append("🟥N")
    return buildRecord


def toVisual2(fL): #builds new heatmap
    #buildRecord = [sg.Image("images/red.png")]
    buildRecord = []
    for record in fL:
        if record == "Y":
            buildRecord.append(sg.Image("images/resources/green-50x50.png"))
        elif record == "H":
            buildRecord.append(sg.Image("images/resources/orange-50x50.png"))
        else:
            buildRecord.append(sg.Image("images/resources/red-50x50.png"))
    return buildRecord


def insert(letter): #allows for letters to be inserted into the completion record
    file = open(dataLocation.completionRecord(), "a")
    file.write(letter + ", ")
    file.close()
    return True


def get(version = 1): #fetches completion record of last 7 days
    file = open(dataLocation.completionRecord(), "r")
    fileContent = file.read()
    fileList = fileContent.split(", ")
    file.close()
    visualRecord = []
    if version == 1:
        if len(fileList) <= 8: #if more than 7 days are past, build only last 7 entries
            visualRecord = toVisual(fileList[0:-1])
        else:
            visualRecord = toVisual(fileList[-8:-1]) #if not, build all entries
        return(" ".join(visualRecord))
    elif version == 2:
        if len(fileList) <= 8: #if more than 7 days are past, build only last 7 entries
            visualRecord = toVisual2(fileList[0:-1])
        else:
            visualRecord = toVisual2(fileList[-8:-1]) #if not, build all entries
        return visualRecord

def fill(days): #fills in skipped days when the app was not opened
    file = open(dataLocation.completionRecord(), "r+")
    fileContent = file.read()
    fileList = fileContent.split(", ")[0:-1]
    if len(fileList) < days: #checks if number of records on completionRecord.txt is less than days past
        missedDays = days - len(fileList)
        if exerciseList.checkHalf():
            missedDays = missedDays - 1
            file.write("H, ")
        for _ in range(missedDays): #adds N for each day missed
            file.write("N, ")
        file.close()
        return True
    elif len(fileList) > days+1: #if days in completionRecord.txt more than days past, pass error
        file.close()
        return False
    else: #if they equal then nothing
        file.close()
        return True