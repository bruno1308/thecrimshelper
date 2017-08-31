import constants
from logger import *
import json
from singleRobbery import *
from bs4 import BeautifulSoup
from gameSession import *
import config

log = getLogger()
lastRobberyHash = ""

def findRobberyHash():
    try:
        log.debug("Getting robbery hash")
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"}
        page = httpSession.get(constants.baseUrl, verify=False, cookies=httpSession.cookies, headers=headers)
        parser = BeautifulSoup(page.text, "html5lib")
        action = parser.find("div", {"id": constants.robberyKey})
        action = action.parent.get("data-link")
        log.debug("Hash is " + action)
        playerInfo = parser.find("script", {"name": "user"}).contents[0]
        player.updatePlayerWithDict(json.loads(playerInfo))
    except Exception, e:
        log.error("Error while getting robbery hash: " + e.message)
    return action


def commitRobbery(robbery):
    enterRobberyMenu()
    fullURL = constants.baseUrl+lastRobberyHash+"/".decode('utf-8')+str(robbery.id).decode('utf-8')
    robAnswer = httpSession.post(fullURL, "", verify=False, cookies=httpSession.cookies)

    jsonResponse = json.loads(robAnswer.content)
    player.updatePlayerWithDict(jsonResponse["user"])

    log.log(LOG_LEVEL_SUCCESS, "Robbed " + robbery.name + " with success! " + jsonResponse["messages"][0][0])
    log.log(LOG_LEVEL_SUCCESS, "Cash: " + str(player.cash) + " - Respect: " + str(player.respect)
            + " - Strength: " + str(player.strength) + " - Resistance: " + str(player.resistance)
            + " - Intelligence: " + str(player.intelligence) + " - Charisma: " + str(player.charisma))

    return robAnswer


def updateRobberiesListWithDict(dict):
    clearRobberies()
    del singleRobberies [:]
    for entry in dict:
        robbery = SingleRobbery.initWithJson(entry)
        singleRobberies.append(robbery)

def enterRobberyMenu():
    global lastRobberyHash
    try:
        log.info("Entering robbery...")
        lastRobberyHash = findRobberyHash()
        page = httpSession.get(constants.baseUrl+lastRobberyHash, verify=False, cookies=httpSession.cookies)
        parser = BeautifulSoup(page.text, "html5lib")
        robberies = parser.find("script", {"name": constants.robberiesScriptKey}).contents[0]
        dict = json.loads(robberies)
        updateRobberiesListWithDict(dict)
        log.log(LOG_LEVEL_SUCCESS, "Successfully found available robberies, total = " + str(len(singleRobberies)))
    except Exception, e:
        log.error("Error while entering robbery:" + str(e))


def commitBasicRobbery():
    try:
        robberyResponse = commitRobbery(1)
        jsonResponse = json.loads(robberyResponse.content)
        updateRobberiesListWithDict(jsonResponse["singleRobberies"])
        player.updatePlayerWithDict(jsonResponse["user"])
        log.log(LOG_LEVEL_SUCCESS, "Robbery success! "+jsonResponse["messages"][0][0])
        log.log(LOG_LEVEL_SUCCESS, "Respect now: "+str(player.respect))
    except Exception, e:
        log.error("Error while comitting robbery:" + str(e))

def findMostSuccessRobbery():
    count = 0
    for i in range(len(singleRobberies)):
        robbery = singleRobberies[i]
        if robbery.successProb < config.MIN_SUCCESS_TO_ROBBERY:
            break
        else:
            count = count + 1
            continue
    if count == 0:
        count = 1
    log.info("Most safe robbery is "+str(singleRobberies[count-1].name) + " with " + str(singleRobberies[count-1].successProb)+ "% chance of success")
    return singleRobberies[count-1]

