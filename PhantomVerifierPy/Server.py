from BLClient import BClient
import Utils

class Server():

    guid = None
    serverInfoJSON = None
    playersJSON = None
    snapShotJSON = None
        
    def __init__(self, GUID):
        self.guid = GUID
                              
    def GetServerJSON(self):
        serverURL = "http://battlelog.battlefield.com/bf4/servers/show/pc/"
        Url = serverURL + self.guid + "/?json=1"

        return Utils.GetJSON(Url)

    def GetServerPlayersJSON(self):
        playersURL = "http://battlelog.battlefield.com/bf4/servers/getPlayersOnServer/pc/"
        Url = playersURL + self.guid + "/"

        return Utils.GetJSON(Url)

    def GetScoreBoardJSON(self):        
        snapshotURL = "http://keeper.battlelog.com/snapshot/"
        Url = snapshotURL + self.guid + "/"

        return Utils.GetJSON(Url)

    def GetPlayerNames(self):        
        players = []
        for p in self.playersJSON["players"]:
            players.append(p["persona"]["personaName"])
                            
        return players

    def UpdateServer(self):
        self.serverInfo = self.GetServerJSON()
        self.playersJSON = self.GetServerPlayersJSON()
        self.snapShotJSON = self.GetScoreBoardJSON()

