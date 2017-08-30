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
        log.info("Getting robbery hash")
        httpSession.headers.update({
                             "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"})
        page = httpSession.get(constants.baseUrl, verify=False, cookies=constants.realCookies)
        parser = BeautifulSoup(page.text, "html5lib")
        action = parser.find(id=constants.robberyKey)
        action = action.parent.get("data-link")
        log.log(LOG_LEVEL_SUCCESS, "Got robbery hash successfully!")
        log.debug("Hash is " + action)
        playerInfo = parser.find("script", {"name": "user"}).contents[0]
        player.updatePlayerWithDict(json.loads(playerInfo))
        log.log(LOG_LEVEL_SUCCESS, "Update player info!")
    except Exception, e:
        log.error("Error while getting robbery hash: " + e.message)
    return action


def commitRobbery(id):
    enterRobberyMenu()
    fullURL = constants.baseUrl+lastRobberyHash+"/".decode('utf-8')+str(id).decode('utf-8')
    robAnswer = httpSession.post(fullURL, "", verify=False, cookies=constants.realCookies)
    constants.realCookies = httpSession.cookies

    jsonResponse = json.loads(robAnswer.content)
    log.log(LOG_LEVEL_SUCCESS, "Robbery success! " + jsonResponse["messages"][0][0])

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
        page = httpSession.get(constants.baseUrl+lastRobberyHash, verify=False, cookies=constants.realCookies)
        constants.realCookies = httpSession.cookies
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
    return singleRobberies[count-1]

