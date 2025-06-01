import socket
import xbmc
import xbmcgui
import requests
import os
import sys
import time

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
                    xbmc.executebuiltin('Notification("XLink Revived", "Kai Engine found at %s", 5000, "icon-xlinkkai.png")' % kai_ip)
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
            if r.status_code == 200:
                xbmc.executebuiltin('Notification("XLink Revived", "Arena set to: %s", 5000, "icon-xlinkkai.png")' % game_name)
            else:
                xbmc.executebuiltin('Notification("XLink Revived", "Failed to set vector, Error Code: %d", 5000, "icon-error.png")' % r.status_code)
        except requests.exceptions.RequestException:
            xbmc.executebuiltin('Notification("XLink Revived", "Connection timed out. Please check the Kai Client.", 5000, "icon-error.png")')
    
    def GetVectorsFromAPI(self):
        try:
            response = requests.get("http://api.teamxlink.co.uk/kai/GetGameList/v2")
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

    def DisplayVectorsMenu(self, vectors):
        if not vectors:
            xbmc.executebuiltin('Notification("No Arenas", "No game arenas available.", 5000, "icon-error.png")')
            return

        categories = list(vectors.keys())
        category_choice = xbmcgui.Dialog().select('Arenas', categories)
        if category_choice != -1:
            chosen_category = categories[category_choice]
            subcategory_choice = xbmcgui.Dialog().select('Games', vectors[chosen_category])
            if subcategory_choice != -1:
                cat_encoded = chosen_category.replace(' ', '%20')
                title_encoded = vectors[chosen_category][subcategory_choice].replace(' ', '%20')
                vector = "Arena/XBox/%s/%s" % (cat_encoded, title_encoded)
                self.SetVector(vector)

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
                xbmc.executebuiltin('Notification("XLink Kai - Settings", "%s", 5000, "icon-xlinkkai.png")' % setting_value)

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
            vectors = self.GetVectorsFromAPI()
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
                xbmc.executebuiltin('Notification("XLink Kai", "Status: %s", 5000, "icon-xlinkkai.png")' % status.encode('ascii', 'ignore'))
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
            'Return to Default Arena',
            'Settings'
        ])

        if choice == 0:
            vectors = self.GetVectorsFromAPI()
            self.DisplayVectorsMenu(vectors)
        elif choice == 1:
            vectors = self.GetActiveVectorsFromAPI()
            self.DisplayActiveVectorsMenu(vectors)
        elif choice == 2:
            self.SetVector('Arena')
        elif choice == 3:
            self.DisplaySettings()

if __name__ == '__main__':
    kc = KaiConnect()
    kc.main()
