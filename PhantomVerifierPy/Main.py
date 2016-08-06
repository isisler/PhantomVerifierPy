import webbrowser, os, sys
from StatsClient import StatsClient
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

while(True):
    name = input("Enter user name: ")
    P = Player(name)

    nameOK = False
    sc = StatsClient()

    while(not nameOK):
        try:
            sc.GetPInfo(P)           
        except Exception as e:
            print(e)                   
        else: 
            nameOK = True
            break;  

        print("\n")
        name = input("Enter another user name or type Exit to quit: ")
        if name.lower() == "exit":
            sys.exit()            
        P = Player(name)
                

    print("-----------------------------------------------------------------")
    print("Player name: " + P.name)
    print("Player ID: " + P.pid)
    print("User ID: " + P.uid)

    try:
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
        sc.CheckPhantomStatus(P)
    except Exception as e:
        print(e)
        continue;

    print("-----------------------------------------------------------------")
    print("Premium status: " + str(P.isPremium))
    print("Assignments complete: " + str(P.assignmentsComplete))

    if not P.assignmentsComplete:
        print(P.assignments)

    if P.leftTag in basicPhantomTags.keys():
        print("Left tag: " + basicPhantomTags[P.leftTag])
    else:
        print("Left tag: " + str(P.leftTag))

    if P.rightTag in advancedPhantomTags.keys():
        print("Right tag: " + advancedPhantomTags[P.rightTag])
    else:
        print("Right tag: " + str(P.rightTag))          
    
    print("Gun cammo correct: " + str(P.gunCammoCorrect))
    print("-----------------------------------------------------------------")    
    print("Ready for elevator: " + str(P.readyForElevator))
    print("Player is Phantom: " + str(P.isPhantom))
    print("\n")

    cont = input("Check another player? (Y/N): ")

    if cont.lower() == "y":
        clear = lambda: os.system('cls')
        clear()
    else:
        break;

