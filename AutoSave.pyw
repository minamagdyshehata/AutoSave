#########################################
##      AutoSave every 60 seconds      ##
## Written by: Eng. Mina Magdy Shehata ##
## https://github.com/minamagdyshehata ##
#########################################

import winsound, sys, getopt, winreg, os, subprocess,threading
from time import sleep
try:
    import easygui
except:
    subprocess.call("pip install easygui",shell=True)
    import easygui
try:
    import win32gui
except:
    subprocess.call("pip install pywin32",shell=True)
    import win32gui
try:
    from pynput.keyboard import Key, Controller
    keyboard = Controller()
except:
    subprocess.call("pip install pynput",shell=True)
    from pynput.keyboard import Key, Controller
    keyboard = Controller()
    
#Declaring variables
scriptname =  os.path.basename(sys.argv[0])
scriptfullpath = sys.argv[0]
RUN_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
keyCURRENTRUN = winreg.CreateKey(winreg.HKEY_CURRENT_USER, RUN_PATH)
w=win32gui
Found = False
StopList = []
StopListString = ""
Delay = 0
DelayString = ""
NotifyStatus = ""
ScriptOnOff = ""

def GetSettings():
    global StopList
    global StopListString
    global Delay
    global DelayString
    global NotifyStatus
    global ScriptOnOff
    #Extracting settings from the settings file:
    if not os.path.isfile(sys.argv[0][:-len(os.path.basename(sys.argv[0]))] + "AutoSave.Settings"): #Search for settings file and create a default file if it doesn't exist
        f = open(sys.argv[0][:-len(os.path.basename(sys.argv[0]))] + "AutoSave.Settings", "w")
        f.write( "Mozilla Firefox,Google Chrome,Tor Browser,Task Manager,Program Manager,Command Prompt" + chr(10) + "60" + chr(10) + "True" + chr(10) + "ON")
        f.close()
        StopList = ["Mozilla Firefox","Google Chrome","Tor Browser","Task Manager","Program Manager","Command Prompt"]
        StopListString = "Mozilla Firefox,Google Chrome,Tor Browser,Task Manager,Program Manager,Command Prompt"
        Delay = 60
        DelayString = "60"
        NotifyStatus = "True"
        ScriptOnOff = "ON"

    ###Default Settings:
    ##StopList = ["Mozilla Firefox","Google Chrome","Tor Browser","Task Manager","Program Manager","Command Prompt"]
    ##Delay Time(secs): 60
    ##Sound Notification Status: True
    ##Script ON/OFF status: son

    else:
        f = open(sys.argv[0][:-len(os.path.basename(sys.argv[0]))] + "AutoSave.Settings", "r")
        StopListString = f.readline()
        StopListString = StopListString[:len(StopListString)-1]
        StopList = StopListString.split(",")#extracting StopList
        DelayString = f.readline()
        DelayString = DelayString[:len(DelayString)-1]
        Delay = int(DelayString)#extracting delay
        NotifyStatus = f.readline()
        NotifyStatus = NotifyStatus[:len(NotifyStatus)-1]#extracting the sound notification status
        ScriptOnOff = f.readline()
        f.close()

def SaveSettings():
    global StopList
    global StopListString
    global Delay
    global DelayString
    global NotifyStatus
    global ScriptOnOff
    f = open(sys.argv[0][:-len(os.path.basename(sys.argv[0]))] + "AutoSave.Settings", "w")
    f.write( StopListString + chr(10) + DelayString + chr(10) + NotifyStatus + chr(10) + ScriptOnOff)
    f.close()
    winsound.Beep(300,100)
    os._exit(0)
    
def ActiveWindow():
    global StopList
    activewindow = w.GetWindowText(w.GetForegroundWindow())
    for x in range(0,len(StopList)):#searching for StopList in the beginning and ending of active window(crazy i know, but i have my reasons :D)
        if (len(activewindow) > len(StopList[x])) and (activewindow[:len(StopList[x])] == StopList[x] or activewindow[len(activewindow)-len(StopList[x]):]== StopList[x]):
            return StopList[x]
    #seaching backwards for - or — to find the name of the program(like chrome or firefox for example if there is a webpage opened)
    if activewindow.rfind("—") != -1:
        loc = activewindow.rfind("—") + 2
    elif activewindow.rfind("-") != -1:
        loc = activewindow.rfind("-") + 2
    else:
        loc = 0
    return activewindow[loc:]

def FoundInStopList():#searches for the active window in the StopList
    global StopList
    activewindow = ActiveWindow()   
    if activewindow in StopList:
        return True
    else:
        return False 
    

#Handeling arguments:
full_cmd_arguments = sys.argv
argument_list = full_cmd_arguments[1:]
short_options = "hruaxsgd:omtq"
long_options = ["help","register","unregister","addwindow","removewindow","settings","resetsettings","delay=","onnotify","mutenotify","runscript","quitscript"]

try:
    arguments, values = getopt.getopt(argument_list, short_options, long_options)
except getopt.error as err:
    easygui.msgbox("Please use -h or --help to check the regcognized arguments.", title="Argument not recognized")#Msg when using unrecognized argument.
    os._exit(0)
try:
    
    if sys.argv[1][0] != "-":
        easygui.msgbox("Please use -h or --help to check the regcognized arguments.", title="Argument not recognized")#Msg when using unrecognized argument.
        os._exit(0)
except:
    pass

for current_argument, current_value in arguments:
    
    if current_argument in ("-h", "--help"):
        easygui.msgbox("-h     --help           Shows help menu options." + chr(10) +
                       "-r     --register       Adds AutoSave script to registery." + chr(10) +
                       "-u     --unregister     Removes AutoSave script from registry." + chr(10) +
                       "-a     --addwindow      Adds a window to the StopList." + chr(10) +
                       "-x     --removewindow   Removes a window from the StopList." + chr(10) +
                       "-s     --settings       Shows current settings." + chr(10) +
                       "-g     --resetsettings  Resets settings." + chr(10) +
                       "-d T   --delay T        Sets the delay time (in seconds) between autosaves." + chr(10) +
                       "-o     --onnotify       Turns sound notification ON for every autosave." + chr(10) +
                       "-m     --mutenotify     Turns sound notification OFF for every autosave." + chr(10) +
                       "-t     --runscript      Turns AutoSave script ON." + chr(10) +
                       "-q     --quitscript     Turns AutoSave script OFF.", title="Help Menu")
        os._exit(0)

    elif current_argument in ("-r", "--register"):#registers the script.
        winreg.SetValueEx(keyCURRENTRUN, scriptname, 0, winreg.REG_SZ, scriptfullpath)
        winsound.Beep(300,100)
        winsound.Beep(300,100)
        os._exit(0)

    elif current_argument in ("-u", "--unregister"):#unregisters the script.
        try:
            winreg.DeleteValue(keyCURRENTRUN, scriptname)
            winsound.Beep(300,100)
            winsound.Beep(300,100)
            os._exit(0)
        except:
            easygui.msgbox("AutoSave script was not registered!!", title="Unregister AutoSave script")
            os._exit(0)

    elif current_argument in ("-a", "--addwindow"):#adds a window to StopList if it doesn't already exist.
        sleep(5)
        activewindow = ActiveWindow()
        GetSettings()#extracts current settings
        for x in range (0,len(StopList)):
            if StopList[x] == activewindow:
                easygui.msgbox(chr(34) + activewindow + chr(34) + " is already in StopList[]!!", title="Add Window")#msg incase window already in StopList
                os._exit(0)
        
        #Modifies StopList.
        StopList.append(activewindow)
        StopListString = ""
        for x in range (0,len(StopList)):
            StopListString += StopList[x] + ","
        StopListString = StopListString[:len(StopListString)-1]
        SaveSettings()#Saves Settings.
        

    elif current_argument in ("-x", "--removewindow"):#removes a window to StopList if it exists.
        sleep(5)
        activewindow = ActiveWindow()
        try:
            GetSettings()#extracts current settings
            StopList.remove(activewindow)#Removes unwanted window
            StopListString = ""
            for x in range (0,len(StopList)):
                StopListString += StopList[x] + ","
            StopListString = StopListString[:len(StopListString)-1]
            SaveSettings()#Saves Settings. 
        except:
            easygui.msgbox(chr(34) + activewindow + chr(34) + " was not found in StopList[]!!", title="Remove Window")#msg incase window doesn't exist in StopList
        os._exit(0)

    elif current_argument in ("-s", "--settings"):
        GetSettings()#extracts current settings
        easygui.msgbox("++StopList: " + StopListString + chr(10) + "++Delay Time(secs): " + DelayString + chr(10) +
                       "++Sound Notification Status: " + NotifyStatus + chr(10) + "++Script ON/OFF status: " + ScriptOnOff, title="Current Settings")
        os._exit(0)

    elif current_argument in ("-g", "--resetsettings"):#resets settings by deleting settings file if it exists.
        if os.path.isfile(sys.argv[0][:-len(os.path.basename(sys.argv[0]))] + "AutoSave.Settings"):
            os.remove(sys.argv[0][:sys.argv[0].rfind(chr(92))+1] + "AutoSave.Settings")
        GetSettings()#creates the default settings file.
        winsound.Beep(300,100)
        os._exit(0)

    elif current_argument in ("-d", "--delay"):#modifies the delay time.
        GetSettings()
        try:#to make sure only numbers are entered.
            DelayString = current_value
            Delay = int(DelayString)
            SaveSettings()
        except:
            easygui.msgbox("Only numbers are allowed to modify autosave rate.", title="Delay Modification")#error msg incase numbers are not used.
        os._exit(0)

    elif current_argument in ("-o", "--onnotify"):#sound notifications ON with every autosave.
        GetSettings()
        if NotifyStatus == "True":
            easygui.msgbox("Sound notifications are already ON", title="Sound Notifications")#error msg incase notificantions are already ON.
            os._exit(0)
        NotifyStatus = "True"
        SaveSettings()
        os._exit(0)

    elif current_argument in ("-m", "--mutenotify"):#sound notifications OFF with every autosave.
        GetSettings()
        if NotifyStatus == "False":
            easygui.msgbox("Sound notifications are already OFF", title="Sound Notifications")#error msg incase notificantions are already OFF.
            os._exit(0)
        NotifyStatus = "False"
        SaveSettings()
        os._exit(0)

    elif current_argument in ("-t", "--runscript"):#makes Script ON/OFF status ON.
        GetSettings()
        if ScriptOnOff == "ON":
            easygui.msgbox("Script ON/OFF status is already ON", title="Script ON/OFF")#error msg incase script ON/OFF status is already ON.
            os._exit(0)
        ScriptOnOff = "ON"
        SaveSettings()
        os._exit(0)

    elif current_argument in ("-q", "--quitscript"):#makes Script ON/OFF status OFF.
        GetSettings()
        if ScriptOnOff == "OFF":
            easygui.msgbox("Script ON/OFF status is already OFF", title="Script ON/OFF")#error msg incase script ON/OFF status is already OFF.
            os._exit(0)
        ScriptOnOff = "OFF"
        SaveSettings()
        os._exit(0)

#this function will be called using threading so it is always running in parallel with the main loop
def Always_Checking():
    global Found
    while True:
        Found = FoundInStopList()
        GetSettings()
        if ScriptOnOff == "OFF":
            os._exit(0)

#main loop:       
while True:
    Parallel = threading.Timer(0,Always_Checking)
    Parallel.start()          
    sleep(Delay)# AutoSave interval in seconds.
    while Found:
        Found = Found
    keyboard.press(Key.ctrl_l)# Press left control btm.
    keyboard.press('s')# Press s.
    keyboard.release('s')# Release s.
    keyboard.release(Key.ctrl_l)# Release left control btm.
    if NotifyStatus == "True":
        winsound.Beep(300,100)# One beep indicating that (ctrl+s) combination is done.
    Parallel.cancel()

# AutoSave
## Auto save every a pre-set interval of time by pressing (Ctrl+S) so that you don't lose your work incase of power loss.
##* All Settings are adjustable through arguments (use -h or --help to check them)
##* The the registery path used for the script to autorun when your machine boots:
##```
##   Computer\HKEY_USERS\S-1-5-21-3977970283-3160422839-3940440513-1001\Software\Microsoft\Windows\CurrentVersion\Run
##```
##* Call it with argument -r or -u to register or unregister.
##* To add or remove a window to the StopList (list of programs were AutoSave script is paused) do the following:
##*     open the needed program and minimize it.
##*     call the script with the correct argument
##*     in 5 seconds maximize you program and it will be added or removed automatically
##*  Any change in the registry will be acknowledged by 2 beeps.
##*  Any change in the registry will be acknowledged by 1 beep.
##*  This script is for Windows machines.
