import datetime; #transferred
import completionRecord; #transferred
import exerciseList; #transferred
import addExercise; #transferred
import submitExercises; #transferred
import daily; #transferred
import os; #transferred


def getDay(date): #calculates the days between current date and the date this app was first opened #transferred
    todayDateTime = str(datetime.datetime.now().astimezone()) #gets current date
    todayDateStr = todayDateTime.split()[0]
    todayDateList = todayDateStr.split("-") #formats the date
    startDateList = date.split("/") #gets the start date

    todayDate = datetime.date(int(todayDateList[0]), int(todayDateList[1]), int(todayDateList[2])) #converts to datetime
    startDate = datetime.date(int(startDateList[0]), int(startDateList[1]), int(startDateList[2])) #converts to datetime
    difDates = todayDate-startDate #subtracts days
    return(difDates.days) #returns difference


def getDate(): #gets the current date in string format #transferred
    todayDateTime = str(datetime.datetime.now().astimezone()) #gets current date
    todayDateStr = todayDateTime.split()[0]
    todayDateList = todayDateStr.split("-") #formats the date
    todayDate = todayDateList[0] + "/" + todayDateList[1] + "/" + todayDateList[2] #formats the date for humans
    return(todayDate)


def mainMenu(days, date): #runs through main menu  #transferred
    if days > 1: #if not first time
        print("\nWelcome back")
        daily.checkDailyFirst(date) #runs daily first login check if not first time
    else: #if first time
        print ("\nWelcome")
        daily.firstTime(date) #runs daily.txt set up if first time
    print("Today is Day " + str(days) + " of using this app")
    exerciseList.resetCheck() #checks if exerciseList has been reset
    exerciseList.checkComplete() #checks if all activities are complete
    print("\nYour activity this past week:\n" + completionRecord.get()) #gets visual of exercise in past 7 days
    print("\nToday's exercises:")
    print(exerciseList.getList()) #gets list of exercises and remaining reps and sets for the day
    return True


def editExercise(): #runs through exercise edit menu
    print("\nEdit Menu:")
    print(exerciseList.keyList()) #prints list of exercises
    print("Type the name of the exercise you wish to edit")
    selectedKey = input().lower()
    print("Type the value you wish to edit")
    selectedValue = input().lower()
    print("Type the edit you wish to make")
    selectedEdit = input().lower()
    success = exerciseList.editItem(selectedKey, selectedValue, selectedEdit) #makes the edit in file
    return success


def addRep(date): #runs through submit menu
    print("\nSubmit Today's Sets:")
    print(exerciseList.keyList()) #prints list of exercises
    print("Type the name of the exercise you wish to submit to (alternatively, type \"mark all complete\")")
    selected = input().lower()
    if selected == "mark all complete":
        success = submitExercises.markAll(date) #allows all exercises to be marked as done quickly
        return success
    else: #individual submissions
        list = exerciseList.keyList().split("\n")[0:-1] #creates list of all exercises
        exists = False
        for exercise in list: #tests if exercise exists
            if exercise.lower() == selected:
                exists = True
        if exists:
            success = submitExercises.markOne(selected, date) #if exercise exists, run submit function
            return success
        else:
            return False


def deleteExercise():
    print("\nType the exercise you wish to delete:")
    print(exerciseList.keyList()) #prints list of exercises
    selected = input().lower()
    list = exerciseList.keyList().split("\n")[0:-1] #creates list of all exercises
    exists = False
    for exercise in list: #tests if exercise exists
        if exercise.lower() == selected:
            exists = True
    if exists:
        success = addExercise.deleteExercise(selected)
        return success
    else:
        return False


def detailsExercise():
    print("\nType the exercise you wish to view more details on:")
    print(exerciseList.keyList()) #prints list of exercises
    selected = input().lower()
    list = exerciseList.keyList().split("\n")[0:-1] #creates list of all exercises
    exists = False
    for exercise in list: #tests if exercise exists
        if exercise.lower() == selected:
            exists = True
    if exists:
        exerciseDetails = exerciseList.getList(selected)
        print("\nYou have " + str(exerciseDetails[1]) + " set(s) of " + str(exerciseDetails[0]) + " rep(s) left.")
        print("This exercise targets your " + str(exerciseDetails[2]) + ".")
        original = exerciseDetails[3].split("*")
        current = exerciseDetails[4].split("*")
        print("Your original daily goal was " + str(original[1]) + " set(s) of " + str(original[0]) + " rep(s).")
        print("Your current daily goal is " + str(current[1]) + " set(s) of " + str(current[0]) + " rep(s).")
        print("\nPress enter to continue:" )
        wait = input()
        return True
    else:
        return False


def askAgain(): #shorten code line lengths for clarity #transferred
    print("Actions: [S\u0332ubmit Today's Reps] [A\u0332dd Exercise] [M\u0332ore Exercise Details]") 
    print("         [E\u0332dit Exercises] [D\u0332elete Exercise] [O\u0332ptions] [Q\u0332uit]")
    return True


loop = True

if not os.path.exists("records"): #transferred
    os.makedirs("records")

try: #transferred
    file = open("completionRecord.txt", "r")
    file.close()
    file = open("exerciseList.txt", "r")
    file.close()
except:
    file = open("completionRecord.txt", "a+")
    file.close()
    file = open("exerciseList.txt", "a+")
    file.close()

try: #transferred
    file = open("daily.txt", "r")
    infoString = file.read()
    dateStart = infoString.split(" - ")[3]
    file.close()
except:
    dateStart = getDate()

daysSince = getDay(dateStart) #transferred
if completionRecord.fill(daysSince) == False: #checks if completion record matches days past
    print("RecordError: Record mismatch")
    loop = False #exits app

testRecords = exerciseList.testRecords(getDate()) #checks if each exercise has its file #transferred
if not testRecords:
    print("RecordError: One or more exercise records were missing, data lost")

while loop:
    mainMenu(daysSince+1, str(getDate())) #runs main menu
    askAgain()
    prompt = True
    while prompt:
        choice = input() #input for action menu
        if choice.lower() == "s": #submit reps
            prompt = False
            loop = False
            success = addRep(str(getDate())) #runs add rep menu
            if not success: #loops action menu if fails
                print("SubmitError: Your sets could not be submitted")
                prompt = True
                askAgain()
            else: #returns to main menu if succeeds
                loop = True
        elif choice.lower() == "a": #add exercises
            prompt = False
            loop = False
            success = addExercise.add(getDate()) #runs through process of adding a new exercise
            if not success: #loops action menu if fails
                print("EditError: Your exercise could not be added")
                askAgain()
                prompt = True
            else: #returns to main menu if succeeds
                loop = True
        elif choice.lower() == "m": #show more exercise details
            prompt = False
            loop = False
            success = detailsExercise()
            if not success: #loops action menu if fails
                print("DisplayError: Your exercise details could not be displayed")
                prompt = True
                askAgain()
            else: #returns to main menu if succeeds
                loop = True
        elif choice.lower() == "e": #edit exercises
            prompt = False
            loop = False
            success = editExercise() #runs edit exercise menu
            if not success: #loops action menu if fails
                print("EditError: Your exercise could not be edited")
                prompt = True
                askAgain()
            else: #returns to main menu if succeeds
                loop = True
        elif choice.lower() == "d": #deletes exercise
            prompt = False
            loop = False
            success = deleteExercise() #runs delete exercise menu
            if not success: #loops action menu if fails
                print("EditError: Your exercise could not be deleted")
                prompt = True
                askAgain()
            else: #returns to main menu if succeeds
                loop = True
        elif choice.lower() == "o": #opens options
            prompt = False
            loop = False
            success = False #temp
            if not success: #loops action menu if fails
                print("AppError: WIP") #WORK IN PROGRESS
                prompt = True
                askAgain()
            else: #returns to main menu if succeeds
                loop = True
        elif choice.lower() == "q": #quit app (stops loop)
            prompt = False
            loop = False
        else: #loops action menu if input not understood by code
            print("UserError: The input was not a command, try again")
            askAgain()