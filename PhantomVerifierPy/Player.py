class Player:
    def __init__(self, Name):
        self.name = Name
        self.pid = None
        self.uid = None
        self.isPremium = False
        self.kitID = None
        self.leftTag = None
        self.leftTagCorrect = False
        self.rightTag = None
        self.rightTagCorrect = False
        self.hasBow = False
        self.hasPapers = False
        self.assignments = {}
        self.assignmentsComplete = False
        self.basicTags = []
        self.advancedTags = []
        self.unlockedPhantomTags = {}
        self.loadout = []
        self.kit = []
        self.primaryWeap = []
        self.secondaryWeap = []
        self.primaryCammoCorrect = False
        self.secondaryCammoCorrect = False
        self.gunCammoCorrect = False
        self.readyForElevator = False


