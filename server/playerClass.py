import time,random,hashlib,os,json
from dotenv import load_dotenv
from base64 import b64encode, b64decode

load_dotenv()

SECRET_TOKEN = os.getenv("SECRET_TOKEN")

def newSnowflakeId(name):
    return (str(time.time())+"-"+str(random.randint(100,999)))

def base64_url_encode(input):
    return b64encode(input).decode('utf-8').replace("=","-").replace("/","_")


def base64_url_decode(input):
    return b64decode(input.replace("-","=").replace("_","/"))


def randomSpawnLocation():
    return (random.randint(0,100))


import struct

def pack_player_data(player_data):
    # Pack numerical values as bytes (unsigned 8-bit)
    stats = struct.pack(
        "10B",  # 10 unsigned 8-bit integers
        player_data[2],  # health
        player_data[3],  # maxHealth
        player_data[4],  # mana
        player_data[5],  # maxMana
        player_data[6],  # strength
        player_data[7],  # dexterity
        player_data[8],  # constitution
        player_data[9],  # intelligence
        player_data[10], # wisdom
        player_data[11]  # charisma
    )
    # Include other data (strings, lists) as-is
    return [
        player_data[0], #playerId
        player_data[1], #name
        base64_url_encode(stats),  # encoded stats
        player_data[12], #spells
        player_data[13] #currentRoomId
    ]

def unpack_player_data(data):
    stats = struct.unpack(
        "10B", base64_url_decode(data[2])
    )
    return [
        data[0], # playerId
        data[1], # name
        stats[0],  # health
        stats[1],  # maxHealth
        stats[2],  # mana
        stats[3],  # maxMana
        stats[4],  # strength
        stats[5],  # dexterity
        stats[6],  # constitution
        stats[7],  # intelligence
        stats[8],  # wisdom
        stats[9],  # charisma
        data[3], #spells
        data[4]  # currentRoomId
    ]

def generateNewPlayerSave(name):
    playerData = [
        newSnowflakeId(name),  # playerId
        name,  # name
        100,  # health
        100,  # maxHealth
        100,  # mana
        100,  # maxMana
        10,   # strength
        10,   # dexterity
        10,   # constitution
        10,   # intelligence
        10,   # wisdom
        10,   # charisma
        [],   # spells
        randomSpawnLocation()  # currentRoomId
    ]

    packed_data = pack_player_data(playerData)
    signature = hashlib.sha256((SECRET_TOKEN + json.dumps(packed_data)).encode('utf-8')).hexdigest()[:10]

    payload = {
        "playerData": packed_data,
        "signature": signature
    }
    return base64_url_encode(json.dumps(payload).encode("utf-8"))

def verifySaveString(saveString):
    try:
        save = json.loads(base64_url_decode(saveString))
        packed_data = save["playerData"]
        return save["signature"] == hashlib.sha256((SECRET_TOKEN + json.dumps(packed_data)).encode('utf-8')).hexdigest()[:10]
    except:
        return False

class Player:
    def __init__(self, saveString):
        if verifySaveString(saveString):
            data = json.loads(base64_url_decode(saveString))
            playerData = unpack_player_data(data["playerData"])

            self.playerId = playerData[0]
            self.name = playerData[1]
            self.health = playerData[2]
            self.maxHealth = playerData[3]
            self.mana = playerData[4]
            self.maxMana = playerData[5]
            self.strength = playerData[6]
            self.dexterity = playerData[7]
            self.constitution = playerData[8]
            self.intelligence = playerData[9]
            self.wisdom = playerData[10]
            self.charisma = playerData[11]
            self.spells = playerData[12]
            self.currentRoomId = playerData[13]
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
        playerData = [
            self.playerId,
            self.name,
            self.health,
            self.maxHealth,
            self.mana,
            self.maxMana,
            self.strength,
            self.dexterity,
            self.constitution,
            self.intelligence,
            self.wisdom,
            self.charisma,
            self.spells,
            self.currentRoomId
        ]

        packed_data = pack_player_data(playerData)
        signature = hashlib.sha256((SECRET_TOKEN + json.dumps(packed_data)).encode('utf-8')).hexdigest()[:10]

        payload = {
            "playerData": packed_data,
            "signature": signature
        }
        return base64_url_encode(json.dumps(payload).encode("utf-8"))
