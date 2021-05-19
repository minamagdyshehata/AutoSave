# AutoSave
## Auto save every a pre-set interval of time by pressing (Ctrl+S) so that you don't lose your work incase of power loss.

* The sound notification can be removed by adding # at the beginning of the line no.51.
* To run the script when the machine is turned on, add it in to the registery:
* by calling the script with the argument -r.

    The Registry path:
```
   Computer\HKEY_USERS\S-1-5-21-3977970283-3160422839-3940440513-1001\Software\Microsoft\Windows\CurrentVersion\Run
```
* Call it with argument -u to unregister.
* Any change in the registry will be acknowledged by 2 beeps.
* This script is for Windows machines.

