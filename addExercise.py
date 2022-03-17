import exerciseList;
import os;


def add(date): #runs through process of adding exercises
    list = exerciseList.keyList().split("\n")[0:-1] #creates list of exercises
    print("Type the name of the exercise you want to add")
    name = input().lower()

    exist = False
    for exercise in list: #checks if exercise being added already exists
        if exercise == name:
            exist = True
    if exist: #if exists, returns function as fails
        print("The exercise already exists")
        return False
    else: #otherwise continue with adding process
        newExercise = []
        print("Type the muscle group this exercise targets")
        muscleGroup = input()

        print("Perform the exercise and attempt the maximum in one go without overexertion")
        testInt = True
        while testInt:
            print("Type the number of reps you were able to achieve (as whole number)")
            original = input()
            try: #tests if input is int
                int(original)
                testInt = False
            except ValueError():
                print("The input was not a whole number, try again")
        
        testInt = True
        while testInt:
            print("How many sets do you want to do each day (as whole number)")
            sets = input()
            try: #tests if input is int
                int(sets)
                testInt = False
            except ValueError():
                print("The input was not a whole number, try again")

        formatOriginal = str(original) + "*" + str(sets)

        if int(sets) == 1:
            original = 0
        newExercise.append(original)
        newExercise.append(int(sets)-1)
        newExercise.append(muscleGroup)
        newExercise.append(formatOriginal)
        newExercise.append(formatOriginal)
        success = exerciseList.addTo(name, newExercise) #adds formatted exercise to exerciseList.txt
        exerciseRecord = {}
        addRecord = str(original) + "*" +str(1)
        recordList = [addRecord, formatOriginal]
        exerciseRecord[date] = recordList
        file = open("records\\" + name + "_record.txt", "a+") #creates new file for exercise record
        file.write(str(exerciseRecord))
        file.close()
        return success


def deleteExercise(key):
    print("\nType the name of the exercise again to confirm: " + key)
    print("Else the action will cancel")
    reply = input()        
    if reply == key:
        if os.path.exists("records\\" + key + "_record.txt"):
            os.remove("records\\" + key + "_record.txt")
        else:
            success = False
        success = exerciseList.deleteItem(key)
    else:
        success = False
    return success