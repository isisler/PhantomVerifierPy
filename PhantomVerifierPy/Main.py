import webbrowser, os
from StatsClient import StatsClient
from BLClient import BClient
from Player import Player


advancedPhantomTags = {}
advancedPhantomTags[290] = "Phantom Skull"
advancedPhantomTags[396] = "Advanced Black"

basicPhantomTags = {}
basicPhantomTags[283] = "Basic Black"
basicPhantomTags[284] = "Whiteout"
basicPhantomTags[285] = "Hammerhead"
basicPhantomTags[286] = "Hangar 21"
basicPhantomTags[287] = "Giants of Karelia"  

##==========================================================================================================

name = input("Enter user name: ")
P = Player(name)
sc = StatsClient()
sc.GetPInfo(P)
print(P.name)
print(P.pid)
print(P.uid)
statData = sc.GetStats(P, "general")
tagData = sc.GetStats(P, "tag")
assignmentData = sc.GetStats(P, "assignments")
weaponData = sc.GetStats(P, "weapons")
loadoutData = sc.GetStats(P, "loadout")
sc.GetUnlockedTags(P, tagData, advancedPhantomTags, basicPhantomTags)
sc.CheckForBow(P, weaponData)
sc.GetAssignments(P, assignmentData)
sc.CheckForPapers(P, assignmentData)
sc.GetCammos(P, loadoutData)
sc.CheckPremium(P, loadoutData)
sc.CheckElevatorStatus(P)

print("-----------------------------------------------------------------")
print("Premium status: " + str(P.isPremium))
print("Assignments complete: " + str(P.assignmentsComplete))

if not P.assignmentsComplete:
    print(P.assignments)

if P.leftTag in basicPhantomTags.keys():
    print("Left tag: " + basicPhantomTags[P.leftTag])
else:
    print("Left tag: " + str(P.lefTag))

if P.rightTag in advancedPhantomTags.keys():
    print("Right tag: " + advancedPhantomTags[P.rightTag])
else:
    print("Right tag: " + str(P.rightTag))          
    
print("Gun cammo correct: " + str(P.gunCammoCorrect))
print("-----------------------------------------------------------------")    
print("Ready for elevator: " + str(P.readyForElevator))
print("\n")