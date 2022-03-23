import ast;
import datetime;
import settings;
import dataLocation;


def evaluateExercise(oldGoal, entry):
    difficulty = settings.readSettings()["difficulty"]
    if difficulty == "normal":
        raiseMultiplier = 1.2
        lowerMultiplier = 0.9
    elif difficulty == "hard":
        raiseMultiplier = 1.5
        lowerMultiplier = 1
    elif difficulty == "easy":
        raiseMultiplier = 1.1
        lowerMultiplier = 0.7
    else:
        raiseMultiplier = 1
        lowerMultiplier = 1
    goal = oldGoal
    todayDateTime = str(datetime.datetime.now().astimezone()) #gets current date
    todayDateStr = todayDateTime.split()[0]
    todayDateList = todayDateStr.split("-")
    todayDate = datetime.date(int(todayDateList[0]), int(todayDateList[1]), int(todayDateList[2]))
    file = open(dataLocation.records(entry), "r") #opens record of the exercise
    recordStr = file.read()
    file.close()
    try: #turns string into dict if not empty
        record = ast.literal_eval(recordStr)
    except:
        record = {}
    autoList = settings.readSettings()["autoAdjust"]
    
    if entry in autoList:
        try: #lowers daily goal if last three days failed significantly
            lastThree = []
            for i in range(1, 4):
                unformatDate = todayDate - datetime.timedelta(days=i)
                lastThree.append(unformatDate.strftime("%Y/%m/%d"))
            recordHalf = True
            recentChange = False
            for date in lastThree:
                completedSets = record[date][0].split("*")[1]
                goalSets = record[date][1].split("*")[1]
                if int(completedSets) >= int(goalSets):
                    recordHalf = False
                if str(record[date][1]) != str(record[lastThree[0]][1]):
                    recentChange = True
            if recordHalf and not recentChange:
                goal[0] = int(goal[0])*lowerMultiplier
                goal[0] = str(int(goal[0]))
        except:
            pass

        try: #raises daily goal if last 5 days were done (works on 5+ reps only)
            lastFive = []
            for i in range(1, 6):
                unformatDate = todayDate - datetime.timedelta(days=i)
                lastFive.append(unformatDate.strftime("%Y/%m/%d"))
            recordDone = True
            recentChange = False
            for date in lastFive:
                if record[date][0] != record[date][1]:
                    recordDone = False
                if str(record[date][1]) != str(record[lastFive[0]][1]):
                    recentChange = True
            if recordDone and not recentChange:
                goal[0] = int(goal[0])*raiseMultiplier
                goal[0] = str(int(goal[0]))
        except:
            pass

        try: #raise daily goal if last 10 days were done (works for under 5 reps only) WIP
            lastTen = []
            for i in range(1, 6):
                unformatDate = todayDate - datetime.timedelta(days=i)
                lastTen.append(unformatDate.strftime("%Y/%m/%d"))
            recordDone = True
            recentChange = False
            for date in lastTen:
                details = record[date][1].split("*")
                if record[date][0] != record[date][1] and int(details[0]) >= 5:
                    recordDone = False
                if str(record[date][1]) != str(record[lastTen[0]][1]):
                    recentChange = True
            if recordDone and not recentChange:
                goal[0] = int(goal[0])+1
                goal[0] = str(int(goal[0]))
        except:
            pass

    newGoal = "*".join(goal)
    return newGoal #if nothing special, daily goal remains same