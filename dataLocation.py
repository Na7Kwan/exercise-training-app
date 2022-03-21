import shutil;


def createLocation():
    try:
        file = open("dataLocation.txt", "r")
        file.close()
    except:
        file = open("dataLocation.txt", "a+")
        file.write("data")
        file.close()
    return True


def root():
    file = open("dataLocation.txt", "r")
    rootFolder = file.read()
    file.close()
    return str(rootFolder)


def setLocation(destination):
    file = open("dataLocation.txt", "r")
    source = str(file.read())
    file.close()
    shutil.move(source, destination)
    file = open("dataLocation.txt", "w")
    file.write(destination + "\\data")
    file.close()


def importLocation(folder):
    file = open("dataLocation.txt", "w")
    file.write(folder)
    file.close()


def completionRecord():
    file = open("dataLocation.txt", "r")
    rootFolder = file.read()
    file.close()
    location = str(rootFolder) + "\\completionRecord.txt"
    return location


def exerciseList():
    file = open("dataLocation.txt", "r")
    rootFolder = file.read()
    file.close()
    location = str(rootFolder) + "\\exerciseList.txt"
    return location


def settings():
    file = open("dataLocation.txt", "r")
    rootFolder = file.read()
    file.close()
    location = str(rootFolder) + "\\settings.txt"
    return location


def daily():
    file = open("dataLocation.txt", "r")
    rootFolder = file.read()
    file.close()
    location = str(rootFolder) + "\\daily.txt"
    return location


def records(exercise):
    file = open("dataLocation.txt", "r")
    rootFolder = file.read()
    file.close()
    location = str(rootFolder) + "\\records\\" + exercise + "_record.txt"
    return location