class Drug:
    id = 0,
    name = "",
    price = float(0),
    stamina = float(0)

    def __init__(self):
        self.id = 0
        self.name = ""
        self.price = float(0)
        self.stamina = float(0)

    def costBenefit(self):
        return float(self.stamina/self.price)

    @staticmethod
    def initWithJson(dict):
        drug = Drug()
        drug.id = dict["id"]
        drug.name = dict["name"]
        drug.price = float(dict["price"].encode('utf8').replace("$",""))
        drug.stamina = float(dict["stamina"])
        return drug