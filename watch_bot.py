#!/usr/bin/python3

import os
import telebot as tb
import time
import logging as log
import time as t
import lib

botIdPath = "/home/projects/watch_bot/bot_id"
botsPath = "/home/projects/watch_bot/bots"
creator_path = "/home/projects/weatherman/creator"

#define log format
log.basicConfig(filename="/var/log/watch_bot/log.txt", level=log.INFO, format="%(asctime)s:%(message)s")
log.info("App started!")

with open(botIdPath, "r") as f:
    bot_id = f.readline()

with open(botsPath, "r") as f:
    bots = f.readline().split()

with open(creator_path, "r") as f:
    creator = f.readline()

bot = tb.TeleBot(bot_id)
# define keyboards
buttons = ["check stop or start", "check", "joke"]
keyboard = tb.types.ReplyKeyboardMarkup()
keyboard.row(*buttons)
# flag to start lib.checkBotStates() only once
flag: bool = True

@bot.message_handler(commands=["start"])
def say_hi(message):
    global flag
    bot.send_message(message.chat.id, "Checking started", reply_markup=keyboard)
    if message.from_user.username == creator:
        while flag and lib.isDay():
            lib.checkBotStates(message, bots, bot)
            t.sleep(5)

#if message is "ping", bot will say "pong"
@bot.message_handler(content_types=["text"])
def answerToMessage(message):
    if message.from_user.username == creator:
        if message.text == buttons[0]:
            global flag
            if not flag:
                flag = True
                say_hi(message)
            else:
                bot.send_message(message.chat.id, "Checking stopped")
                flag = False
        
        elif message.text == buttons[1]:
            answerCode = lib.checkBotStates(message, bots, bot)
            if answerCode == 0:
                bot.send_message(message.chat.id, "Everything is okay")
            else:
                bot.send_message(message.chat.id, "Something went wrong")

        elif message.text == buttons[2]:
            joke = lib.getJoke()
            bot.send_message(message.chat.id, joke)
try:
    bot.polling()
except Exception as e:
    log.error(f"Error: {e}")
    time.sleep(10)
    log.info("Restarting the bot")
    os.system("systemctl restart watch_bot")