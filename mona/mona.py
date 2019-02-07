from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import argparse
import random
import re
import sqlite3


reply_map = {}
sqlite_path = None


def insert_reply_into_db(keyword, reply):
    conn = sqlite3.connect(sqlite_path)
    c = conn.cursor()
    c.execute("insert into replies (keyword, reply) values (?, ?)",
              (keyword, reply))
    conn.commit()
    conn.close()


def set_reply(bot, update, args):
    try:
        word = args[0]
        reply = args[1]
        if word in reply_map:
            reply_map[word].append(reply)
        else:
            reply_map[word] = [reply]
        insert_reply_into_db(word, reply)
        update.message.reply_text(
            "Set successful: {} -> {}".format(word, reply))
    except Exception:
        update.message.reply_text("Usage: /set <word> <reply>")


def message(bot, update):
    text = update.message.text
    # reply with regular expression
    try:
        result = re.findall(r'(\w+)还是不\1', text)
        if result:
            message = random.choice(["不", ""]) + result[0]
            update.message.reply_text(message)
            return
    except Exception:
        pass
    # reply with predefined word
    for k, v in reply_map.items():
        if k in text:
            update.message.reply_text(random.choice(v))


def init_db():
    conn = sqlite3.connect(sqlite_path)
    c = conn.cursor()
    c.execute("select keyword, reply from replies")
    for keyword, reply in c.fetchall():
        if keyword in reply_map:
            reply_map[keyword].append(reply)
        else:
            reply_map[keyword] = [reply]
    conn.close()


def main():
    parser = argparse.ArgumentParser(description='Mona')
    parser.add_argument('--token', help="token of bot", required=True)
    parser.add_argument("--db", help="path to sqlite", required=True)
    args = parser.parse_args()

    global sqlite_path
    sqlite_path = args.db
    init_db()

    updater = Updater(args.token)
    updater.dispatcher.add_handler(
        CommandHandler('set', set_reply, pass_args=True))
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text, message)
    )
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
