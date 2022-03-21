import ast;
import daily;
import exerciseTarget;
import completionRecord;
import dataLocation;


def getList(key = False): #fetches reps and sets remaining per exercise each day
    file = open(dataLocation.exerciseList(), "r")
    exercisesStr = file.read()
    file.close()
    try: #turns string into dict if not empty
        exercises = ast.literal_eval(exercisesStr)
    except:
        exercises = {}
    if not key: #if a key is not specified
        response = ""
        for entry in exercises:
            try:
                nameSplit = entry.split(" ")
                nameList = []
                for word in nameSplit:
                    nameList.append(word.capitalize())
                name = " ".join(nameList)
            except:
                name = entry.capitalize()
            if len(entry) < 20: #if exercise name less than 20 char, fill to 20
                response = response + name + ": "
                spaces = 20 - len(entry)
                response = response + " "*spaces
            elif len(entry) == 20: #if exercise name is 20, do nothing
                response = response + name + ": "
            else: #if exercise name more than 20 char, replace with ...
                response = response + name[0:17] + "...: "
            response = response + str(exercises[entry][0]) + " rep(s) "
            response = response + str(exercises[entry][1]) + " set(s) left today\n"
        return response
    else: #else return specified key only
        response = exercises[key]
        return response


def keyList(): #returns a list of exercise names
    file = open(dataLocation.exerciseList(), "r")
    exercisesStr = file.read()
    file.close()
    try: #turns string into dict if not empty
        exercises = ast.literal_eval(exercisesStr)
    except:
        exercises = {}
    list = ""
    for entry in exercises: #builds list of exercise names
        try:
            nameSplit = entry.split(" ")
            nameList = []
            for word in nameSplit:
                nameList.append(word.capitalize())
                name = " ".join(nameList)
        except:
            name = entry.capitalize()
        list = list + name + "\n"
    return list


def editItem(key, value, edit): #allows for editing of the exerciseList.txt from console
    file = open(dataLocation.exerciseList(), "r")
    exercisesStr = file.read()
    file.close()
    try: #turns string into dict if not empty
        exercises = ast.literal_eval(exercisesStr)
    except:
        exercises = {}
    try:
        edit = int(edit) #if edit is int, try making int before inserting
    except:
        edit = edit
    exercises[key][int(value)] = edit
    file = open(dataLocation.exerciseList(), "w")
    file.write(str(exercises))
    file.close()
    return True


def completeItemAll(): #changes all remaining reps and sets for each exercise to 0
    file = open(dataLocation.exerciseList(), "r")
    exercisesStr = file.read()
    file.close()
    try: #turns string into dict if not empty
        exercises = ast.literal_eval(exercisesStr)
    except:
        exercises = {}
    for entry in exercises: #changes all exercise remaining reps and sets to 0
        exercises[entry][0] = 0
        exercises[entry][1] = 0
    file = open(dataLocation.exerciseList(), "w")
    file.write(str(exercises))
    file.close()
    return True


def addTo(entryKey, entryValue): #adds a formated exercise to the dictionary
    file = open(dataLocation.exerciseList(), "r")
    exercisesStr = file.read()
    file.close()
    try: #turns string into dict if not empty
        exercises = ast.literal_eval(exercisesStr)
    except:
        exercises = {}
    exercises[entryKey] = entryValue #adds the exercise to dict
    file = open(dataLocation.exerciseList(), "w")
    file.write(str(exercises))
    file.close()
    return True


def testRecords(date): #checks if each exercise has its record sheet and creates a new one if there isnt
    file = open(dataLocation.exerciseList(), "r")
    exercisesStr = file.read()
    file.close()
    try: #turns string into dict if not empty
        exercises = ast.literal_eval(exercisesStr)
    except:
        exercises = {}
    success = True
    for entry in exercises:
        try: #tries opening record file for each exercise
            file = open(dataLocation.records(entry), "r")
            file.close()
        except: #if it fails, create a new empty file
            success = False #report that at least one file was lost
            exerciseRecord = {}
            insert = str(exercises[entry][0]) + "*" + str(exercises[entry][1])
            exerciseRecord[date] = insert
            file = open(dataLocation.records(entry), "a+")
            file.write(str(exerciseRecord))
            file.close()
    return success


def resetCheck(): #resets the daily goal
    if daily.checkDailyReset():
        return False
    else:
        file = open(dataLocation.exerciseList(), "r")
        exercisesStr = file.read()
        file.close()
        try: #turns string into dict if not empty
            exercises = ast.literal_eval(exercisesStr)
        except:
            exercises = {}
        for entry in exercises: #for every exercise replace today reps and sets with "tmrw" goal
            oldGoal = exercises[entry][4].split("*")
            newGoal = exerciseTarget.evaluateExercise(oldGoal, entry) #runs exercise goal evaluation
            reps = oldGoal[0]
            sets = oldGoal[1]
            exercises[entry][0] = reps
            exercises[entry][1] = sets
            exercises[entry][4] = newGoal
        file = open(dataLocation.exerciseList(), "w")
        file.write(str(exercises))
        file.close()
        daily.dailyMarkReset() #mark that the reset has occured this day
        return True


def checkComplete(): #checks if record is marked complete if all sets are done
    success = False
    if not daily.checkDailyComplete(): #if not already marked done
        file = open(dataLocation.exerciseList(), "r")
        exercisesStr = file.read()
        file.close()
        try: #turns string into dict if not empty
            exercises = ast.literal_eval(exercisesStr)
        except:
            exercises = {}
        if exercises:
            allDone = True
            for entry in exercises:
                if int(exercises[entry][1]) != 0:
                    allDone = False
            if allDone: #if all exercises are done, mark as done in daily.txt and insert Y to record
                success = daily.dailyMarkComplete()
                completionRecord.insert("Y")
        return success
    else:
        return success


def recordUpdate(key, original, completed, date): #updates exercise after every submission in exercise records
    file = open(dataLocation.records(key), "r") #open record of specific exercise
    exerciseRecord = file.read()
    file.close()
    try: #turns string into dict if not empty
        record = ast.literal_eval(exerciseRecord)
    except:
        record = {}
    temp = original.split("*")
    try:
        alreadySets = record[date][0].split("*")
        completed = int(completed) + int(alreadySets[1])
    except:
        completed = int(completed)
    completed = str(temp[0]) + "*" + str(completed)
    record[date] = [completed, original] #updates new entry with date, and completed and original goal
    file = open(dataLocation.records(key), "w")
    file.write(str(record))
    file.close()
    return True


def deleteItem(key): #allows for deleting of an exercise from exerciseList.txt from console
    file = open(dataLocation.exerciseList(), "r")
    exercisesStr = file.read()
    file.close()
    try: #turns string into dict if not empty
        exercises = ast.literal_eval(exercisesStr)
    except:
        exercises = {}
    exercises.pop(key, None)
    file = open(dataLocation.exerciseList(), "w")
    file.write(str(exercises))
    file.close()
    return True


def checkHalf():
    file = open(dataLocation.exerciseList(), "r")
    exercisesStr = file.read()
    file.close()
    try: #turns string into dict if not empty
        exercises = ast.literal_eval(exercisesStr)
    except:
        exercises = {}
    sumPercents = 0
    for key in exercises:
        done = int(exercises[key][1])
        goal = exercises[key][4]
        total = int(goal.split("*")[1])
        percent = done / total
        sumPercents = sumPercents + percent
    averageCompletion = sumPercents / len(exercises)
    if averageCompletion > 0.5:
        return True
    else:
        return False


def checkFormatting():
    file = open(dataLocation.exerciseList(), "r")
    exercisesStr = file.read()
    file.close()
    try: #turns string into dict if not empty
        exercises = ast.literal_eval(exercisesStr)
    except:
        exercises = {}
    for key in exercises:
        if len(exercises[key]) != 5:
            replaceValues = []
            try:
                int(exercises[key][0])
                int(exercises[key][1])
                replaceValues.append(exercises[key][0])
                replaceValues.append(exercises[key][1])
                exercises[key].pop(0)
                exercises[key].pop(0)
            except:
                replaceValues.append("0")
                replaceValues.append("0")
                try:
                    int(exercises[key][0])
                    exercises[key].pop(0)
                except:
                    pass
            print(replaceValues)

            
            