import xbmc
import xbmcgui
import requests

VECTORS_FILE_PATH = "Q:/scripts/XLink/vectors.txt"
FAVES = "Q:/scripts/XLink/faves.txt"

class KaiConnect:
    """Connection to Kai Engine via IP and Port."""
    kaiIP = '192.168.1.113'
    kaiPort = 34522
    kaiPortFoward = 30000  # Doubt I'll need this

    def CheckForKai(self):
        url = 'http://' + self.kaiIP + ':' + str(self.kaiPort) + '/api/v1/isalive'
        print('Trying to get ' + url)
        r = requests.get(url)
        if r.status_code != 200:
            xbmcgui.Dialog().ok('Kai Status', 'Wrong address, try again, Error Code: ' + str(r.status_code))
        else:
            xbmcgui.Dialog().ok('Kai Status', r.text)

    def GetFromKai(self, getCall):
        url = 'http://' + self.kaiIP + ':' + str(self.kaiPort) + '/api/v1/' + getCall
        print('Trying to get ' + url)
        r = requests.get(url)
        if r.status_code != 200:
            xbmcgui.Dialog().ok('Kai Status', 'Wrong address, try again, Error Code: ' + str(r.status_code))
        else:
            return r.text

    def GetVector(self):
        url = 'http://' + self.kaiIP + ':' + str(self.kaiPort) + '/api/v1/getvector'
        print('Trying to get ' + url)
        r = requests.get(url)
        if r.status_code != 200:
            xbmcgui.Dialog().ok('Kai Status', 'Failed to get vector, Error Code: ' + str(r.status_code))
        else:
            response = r.text.split(':')
            if len(response) > 1:
                return response[1].strip()
            else:
                return 'Unknown'

    def SetVector(self, vector):
        url = 'http://' + self.kaiIP + ':' + str(self.kaiPort) + '/api/v1/setvector?vector=' + vector
        print('Trying to get ' + url)
        r = requests.get(url)
        if r.status_code != 200:
            xbmcgui.Dialog().ok('Kai Status', 'Failed to set vector, Error Code: ' + str(r.status_code))
        else:
            xbmcgui.Dialog().ok('Kai Status', 'Vector set to: ' + vector)

    def ReadVectorsFromFile(self, filepath):
        try:
            with open(filepath, 'r') as file:
                lines = file.readlines()
            return lines
        except FileNotFoundError:
            xbmcgui.Dialog().ok('Error', 'Vectors file not found.')
            return []

    def DisplayVectorsMenu(self, vectors):
        categories = {}
        current_category = None
        for line in vectors:
            line = line.strip()
            if line.startswith('[') and line.endswith(']'):
                current_category = line[1:-1]
                categories[current_category] = []
            elif current_category:
                categories[current_category].append(line)

        category_choice = xbmcgui.Dialog().select('Choose a Category', list(categories.keys()))
        if category_choice != -1:
            chosen_category = list(categories.keys())[category_choice]
            subcategory_choice = xbmcgui.Dialog().select('Choose a Sub-category', categories[chosen_category])
            if subcategory_choice != -1:
                vector = 'Arena/XBox/' + chosen_category.replace(' ', '%20') + '/' + categories[chosen_category][subcategory_choice].replace(' ', '%20')
                self.SetVector(vector)

    def DisplaySettings(self):
        status = self.GetFromKai('getstatus')
        settings_lines = status.split('\n')
        settings_options = [line.strip() for line in settings_lines if line.strip()]

        choice = xbmcgui.Dialog().select('Settings', settings_options)
        if choice != -1:
            xbmcgui.Dialog().ok('Setting Value', settings_options[choice])

    def main(self):
        choice = xbmcgui.Dialog().select('Choose an option', ['Get XLink Kai Status', 'Get Current Arena', 'Show Arenas', 'Show Favourite Arenas', 'Set Default Arena', 'Settings'])
        
        if choice == 0:  # Get Status
            status = self.GetFromKai('getstatus')
            xbmcgui.Dialog().ok('Kai Status', 'Status: ' + status)
            return
        elif choice == 1:  # Get Vector
            vector = self.GetVector()
            xbmcgui.Dialog().ok('Kai Vector', 'Current Vector: ' + vector)
            return
        elif choice == 2:  # Show Arenas
            vectors = self.ReadVectorsFromFile(VECTORS_FILE_PATH)
            self.DisplayVectorsMenu(vectors)
            return
        elif choice == 3:  # Show Favourite Arenas
            faves = self.ReadVectorsFromFile(FAVES)
            self.DisplayVectorsMenu(faves)
            return
        elif choice == 4:  # Set Vector
            vector = 'Arena'
            self.SetVector(vector)
            return
        elif choice == 5:  # Settings
            self.DisplaySettings()
            return

if __name__ == '__main__':
    kc = KaiConnect()
    kc.main()
