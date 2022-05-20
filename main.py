import datetime;
import completionRecord;
import exerciseList;
import addExercise;
import submitExercises;
import daily;
import os;
import settings;
import dataLocation;
import PySimpleGUI as sg;


def getDay(date): #calculates the days between current date and the date this app was first opened
    todayDateTime = str(datetime.datetime.now().astimezone()) #gets current date
    todayDateStr = todayDateTime.split()[0]
    todayDateList = todayDateStr.split("-") #formats the date
    startDateList = date.split("/") #gets the start date

    todayDate = datetime.date(int(todayDateList[0]), int(todayDateList[1]), int(todayDateList[2])) #converts to datetime
    startDate = datetime.date(int(startDateList[0]), int(startDateList[1]), int(startDateList[2])) #converts to datetime
    difDates = todayDate-startDate #subtracts days
    return(difDates.days) #returns difference
    

def getDate(): #gets the current date in string format
    todayDateTime = str(datetime.datetime.now().astimezone()) #gets current date
    todayDateStr = todayDateTime.split()[0]
    todayDateList = todayDateStr.split("-") #formats the date
    todayDate = todayDateList[0] + "/" + todayDateList[1] + "/" + todayDateList[2] #formats the date for humans
    return(todayDate)

dataLocation.createLocation()

if not os.path.exists(dataLocation.root()):
    os.makedirs(dataLocation.root())

if not os.path.exists(dataLocation.root() + "\\records"):
    os.makedirs(dataLocation.root() + "\\records")

try:
    file = open(dataLocation.completionRecord(), "r")
    file.close()
    file = open(dataLocation.exerciseList(), "r")
    file.close()
    file = open(dataLocation.settings(), "r")
    file.close()
except:
    file = open(dataLocation.completionRecord(), "a+")
    file.close()
    file = open(dataLocation.exerciseList(), "a+")
    file.close()
    file = open(dataLocation.settings(), "a+")
    file.close()
    settings.setupSettings()

try:
    file = open(dataLocation.daily(), "r")
    infoString = file.read()
    dateStart = infoString.split(" - ")[3]
    file.close()
except:
    dateStart = getDate()

daysSince = getDay(dateStart)
date = str(getDate())
month = int(date.split("/")[1])
year = int(date.split("/")[0])

if completionRecord.fill(daysSince) == False: #checks if completion record matches days past
    sg.Print("RecordError: Record mismatch")
    quit() #exits app

testRecords = exerciseList.testRecords(date) #checks if each exercise has its file
if not testRecords:
    sg.Print("RecordError: One or more exercise records were missing, data lost")

if daysSince + 1 > 1:
    welcome = "Welcome Back"
    daily.checkDailyFirst(date)
else:
    welcome = "Welcome"
    daily.firstTime(date)

testOptions = True
while testOptions:
    option = settings.readSettings()
    try:
        themeOption = option["theme"]
        halfSetsOption = option["halfSets"]
        difficultyOption = option["difficulty"]
        autoAdjustOption = option["autoAdjust"]
        cheatDayOption = option["cheatDay"]
        activeOption = option["active"]
        testOptions = False
    except:
        settings.checkSettings()

if themeOption == "light":
    sg.theme("default1")
else:
    sg.theme("darkgrey11")
heading1 = ("Open Sans", 24)
heading2 = ("Open Sans", 18)
default = ("Open Sans", 12)
visual = ("Open Sans", 26)


def main():
    exerciseList.resetCheck() #checks if exerciseList has been reset
    exerciseList.checkComplete() #checks if all activities are complete
    
    buttonSubmit = sg.Button("Submit Today's Sets", font=default, size=(46,2))
    buttonAdd = sg.Button("Add Exercise", font=default, size=(22,2))
    buttonMore = sg.Button("More Exercise Details", font=default, size=(22,2))
    buttonEdit = sg.Button("Edit Exercises", font=default, size=(22,2))
    buttonDelete = sg.Button("Delete Exercise", font=default, size=(22,2))
    buttonCalendar = sg.Button("View Calendar", font=default, size=(22,2))
    buttonLocation = sg.Button("Data Storage Location", font=default, size=(22,2))
    buttonOptions = sg.Button("Options", font=default, size=(22,2))
    buttonQuit = sg.Button("Quit", font=default, size=(22,2))

    layout = [
             [sg.Text(welcome, font=heading1)],
             [sg.Text("Today is Day " + str(daysSince + 1) + " of using this app", font=heading2)],
             [sg.Text("Your activity this past week:", font=heading2)],
             [completionRecord.get(2, (daysSince + 1))], #gets visual of exercise in past 7 days
             [sg.Text("Today's exercises:", font=heading2)],
             [sg.Text(exerciseList.getList(), font=default)], #gets list of exercises and remaining reps and sets for the day
             [buttonSubmit],
             [buttonAdd, buttonMore],
             [buttonEdit, buttonDelete],
             [buttonCalendar, buttonLocation],
             [buttonOptions, buttonQuit]
             ]

    return sg.Window("Exercise Training App", layout, size=(450,800), resizable=True, finalize=True)


def submit():
    list = exerciseList.keyList().split("\n")[0:-1] #creates list of all exercises
    list.reverse()
    layout = [
             [sg.Text("Submit Today's Sets:", font=heading1)],
             [sg.Submit(font=default, key="submitSets"), sg.Button("Mark All As Complete", font=default, key="markAll")],
             [sg.Text("")],
             [sg.Combo(list, font=default, size=(20,1), key="-KEY-")],
             [sg.Button("Submit Half Sets", font=default, key="submitHalf")],
             [sg.Text("")],
             [sg.Button("Cheat Day", font=default, key="cheatSubmit")],
             [sg.Text("")],
             [sg.Button("Close", font=default, key="close")]
             ]
    for exercise in list:
        if exercise.lower() in activeOption:
            if len(exercise) > 20:
                exercise = exercise[0:17] + "..."
            row = [sg.Text(exercise, font=default, size=(40,1)), sg.InputText("0", font=default, size=(4,1), key=exercise)]
            layout.insert(1, row)
    
    return sg.Window("Submit Today's Sets", layout, size=(450,800), resizable=True, finalize=True)


def add():
    layout = [
             [sg.Text("Add Exercise:", font=heading1)],
             [sg.Text("Type the name of the exercise you wish to add:", font=default)],
             [sg.InputText(font=default, size=(21,1), key="-NAME-")],
             [sg.Text("Type the muscle group this exercise targets:", font=default)],
             [sg.InputText(font=default, size=(21,1), key="-MUSCLE-")],
             [sg.Text("Perform the exercise and attempt the maximum in\none go without overexertion", font=default)],
             [sg.Text("Type the number of reps you were able to achieve (as\nwhole number):", font=default)],
             [sg.InputText(font=default, size=(4,1), key="-REPS-")],
             [sg.Text("Type the number of sets you wish to do each day (as\nwhole number):", font=default)],
             [sg.InputText(font=default, size=(4,1), key="-SETS-")],
             [sg.Submit(font=default, key="addSubmit"), sg.Button("Close", font=default, key="close")]
             ]
    
    return sg.Window("Add Exercise", layout, size=(450,800), resizable=True, finalize=True)


def more():
    list = exerciseList.keyList().split("\n")[0:-1] #creates list of all exercises
    layout = [
             [sg.Text("Exercises:", font=heading1)],
             [sg.Text("Choose the name of the exercise you wish to view\nmore details on", font=default)],
             [sg.Combo(list, font=default, size=(20,1), enable_events=True, key="-KEY-")], 
             [sg.Submit(font=default, key="chooseExerciseDetail")],
             [sg.Text("", font=default, key="-LINE1-")],
             [sg.Text("", font=default, key="-LINE2-")],
             [sg.Text("", font=default, key="-LINE3-")],
             [sg.Text("", font=default, key="-LINE4-")],
             [sg.Text("", font=default, key="-LINE5-")],
             [sg.Button("Close", font=default, key="close")]
             ]
    
    return sg.Window("More Exercise Details", layout, size=(450,800), resizable=True, finalize=True)


def edit():
    list = exerciseList.keyList().split("\n")[0:-1] #creates list of all exercises
    layout = [
             [sg.Text("Edit Menu:", font=heading1)],
             [sg.Text("For advanced users only", font=default)],
             [sg.Text("Choose the name of the exercise you wish to edit", font=default)],
             [sg.Combo(list, font=default, size=(20,1), key="-KEY-")],
             [sg.Text("Type the value you wish to edit", font=default)],
             [sg.InputText(font=default, size=(21,1), key="-VALUE-")],
             [sg.Text("Type the edit you wish to make", font=default)],
             [sg.InputText(font=default, size=(21,1), key="-EDIT-")],
             [sg.Submit(font=default, key="editSubmit"), sg.Button("Close", font=default, key="close")]
             ]
    
    return sg.Window("Edit Exercise", layout, size=(450,800), resizable=True, finalize=True)


def delete():
    list = exerciseList.keyList().split("\n")[0:-1] #creates list of all exercises
    layout = [
             [sg.Text("Delete Menu:", font=heading1)],
             [sg.Text("Choose the name of the exercise you wish to delete", font=default)],
             [sg.Combo(list, font=default, size=(20,1), key="-KEY-")],
             [sg.Text("Type out the name of the exercise letter for letter\nto confirm", font=default)],
             [sg.InputText(font=default, size=(21,1), key="-CONFIRMATION-")],
             [sg.Submit(font=default, key="deleteSubmit"), sg.Button("Close", font=default, key="close")]
             ]
    
    return sg.Window("Delete Exercise", layout, size=(450,800), resizable=True, finalize=True)


def calendar(viewMonth = month, viewYear = year):
    weeks = completionRecord.calendarView(viewMonth, viewYear)
    monthName = completionRecord.getMonthName(viewMonth)
    layout = [
             [sg.Text("Calendar View", font=heading1)],
             [sg.InputText(viewMonth, visible=False, font=default, key="-MONTH-")],
             [sg.Text("                             " + monthName, font=heading2)],
             [sg.Text("  Su      M      Tu      W      Th      F       Sa    ", font=heading2)],
             [sg.Frame("", [weeks[0]], border_width=0, key="-WEEK1-")],
             [sg.Frame("", [weeks[1]], border_width=0, key="-WEEK2-")],
             [sg.Frame("", [weeks[2]], border_width=0, key="-WEEK3-")],
             [sg.Frame("", [weeks[3]], border_width=0, key="-WEEK4-")],
             [sg.Frame("", [weeks[4]], border_width=0, key="-WEEK5-")],
             [sg.Frame("", [weeks[5]], border_width=0, key="-WEEK6-")],
             [sg.Button("Previous Month", font=default, key="previous"), sg.Button("Next Month", font=default, key="next")],
             [sg.Button("Close", font=default, key="close")],
             ]
    
    return sg.Window("View Calendar", layout, size=(450,800), resizable=True, finalize=True)


def location():
    rootFolder = dataLocation.root()

    layout = [
             [sg.Text("Data Storage Location:", font=heading1)],
             [sg.InputText(rootFolder, size=(20,1), font=default, key="-FOLDER-"), sg.FolderBrowse(font=default)], 
             [sg.Submit("Save Location", font=default, key="locationSubmit"), sg.Submit("Import from Location", font=default, key="importSubmit")], 
             [sg.Button("Close", font=default, key="close")]
             ]

    return sg.Window("Data Storage Location", layout, size=(450,800), resizable=True, finalize=True)


def options():
    list = exerciseList.keyList().split("\n")[0:-1] #creates list of all exercises
    autoOption = []
    for entry in autoAdjustOption:
        try:
            nameSplit = entry.split(" ")
            nameList = []
            for word in nameSplit:
                nameList.append(word.capitalize())
                name = " ".join(nameList)
        except:
            name = entry.capitalize()
        autoOption.append(name)
    
    actOption = []
    for entry in activeOption:
        try:
            nameSplit = entry.split(" ")
            nameList = []
            for word in nameSplit:
                nameList.append(word.capitalize())
                name = " ".join(nameList)
        except:
            name = entry.capitalize()
        actOption.append(name)

    layout = [
             [sg.Text("Options:", font=heading1)],
             [sg.Text("Theme", font=default)],
             [sg.Combo(["Dark", "Light"], default_value=themeOption.capitalize(), font=default, size=(20,1), key="-THEME-")],
             [sg.Text("Half Sets", font=default)],
             [sg.Combo(["On", "Off"], default_value=halfSetsOption.capitalize(), font=default, size=(20,1), key="-HALFSETS-")],
             [sg.Text("Difficulty", font=default)],
             [sg.Combo(["Hard", "Normal", "Easy"], default_value=difficultyOption.capitalize(), font=default, size=(20,1), key="-DIFFICULTY-")],
             [sg.Text("Auto Adjust Exercises", font=default)],
             [sg.Listbox(list, default_values=autoOption, select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, font=default, size=(20,3), key="-EXERCISES-")],
             [sg.Text("Cheat Day", font=default)],
             [sg.Combo(["On", "Off"], default_value=cheatDayOption.capitalize(), font=default, size=(20,1), key="-CHEATDAY-")],
             [sg.Text("Enable Exercises", font=default)],
             [sg.Listbox(list, default_values=actOption, select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, font=default, size=(20,3), key="-ACTIVE-")],
             [sg.Submit("Apply Changes", font=default, key="optionsSubmit"), sg.Button("Close", font=default, key="close")]
             ]
    
    return sg.Window("Options", layout, size=(450,800), resizable=True, finalize=True)


window1, window2 = main(), None

while True:
    window, event, values = sg.read_all_windows()
    if event == "Submit Today's Sets":
        window2 = submit()
        window2.TKroot.focus_set()
        window.close()
        window1 = None
    if event == "markAll": #done
        submitExercises.markAll(date)
        event = "close"
    if event == "submitSets": #done
        allInts = True
        values.pop("-KEY-")
        for exercise in values:
            try:
                int(values[exercise])
            except:
                allInts = False
        if allInts:
            for exercise in values:
                completeSets = int(values[exercise])
                if completeSets != 0:
                    exerciseDetails = exerciseList.getList(exercise.lower())
                    currentReps = int(exerciseDetails[0])
                    currentSets = int(exerciseDetails[1])
                    if completeSets > currentSets:
                        completeSets = currentSets
                    currentSets = currentSets - completeSets
                    submitExercises.markOne(exercise.lower(), currentSets, date)
            event = "close"
    if event == "submitHalf": #done
        if halfSetsOption == "on" and values["-KEY-"] != "":
            exerciseDetails = exerciseList.getList(values["-KEY-"].lower()) #retrieves current remaining reps and sets
            currentReps = int(exerciseDetails[0])
            currentSets = int(exerciseDetails[1])
            if settings.readSettings()["difficulty"] == "hard":
                scale = 0.7
            elif settings.readSettings()["difficulty"] == "easy":
                scale = 0.95
            else:
                scale = 0.85
            message = "Type the number of reps done per half completed\nsets (separated by \"-\"):"
            halfSets = sg.popup_get_text(message, title="Submit Half Sets", font=default, keep_on_top=True)
            try:
                sumReps = int(halfSets)
            except:
                try:
                    repList = halfSets.split("-")
                    sumReps = 0
                    count = 0
                    for item in repList:
                        sumReps += int(repList[count])
                        count += 1
                except:
                    pass
            calculatedSets = sumReps // currentReps #calculates how many sets would have been done
            calculatedSets = calculatedSets * scale #multiplier due to time spread
            calculatedSets = round(calculatedSets)
            currentSets = currentSets - calculatedSets
            submitExercises.markOne(values["-KEY-"].lower(), currentSets, date)
    if event == "cheatSubmit": #done
        if cheatDayOption == "on":
            submitExercises.cheatDay(date)
        event = "close"

    if event == "Add Exercise": #done
        window2 = add()
        window2.TKroot.focus_set()
        window.close()
        window1 = None
    if event == "addSubmit": #done
        list = exerciseList.keyList().split("\n")[0:-1]
        exist = False
        for exercise in list: #checks if exercise being added already exists
            if exercise.lower() == values["-NAME-"].lower():
                exist = True
        if not exist:
            try:
                int(values["-REPS-"])
                int(values["-SETS-"])
                addExercise.add(values["-NAME-"].lower(), values["-MUSCLE-"].lower(), values["-REPS-"], values["-SETS-"], date)
                event = "close"
            except:
                pass

    if event == "More Exercise Details": #done
        window2 = more()
        window2.TKroot.focus_set()
        window.close()
        window1 = None
    if event == "chooseExerciseDetail": #done
        selected = values["-KEY-"].lower()
        list = exerciseList.keyList().split("\n")[0:-1] #creates list of all exercises
        exists = False
        for exercise in list: #tests if exercise exists
            if exercise.lower() == selected:
                exists = True
        if exists:
            exerciseDetails = exerciseList.getList(selected)
            line1 = "You have " + str(exerciseDetails[1]) + " set(s) of " + str(exerciseDetails[0]) + " rep(s) left."
            line2 = "This exercise targets your " + str(exerciseDetails[2]) + "."
            original = exerciseDetails[3].split("*")
            current = exerciseDetails[4].split("*")
            line3 = "Your original daily goal was " + str(original[1]) + " set(s) of " + str(original[0]) + " rep(s)."
            line4 = "Your current daily goal is " + str(current[1]) + " set(s) of " + str(current[0]) + " rep(s)."
            autoList = settings.readSettings()["autoAdjust"]
            print(autoList)
            print(selected)
            if selected in autoList:
                auto = " "
            else:
                auto = " not "
            line5 = "This exercise will" + auto + "adjust automatically based\non your progress."
            window["-LINE1-"].update(line1)
            window["-LINE2-"].update(line2)
            window["-LINE3-"].update(line3)
            window["-LINE4-"].update(line4)
            window["-LINE5-"].update(line5)
    
    if event == "Edit Exercises": #done
        window2 = edit()
        window2.TKroot.focus_set()
        window.close()
        window1 = None
    if event == "editSubmit": #done
        if values["-KEY-"] != "" and values["-VALUE-"] != "" and values["-EDIT-"] != "":
            exerciseList.editItem(values["-KEY-"].lower(), values["-VALUE-"], values["-EDIT-"])
            event = "close"
    
    if event == "Delete Exercise": #done
        window2 = delete()
        window2.TKroot.focus_set()
        window.close()
        window1 = None
    if event == "deleteSubmit": #done
        key = values["-KEY-"].lower()
        confirm = values["-CONFIRMATION-"].lower()
        if key == confirm:
            addExercise.deleteExercise(key)
            event = "close"
    
    if event == "View Calendar": #WIP
        window2 = calendar()
        window2.TKroot.focus_set()
        window.close()
        window1 = None
    if event == "previous": #WIP
        if int(values["-MONTH-"]) != 1:
            lastMonth = int(values["-MONTH-"])-1
            window2 = calendar(lastMonth)
            window2.TKroot.focus_set()
            window.close()
    if event == "next": #WIP
        if int(values["-MONTH-"]) != 12:
            nextMonth = int(values["-MONTH-"])+1
            window2 = calendar(nextMonth)
            window2.TKroot.focus_set()
            window.close()
    
    if event == "Data Storage Location": #done
        window2 = location()
        window2.TKroot.focus_set()
        window.close()
        window1 = None
    if event == "locationSubmit":
        dataLocation.setLocation(values["-FOLDER-"])
        event = "close"
    if event == "importSubmit": #done
        dataLocation.importLocation(values["-FOLDER-"])
        sg.popup("Restart the app to ensure all data is imported correctly")
        try:
            file = open(dataLocation.daily(), "r")
            infoString = file.read()
            dateStart = infoString.split(" - ")[3]
            file.close()
        except:
            dateStart = getDate()
        daysSince = getDay(dateStart)
        event = "close"
    
    if event == "Options": #WIP
        window2 = options()
        window2.TKroot.focus_set()
        window.close()
        window1 = None
    if event == "optionsSubmit": #WIP
        if values["-THEME-"] == "Light":
            sg.theme("default1")
            settings.changeSetting("theme", "light")
        else:
            sg.theme("darkgrey11")
            settings.changeSetting("theme", "dark")
        
        if values["-HALFSETS-"] == "On":
            settings.changeSetting("halfSets", "on")
        else:
            settings.changeSetting("halfSets", "off")
        
        if values["-DIFFICULTY-"] == "Hard":
            settings.changeSetting("difficulty", "hard")
        elif values["-DIFFICULTY-"] == "Easy":
            settings.changeSetting("difficulty", "easy")
        else:
            settings.changeSetting("difficulty", "normal")

        autoAdjustExercises = []
        for exercise in values["-EXERCISES-"]:
            autoAdjustExercises.append(exercise.lower())
        settings.changeSetting("autoAdjust", autoAdjustExercises)

        if values["-CHEATDAY-"] == "On":
            settings.changeSetting("cheatDay", "on")
        else:
            settings.changeSetting("cheatDay", "off")

        activeExercises = []
        for exercise in values["-ACTIVE-"]:
            activeExercises.append(exercise.lower())
        settings.changeSetting("active", activeExercises)

        option = settings.readSettings()
        themeOption = option["theme"]
        halfSetsOption = option["halfSets"]
        difficultyOption = option["difficulty"]
        autoAdjustOption = option["autoAdjust"]
        cheatDayOption = option["cheatDay"]
        activeOption = option["active"]
        event = "close"

    if event == "Quit": #done
        break
    if event == "close": #done
        window1 = main()
        window1.TKroot.focus_set()
        window.close()
        window2 = None
    if window == window1 and event == sg.WIN_CLOSED: #done
        break
    if window == window2 and event == sg.WIN_CLOSED: #done
        window1 = main()
        window1.TKroot.focus_set()
        window.close()
        window2 = None
    
window.close()