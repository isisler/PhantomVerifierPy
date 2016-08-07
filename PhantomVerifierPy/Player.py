class Player:
    pid = None
    uid = None
    isPremium = False
    kitID = None
    leftTag = None
    leftTagCorrect = False
    rightTag = None
    rightTagCorrect = False
    hasBow = False
    hasPapers = False
    assignments = {}
    assignmentsComplete = False
    basicTags = []
    advancedTags = []
    unlockedPhantomTags = {}
    loadout = []
    kit = []
    primaryWeap = []
    secondaryWeap = []   
    readyForElevator = False
    primaryCammoCorrect = False
    secondaryCammoCorrect = False
    _gunCammoCorrect = False
    soldierCammoCorrect = False
    soldierCammo = None
    isPhantom = False
    name = None
    factionID = None
    teamID = None

    def __init__(self, Name):
        self.name = Name      
    
    @property
    def gunCammoCorrect(self):
        _gunCammoCorrect = self.primaryCammoCorrect and self.secondaryCammoCorrect
        return _gunCammoCorrect

   



