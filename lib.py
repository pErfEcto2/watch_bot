import time as t
import logging as log
import os
import re

#define logging format
log.basicConfig(filename="/var/log/watch_bot/log.txt", level=log.INFO, format="%(asctime)s:%(message)s")

def isDay() -> bool:
    curTime = int(t.strftime("%H", t.gmtime())) + 3
    return not (curTime >= 22 or curTime <= 9)

def checkBotStates(message, bots: list, messageBot):
    while True:
        os.system("ps ax > processes")
        with open("processes", "r") as f:
            processes = f.readlines()
        for bot in bots:
            # enumerate function to check end of the list
            for i, proc in enumerate(processes):
                pyProc = re.search(bot, proc)
                # if bot is active
                if pyProc:
                    break
                # if bot is inactive and it's end of the list
                if not pyProc and i + 1 == len(processes) and isDay():
                    log.error(f"Error: {bot} is inactive, trying to restart")
                    answer = f"**{bot}** is inactive"
                    messageBot.send_message(message.chat.id, answer, parse_mode="Markdown")
                    messageBot.send_message(message.chat.id, "Trying to restart")
                    # trying to restart bot three times
                    for i in range(3):
                        if not os.system(f"systemctl restart {bot[:-3] + '.service'}"):
                            answer = f"{bot} was restarted"
                            log.info(answer)
                            messageBot.send_message(message.chat.id, answer)
                            break
                        if i == 2:    
                            answer = f"{bot} wasn't restarted"
                            log.info(answer)
                            messageBot.send_message(message.chat.id, answer)
        t.sleep(5)