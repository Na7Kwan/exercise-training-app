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


def markOne(key, sets, date):
    exerciseDetails = exerciseList.getList(key)
    completed = int(exerciseDetails[1]) - sets
    if sets == 0: #if all sets are done, set reps to 0
        success1 = exerciseList.editItem(key, 0, 0)
    else:
        success1 = True
    success2 = exerciseList.editItem(key, 1, sets)
    if success1 and success2:
        success = exerciseList.recordUpdate(key, exerciseDetails[4], completed, date) #updates records
        return success
    else:
        return False


def cheatDay(date): #marks today as cheatday
    if daily.checkDailyComplete(): #if already marked done
        return False
    else:
        success1 = completionRecord.insert("C") #inserts C into completionRecord.txt
        success2 = daily.dailyMarkComplete() #marks all done for the day
        if success1 and success2:
            return True
        else:
            return False