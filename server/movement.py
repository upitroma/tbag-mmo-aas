from playerClass import Player, verifySaveString
from map import rooms

def moveToDestination(saveString, destinationId):
    if not saveString:
        return {
            "gameState": "error",
            "flavor": "missing saveString",
            "options": [
                {
                    "action":"Make a new character",
                    "path":"/character-creation"
                }
            ]
        }
    elif not verifySaveString(saveString):
        return {
            "gameState": "error",
            "flavor": "invalid saveString",
            "options": [
                {
                    "action":"Make a new character",
                    "path":"/character-creation"
                }
            ]
        }

    player = Player(saveString)

    # validate destination
    if not destinationId:
        return {
            "gameState": "error",
            "flavor": "No destination specified",
            "playerInfo": player.getPlayerInfo(),
            "options": player.getPossibleActions()
        }

    try:
        destinationId = int(destinationId)
    except:
        return {
            "gameState": "error",
            "flavor": "Invalid destination",
            "playerInfo": player.getPlayerInfo(),
            "options": player.getPossibleActions()
        }
    
    # validate movement
    if int(destinationId) not in player.getReachableRoomIds():
        return {
            "gameState": "error",
            "flavor": "You cannot move there",
            "playerInfo": player.getPlayerInfo(),
            "options": player.getPossibleActions(),
            "tmp": player.getReachableRoomIds()
        }

    player.currentRoomId = destinationId
    return {
        "gameState": "move",
        "flavor": "You see "+rooms[destinationId]["description"],
        "playerInfo": player.getPlayerInfo(),
        "options": player.getPossibleActions()
    }