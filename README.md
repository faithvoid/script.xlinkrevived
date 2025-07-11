# XLink Revived - XLink Kai script for XBMC4Xbox

![](screenshots/1.png)
![](screenshots/5.png)
![](screenshots/6.png)
![](screenshots/2.png)
![](screenshots/3.png)
![](screenshots/7.png)
![](screenshots/8.png)

## Installation:
- Download the latest release .zip
- Copy the "XLinkRevived" folder to "Q:/scripts/"
- Launch XLink Kai on your host machine, then launch the XLink Revived script and watch as it connects automagically!
- (For the best user experience, pair this script with [Cortana Server Browser](https://github.com/faithvoid/script.cortanaserverbrowser) so you can view current session information including playercounts!)

## FAQ:
- "My XLink system isn't detected?"

Make sure that XLink Kai is running, has "Allow remote UI connections" enabled in the settings (usually on by default), and that UDP/TCP ports 34522 are allowed in your firewall settings.

- "I downloaded it from the repository instead of the release .zip and it doesn't work?"

That's why there's a release zip. Changes made directly to the repository are experimental, you're on your own if you run the repo builds.

- "Will you integrate *XYZ feature?*"

If Team XLink supports it in their API, sure! Otherwise, there's only so much I can do.

- "I've figured out how to do *XYZ feature*, can I add a pull request to integrate it?"

Please do! This should be a community effort that brings players together. Any and all assistance on this project is much appreciated!

## TODO:
- [] Integrate Kai UI attacher script (works for messaging, not for anything else)
- [] Integrate chat services (arena chat works, PM support doesn't)
- [] Fix this TODO list

## Working
- Displaying username + current Arena
- Querying and joining Arenas (via "Arenas List" and "Active Arenas")
- Querying and joining sub-Arenas (via "Arenas List")
- Setting the Arena back to the default Arena!
- Viewing XLink Kai statistics
- sys.argv support for skin integration [ie; calling RunScript(Q:/scripts/XLink/default.py,ActiveArenas) will automatically launch the Active Arenas subcategory

## Not Working
- Joining sub-Arenas from Active Arenas (as it's not implemented in the GetActiveGames API, only in GetGamesList)
- Showing additional user information
- Editing settings of any kind
- Most social feature (ie; friends, chatting)

## Bugs:
- Toast notification icons will end up being blank for most users. A workaround is to add an "icon-xlinkkai.png" file to your skin, or modify the lines in default.py that say "icon-xlinkkai.png" to point to the icon of your choice.

## TODO
- Finish adding additional chat features (figured out how to send PMs, Arena PMs & chat messages, but haven't figured out how to receive them, or receive player information).
- Finish implementing login feature for users not using auto-login (you really should use auto-login though).
- Integrate into Cortana Server Browser
- Better custom notification icon support for non-Cortana users.

# Credits
- SolAZDev - Original "xbmc-kai" script that this uses initialization code from.
- CrunchBite - For working on XLink Kai, providing accessible REST API requests, and chatting with me about how certain systems work! :)
- Milenko - For all the discussions about different methods of XLink integration we've had!
