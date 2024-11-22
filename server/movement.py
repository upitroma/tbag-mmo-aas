from playerClass import Player, verifySaveString
from map import rooms

# track all players' movement to detect encounters

playerPositions = {}
for roomId in rooms.keys():
    playerPositions[roomId] = []

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

    # update player position
    for roomId in playerPositions.keys():
        if player.getPlayerInfo()["playerId"] in playerPositions[roomId]:
            playerPositions[roomId].remove(player.getPlayerInfo()["playerId"])

    player.currentRoomId = destinationId
    playerPositions[destinationId].append(player.getPlayerInfo()["playerId"])

    # if no other players in the room
    if len(playerPositions[destinationId]) == 1:
        return {
            "gameState": "move",
            "flavor": "You see "+rooms[destinationId]["description"],
            "playerInfo": player.getPlayerInfo(),
            "options": player.getPossibleActions()
        }

    # if other players in the room
    else:
        otherPlayerInfo = []
        for otherPlayerId in playerPositions[destinationId]:
            if otherPlayerId != player.getPlayerInfo()["playerId"]:
                otherPlayerInfo.append(otherPlayerId)
        return {
            "gameState": "combat",
            "flavor": "You see "+rooms[destinationId]["description"],
            "playerInfo": player.getPlayerInfo(),
            "options": player.getPossibleActions(),
            "otherPlayerInfo": otherPlayerInfo
        }