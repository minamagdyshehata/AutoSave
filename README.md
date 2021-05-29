# AutoSave
## Auto save every a pre-set interval of time by pressing (Ctrl+S) so that you don't lose your work incase of power loss.

* All Settings are adjustable through arguments (use -h or --help to check them)
* The the registery path used for the script to autorun when your machine boots:
```
   Computer\HKEY_USERS\S-1-5-21-3977970283-3160422839-3940440513-1001\Software\Microsoft\Windows\CurrentVersion\Run
```
* Call it with argument -r or -u to register or unregister.
* To add or remove a window to the StopList (list of programs were AutoSave script is paused) do the following:
*     open the needed program and minimize it.
*     call the script with the correct argument
*     in 5 seconds maximize you program and it will be added or removed automatically
*  Any change in the registry will be acknowledged by 2 beeps.
*  Any change in the registry will be acknowledged by 1 beep.
*  This script is for Windows machines.
*  While testing the script I realized that for some strange reason it isn't working with Microsoft Edge (you can't add it to StopList and it damage the settings file to the point that you will need to reset the settings using -g. I really don't care...no one is using it anyway :D:D.
*  Update 29.05.2021:
*    I couldn't resiste finding out why it doesn't work with Microsoft Edge, and it turned out that after the word Microsoft there is a unicode character 'u200b'(ZERO WIDTH SPACE)!!
*    The script is modified so that it detects that character and replace it with '*' so that it doesn't damage the settings file.
