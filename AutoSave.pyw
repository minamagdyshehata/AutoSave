#########################################
##      AutoSave every 60 seconds      ##
## Written by: Eng. Mina Magdy Shehata ##
## https://github.com/minamagdyshehata ##
#########################################

import winsound, sys, getopt, winreg, os
from time import sleep
from pynput.keyboard import Key, Controller
keyboard = Controller()

scriptname =  os.path.basename(sys.argv[0])
scriptfullpath = sys.argv[0]
RUN_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
keyCURRENTRUN = winreg.CreateKey(winreg.HKEY_CURRENT_USER, RUN_PATH)

#Handeling arguments:
full_cmd_arguments = sys.argv
argument_list = full_cmd_arguments[1:]

short_options = "ru"
long_options = ["register", "unregister"]

try:
    arguments, values = getopt.getopt(argument_list, short_options, long_options)
except getopt.error as err:
    print (str(err))# Output error, and return with an error code.
    pass

for current_argument, current_value in arguments:
    if current_argument in ("-r", "--register"):
        winreg.SetValueEx(keyCURRENTRUN, scriptname, 0, winreg.REG_SZ, scriptfullpath)
        winsound.Beep(300,100)
        winsound.Beep(300,100)
        os._exit(0)
    elif current_argument in ("-u", "--unregister"):
        try:
            winreg.DeleteValue(keyCURRENTRUN, scriptname)
            winsound.Beep(300,100)
            winsound.Beep(300,100)
            os._exit(0)
        except:
            os._exit(0)

while True:
    sleep(60)# AutoSave interval in seconds.
    keyboard.press(Key.ctrl_l)# Press left control btm.
    keyboard.press('s')# Press s.
    keyboard.release('s')# Release s.
    keyboard.release(Key.ctrl_l)# Release left control btm.
    winsound.Beep(300,100)# One beep indicating that (ctrl+s) combination is done.

# AutoSave
## Auto save every a pre-set interval of time by pressing (Ctrl+S) so that you don't lose your work incase of power loss.

## The sound notification can be removed by adding # at the beginning of the line no.51.
## To run the script when the machine is turned on, add it in to the registery:
## by calling the script with the argument -r.
##    The Registry path:
##      Computer\HKEY_USERS\S-1-5-21-3977970283-3160422839-3940440513-1001\Software\Microsoft\Windows\CurrentVersion\Run
## Call it with argument -u to unregister.
## Any change in the registry will be acknowledged by 2 beeps.
## This script is for Windows machines.
