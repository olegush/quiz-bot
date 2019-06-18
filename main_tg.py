import os
import logging
import logging.config
from functools import partial
from dotenv import load_dotenv
from telegram import Bot, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          RegexHandler, ConversationHandler, Filters)
from redis import Redis

from tg_logging import create_logger
from quiz_tools import get_question_and_answer, format_answer, format_question


QUESTION, ATTEMPT = range(2)


def main():
    class LoggerTelegramBot(logging.Handler):
        def emit(self, record):
            log_entry = self.format(record)
            bot.send_message(chat_id=chat_id_tg_admin, text=log_entry)

    dictLogConfig = {
        'version': 1,
        'handlers': {
            'handler': {
                '()': LoggerTelegramBot,
                'formatter': 'formatter'
                }
        },
        'loggers': {
            'tg_logger': {
                'handlers': ['handler'],
                'level': 'INFO'
            }
        },
        'formatters': {
            'formatter': {
                'format': '%(asctime)s - %(levelname)s - %(message)s'
            }
        }
    }

    load_dotenv()
    chat_id_tg_admin = os.getenv('CHAT_ID_TG_ADMIN')
    bot = Bot(token=os.getenv('TOKEN_TG'))
    logging.config.dictConfig(dictLogConfig)
    logger = logging.getLogger('tg_logger')
    handler = LoggerTelegramBot()
    logger.addHandler(handler)
    rediser = Redis(
                host=os.getenv('REDIS_HOST'),
                port=os.getenv('REDIS_PORT'),
                db=0,
                password=os.getenv('REDIS_PWD'))
    updater = Updater(token_tg)
    dp = updater.dispatcher
    logger.info(dp)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            QUESTION: [
                RegexHandler('^Выход$', do_exit),
                MessageHandler(Filters.text, partial(handle_new_question, rediser))],
            ATTEMPT: [
                RegexHandler('^Выход$', do_exit),
                RegexHandler('^(Новый вопрос|Другой вопрос)$', partial(handle_new_question, rediser)),
                RegexHandler('^Показать ответ$', partial(display_answer, rediser)),
                MessageHandler(Filters.text, partial(handle_attempt, rediser))],
        },
        fallbacks=[CommandHandler('cancel', do_exit)]
    )
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


def do_reply(update, text, keyboard=None):
    if keyboard is None:
        markup = ReplyKeyboardRemove()
        return update.message.reply_text(text, reply_markup=markup)
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return update.message.reply_text(text, reply_markup=markup)


def start(bot, update):
    do_reply(update, 'Привет знатоку в чате-викторине! Начинаем?', [['Да!']])
    return QUESTION


def handle_new_question(rediser, bot, update):
    new_question, new_answer = get_question_and_answer()
    chat_id = update.message.chat_id
    rediser.set(chat_id, new_answer)
    do_reply(update, format_question(new_question))
    return ATTEMPT


def display_answer(rediser, bot, update):
    chat_id = update.message.chat_id
    answer = rediser.get(chat_id).decode()
    do_reply(update, answer, [['Новый вопрос', 'Выход']])
    return QUESTION


def handle_attempt(rediser, bot, update):
    chat_id = update.message.chat_id
    attempt = update.message.text.strip().lower()
    answer = rediser.get(chat_id).decode()
    if attempt == format_answer(answer):
        text = 'Правильно! \n\n {}'.format(answer)
        reply_keyboard = [['Новый вопрос', 'Выход']]
    else:
        text = 'Неверно! Попробуйте еще раз.'
        reply_keyboard = [['Показать ответ', 'Другой вопрос', 'Выход']]
    do_reply(update, text, reply_keyboard)
    return ATTEMPT


def do_exit(bot, update):
    text = 'До скорой встречи! Желаете начать заново? Жмите /start'
    do_reply(update, text)
    return ConversationHandler.END


if __name__ == '__main__':
    main()
