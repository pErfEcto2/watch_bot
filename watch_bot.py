#!/usr/bin/python3

import telebot
import os
import re
import time

from telebot.types import MaskPosition

botIdPath = "/home/projects/watch_bot/bot_id"

with open(botIdPath, "r") as f:
    bot_id = f.readline().strip()

bots = ["weatherman.py"]

bot = telebot.TeleBot(bot_id)
#returns list of lines in file
def openFile(name):
    with open(name, "r") as f:
        return f.readlines()
#finds active bots
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
#returns True if bot is active
def isRunning(processName):
    command = f"ps ax | grep {processName} > process_status"
    os.system(command)
    l = openFile("process_status")
    if findCorrect(l, processName):
        return True


buttons = ["/start", "ping"]
keyboard = telebot.types.ReplyKeyboardMarkup()
keyboard.row(*buttons)

@bot.message_handler(commands=["start"])
def say_hi(message):
    bot.send_message(message.chat.id, "Hi", reply_markup=keyboard)
    while True:
        for tbot in bots:
            if not isRunning(tbot):
                ans = f"*{tbot[:-3]}* is not active"
                bot.send_message(message.chat.id, ans, parse_mode="Markdown")
        time.sleep(10)
#if message == "ping", bot will say "pong"
@bot.message_handler(content_types=["text"])
def pong(message):
    if message.text == "ping":
        bot.send_message(message.chat.id, "pong")

bot.polling()