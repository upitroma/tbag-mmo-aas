import time,random,hashlib,os,json
from dotenv import load_dotenv
from base64 import b64encode, b64decode

import array

load_dotenv()

SECRET_TOKEN = os.getenv("SECRET_TOKEN")

def newSnowflakeId(name):
    return (str(int(time.time()))+str(random.randint(100,999)))

def base64_url_encode(input):
    return b64encode(input).decode('utf-8').replace("=","-").replace("/","_")


def base64_url_decode(input):
    return b64decode(input.replace("-","=").replace("_","/"))


def randomSpawnLocation():
    return (random.randint(0,100))


def pack_player_data(player_data):
    # Pack numerical values as bytes (unsigned 8-bit)
    stats = array.array('B',[ 
        player_data["health"],
        player_data["maxHealth"],
        player_data["mana"],
        player_data["maxMana"],
        player_data["strength"],
        player_data["dexterity"],
        player_data["constitution"],
        player_data["intelligence"],
        player_data["wisdom"], 
        player_data["charisma"]
    ])

    # Include other data (strings, lists) as-is
    return [
        player_data["playerId"],
        player_data["name"],
        base64_url_encode(stats),  # encoded stats
        player_data["spells"],
        player_data["currentRoomId"]
    ]

def unpack_player_data(data):
    stats = array.array('B', base64_url_decode(data[2]))
    return {
        "playerId": data[0],
        "name": data[1],
        "health": stats[0],
        "maxHealth": stats[1],
        "mana": stats[2],
        "maxMana": stats[3],
        "strength": stats[4],
        "dexterity": stats[5],
        "constitution": stats[6],
        "intelligence": stats[7],
        "wisdom": stats[8],
        "charisma": stats[9],
        "spells": data[3],
        "currentRoomId": data[4]
    }

def generateNewPlayerSave(name):
    playerData = {
        "playerId": newSnowflakeId(name),
        "name": name,
        "health": 100,
        "maxHealth": 100,
        "mana": 100,
        "maxMana": 100,
        "strength": 10,
        "dexterity": 10,
        "constitution": 10,
        "intelligence": 10,
        "wisdom": 10,
        "charisma": 10,
        "spells": [],
        "currentRoomId": randomSpawnLocation()
    }


    packed_data = pack_player_data(playerData)
    signature = hashlib.sha256((SECRET_TOKEN + json.dumps(packed_data)).encode('utf-8')).hexdigest()[:10]

    payload = [packed_data,signature]
    return base64_url_encode(json.dumps(payload).encode("utf-8"))

def verifySaveString(saveString):
    try:
        save = json.loads(base64_url_decode(saveString))
        packed_data = save[0]
        return save[1] == hashlib.sha256((SECRET_TOKEN + json.dumps(packed_data)).encode('utf-8')).hexdigest()[:10]
    except:
        return False

class Player:
    def __init__(self, saveString):
        if verifySaveString(saveString):
            data = json.loads(base64_url_decode(saveString))
            playerData = unpack_player_data(data[0])

            self.playerId = playerData["playerId"]
            self.name = playerData["name"]
            self.health = playerData["health"]
            self.maxHealth = playerData["maxHealth"]
            self.mana = playerData["mana"]
            self.maxMana = playerData["maxMana"]
            self.strength = playerData["strength"]
            self.dexterity = playerData["dexterity"]
            self.constitution = playerData["constitution"]
            self.intelligence = playerData["intelligence"]
            self.wisdom = playerData["wisdom"]
            self.charisma = playerData["charisma"]
            self.spells = playerData["spells"]
            self.currentRoomId = playerData["currentRoomId"]
        else:
            raise Exception("Invalid save string")
        
    def getPlayerInfo(self):
        return {
            "playerId": self.playerId,
            "name": self.name,
            "health": self.health,
            "maxHealth": self.maxHealth,
            "mana": self.mana,
            "maxMana": self.maxMana,
            "strength": self.strength,
            "dexterity": self.dexterity,
            "constitution": self.constitution,
            "intelligence": self.intelligence,
            "wisdom": self.wisdom,
            "charisma":self.charisma,
            "spells": self.spells,
            "currentRoomId": self.currentRoomId
        }

    def save(self):
        packed_data = pack_player_data(self.getPlayerInfo())
        signature = hashlib.sha256((SECRET_TOKEN + json.dumps(packed_data)).encode('utf-8')).hexdigest()[:10]

        payload = [packed_data,signature]
        
        return base64_url_encode(json.dumps(payload).encode("utf-8"))
