import exerciseList;
import os;
import dataLocation;


def add(name, muscleGroup, original, sets, date): #runs through process of adding exercises
    newExercise = []
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
    file = open(dataLocation.records(name), "a+") #creates new file for exercise record
    file.write(str(exerciseRecord))
    file.close()
    return success


def deleteExercise(key):
    if os.path.exists(dataLocation.records(key)):
        os.remove(dataLocation.records(key))
        success = exerciseList.deleteItem(key)
    else:
        success = False
    return success