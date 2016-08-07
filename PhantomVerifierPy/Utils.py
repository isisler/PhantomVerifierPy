import json, os
from BLClient import BClient
        
def Clear():
    os.system("cls")

def parseInt(s, base=10, val=None):
    if s.isdigit():
        return int(s, base)
    else:
        return val

def GetJSON(Url):
    bc = BClient()

    try:
        response = bc.fetchURL(Url)
        Data = json.loads(response)
        return Data
    except Exception as e:            
        raise