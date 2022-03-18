import exerciseList;


def toVisual(fL): #builds heatmap
    buildRecord = []
    for record in fL:
        if record == "Y":
            buildRecord.append("🟩")
        elif record == "H":
            buildRecord.append("🟨")
        else:
            buildRecord.append("🟥")
    return buildRecord


def insert(letter): #allows for letters to be inserted into the completion record
    file = open("completionRecord.txt", "a")
    file.write(letter + ", ")
    file.close()
    return True


def get(): #fetches completion record of last 7 days
    file = open("completionRecord.txt", "r")
    fileContent = file.read()
    fileList = fileContent.split(", ")
    file.close()
    visualRecord = []
    if len(fileList) <= 8: #if more than 7 days are past, build only last 7 entries
        visualRecord = toVisual(fileList[0:-1])
    else:
        visualRecord = toVisual(fileList[-8:-1]) #if not, build all entries

    return(" ".join(visualRecord))


def fill(days): #fills in skipped days when the app was not opened
    file = open("completionRecord.txt", "r+")
    fileContent = file.read()
    fileList = fileContent.split(", ")[0:-1]
    if len(fileList) < days: #checks if number of records on completionRecord.txt is less than days past
        missedDays = days - len(fileList)
        if exerciseList.checkHalf():
            missedDays = missedDays - 1
            file.write("H, ")
        print("You skipped " + str(missedDays) + " day(s)")
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