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
    return (random.randint(0,100),random.randint(0,100))

def generateNewPlayerSave(name):
    playerData = [
        newSnowflakeId(name), # playerId
        name, # name
        100, # health
        100, # maxHealth
        100, # mana
        100, # maxMana
        10, # strength
        10, # dexterity
        10, # constitution
        10, # intelligence
        10, # wisdom
        10, # charisma
        [], # spells
        randomSpawnLocation() # currentRoomId
    ]

    signature = hashlib.sha256((SECRET_TOKEN+json.dumps(playerData)).encode('utf-8')).hexdigest()[:10]

    payload = {
        "playerData":playerData,
        "signature":signature
    } 

    return base64_url_encode(json.dumps(payload).encode("utf-8"))

def verifySaveString(saveString):
    try:
        save = json.loads(base64_url_decode(saveString))
        return save["signature"] == hashlib.sha256((SECRET_TOKEN+json.dumps(save["playerData"])).encode('utf-8')).hexdigest()[:10]
    except:
        return False


class Player:
    def __init__(self, saveString):
        print(saveString)
        if verifySaveString(saveString):
            playerData = json.loads(base64_url_decode(saveString))["playerData"]

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
    
    def save(self):
        # output a signed hex string of the player data
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

        signature = hashlib.sha256((SECRET_TOKEN+json.dumps(playerData)).encode('utf-8')).hexdigest()[:10]

        payload = {
            "playerData":playerData,
            "signature":signature
        } 

        return base64_url_encode(json.dumps(payload).encode("utf-8"))
            