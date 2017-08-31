from logger import *
from bs4 import BeautifulSoup
import requests
from gameSession import *
import constants
import json

log = getLogger()

def enterShop():
    log.info("Entering shop...")
    httpSession.headers.update({
        "User-Agent": constants.userAgent,
        "Referer": constants.hospitalUrl,
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Upgrade-Insecure-Requests": "1"
    })
    page = httpSession.get(constants.hospitalUrl, verify=False, cookies=httpSession.cookies)
    httpSession.headers = {u'X-Requested-With': None}
    httpSession.headers = {u'Connection': None}
    httpSession.headers = {u'Accept': 'application/json, text/plain, */*'}
    parser = BeautifulSoup(page.text, "html5lib")
    playerInfo = parser.find("script", {"name": "user"}).contents[0]
    player.updatePlayerWithDict(json.loads(playerInfo))
    log.info("Player addiction: " + str(player.addiction))



def buyMethadone(quantity):
    fullUrl = constants.hospitalUrl+ "/buyhealing/10/"+str(quantity)
    httpSession.headers.update({
        "User-Agent": constants.userAgent,
        "Referer": constants.hospitalUrl,
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br"
    })

    htmlResponse = httpSession.post(fullUrl, "", verify=False, cookies=httpSession.cookies)
    responseJson = json.loads(htmlResponse.content)
    player.updatePlayerWithDict(responseJson["user"])

    log.log(LOG_LEVEL_SUCCESS, "Player addiction: " + str(player.addiction) + "%")
    httpSession.headers = {u'X-Requested-With': None}
    httpSession.headers = {u'Connection': None}
    httpSession.headers = {u'Accept': 'application/json, text/plain, */*'}


def findMethadoneQty():
    return int(player.addiction+1)