import re, json, time
from BLClient import BClient

class StatsClient:
    def GetPInfo(self, Player):
        url = 'http://battlelog.battlefield.com/bf4/user/' + Player.name
        bc = BClient()
        response = bc.fetchURL(url)

        m = re.search("bf4/soldier/" + Player.name + "/stats/(\d+)", response)
        Player.pid = m.group(1).strip()

        m = re.search("data-user-id=\"(\d+)\"", response, re.I)        
        Player.uid = m.group(1).strip()

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

        bc = BClient()
        response = bc.fetchURL(Url)
        Data = json.loads(response)
        return Data

    def GetUnlockedTags(self, Player, tagData, advPhanTags, basPhanTags):        
        advancedTags = tagData["data"]["unlockedDogTagsIndices"]["advanced"]
        basicTags = tagData["data"]["unlockedDogTagsIndices"]["basic"]
        
        leftTag = tagData["data"]["basic"]["index"]
        rightTag = tagData["data"]["advanced"]["index"]

        unlockedPhantomTags = {}
        for tags in advPhanTags.keys():
            if tags in advancedTags:
                unlockedPhantomTags[tags] = advPhanTags[tags]        

        for tags in basPhanTags.keys():
            if tags in basicTags:
                unlockedPhantomTags[tags] = basPhanTags[tags]

        if leftTag in basPhanTags.keys():
            Player.leftTagCorrect = True
        if rightTag in advPhanTags.keys():
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

    def GetCammos(self, Player, loadoutData):
        phantomGunCammo = '2691423844'

        selectedKitIndex = int(loadoutData["data"]["currentLoadout"]["selectedKit"])
        selectedKit = loadoutData["data"]["currentLoadout"]["kits"][selectedKitIndex]
        primaryWeapID = selectedKit[0]
        secondaryWeapID = selectedKit[1]

        primaryWeap = loadoutData["data"]["currentLoadout"]["weapons"][primaryWeapID]
        secondaryWeap = loadoutData["data"]["currentLoadout"]["weapons"][secondaryWeapID]

        primaryCammoCorrect = False
        if phantomGunCammo in primaryWeap:
            primaryCammoCorrect = True

        secondaryCammoCorrect = False
        if phantomGunCammo in secondaryWeap:
            secondaryCammoCorrect = True

        gunCammoCorrect = primaryCammoCorrect and secondaryCammoCorrect

        Player.kitID = selectedKitIndex
        Player.kit = selectedKit
        Player.primaryWeap = primaryWeap
        Player.secondaryWeap = secondaryWeap
        Player.primaryCammoCorrect = primaryCammoCorrect
        Player.secondaryCammoCorrect = secondaryCammoCorrect
        Player.gunCammoCorrect = gunCammoCorrect
        Player.loadout = loadoutData["data"]["currentLoadout"]

    def CheckPremium(self, Player, loadoutData):        
        Player.isPremium = loadoutData["data"]["isPremium"]

    def CheckElevatorStatus(self, Player):
        readyForElevator = False
        
        if Player.gunCammoCorrect and Player.assignmentsComplete and Player.rightTagCorrect and Player.leftTagCorrect:
            readyForElevator = True
        if Player.assignmentsComplete:
            if Player.leftTag == 283 or Player.rightTag == 396:
                readyForElevator = True

        Player.readyForElevator = readyForElevator  


