# ______ ___  _____ _____ _   _ _   _  _____ ___________ 
# |  ___/ _ \|_   _|_   _| | | | | | ||  _  |_   _|  _  \
# | |_ / /_\ \ | |   | | | |_| | | | || | | | | | | | | |
# |  _||  _  | | |   | | |  _  | | | || | | | | | | | | |
# | |  | | | |_| |_  | | | | | \ \_/ /\ \_/ /_| |_| |/ / 
# \_|  \_| |_/\___/  \_/ \_| |_/\___/  \___/ \___/|___/  
# XLink Revived - XLink Kai script for XBMC4Xbox / XBMC4Gamers (https://github.com/faithvoid/script.xlinkrevived)

import socket
import xbmc
import xbmcgui
import requests
import os
import sys
import time

XLINK_ICON = os.path.join(os.path.dirname(__file__), "icon-xlinkkai.png")

class KaiConnect:
    kaiPort = 34522
    kaiPortFoward = 30000  # Probably unused

    def __init__(self):
        self.kaiIP = self.get_kai_ip()

    def get_kai_ip(self):
        return self.discover_kai_engine()

    def discover_kai_engine(self, timeout=10):
        message = b'KAI_CLIENT_DISCOVER;'
        response_signature = b'KAI_CLIENT_ENGINE_HERE;'
        broadcast_addr = '<broadcast>'
        port = self.kaiPort

        # Set up UDP socket for broadcast
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(timeout)

        # Send broadcast
        try:
            sock.sendto(message, (broadcast_addr, port))
        except Exception as e:
            xbmc.executebuiltin('Notification("XLink Revived", "Failed to send broadcast: %s", 5000, "defaulticonerror.png")' % str(e))
            sock.close()
            return ""
    
        # Listen for reply
        start = time.time()
        kai_ip = ""
        while time.time() - start < timeout:
            try:
                data, addr = sock.recvfrom(1024)
                if data.strip() == response_signature:
                    kai_ip = addr[0]
                    xbmc.executebuiltin('Notification("XLink Revived", "Kai Engine found at %s", 5000, "%s")' % (kai_ip, XLINK_ICON))
                    break
            except socket.timeout:
                break
            except Exception as e:
                xbmc.executebuiltin('Notification("XLink Revived", "Error discovering Kai: %s", 5000, "defaulticonerror.png")' % str(e))
                break
        sock.close()
        if not kai_ip:
            xbmc.executebuiltin('Notification("XLink Revived", "Kai Engine not found on network.", 5000, "defaulticonerror.png")')
        return kai_ip

    def Login(self):
        # Prompt for username and password
        keyboard_user = xbmc.Keyboard('', 'Enter XLink Kai Username')
        keyboard_user.doModal()
        if not keyboard_user.isConfirmed():
            return False
        user = keyboard_user.getText()
        if not user:
            xbmc.executebuiltin('Notification("XLink Revived", "Username required.", 3000, "defaulticonerror.png")')
            return False

        keyboard_pass = xbmc.Keyboard('', 'Enter XLink Kai Password', True)
        keyboard_pass.doModal()
        if not keyboard_pass.isConfirmed():
            return False
        password = keyboard_pass.getText()
        if not password:
            xbmc.executebuiltin('Notification("XLink Revived", "Password required.", 3000, "defaulticonerror.png")')
            return False

        # Send login to Kai Engine
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(4)
            msg = 'KAI_CLIENT_LOGIN;%s;%s;' % (user, password)
            sock.sendto(msg.encode("utf-8"), (self.kaiIP, self.kaiPort))
            # Listen for login response (such as KAI_CLIENT_LOGGED_IN or KAI_CLIENT_AUTHENTICATION_FAILED)
            try:
                data, addr = sock.recvfrom(1024)
                response = data.decode('utf-8', errors='ignore').strip()
                if response == 'KAI_CLIENT_LOGGED_IN;':
                    xbmc.executebuiltin('Notification("XLink Revived", "Login successful!", 3000, "%s")' % XLINK_ICON)
                    sock.close()
                    return True
                elif response.startswith('KAI_CLIENT_AUTHENTICATION_FAILED'):
                    xbmc.executebuiltin('Notification("XLink Revived", "Login failed: Invalid credentials.", 5000, "defaulticonerror.png")')
                    sock.close()
                    return False
                else:
                    xbmc.executebuiltin('Notification("XLink Revived", "Login: Unexpected response.", 4000, "defaulticonerror.png")')
            except socket.timeout:
                xbmc.executebuiltin('Notification("XLink Revived", "Login: No response from Kai Engine.", 4000, "defaulticonerror.png")')
            sock.close()
        except Exception as e:
            xbmc.executebuiltin('Notification("XLink Revived", "Login Error: %s", 5000, "defaulticonerror.png")' % str(e))
        return False

    def SendChatMessage(self, message):
        if not self.kaiIP:
            xbmc.executebuiltin('Notification("XLink Revived", "Kai Engine not found.", 5000, "defaulticonerror.png")')
            return
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(2)
            msg = 'KAI_CLIENT_CHAT;%s;' % message
            sock.sendto(msg.encode("utf-8"), (self.kaiIP, self.kaiPort))
            sock.close()
            xbmc.executebuiltin('Notification("XLink Revived", "Message sent.", 3000, "%s")' % XLINK_ICON)
        except Exception as e:
            xbmc.executebuiltin('Notification("XLink Revived", "Failed to send message: %s", 5000, "defaulticonerror.png")' % str(e))

    def SendPrivateMessage(self, user, message):
        if not self.kaiIP:
            xbmc.executebuiltin('Notification("XLink Revived", "Kai Engine not found.", 5000, "defaulticonerror.png")')
            return
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(2)
            msg = 'KAI_CLIENT_PM;%s;%s;' % (user, message)
            sock.sendto(msg.encode("utf-8"), (self.kaiIP, self.kaiPort))
            sock.close()
            xbmc.executebuiltin('Notification("XLink Revived", "Private Message sent.", 3000, "%s")' % XLINK_ICON)
        except Exception as e:
            xbmc.executebuiltin('Notification("XLink Revived", "Failed to send PM: %s", 5000, "defaulticonerror.png")' % str(e))

    def SendArenaPM(self, user, message):
        if not self.kaiIP:
            xbmc.executebuiltin('Notification("XLink Revived", "Kai Engine not found.", 5000, "defaulticonerror.png")')
            return
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(2)
            msg = 'KAI_CLIENT_ARENA_PM;%s;%s;' % (user, message)
            sock.sendto(msg.encode("utf-8"), (self.kaiIP, self.kaiPort))
            sock.close()
            xbmc.executebuiltin('Notification("XLink Revived", "Arena Private Message sent.", 3000, "%s")' % XLINK_ICON)
        except Exception as e:
            xbmc.executebuiltin('Notification("XLink Revived", "Failed to send Arena PM: %s", 5000, "defaulticonerror.png")' % str(e))
    
    def GetFromKai(self, getCall):
        url = 'http://{}:{}/api/v1/{}'.format(self.kaiIP, self.kaiPort, getCall)
        print('Trying to get ' + url)
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                return r.text
        except requests.exceptions.RequestException:
            xbmc.executebuiltin('Notification("XLink Revived", "Connection timed out. Please check the Kai Client.", 5000, "icon-error.png")')
        return None
    
    def GetVector(self):
        response = self.GetFromKai('getvector')
        return response.split(':')[-1].strip() if response and ':' in response else 'Unknown'
    
    def SetVector(self, vector):
        url = 'http://{}:{}/api/v1/setvector?vector={}'.format(self.kaiIP, self.kaiPort, vector)
        print('Trying to get ' + url)
        try:
            r = requests.get(url, timeout=10)
            game_name = vector.split('/')[-1].replace('%20', ' ')
            arena_image_url = self.GetArenaImage(vector)

            if r.status_code == 200:
                xbmc.executebuiltin('Notification("XLink Revived", "Arena set to: %s", 5000, "%s")' % (game_name, arena_image_url or XLINK_ICON))
            else:
                xbmc.executebuiltin('Notification("XLink Revived", "Failed to set vector, Error Code: %d", 5000, "icon-error.png")' % r.status_code)
        except requests.exceptions.RequestException:
            xbmc.executebuiltin('Notification("XLink Revived", "Connection timed out. Please check the Kai Client.", 5000, "icon-error.png")')

        def GetArenaImage(self, vector):
        try:
            encoded_vector = vector.replace(' ', '%20')
            response = requests.get("http://api.teamxlink.co.uk/kai/GetGameList/v3", timeout=10)
            response.raise_for_status()
            data = response.json()

            for game in data.get("gamelist", {}).get("games", []):
                primary = game.get("primaryVector", "").replace(' ', '%20')
                if primary == encoded_vector:
                    return game.get("arenaImage")

                for sub in game.get("subVectors", []):
                    if sub.replace(' ', '%20') == encoded_vector:
                        return game.get("arenaImage")

        except Exception as e:
            xbmc.log("Failed to fetch arena image: %s" % str(e), xbmc.LOGERROR)

        return None  # fallback if not found

    # Fetch vectors and subVectors
    def GetFullVectorsFromAPI(self):
        try:
            response = requests.get("http://api.teamxlink.co.uk/kai/GetGameList/v3")
            response.raise_for_status()
            data = response.json()
            # Map: category -> [ (game_title, subvector_list) ]
            vectors = {}
            for game in data.get("gamelist", {}).get("games", []):
                vector = game.get("primaryVector")
                if vector and vector.startswith("Arena/XBox/"):
                    parts = vector.split('/')
                    if len(parts) >= 4:
                        category = parts[2]
                        title = parts[3]
                        subvectors = game.get("subVectors", [])
                        if category not in vectors:
                            vectors[category] = []
                        vectors[category].append((title, subvectors))
            return vectors
        except Exception as e:
            xbmc.executebuiltin('Notification("Error", "Failed to fetch arenas: %s", 5000, "icon-error.png")' % str(e))
            return {}

    def DisplayVectorsMenu(self, vectors):
        if not vectors:
            xbmc.executebuiltin('Notification("No Arenas", "No game arenas available.", 5000, "icon-error.png")')
            return

        categories = list(vectors.keys())
        category_choice = xbmcgui.Dialog().select('Arenas', categories)
        if category_choice != -1:
            chosen_category = categories[category_choice]
            games = vectors[chosen_category]
            game_titles = [g[0] for g in games]
            subcategory_choice = xbmcgui.Dialog().select('Games', game_titles)
            if subcategory_choice != -1:
                chosen_game, subvectors = games[subcategory_choice]
                parent_vector = "Arena/XBox/%s/%s" % (chosen_category, chosen_game)
                if subvectors:
                    # Prepare sub-arena menu with parent as first option
                    display_names = ["[ %s ]" % chosen_game]
                    vector_choices = [parent_vector.replace(' ', '%20')]
                    # Indented display for nested sub-vectors
                    for sv in subvectors:
                        name = sv.split('/')[-1]
                        parent_found = False
                        for parent in subvectors:
                            if sv != parent and sv.startswith(parent + "/"):
                                display_names.append("  - " + name)
                                parent_found = True
                                break
                        if not parent_found:
                            display_names.append(name)
                        vector_choices.append(sv)
                    sub_choice = xbmcgui.Dialog().select('Select Sub Arena', display_names)
                    if sub_choice == -1:
                        # User backed out, do nothing
                        return
                    else:
                        self.SetVector(vector_choices[sub_choice])
                        return
                # If no subvectors, just select the main vector
                self.SetVector(parent_vector.replace(' ', '%20'))

    def GetActiveVectorsFromAPI(self):
        try:
            response = requests.get("http://api.teamxlink.co.uk/kai/GetActiveGames/v2")
            response.raise_for_status()
            data = response.json()
            vectors = {}

            for game in data.get("gamelist", {}).get("games", []):
                vector = game.get("primaryVector")
                if vector and vector.startswith("Arena/XBox/"):
                    parts = vector.split('/')
                    if len(parts) >= 4:
                        category = parts[2]
                        title = parts[3]
                        if category not in vectors:
                            vectors[category] = []
                        vectors[category].append(title)
            return vectors
        except Exception as e:
            xbmc.executebuiltin('Notification("Error", "Failed to fetch arenas: %s", 5000, "icon-error.png")' % str(e))
            return {}

    def DisplayActiveVectorsMenu(self, vectors):
        if not vectors:
            xbmc.executebuiltin('Notification("No Arenas", "No game arenas available.", 5000, "icon-error.png")')
            return

        categories = list(vectors.keys())
        category_choice = xbmcgui.Dialog().select('Active Arenas', categories)
        if category_choice != -1:
            chosen_category = categories[category_choice]
            subcategory_choice = xbmcgui.Dialog().select('Active Games', vectors[chosen_category])
            if subcategory_choice != -1:
                cat_encoded = chosen_category.replace(' ', '%20')
                title_encoded = vectors[chosen_category][subcategory_choice].replace(' ', '%20')
                vector = "Arena/XBox/%s/%s" % (cat_encoded, title_encoded)
                self.SetVector(vector)
    
    def DisplaySettings(self):
        status = self.GetFromKai('getstatus')
        if status:
            settings_options = [line.strip() for line in status.split('\n') if line.strip()]
            choice = xbmcgui.Dialog().select('XLink Kai - Settings', settings_options)
            if choice != -1:
                setting_value = settings_options[choice]
                if isinstance(setting_value, unicode):
                    setting_value = setting_value.encode('ascii', 'ignore')
                xbmc.executebuiltin('Notification("XLink Kai - Settings", "%s", 5000, "%s")' % (setting_value, XLINK_ICON))

    def GetUsername(self):
        status = self.GetFromKai('getstatus')
        if status:
            for line in status.split('\n'):
                if line.strip().startswith('username:'):
                    return line.strip().split(':', 1)[1]
        return 'N/A'
    
    def main(self):
        arg = None
        if len(sys.argv) > 1:
            arg = sys.argv[1].lstrip('?')

        if arg == 'Arenas':
            vectors = self.GetFullVectorsFromAPI()
            self.DisplayVectorsMenu(vectors)
            return
        elif arg == 'ActiveArenas':
            vectors = self.GetActiveVectorsFromAPI()
            self.DisplayActiveVectorsMenu(vectors)
            return
        elif arg == 'Default':
            self.SetVector('Arena')
            return
        elif arg == 'Status':
            status = self.GetFromKai('getstatus')
            if status:
                xbmc.executebuiltin('Notification("XLink Kai", "Status: %s", 5000, "%s")' % (status.encode('ascii', 'ignore'), XLINK_ICON))
            return
        elif arg == 'Settings':
            self.DisplaySettings()
            return

        username = self.GetUsername()
        vector = self.GetVector()

        if vector != 'Unknown':
            current_vector_display = vector.split('/')[-1].replace('%20', ' ')
        else:
            current_vector_display = 'N/A'

        menu_title = '%s - Arena: %s' % (username, current_vector_display)

        choice = xbmcgui.Dialog().select(menu_title, [
            'Arena List',
            'Active Arenas',
            'Chat',
            'Return to Default Arena',
            'Settings'
        ])

        if choice == 0:
            vectors = self.GetFullVectorsFromAPI()
            self.DisplayVectorsMenu(vectors)
        elif choice == 1:
            vectors = self.GetActiveVectorsFromAPI()
            self.DisplayActiveVectorsMenu(vectors)
        elif choice == 2:
            # Chat submenu
            chat_choice = xbmcgui.Dialog().select('Chat', [
                'Send Chat Message',
                'Send Private Message',
                'Send Arena PM'
            ])
            if chat_choice == 0:
                keyboard = xbmc.Keyboard('', 'Enter chat message')
                keyboard.doModal()
                if keyboard.isConfirmed():
                    message = keyboard.getText()
                    if message:
                        self.SendChatMessage(message)
            elif chat_choice == 1:
                keyboard = xbmc.Keyboard('', 'Enter recipient username')
                keyboard.doModal()
                if keyboard.isConfirmed():
                    user = keyboard.getText()
                    if user:
                        keyboard2 = xbmc.Keyboard('', 'Enter private message')
                        keyboard2.doModal()
                        if keyboard2.isConfirmed():
                            message = keyboard2.getText()
                            if message:
                                self.SendPrivateMessage(user, message)
            elif chat_choice == 2:
                keyboard = xbmc.Keyboard('', 'Enter recipient username')
                keyboard.doModal()
                if keyboard.isConfirmed():
                    user = keyboard.getText()
                    if user:
                        keyboard2 = xbmc.Keyboard('', 'Enter arena PM message')
                        keyboard2.doModal()
                        if keyboard2.isConfirmed():
                            message = keyboard2.getText()
                            if message:
                                self.SendArenaPM(user, message)
        elif choice == 3:
            self.SetVector('Arena')
        elif choice == 4:
            self.DisplaySettings()

if __name__ == '__main__':
    kc = KaiConnect()
    kc.main()
