from nightclub import *
from robbery import *
from bs4 import BeautifulSoup
import warnings
import sys
from gameSession import *


def login():
    httpSession.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"})
    page = httpSession.get(constants.baseUrl, verify=False)
    log.info("Getting home page")
    parser = BeautifulSoup(page.text, "html5lib")
    action = parser.find("form").find("input", {"name": "action"}).get("value")
    log.info("Getting player info and logging in...")
    data = {"username": player.username, "password": player.password, "env": "1920;1080;pt-BR;24", "pl": "",
            "action": action}

    httpSession.post(constants.loginUrl, data, verify=False)
    log.log(LOG_LEVEL_SUCCESS, "Logged in successfully!")
    constants.realCookies = httpSession.cookies

    page = httpSession.get(constants.baseUrl, verify=False)
    log.info("Getting home page, now logged")
    parser = BeautifulSoup(page.text, "html5lib")
    playerInfo = parser.find("script", {"name": "user"}).contents[0]
    player.updatePlayerWithDict(json.loads(playerInfo))


def leavePrison():
    page = httpSession.get(constants.baseUrl+"/prison".decode('utf-8'), verify=False, cookies=constants.realCookies)
    log.info("Getting prison page")
    parser = BeautifulSoup(page.text, "html5lib")
    playerInfo = parser.find("script", {"name": "user"}).contents[0]
    player.updatePlayerWithDict(json.loads(playerInfo))
    valueToBribe = parser.find("input", {"name": "bribe"}).get("value")
    if player.cash >= int(valueToBribe):
        fullURL = constants.baseUrl +"/prison/cashbribe".decode('utf-8')
        robAnswer = httpSession.post(fullURL, "", verify=False, cookies=constants.realCookies)
        return True
    else:
        return False


def loop():
    errorMsg = "Error"
    while True:
        if player.inPrison:
            if config.AUTO_LEAVE_PRISON:
                left = leavePrison()
                if ~left:
                    errorMsg = "You were arrested"
                    break
            else:
                errorMsg = "You were arrested"
                break
        enterRobberyMenu()
        mostSafeRobbery = findMostSuccessRobbery()
        if player.stamina >= mostSafeRobbery.energy:
            commitRobbery(mostSafeRobbery.id)
            break
        else:
            errorMsg = "Too tired, recover feature not yet implemented"
            # nightclubHash = findNightclubHash()
            break
    log.error("Finished helper with error: " + errorMsg)


def main(argv):
    warnings.filterwarnings("ignore")
    login()
    loop()
    log.error("Terminate program")
    pass

if __name__ == "__main__":
    main(sys.argv)


