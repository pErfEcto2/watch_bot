#!/usr/bin/python3

import os
import telebot as tb
import time
import logging as log
import time as t
import lib

botIdPath = "/home/projects/watch_bot/bot_id"
botsPath = "/home/projects/watch_bot/bots"

#define log format
log.basicConfig(filename="/var/log/watch_bot/log.txt", level=log.INFO, format="%(asctime)s:%(message)s")
log.info("App started!")

with open(botIdPath, "r") as f:
    bot_id = f.readline()

with open(botsPath, "r") as f:
    bots = f.readline().split()

bot = tb.TeleBot(bot_id)
# define a keyboard
buttons = ["/start", "ping", "check", "joke"]
keyboard = tb.types.ReplyKeyboardMarkup()
keyboard.row(*buttons)
# flag to start lib.checkBotStates() only once
flag: bool = True

@bot.message_handler(commands=["start"])
def say_hi(message):
    global flag
    bot.send_message(message.chat.id, "Hi", reply_markup=keyboard)
    if flag:
        while lib.isDay():
            flag = not flag
            lib.checkBotStates(message, bots, bot)
            t.sleep(5)

#if message is "ping", bot will say "pong"
@bot.message_handler(content_types=["text"])
def answerToMessage(message):
    if message.text == buttons[1]:
        bot.send_message(message.chat.id, "pong")
    
    elif message.text == buttons[2]:
        answerCode = lib.checkBotStates(message, bots, bot)
        if answerCode == 0:
            bot.send_message(message.chat.id, "Everything is okay")
    
    elif message.text == buttons[3]:
        joke = lib.getJoke()
        bot.send_message(message.chat.id, joke)
try:
    bot.polling()
except Exception as e:
    log.error(f"Error: {e}")
    time.sleep(10)
    log.info("Restarting the bot")
    os.system("systemctl restart watch_bot")