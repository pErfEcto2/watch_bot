import logging as log
import os
import re
import time as t
import requests as r

#define logging format
log.basicConfig(filename="/var/log/watch_bot/log.txt", level=log.INFO, format="%(asctime)s:%(message)s")

def isDay() -> bool:
    curTime = int(t.strftime("%H", t.gmtime())) + 3
    return not (curTime >= 23 or curTime <= 8)

def checkBotStates(message, bots: list, messageBot) -> int: # 0 - everything is okay; 1 - bot was restarted
    os.system("ps ax > processes")
    with open("processes", "r") as f:
        processes = f.readlines()
    for bot in bots:
        # enumerate function to check end of the list
        for i, proc in enumerate(processes):
            pyProc = re.search(bot, proc)
            # if bot is active
            if pyProc:
                return 0
            # if bot is inactive and it's end of the list and it's day
            if not pyProc and i + 1 == len(processes):
                log.warning(f"Warning: {bot} is inactive, trying to restart")
                answer = f"**{bot}** is inactive"
                messageBot.send_message(message.chat.id, answer, parse_mode="Markdown")
                messageBot.send_message(message.chat.id, "Trying to restart")
                # trying to restart bot three times
                for i in range(3):
                    if not os.system(f"systemctl restart {bot[:-3] + '.service'}"):
                        answer = f"{bot} was restarted"
                        log.info(answer)
                        messageBot.send_message(message.chat.id, answer)
                        return 1
                    if i == 2:
                        answer = f"{bot} wasn't restarted"
                        log.info(answer)
                        messageBot.send_message(message.chat.id, answer)

def getJoke() -> str:
    url = "http://rzhunemogu.ru/RandJSON.aspx?CType=1"
    response = r.get(url)
    if response.status_code < 300:
        log.info(f"Request to {url} was successful")
    else:
        log.info(f"Request to {url} was unsuccessful")
    return response.text[12:-3]