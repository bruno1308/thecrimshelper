from logger import *

log = getLogger()

class Player:

    playerId = ""
    password = ""
    playerEid = ""
    pusherId = ""
    username = ""
    respect = 0
    credits = 0
    resistance = 0
    strength = 0
    charisma = 0
    intelligence = 0
    cash = 0
    name = ""
    stamina = 0
    addiction = 0
    tickets = 0
    alive = 0
    inPrison = 0
    robberyPower = 0
    singleRobberyPower = 0
    gangRobberyPower = 0
    assaultPower = 0

    def updatePlayerWithDict(self, toDict):
        self.playerId = toDict["id"]
        self.playerEid = toDict["eid"]
        self.pusherId = toDict["pusher_id"]
        self.username = toDict["username"]
        self.respect = toDict["respect"]
        self.credits = toDict["credits"]
        self.resistance = toDict["tolerance"]
        self.strength = toDict["strength"]
        self.charisma = toDict["charisma"]
        self.intelligence = toDict["intelligence"]
        self.cash = toDict["cash_numeric"]
        self.name = toDict["character_name"]
        self.stamina = toDict["stamina"]
        self.addiction = toDict["addiction"]
        self.tickets = toDict["tickets"]
        self.alive = toDict["alive"]
        self.inPrison = toDict["in_prison"]
        self.robberyPower = toDict["robbery_power"]
        self.singleRobberyPower = toDict["single_robbery_power"]
        self.gangRobberyPower = toDict["gang_robbery_power"]
        self.assaultPower = toDict["assault_power"]
        log.log(LOG_LEVEL_SUCCESS, "Updated player info!")
        return

    def __init__(self, username, password):
        self.username = username
        self.password = password
        return
