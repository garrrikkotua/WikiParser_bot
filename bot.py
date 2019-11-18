from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import wiki_parser as wp
from stats import Stats
from visual import Visual

"""
Data storage:
info is save in format:
texts + chat_id: texts parsed from wikipedia
model + chat_id: model trained in train.py (stored via pickle)
output + chat_id: text generated in generate.py
counter + chat_id: counter object to do stats (stored via pickle)
"""


myToken = 'your telegram bot token'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update, args):
    """Take url from user and depth of search"""
    if len(args) == 0:
        help(bot, update)
        return
    update.message.reply_text('This may take a while...')
    update.message.reply_text('I will tell you when I am ready')
    wp.prepare_to_generate(args[0], update.message.chat_id,
                           int(args[1]))
    st = Stats()
    st.make_counter(st, update.message.chat_id)
    update.message.reply_text('I am ready for further commands, sir!')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Hi, I am here to help you!')
    update.message.reply_text('To start, you should call'
                              ' start command with two args:')
    update.message.reply_text('Url to wiki and depth of search')
    update.message.reply_text('Bot only works with English wiki for now!')




def write_n(bot, update, args):
    wp.generate_text(int(args[0]), update.message.chat_id)
    output = 'output{}.txt'.format(update.message.chat_id)
    with open(output, 'r', encoding='utf-8') as file:
        update.message.reply_text(''.join(file.readlines()))


def top(bot, update, args):
    st = Stats()
    c = st.get_counter(st, update.message.chat_id)
    words = st.top(st, c, int(args[0]),
                   args[1])
    text = ''
    for i, item in enumerate(words):
        a, b = item
        text += '{}. {} {}\n'.format(i, a, b)
    update.message.reply_text(text)


def stop_words(bot, update):
    st = Stats()
    c = st.get_counter(st, update.message.chat_id)
    text = ''
    for i, item in enumerate(st.stop_words(st, c)):
        text += '{}. {}\n'.format(i, item)
    update.message.reply_text(text)


def cloud(bot, update, args):
    st = Stats()
    c = st.get_counter(st, update.message.chat_id)
    c = st.delete_stops(st, c)
    vs = Visual()
    image = vs.cloud(vs, dict(c), args[0])
    bot.send_photo(update.message.chat_id, photo=image)


def describe(bot, update, args):
    if len(args) == 0:
        describe_all(bot, update)
    else:
        describe_word(bot, update, args[0])


def describe_all(bot, update):
    st = Stats()
    c = st.get_counter(st, update.message.chat_id)
    vs = Visual()
    image1 = vs.word_dist(vs, c)
    bot.send_photo(update.message.chat_id, photo=image1)
    image2 = vs.word_lens(vs, c)
    bot.send_photo(update.message.chat_id, photo=image2)


def describe_word(bot, update, word):
    st = Stats()
    c = st.get_counter(st, update.message.chat_id)
    vs = Visual()
    image1 = vs.word_rank(vs, c, word)
    bot.send_photo(update.message.chat_id, photo=image1)
    text = 'Most common words after {}\n'.format(word)
    words_n = st.words_near(st, update.message.chat_id, word)
    for i, item in enumerate(words_n):
        a, b = item
        text += '{}. {} {}\n'.format(i, a, b)
    update.message.reply_text(text)
    d = st.dist_by_sentence(st, update.message.chat_id, word)
    image2 = vs.dist_by_sentence(vs, d, word)
    bot.send_photo(update.message.chat_id, photo=image2)


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    updater = Updater(token=myToken)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start, pass_args=True))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler('write', write_n, pass_args=True))
    dp.add_handler(CommandHandler('top', top, pass_args=True))
    dp.add_handler(CommandHandler('stopwords', stop_words))
    dp.add_handler(CommandHandler('wordcloud', cloud, pass_args=True))
    dp.add_handler(CommandHandler('describe', describe, pass_args=True))

    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
