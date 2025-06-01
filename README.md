# XLink Revived - XLink Kai script for XBMC4Xbox

![](screenshots/1.png)
![](screenshots/5.png)
![](screenshots/6.png)
![](screenshots/2.png)
![](screenshots/3.png)
![](screenshots/7.png)
![](screenshots/8.png)

## Installation:
- Copy "default.py" to "Q:/scripts/XLinkRevived/default.py"
- Modify "IP.txt" with the IP address of your XLink Kai machine, then copy it to the same folder as default.py (don't worry if you don't do this, the script will prompt you to enter your IP if the file is missing!)
- Launch XLink Kai on your host machine, then launch the XLink Revived script.
- ???
- Profit!
- (For the best user experience, pair this script with [Cortana Server Browser](https://github.com/faithvoid/script.cortanaserverbrowser) so you can view current session information including playercounts!)

## Working
- Displaying username + current Arena
- Querying and joining Arenas (via "Arenas List" and "Active Arenas")
- Setting the Arena back to the default Arena!
- Viewing XLink Kai statistics
- sys.argv support for skin integration [ie; calling RunScript(Q:/scripts/XLink/default.py,ActiveArenas) will automatically launch the Active Arenas subcategory

## Not Working
- Showing additional user information
- Editing settings of any kind
- Any sort of social feature (ie; friends, chatting)

## Bugs:
- Toast notification icons will end up being blank for most users. A workaround is to add an "icon-xlinkkai.png" file to your skin, or modify the lines in default.py that say "icon-xlinkkai.png" to point to the icon of your choice.

## TODO
- Integrate into Cortana Server Browser
- Add a function to manually edit "IP.txt"

# Credits
- SolAZDev - Original "xbmc-kai" script that this uses initialization code from.
- CrunchBite - For working on XLink Kai, providing accessible REST API requests, and chatting with me about how certain systems work! :)
- Milenko - For all the discussions about different methods of XLink integration we've had!
