import completionRecord;
import exerciseList;
import daily;


def markAll(date): #marks all exercises as complete for the day
    if daily.checkDailyComplete(): #if already marked done
        return False
    else:
        success1 = completionRecord.insert("Y") #inserts Y into completionRecord.txt
        success2 = exerciseList.completeItemAll() #sets remaining sets and reps for the day to 0
        success3 = daily.dailyMarkComplete() #marks all done for the day
        if success1 and success2 and success3:
            return True
        else:
            return False


def markOne(key, date):
    exerciseDetails = exerciseList.getList(key) #retrieves current remaining reps and sets
    currentReps = int(exerciseDetails[0])
    currentSets = int(exerciseDetails[1])
    completed = 0
    if currentReps == 0 and currentSets == 0: #error submitting if already completed
        return False
    else:
        testInt = True
        while testInt:
            print("Type the number of sets completed (ignore half complete sets)") #marks completed sets done
            completeSets = input()
            try: #tests if input is int
                completeSets = int(completeSets)
                testInt = False
            except ValueError():
                print("The input was not a whole number, try again")
        if completeSets > currentSets:
            completeSets = currentSets
        completed = completeSets
        currentSets = currentSets - completeSets
        if currentSets > 0: #if all sets not completed, ask for half completed sets
            testInt = True
            while testInt:
                print("Type the number of incomplete sets attempted")
                completeHalfSets = input()
                try: #tests if input is int
                    completeHalfSets = int(completeHalfSets)
                    testInt = False
                except ValueError():
                    print("The input was not a whole number, try again")
            if completeHalfSets > 0: #if half sets were done, ask for reps
                testInt = True
                while testInt:
                    print("Type the number of reps done per half completed sets (separated by \"-\")")
                    print("If you do not wish to count half reps, type \"0\"")
                    halfReps = input()
                    if int(completeHalfSets) != 1:
                        try: #tests if input is splitable
                            splitReps = halfReps.split("-")
                            if len(splitReps) != int(completeHalfSets):
                                print("The input was not formatted correctly, try again")
                            else:
                                testInt = False
                        except:
                            print("The input was not formatted correctly, try again3")
                        sumReps = 0
                        count = 0
                        splitReps = halfReps.split("-")
                        for item in splitReps: #sums up the total extra reps done
                            sumReps += int(splitReps[count])                                
                            count += 1
                    else:
                        sumReps = int(halfReps)
                        if sumReps >= currentReps:
                            print("The input was not formatted correctly, try again")
                        else:
                            testInt = False
                    calculatedSets = sumReps // currentReps #calculates how many sets would have been done
                    calculatedSets = calculatedSets * 0.85 #multiplier due to time spread
                    calculatedSets = round(calculatedSets)
                currentSets = currentSets - calculatedSets
                completed += calculatedSets
                if currentSets == 0:
                    currentReps = 0
        else: #if all sets are done, set reps to 0
            currentReps = 0
        success1 = exerciseList.editItem(key, 0, currentReps)
        success2 = exerciseList.editItem(key, 1, currentSets)
        if success1 and success2:
            success = exerciseList.recordUpdate(key, exerciseDetails[4], completed, date) #updates records
            return success
        else:
            return False