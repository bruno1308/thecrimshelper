import constants
from logger import *
from bs4 import BeautifulSoup
from gameSession import *
import json

log = getLogger()


def findNightclubHash():
    try:
        log.info("Getting nightclub hash")
        httpSession.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"})
        page = httpSession.get(constants.baseUrl, verify=False, cookies=constants.realCookies)
        parser = BeautifulSoup(page.text, "html5lib")
        action = parser.find(id=constants.nightclubKey)
        action = action.parent.get("data-link")
        log.log(LOG_LEVEL_SUCCESS, "Got Nightclub hash successfully!")
        log.debug("Hash is " + action)

        playerInfo = parser.find("script", {"name": "user"}).contents[0]
        player.updatePlayerWithDict(json.loads(playerInfo))
        log.log(LOG_LEVEL_SUCCESS, "Update player info!")
    except Exception:
        log.error("Error while getting nightclub hash")
    return action

