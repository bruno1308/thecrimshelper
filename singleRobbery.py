

class SingleRobbery:
    id = 0
    difficulty = 0
    energy = 0
    type = 0
    name = ""
    successProb = 0

    def __init__(self, id, difficulty, energy, type, name, successProb):
        self.id = id
        self.difficulty = difficulty
        self.energy = energy
        self.type = type
        self.name = name
        self.successProb = successProb
        return

    @staticmethod
    def initWithJson(toDict):
        newRobbery = SingleRobbery(toDict["id"], toDict["difficulty"], toDict["energy"], toDict["type"], toDict["translatedname"], toDict["successprobability"])
        return newRobbery
