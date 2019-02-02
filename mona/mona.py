from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import argparse
import random

reply_map = {
    "sony": ["大法好"],
    "启动": ["P5R天下第一"],
    "合理": ["reasonable"]
}


def hello(bot, update, args):
    try:
        word = args[0]
        reply = args[1]
        if word in reply_map:
            reply_map[word].append(reply)
        else:
            reply_map[word] = [reply]
        update.message.reply_text(
            "Set successful: {} -> {}".format(word, reply))
    except Exception:
        update.message.reply_text("Usage: /set <word> <reply>")


def message(bot, update):
    text = update.message.text
    for k, v in reply_map.items():
        if k in text:
            update.message.reply_text(random.choice(v))


def main():
    parser = argparse.ArgumentParser(description='Mona')
    parser.add_argument('--token', help="token of bot", required=True)
    args = parser.parse_args()

    updater = Updater(args.token)
    updater.dispatcher.add_handler(CommandHandler('set', hello, pass_args=True))
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text, message)
    )
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()