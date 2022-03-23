import ast;
import dataLocation;


def setupSettings(): #sets up settings.txt
    settings = {
        "theme" : "dark",
        "halfSets" : "on",
        "difficulty" : "normal",
        "autoAdjust" : []
    }
    file = open(dataLocation.settings(), "w")
    file.write(str(settings))
    file.close()
    return True


def readSettings(): #reads and returns all settings as dictionary
    file = open(dataLocation.settings(), "r")
    settingsStr = file.read()
    file.close()
    try: #turns string into dict if not empty
        settings = ast.literal_eval(settingsStr)
    except:
        settings = {}
    return settings


def changeSetting(setting, value): #changes the value of one setting
    file = open(dataLocation.settings(), "r")
    settingsStr = file.read()
    file.close()
    try: #turns string into dict if not empty
        settings = ast.literal_eval(settingsStr)
    except:
        settings = {}
    try:
        str(settings[setting])
        settings[setting] = value
        file = open(dataLocation.settings(), "w")
        file.write(str(settings))
        file.close()
        return True
    except:
        return False


def checkSettings(): #checks all settings exist
    file = open(dataLocation.settings(), "r")
    settingsStr = file.read()
    file.close()
    try: #turns string into dict if not empty
        settings = ast.literal_eval(settingsStr)
    except:
        settings = {}
    newSettings = {
        "theme" : "dark",
        "halfSets" : "on",
        "difficulty" : "normal",
        "autoAdjust" : []
    }
    for option in newSettings:
        try:
            newSettings[option] = settings[option]
        except:
            pass
    file = open(dataLocation.settings(), "w")
    file.write(str(newSettings))
    file.close()
    return True