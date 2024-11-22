def characterCreation():
    return {
        "gameState": "enter_name",
        "flavor": "Name your character (1-20 alphanumeric chars)",
        "options": [
            {
                "action":"enterName",
                "path":"/new-character?name=<name>"
            }
        ]
    }