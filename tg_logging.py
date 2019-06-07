import logging

def create_logger(bot, chat_id):
    """ Sends formatted logs to Telegram Bot."""

    class LoggerTelegramBot(logging.Handler):
        def emit(self, record):
            log_entry = self.format(record)
            bot.send_message(
                chat_id=chat_id,
                text=log_entry,
                parse_mode='HTML',
                disable_web_page_preview=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    handler = LoggerTelegramBot()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
