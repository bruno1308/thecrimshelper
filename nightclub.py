import constants
from logger import *
from bs4 import BeautifulSoup
from gameSession import *
import json
from drug import *
import math

log = getLogger()
lastNightclubHash = ""
drugs = []


def findNightclubHash():
    try:
        log.debug("Getting nightclub hash")
        httpSession.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"})
        page = httpSession.get(constants.baseUrl, verify=False, cookies=constants.realCookies)
        constants.realCookies = httpSession.cookies
        parser = BeautifulSoup(page.text, "html5lib")
        action = parser.find(id=constants.nightclubKey)
        action = action.parent.get("data-link")
        log.debug("Got Nightclub hash successfully!")
        log.debug("Hash is " + action)

        playerInfo = parser.find("script", {"name": "user"}).contents[0]
        player.updatePlayerWithDict(json.loads(playerInfo))
    except Exception,e :
        log.error("Error while getting nightclub hash "+str(e))
    return action


def exitNightclub():
    httpSession.headers.update({
                                   "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"})
    httpSession.get(constants.baseUrl+lastNightclubHash+"/exit".decode('utf-8'), verify=False, cookies=httpSession.cookies)
    httpSession.get(constants.baseUrl, verify=False, cookies=httpSession.cookies)
    log.log(LOG_LEVEL_SUCCESS, "Left nightclub so I do not get beat up")


def findFirstFavoriteNightclubUrl():
    try:
        global lastNightclubHash
        nightclubHash = findNightclubHash()
        lastNightclubHash = nightclubHash
        log.info("Getting nightclub id...")
        httpSession.headers.update({
            "User-Agent": constants.userAgent,
            "Referer": constants.baseUrl + lastNightclubHash
        })
        page = httpSession.get(constants.baseUrl+lastNightclubHash, verify=False, cookies=constants.realCookies)
        constants.realCookies = httpSession.cookies
        parser = BeautifulSoup(page.text, "html5lib")
        nightclubUrl = parser.find("input", {"value": "Entrar"}).parent.get("action")
        log.log(LOG_LEVEL_SUCCESS, "Found your favorite nightclub!")

        return nightclubUrl
    except Exception, e:
        log.error("Error while finding first favorite nightclub "+ str(e))
        return ""


def sendPusherAuth():
    fullURL = constants.baseUrl+"/pusher/auth".decode('utf-8')
    httpSession.headers.update({
                                   "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
                                    "Referer": constants.baseUrl+lastNightclubHash,
                                    "Content-Type": "application/x-www-form-urlencoded"})

    httpSession.post(fullURL, "", verify=False, cookies=constants.realCookies)
    constants.realCookies = httpSession.cookies


def getVisitors():
    httpSession.headers.update({
        "User-Agent": constants.userAgent,
        "Referer": constants.baseUrl + lastNightclubHash
    })
    httpSession.get(constants.baseUrl + lastNightclubHash + "/visitors".decode("utf-8"), verify=False, cookies=constants.realCookies)
    constants.realCookies = httpSession.cookies


def enterNightclub(nightclubUrl):
    try:
        global drugs
        del drugs[:]
        fullURL = nightclubUrl
        httpSession.headers.update({
            "User-Agent": constants.userAgent,
            "Referer": constants.baseUrl + lastNightclubHash
        })
        httpSession.post(fullURL, "", verify=False, cookies=constants.realCookies)
        # sendPusherAuth()
        getVisitors()
        pageOn = httpSession.get(constants.baseUrl+lastNightclubHash, verify=False, cookies=constants.realCookies)
        constants.realCookies = httpSession.cookies
        parser = BeautifulSoup(pageOn.text, "html5lib")
        drugsHtml = parser.find("script", {"name": "drugs"})
        drugsContent = drugsHtml.contents[0]
        drugsJson = json.loads(drugsContent)
        for drug in drugsJson:
            newDrug = Drug.initWithJson(drug)
            drugs.append(newDrug)
        log.log(LOG_LEVEL_SUCCESS, "Found drugs available, total = " + str(len(drugs)))

    except Exception,e:
        log.error("Error while entering nightclub "+ str(e))


def findBestCostBenefitDrug():
    global drugs
    bestCostBenefit = drugs[0].costBenefit()
    bestCostBenefitDrug = drugs[0]
    for drug in drugs:
        if drug.costBenefit() > bestCostBenefit:
            bestCostBenefit = drug.costBenefit()
            bestCostBenefitDrug = drug
    return bestCostBenefitDrug


def consumeBestCostBenefit():
    bestDrug = findBestCostBenefitDrug()
    quantity = float(float(100) - player.stamina)/bestDrug.stamina
    quantity = int(math.ceil(quantity))
    log.log(LOG_LEVEL_SUCCESS, "Will buy " + str(quantity) + " of " + str(bestDrug.name))
    consumeDrug(bestDrug, quantity)

    return


def consumeDrug(drug, quantity):
    fullURL = constants.baseUrl+lastNightclubHash+"/buydrug/".decode('utf-8')+str(drug.id).decode('utf-8')+"/".decode('utf-8')+str(quantity).decode('utf-8')
    httpSession.headers = {
        "User-Agent": constants.userAgent,
        "Referer": constants.baseUrl + lastNightclubHash,
         "X-Requested-With": "XMLHttpRequest"
    }
    response = httpSession.post(fullURL, "", verify=False, cookies=httpSession.cookies)
    log.log(LOG_LEVEL_SUCCESS, "Consumed drugs! Energy should be full by now")
    responseJson = json.loads(response.content)
    player.updatePlayerWithDict(responseJson["user"])
    log.debug("Player now has " + str(player.stamina) + "% stamina")
    httpSession.headers = {u'X-Requested-With': None}
    return