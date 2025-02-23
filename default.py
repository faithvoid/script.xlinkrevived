import xbmc
import xbmcgui
import requests

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

    def main(self):
        self.CheckForKai()
        status = self.GetFromKai('getstatus')
        vector = self.GetFromKai('getvector')
        xbmcgui.Dialog().ok('Kai Status', 'Status: ' + status + '\nVector: ' + vector)

if __name__ == '__main__':
    kc = KaiConnect()
    kc.main()
