import ldap

con = ldap.initialize('ldap://127.0.0.1')
base_dn = "dc=iais, dc=com"
con.protocol_version = ldap.VERSION3
con.set_option(ldap.OPT_REFERRALS, 0)
con.simple_bind_s('username', 'password')
search_filter = "(uid=m.rostampoor)"
result = con.search_s(base_dn, ldap.SCOPE_SUBTREE, search_filter, None)
user_dn = result[0][0]  # get the user DN
con.simple_bind_s(user_dn, "password")

if __name__ == "__main__":
    ldap_server = "ldap://127.0.0.1/"
    username = "mahdis rostampoor"
    password = "password"
    # the following is the user_dn format provided by the ldap server
    user_dn = "cn=" + username + ",ou=users,dc=iais,dc=com"
    # adjust this to your base dn for searching
    base_dn = "dc=iais,dc=com"
    connect = ldap.initialize(ldap_server)
    search_filter = "(uid=mahdis rostampoor)"
    try:
        # if authentication successful, get the full user data
        connect.simple_bind_s(user_dn, password)
        result = connect.search_s(base_dn, ldap.SCOPE_SUBTREE, search_filter)
        print(result)
        # return all user data results
        connect.unbind_s()

    except ldap.LDAPError:
        connect.unbind_s()
        print("authentication error"")
l = ldap.initialize("ldap://192.168.43.113")
try:
    l.protocol_version = ldap.VERSION3
    l.set_option(ldap.OPT_REFERRALS, 0)

    bind = l.simple_bind_s("me@example.com", "password")

    base = "dc=example, dc=com"
    criteria = "(&(objectClass=user)(sAMAccountName=username))"
    attributes = ['displayName', 'company']
    result = l.search_s(base, ldap.SCOPE_SUBTREE, criteria, attributes)

    results = [entry for dn, entry in result if isinstance(entry, dict)]
    print
    results
finally:
    l.unbind()

import sys
import ldap
import sqlite3
import functools
import re
import logging
import telebot
from telebot import types


def load_db_password():
    conn = sqlite3.connect('telegram_bot_last.sqlite')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS telegram_bot_db_password
       (ID INTEGER NOT NULL PRIMARY KEY UNIQUE, 
        user_name TEXT, 
        password INTEGER,
        chat_id INTEGER);''')
    conn.commit()
    conn.close()


def update_username(username,message):
    conn = sqlite3.connect('telegram_bot_last.sqlite')
    cur = conn.cursor()
    cur.execute("INSERT INTO telegram_bot_db_password(user_name,chat_id) VALUES (?,?)",
                (username, message.from_user.id))
    conn.commit()
    conn.close()


def update_password(password,message):
    conn = sqlite3.connect('telegram_bot_last.sqlite')
    cur = conn.cursor()
    cur.execute("UPDATE telegram_bot_db_password SET password=? WHERE chat_id = ?" ,(password,message))
    conn.commit()
    conn.close()


def select_password_admin(message):
    conn = sqlite3.connect('telegram_bot_last.sqlite')
    cur = conn.cursor()
    cur.execute("SELECT user_name FROM telegram_bot_db_password"
                " WHERE chat_id = ?", (message,))
    username_admin, = cur.fetchone()
    cur.execute("SELECT password FROM telegram_bot_db_password"
                " WHERE chat_id = ?", (message,))
    password_admin, = cur.fetchone()
    user_dn = "cn=" + username_admin + ",cn=admin,ou=groups,dc=iais,dc=com"
    base_dn = "dc=iais,dc=com"
    connect = ldap.initialize("ldap://127.0.0.1/")
    try:
        search_filter = "(uid=" + username_admin + ")"
        connect.simple_bind_s(user_dn, password_admin)
        result = connect.search_s(base_dn, ldap.SCOPE_SUBTREE, search_filter, None)
        msg = bot.send_message(message, "authentication successful as an admin")
        print(result)
        connect.unbind_s()
        sub_two_markup = types.ReplyKeyboardMarkup(row_width=2)
        item7 = types.KeyboardButton('yes')
        item8 = types.KeyboardButton('No')
        sub_two_markup.add(item7, item8)
        msg = bot.reply_to(msg, text="Is the ip correct?", reply_markup=sub_two_markup)
    except ldap.LDAPError:
        connect.unbind_s()
        msg = bot.send_message(message, "authentication error as admin")


bot = telebot.TeleBot('bot_token')
# Start bot


@bot.message_handler(commands=['start'])
def admin(message):
    msg = bot.send_message(message.chat.id, "Hello")  # add username like "hello Mahdis"
    message = bot.send_message(message.chat.id, "please enter your username")
    bot.register_next_step_handler(message, username_admin)


def username_admin(message):
    load_db_password()
    username = message.text
    update_username(username, message)
    msg = bot.send_message(message.chat.id, "please enter your password")
    bot.register_next_step_handler(msg, password_admin)


def password_admin(msg):
    password = msg.text
    update_password(password, msg.from_user.id)
    select_password_admin(msg.from_user.id)



bot.polling()
