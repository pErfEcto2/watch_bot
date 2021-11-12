#!/usr/bin/python3

import os
import telebot as tb
import time
import logging as log
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
buttons = ["/start", "ping"]
keyboard = tb.types.ReplyKeyboardMarkup()
keyboard.row(*buttons)
# flag to start lib.checkBotStates() only once
flag: bool = True

@bot.message_handler(commands=["start"])
def say_hi(message):
    global flag
    bot.send_message(message.chat.id, "Hi", reply_markup=keyboard)
    if flag:
        flag = not flag
        lib.checkBotStates(message, bots, bot)
    
#if message is "ping", bot will say "pong"
@bot.message_handler(content_types=["text"])
def pong(message):
    if message.text == "ping":
        bot.send_message(message.chat.id, "pong")

try:
    bot.polling()
except Exception as e:
    log.error(f"Error: {e}")
    time.sleep(10)
    log.info("Restarting the bot")
    os.system("systemctl restart watch_bot")