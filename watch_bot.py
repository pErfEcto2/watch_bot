#!/usr/bin/python3

import telebot
import os
import re
import time

with open("bot_id", "r") as f:
    bot_id = f.readline().strip()

bots = ["weatherman.py"]

bot = telebot.TeleBot(bot_id)

def openFile(name):
    with open(name, "r") as f:
        return f.readlines()

def findCorrect(processStatus, processName):
    for elem in processStatus:
        exp = f".+\/{processName}"
        res = re.match(exp, elem)
        try:
            if res.group(0):
                return True
            else:
                return False
        except:
            return False

def isRunning(processName):
    command = f"ps ax | grep {processName} > process_status"
    os.system(command)
    l = openFile("process_status")
    if findCorrect(l, processName):
        return True


buttons = ["/start"]
keyboard = telebot.types.ReplyKeyboardMarkup()
keyboard.row(*buttons)

@bot.message_handler(commands=["start"])
def say_hi(message):
    bot.send_message(message.chat.id, "Hi", reply_markup=keyboard)
    if isRunning(bots[0]):
        bot.send_message(message.chat.id, "nice")
    else:
         bot.send_message(message.chat.id, "not nice")

bot.polling()