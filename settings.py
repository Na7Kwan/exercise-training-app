import ast;


def setupSettings(): #sets up settings.txt
    settings = {
        "theme" : "dark",
        "halfSets" : "on",
        "difficulty" : "normal"
    }
    file = open("settings.txt", "w")
    file.write(str(settings))
    file.close()
    return True


def readSettings(): #reads and returns all settings as dictionary
    file = open("settings.txt", "r")
    settingsStr = file.read()
    file.close()
    try: #turns string into dict if not empty
        settings = ast.literal_eval(settingsStr)
    except:
        settings = {}
    return settings


def changeSetting(setting, value): #changes the value of one setting
    file = open("settings.txt", "r")
    settingsStr = file.read()
    file.close()
    try: #turns string into dict if not empty
        settings = ast.literal_eval(settingsStr)
    except:
        settings = {}
    try:
        str(settings[setting])
        settings[setting] = value
        file = open("settings.txt", "w")
        file.write(str(settings))
        file.close()
        return True
    except:
        return False