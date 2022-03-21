import dataLocation;


def firstTime(date): #configures daily.txt first time opening
    file = open(dataLocation.daily(), "a")
    file.write(str(date) + " - 0 - 0 - " + str(date)) #today date, if reset, if complete, start date
    file.close()
    return True


def checkDailyFirst(date): #checks if first time opening that day and resets other params
    file = open(dataLocation.daily(), "r")
    contents = file.read()
    file.close()
    contentList = contents.split(" - ")
    if str(date) == contentList[0]: #checks if current date matches saved date of last opened
        return False
    else: #if it doesnt match:
        contentList[0] = str(date) #replaces date
        contentList[1] = "0" #sets daily reset to false
        contentList[2] = "0" #sets daily complete to false
        contents = " - ".join(contentList)
        file = open(dataLocation.daily(), "w")
        file.write(str(contents))
        file.close()
        return True


def checkDailyReset(): #checks if today's reps have been reset
    file = open(dataLocation.daily(), "r")
    contents = file.read()
    file.close()
    contentList = contents.split(" - ")
    if contentList[1] == "0":
        return False
    else:
        return True


def checkDailyComplete(): #checks if today's reps have been completed
    file = open(dataLocation.daily(), "r")
    contents = file.read()
    file.close()
    contentList = contents.split(" - ")
    if contentList[2] == "0":
        return False
    else:
        return True


def dailyMarkComplete(): #marks that today's exercises are done
    file = open(dataLocation.daily(), "r")
    contents = file.read()
    file.close()
    contentList = contents.split(" - ")
    contentList[2] = "1"
    contents = " - ".join(contentList)
    file = open(dataLocation.daily(), "w")
    file.write(str(contents))
    file.close()
    return True


def dailyMarkReset(): #marks that today's reps and sets have been reset
    file = open(dataLocation.daily(), "r")
    contents = file.read()
    file.close()
    contentList = contents.split(" - ")
    contentList[1] = "1"
    contents = " - ".join(contentList)
    file = open(dataLocation.daily(), "w")
    file.write(str(contents))
    file.close()
    return True