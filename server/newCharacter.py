from playerClass import Player, generateNewPlayerSave
import json

def newCharacter(name):
    # validate name
    if not name:
        return {
            "gameState": "error",
            "flavor": "Name cannot be empty",
            "options": [
                {
                        "action":"enterName",
                        "path":"/new-character?name=<name>"
                }
            ]
        }
    elif len(name) < 1 or len(name) > 20:
        return {
            "gameState": "error",
            "flavor": "Name must be between 1 and 20 characters",
            "options": [
                {
                        "action":"enterName",
                        "path":"/new-character?name=<name>"
                }
            ]
        }
    
    elif not all(char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" for char in name):
        return {
            "gameState": "error",
            "flavor": "Name can only contain alphanumeric characters",
            "options": [
                {
                        "action":"enterName",
                        "path":"/new-character?name=<name>"
                }
            ]
        }
    

    player = Player(generateNewPlayerSave(name))   

    return {
        "gameState": "explore",
        "flavor": "Venture forth, "+player.name+"!",
        "playerInfo": player.getPlayerInfo(),
        "options": [
            {
                "action":"walk forward",
                "path":"/move?save="+player.save()
            }
        ]
    }