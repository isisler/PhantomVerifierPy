import webbrowser, os, sys
from StatsClient import StatsClient
from Player import Player
from Server import Server
import Utils

serverGUID = "24debd5e-6744-48d7-8b0c-812bc261057d"
#serverGUID = "21b6f40b-3c64-4c85-83b3-76284fd76363"

sc = StatsClient()

def fetchPlayers():
    players = []
    playerList = {}    
    players = serv.GetPlayerNames()

    i = 1
    for p in sorted(players, key=str.lower):
        playerList[i] = p
        i += 1
    return playerList

def PrintResults(P):    

    try:
        sc.UpdatePlayer(P, serv)
    except Exception as e:
        print(e)    

    print("-----------------------------------------------------------------")

    print("Premium status: " + str(P.isPremium))
    print("Assignments complete: " + str(P.assignmentsComplete))

    if not P.assignmentsComplete:
        print(P.assignments)

    if P.leftTag in sc.basicPhantomTags.keys():
        print("Left tag: " + sc.basicPhantomTags[P.leftTag])
    else:
        print("Left tag: " + str(P.leftTag))

    if P.rightTag in sc.advancedPhantomTags.keys():
        print("Right tag: " + sc.advancedPhantomTags[P.rightTag])
    else:
        print("Right tag: " + str(P.rightTag))          
    
    print("Gun cammo correct: " + str(P.gunCammoCorrect))

    print("-----------------------------------------------------------------")    

    print("Soldier cammo correct: " + str(P.soldierCammoCorrect))
    if P.soldierCammoCorrect == False:        
        print("Soldier cammo: " + str(P.soldierCammo))
    if P.soldierCammo == "Unknown" or P.soldierCammo == None:
        print("Player must check their solider cammo in game.  Can't check here.")      

    print("-----------------------------------------------------------------")    

    print("Ready for elevator: " + str(P.readyForElevator))
    print("Player is Phantom: " + str(P.isPhantom))
      

    print("\n")

    
def PickFromList():
    while(True):
        playerList = {}     
    
        print("Refreshing players...\n")            
        serv.UpdateServer()    

        playerList = fetchPlayers()
        if len(playerList) == 0:
            print("No players on the server.")
            break;                     

        print("Players on server: ")
        for p in playerList.keys():
                print("(" + str(p) + ")" + " " + playerList[p])

        pID = None
        pID = Utils.parseInt(input("\nSelect player ID: "))
   
        while(pID == None or pID > len(playerList.keys()) or pID < 1):        
            print("ID not recognized.  ID must be an integer between 1 and " + str(len(playerList.keys())))
            pID = Utils.parseInt(input("\nSelect player ID: "))

        print("\nRetrieving Data")
        P = Player(playerList[pID])

               
        try:
            sc.GetPInfo(P)           
        except Exception as e:
            print(e)
            continue;

        print("-----------------------------------------------------------------")
        print("Player name: " + P.name)
        print("Player ID: " + P.pid)
        print("User ID: " + P.uid)

        PrintResults(P)

        cont = input("Check another player using this mode? (Y/N): ")

        if cont.lower() == "y":        
            Utils.Clear()
        else:
            break;  

def EnterName():
    while(True):
        
        nameOK = False
        sc = StatsClient()

        while(not nameOK):            
            name = input("\nEnter user name: ")
            P = Player(name)

            try:
                sc.GetPInfo(P) 
            except Exception as e:
                print(e)
                continue;                  
            else: 
                nameOK = True            
                break;

        print("-----------------------------------------------------------------")
        print("Player name: " + P.name)
        print("Player ID: " + P.pid)
        print("User ID: " + P.uid)
        
        PrintResults(P)

        cont = input("Check another player using this mode? (Y/N): ")

        if cont.lower() == "y":        
            Utils.Clear()
        else:
            break;
            
#==================================================================================================================

while(True):
    serv = Server(serverGUID)
    method = input("Pick from server player list (L) or enter name (N)?: ")

    if method.lower() == "l":
        Utils.Clear()
        PickFromList()
    elif method.lower() == "n":
        Utils.Clear()
        EnterName()

    cont = input("\nContinue program? (Y/N): ")

    if cont.lower() == "y":        
        Utils.Clear()
    else:
        break;
