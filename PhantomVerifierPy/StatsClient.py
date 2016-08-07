import re, json, time
from BLClient import BClient
from Player import Player
import Utils

class StatsClient:
    
    advancedPhantomTags = {}
    advancedPhantomTags[290] = "Phantom Skull"
    advancedPhantomTags[396] = "Advanced Black"

    basicPhantomTags = {}
    basicPhantomTags[283] = "Basic Black"
    basicPhantomTags[284] = "Whiteout"
    basicPhantomTags[285] = "Hammerhead"
    basicPhantomTags[286] = "Hangar 21"
    basicPhantomTags[287] = "Giants of Karelia"

    phantomGunCammo = "2691423844"
    
    phantomSoldierCammos = {}
    phantomSoldierCammos["1718445917"] = "US Recon"
    phantomSoldierCammos["3708038440"] = "US Support"
    phantomSoldierCammos["1106023470"] = "US Engineer"
    phantomSoldierCammos["2272918344"] = "US Assault"
    phantomSoldierCammos["3058802644"] = "RU Recon"
    phantomSoldierCammos["189371737"] = "RU Support"
    phantomSoldierCammos["1328556791"] = "RU Engineer"
    phantomSoldierCammos["619258235"] = "RU Assault"
    phantomSoldierCammos["3967968267"] = "CN Recon"
    phantomSoldierCammos["1791326440"] = "CN Support"
    phantomSoldierCammos["521371829"] = "CN Engineer"
    phantomSoldierCammos["1309593175"] = "CN Assault"
                     

    def GetPInfo(self, Player):
        url = "http://battlelog.battlefield.com/bf4/user/" + Player.name
        bc = BClient()

        try:
            response = bc.fetchURL(url)
        except Exception as e:
            raise

        m = re.search("bf4/soldier/" + Player.name + "/stats/(\d+)", response)
        if m is not None:
            Player.pid = m.group(1).strip()
        else:
            raise Exception("Player ID not found")
        
        m = re.search("data-user-id=\"(\d+)\"", response, re.I)        
        if m is not None:
            Player.uid = m.group(1).strip()
        else:
            raise Exception("User ID not found")
    

    def GetStats(self, Player, statsType):
        if statsType == "tag":
            Url = "http://battlelog.battlefield.com/bf4/soldier/dogtagsPopulateStats/" + Player.name + "/" + Player.pid + "/" + Player.uid + "/1/0/"           
        if statsType == "general":
            Url = "http://battlelog.battlefield.com/bf4/warsawoverviewpopulate/" + Player.pid + "/" + "/1/"
        if statsType == "assignments":
            Url = "http://battlelog.battlefield.com//bf4/soldier/missionsPopulateStats/" + Player.name + "/" + Player.pid + "/" + Player.uid + "/1/"
        if statsType == "weapons":
            Url = "http://battlelog.battlefield.com/bf4/warsawWeaponsPopulateStats/" + Player.pid + "/1/stats/";
        if statsType == "loadout":
            Url = "http://battlelog.battlefield.com/bf4/loadout/get/PLAYER/" + Player.pid + "/1/?cacherand=" + '%.2f' % time.monotonic();

        return Utils.GetJSON(Url)    

    def GetUnlockedTags(self, Player, tagData):
        
        advancedTags = tagData["data"]["unlockedDogTagsIndices"]["advanced"]
        basicTags = tagData["data"]["unlockedDogTagsIndices"]["basic"]
        
        leftTag = tagData["data"]["basic"]["index"]
        rightTag = tagData["data"]["advanced"]["index"]

        unlockedPhantomTags = {}
        for tags in self.advancedPhantomTags.keys():
            if tags in advancedTags:
                unlockedPhantomTags[tags] = self.advancedPhantomTags[tags]        

        for tags in self.basicPhantomTags.keys():
            if tags in basicTags:
                unlockedPhantomTags[tags] = self.basicPhantomTags[tags]

        if leftTag in self.basicPhantomTags.keys():
            Player.leftTagCorrect = True
        if rightTag in self.advancedPhantomTags.keys():
            Player.rightTagCorrect = True
                
        Player.unlockedPhantomTags = unlockedPhantomTags
        Player.basicTags = basicTags
        Player.advancedTags = advancedTags
        Player.leftTag = leftTag
        Player.rightTag = rightTag

    def CheckForBow(self, Player, weaponData):        
        for weapons in weaponData["data"]["mainWeaponStats"]:
            slug = weapons["slug"]
            if "phantom" in slug:
                Player.hasBow = True

    def GetAssignments(self, Player, assignmentData):
        assignments = {}
        assignments[1] = assignmentData["data"]["allMissions"]["ghost1"]["completion"]
        assignments[2] = assignmentData["data"]["allMissions"]["ghost2"]["completion"]
        assignments[3] = assignmentData["data"]["allMissions"]["ghost3"]["completion"]
        assignments[4] = assignmentData["data"]["allMissions"]["ghost4"]["completion"]

        if assignments[1] == 100 and assignments[2] == 100 and assignments[3] == 100:
            Player.assignmentsComplete = True
            
        Player.assignments = assignments

    def CheckForPapers(self, Player, assignmentData):
        Player.hasPapers = assignmentData["data"]["allMissions"]["ghost4"]["active"]

    def GetCammos(self, Player, loadoutData, server):
        selectedKitIndex = int(loadoutData["data"]["currentLoadout"]["selectedKit"])
        selectedKit = loadoutData["data"]["currentLoadout"]["kits"][selectedKitIndex]
        primaryWeapID = selectedKit[0]
        secondaryWeapID = selectedKit[1]

        if primaryWeapID in loadoutData["data"]["currentLoadout"]["weapons"]:
            primaryWeap = loadoutData["data"]["currentLoadout"]["weapons"][primaryWeapID]
        else:
            primaryWeap = "Unknown"
        if secondaryWeapID in loadoutData["data"]["currentLoadout"]["weapons"]:
            secondaryWeap = loadoutData["data"]["currentLoadout"]["weapons"][secondaryWeapID]
        else:
            secondaryWeap = "Unknown"
        
        if server.snapShotJSON != None:
            data = server.snapShotJSON
            for x in range(0, len(data["snapshot"]["teamInfo"])):
                tempPs = data["snapshot"]["teamInfo"][str(x)]["players"]    
                if Player.pid in tempPs:
                    Player.factionID = data["snapshot"]["teamInfo"][str(x)]["faction"]
                    Player.teamID = x

            if Player.factionID == 0:
                Player.soldierCammo = selectedKit[7]
            elif Player.factionID == 1:
                Player.soldierCammo = selectedKit[9]
            elif Player.factionID == 2:
                Player.soldierCammo = selectedKit[11]

            if Player.soldierCammo in self.phantomSoldierCammos:
                Player.soldierCammoCorrect = True
        else:
            Player.soldierCammo = "Unknown"
            Player.soldierCammoCorrect = False
                                                                       
        primaryCammoCorrect = False
        if self.phantomGunCammo in primaryWeap:
            primaryCammoCorrect = True

        secondaryCammoCorrect = False
        if self.phantomGunCammo in secondaryWeap:
            secondaryCammoCorrect = True

        Player.kitID = selectedKitIndex
        Player.kit = selectedKit
        Player.primaryWeap = primaryWeap
        Player.secondaryWeap = secondaryWeap
        Player.primaryCammoCorrect = primaryCammoCorrect
        Player.secondaryCammoCorrect = secondaryCammoCorrect
        Player.loadout = loadoutData["data"]["currentLoadout"]

    def CheckPremium(self, Player, loadoutData):        
        Player.isPremium = loadoutData["data"]["isPremium"]

    def CheckElevatorStatus(self, Player):
        readyForElevator = False
        cammoCorrect = True
        
        if Player.soldierCammo != None and Player.soldierCammoCorrect == False:
            cammoCorrect = False
           
        if Player.gunCammoCorrect and Player.assignmentsComplete and Player.rightTagCorrect and Player.leftTagCorrect and cammoCorrect:
            readyForElevator = True
        if Player.assignmentsComplete:
            if Player.leftTag == 283 or Player.rightTag == 396:
                readyForElevator = True

        Player.readyForElevator = readyForElevator

    def CheckPhantomStatus(self, Player):
        assignmentsComplete = False
        if Player.assignments[1] == 100 and Player.assignments[2] == 100 and Player.assignments[3] == 100 and Player.assignments[4] == 100:
            assignmentsComplete = True

        if Player.hasBow and Player.hasPapers and assignmentsComplete:
            Player.isPhantom = True   

    def UpdatePlayer(self, P, server):
        statData = self.GetStats(P, "general")
        tagData = self.GetStats(P, "tag")
        assignmentData = self.GetStats(P, "assignments")
        weaponData = self.GetStats(P, "weapons")
        loadoutData = self.GetStats(P, "loadout")

        self.GetUnlockedTags(P, tagData)
        self.CheckForBow(P, weaponData)
        self.GetAssignments(P, assignmentData)
        self.CheckForPapers(P, assignmentData)
        self.GetCammos(P, loadoutData, server)
        self.CheckPremium(P, loadoutData)
        self.CheckElevatorStatus(P)
        self.CheckPhantomStatus(P)




