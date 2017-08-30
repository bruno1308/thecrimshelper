import requests
from player import *
import config

singleRobberies = []
httpSession = requests.session()
player = Player(config.USERNAME, config.PASSWORD)


def clearRobberies():
    global singleRobberies
    del singleRobberies [:]