import exerciseList;
import dataLocation;
import daily;
import settings;
import calendar;
import datetime;
import PySimpleGUI as sg;


def getDayMonth(date, month, year): #calculates the days between a date and the date this app was first opened
    startDateList = date #gets the start date

    todayDate = datetime.date(int(year), int(month), 1) #converts to datetime
    startDate = datetime.date(int(startDateList[0]), int(startDateList[1]), int(startDateList[2])) #converts to datetime
    difDates = todayDate-startDate #subtracts days
    return(difDates.days) #returns difference


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


def toVisual2(fL, lastDiff): #builds new heatmap
    buildRecord = []
    if lastDiff and fL[-1] == "Y":
        fL.pop(-1)
        for record in fL:
            if record == "Y":
                buildRecord.append(sg.Image("images/resources/green-50x50.png"))
            elif record == "H":
                buildRecord.append(sg.Image("images/resources/orange-50x50.png"))
            else:
                buildRecord.append(sg.Image("images/resources/red-50x50.png"))
        buildRecord.append(sg.Image("images/resources/darkgreen-50x50.png"))
    else:
        for record in fL:
            if record == "Y":
                buildRecord.append(sg.Image("images/resources/green-50x50.png"))
            elif record == "H":
                buildRecord.append(sg.Image("images/resources/orange-50x50.png"))
            elif record == "N":
                buildRecord.append(sg.Image("images/resources/red-50x50.png"))
            elif record == "B":
                buildRecord.append(sg.Image("images/resources/outline-50x50.png"))
            else:
                if settings.readSettings()["theme"] == "light":
                    buildRecord.append(sg.Image("images/resources/white-50x50.png"))
                else:
                    buildRecord.append(sg.Image("images/resources/black-50x50.png"))
                
    return buildRecord


def insert(letter): #allows for letters to be inserted into the completion record
    file = open(dataLocation.completionRecord(), "a")
    file.write(letter + ", ")
    file.close()
    return True


def get(version = 1, days = 0): #fetches completion record of last 7 days
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
        if len(fileList) == days + 1:
            lastDiff = True
        else:
            lastDiff = False
        if len(fileList) <= 8: #if more than 7 days are past, build only last 7 entries
            visualRecord = toVisual2(fileList[0:-1], lastDiff)
        else:
            visualRecord = toVisual2(fileList[-8:-1], lastDiff) #if not, build all entries
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

    
def calendarView(month, year):
    file = open(dataLocation.completionRecord(), "r")
    fileContent = file.read()
    fileList = fileContent.split(", ")[0:-1]
    file.close()

    startDate = str(daily.getStartDate()).split("/")
    cal = calendar.TextCalendar(6)
    calMonth = str(cal.formatmonth(year, month)).split("\n")[2:-1]

    monthCompletionRecord = []
    weekNumber = 0
    if int(month) == int(startDate[1]) and int(year) == int(startDate[0]):
        recordIndex = 0
    elif int(month) > int(startDate[1]) and int(year) == int(startDate[0]):
        recordIndex = getDayMonth(startDate, month, year)
    for week in calMonth:
        weekRecord = []
        weekNumber += 1
        week = week.replace("  ", " ")
        week = week.strip()
        week = week.split(" ")
        if len(week) < 7:
            missing = 7 - len(week)
            if weekNumber == 1:
                for i in range(missing):
                    week.insert(0, "0")
            else:
                for i in range(missing):
                    week.append("0")
    
        for day in week:
            if day == "0":
                weekRecord.append("B")
            else:
                if int(month) == int(startDate[1]) and int(day) < int(startDate[2]):
                    weekRecord.append("M")
                else:
                    try:
                        weekRecord.append(fileList[recordIndex])
                        recordIndex += 1
                    except:
                        weekRecord.append("M")
        weekCompletionRecord = toVisual2(weekRecord, False)
        monthCompletionRecord.append(weekCompletionRecord)

    if len(monthCompletionRecord) < 6:
        monthCompletionRecord.append("")
    return monthCompletionRecord