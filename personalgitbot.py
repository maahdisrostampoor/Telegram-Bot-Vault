
 # Database


import sys

import sqlite3
import functools
import re
import logging
import telebot
from telebot import types


def load_db_user():
    conn = sqlite3.connect('telegram_bot.sqlite')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS telegram_bot_db_user
       (ID INTEGER NOT NULL PRIMARY KEY UNIQUE, 
        user_name TEXT, 
        user_id INTEGER,
        user_ip TEXT);''')
    conn.commit()
    conn.close()


def load_db_admin():
    conn_ad = sqlite3.connect('telegram_bot.sqlite')
    cur_ad = conn_ad.cursor()
    cur_ad.execute('''CREATE TABLE IF NOT EXISTS telegram_bot_db_admin
       (ID INTEGER NOT NULL PRIMARY KEY UNIQUE, 
        admin_name TEXT,
        admin_id INTEGER,
        user_ip_sendto_admin TEXT);''')
    conn_ad.commit()
    conn_ad.close()


def update_user(message, msg, ip):
    conn = sqlite3.connect('telegram_bot.sqlite')
    cur = conn.cursor()
    cur.execute("INSERT INTO telegram_bot_db_user(user_name,user_id,user_ip) VALUES (?,?,?)",
                (message.from_user.username, message.from_user.id, ip))
    conn.commit()
    conn.close()


def update_admin(message, msg, ip):
    conn = sqlite3.connect('telegram_bot.sqlite')
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM telegram_bot_db_admin"
                " WHERE telegram_bot_db_admin.user_ip_sendto_admin = ?", (ip,))
    j = cur.fetchone()
    res = functools.reduce(lambda sub, ele: sub * 10 + ele, j)
    if res == 0:
        cur.execute("INSERT INTO telegram_bot_db_admin (admin_name,admin_id,user_ip_sendto_admin) VALUES (?,?,?)",
                   (message.from_user.username, message.from_user.id, ip))
    conn.commit()
    conn.close()


def confirm_ip(ip_one):
    conn = sqlite3.connect('telegram_bot.sqlite')
    cur_user_id = conn.cursor()
    cur_admin = conn.cursor()
    cur_user_username = conn.cursor()
    cur_user_id.execute("SELECT telegram_bot_db_user.user_id FROM telegram_bot_db_user,telegram_bot_db_admin"
                        " WHERE user_ip = ?", (ip_one,))
    j= cur_user_id.fetchone()
    res = functools.reduce(lambda sub, ele: sub * 10 + ele, j)
    bot.send_message(res, "It is OK,you can get your OTP")
    cur_admin.execute("SELECT telegram_bot_db_admin.admin_name FROM telegram_bot_db_admin"
                      " WHERE user_ip_sendto_admin = ?", (ip_one,))
    k, = cur_admin.fetchone()
    res_two = k[k.find("(")+1:k.find(")")]
    cur_user_username.execute("SELECT telegram_bot_db_user.user_name FROM telegram_bot_db_user"
                              " WHERE user_ip= ?", (ip_one,))
    m, = cur_user_username.fetchone()
    res_three = m[m.find("(") + 1:m.find(")")]
    logging.basicConfig(format='%(asctime)s', level=logging.INFO)
    logging.info(k + " Gives permission to " + m + " with ip: " + ip_one)
    conn.commit()
    conn.close()


def deny_ip(ip_one):
    conn = sqlite3.connect('telegram_bot.sqlite')
    cur_user_id = conn.cursor()
    cur_admin = conn.cursor()
    cur_user_username = conn.cursor()
    cur_user_id.execute("SELECT telegram_bot_db_user.user_id FROM telegram_bot_db_user,telegram_bot_db_admin"
                        " WHERE user_ip = ?", (ip_one,))
    j = cur_user_id.fetchone()
    res = functools.reduce(lambda sub, ele: sub * 10 + ele, j)
    bot.send_message(res, "Sorry,access denied")
    cur_admin.execute("SELECT telegram_bot_db_admin.admin_name FROM telegram_bot_db_admin"
                      " WHERE user_ip_sendto_admin = ?", (ip_one,))
    k, = cur_admin.fetchone()
    res_two = k[k.find("(") + 1:k.find(")")]
    cur_user_username.execute("SELECT telegram_bot_db_user.user_name FROM telegram_bot_db_user"
                              " WHERE user_ip= ?", (ip_one,))
    m, = cur_user_username.fetchone()
    res_three = m[m.find("(") + 1:m.find(")")]
    logging.basicConfig(format='%(asctime)s', level=logging.INFO)
    logging.info(k + " Did not give permission to " + m + " with ip: " + ip_one)
    conn.commit()
    conn.close()



# Telegram bot branch



bot = telebot.TeleBot('1097568744:AAGZg5uHIS_zmVJEtNHZxkyg6YnWEkJhriM')
ip_list=['''''']
# Start bot


@bot.message_handler(commands=['start'])
def show_menu_one(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    item9 = types.KeyboardButton('User')
    item10 = types.KeyboardButton('Admin')
    markup.add(item9, item10)
    msg = bot.send_message(message.chat.id, text="Choose one of the options", reply_markup=markup)

#User login


@bot.message_handler(func=lambda msg: msg.text is not None and 'User' in msg.text)
def show_menu_two(message):
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
    logging.info(message.from_user.username + " logged in as a User")
    markup = types.ReplyKeyboardRemove(selective=False)
    msg = bot.send_message(message.chat.id, "Hello", reply_markup=markup)  # add username like "hello Mahdis"
    markup2 = types.ReplyKeyboardMarkup(row_width=3)
    item1 = types.KeyboardButton('Vault')
    item2 = types.KeyboardButton('Monitoring')
    item3 = types.KeyboardButton('Others')
    item4 = types.KeyboardButton('Info')
    markup2.add(item1, item2, item3, item4)
    bot.send_message(msg.chat.id, text="Choose one of the options", reply_markup=markup2)


@bot.message_handler(func=lambda msg: msg.text is not None and 'Vault' in msg.text)
def send_welcome(msg):
    markup2 = types.ReplyKeyboardRemove(selective=False)
    msg = bot.send_message(msg.chat.id, "Welcome to vault IP checker", reply_markup=markup2)
    sub_markup = types.ReplyKeyboardMarkup(row_width=3)
    item4 = types.KeyboardButton('IP')
    item5 = types.KeyboardButton('Help')
    item6 = types.KeyboardButton('Others')
    sub_markup.add(item4, item5, item6)
    bot.send_message(msg.chat.id, text="How can I help you?", reply_markup=sub_markup)


@bot.message_handler(func=lambda msg: msg.text is not None and 'Help' in msg.text)
def help(message):
    msg = bot.reply_to(message, "Hello,This is a check ip bot,For further actions please choose IP")


@bot.message_handler(func=lambda msg: msg.text is not None and 'Info' in msg.text)
def info(message):
    msg = bot.reply_to(message, message.from_user.id)

#User gives IP


@bot.message_handler(func=lambda msg: msg.text is not None and 'IP' in msg.text)
def ip(message):
    sub_markup = types.ReplyKeyboardRemove(selective=False)
    msg = bot.reply_to(message, """Please enter your ip""", reply_markup=sub_markup)
    bot.register_next_step_handler(msg, check_ip_process)


def check_ip_process(message):
    ip = message.text
    logging.basicConfig(format='%(asctime)s', level=logging.INFO)
    logging.info(message.from_user.username + " Requests a confirmation on ip: "+ message.text)
    for i in ip_list:
        if i == ip:
            bot.forward_message(324720442, message.from_user.id, message.message_id)
            msg = bot.reply_to(message, "Wait for Confirmation")
            update_user(message, msg, ip)
            return
    msg = bot.reply_to(message, "Error,Please try again")
    bot.register_next_step_handler(msg, check_ip_process)

# Admin login


@bot.message_handler(func=lambda msg: msg.text is not None and 'Admin' in msg.text)
def admin(message):
    logging.basicConfig(format='%(asctime)s ', level=logging.INFO)
    logging.info(message.from_user.username + " logged in as an Admin")
    sub_two_markup = types.ReplyKeyboardMarkup(row_width=2)
    item7 = types.KeyboardButton('yes')
    item8 = types.KeyboardButton('No')
    sub_two_markup.add(item7, item8)
    msg = bot.reply_to(message, text="Is the ip correct?", reply_markup=sub_two_markup)


@bot.message_handler(func=lambda msg: msg.text is not None and 'yes' in msg.text)
def authentication_y(message):
    sub_two_markup = types.ReplyKeyboardRemove(selective=False)
    msg = bot.reply_to(message, text="please confirm the ip by rewrite it again:)")
    bot.register_next_step_handler(msg, authentication_yes)


def authentication_yes(message):
    ip = message.text
    msg = bot.reply_to(message, text="Thanks")
    update_admin(message, msg, ip)
    confirm_ip(ip)


@bot.message_handler(func=lambda msg: msg.text is not None and 'No' in msg.text)
def authentication_n(message):
    sub_two_markup = types.ReplyKeyboardRemove(selective=False)
    msg = bot.reply_to(message, text="please confirm the ip by rewrite it again:)")
    bot.register_next_step_handler(msg, authentication_no)


def authentication_no(message):
    ip = message.text
    msg = bot.reply_to(message, text="Thanks")
    update_admin(message, msg, ip)
    deny_ip(ip)


bot.polling()
load_db_user()
load_db_admin()
