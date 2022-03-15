import ast;


def evaluateExercise(doneSets, oldGoal, entry):
    goal = oldGoal
    if False: #lowers daily goal if failed significantly (WIP)
        return False
    elif False: #raises daily goal if last 5 days were done (WIP)
        try:
            file = open(entry + "_record.txt", "r") #opens record of the exercise
            recordStr = file.read()
            file.close()
            try: #turns string into dict if not empty
                record = ast.literal_eval(recordStr)
            except:
                record = {}
            
        except:
            newGoal = goal[0] + "*" + goal[1]
    else: #if nothing special, daily goal remains same
        newGoal = goal[0] + "*" + goal[1]
    return newGoal