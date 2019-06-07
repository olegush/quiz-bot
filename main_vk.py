import os
import random
from functools import partial

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from redis import Redis

from quiz_tools import get_question_and_answer, format_answer, format_question


def main(token_vk, rediser):
    vk_session = vk_api.VkApi(token=token_vk)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_id = event.user_id
            user_text = event.text
            if user_text in ['Старт']:
                do_reply(
                    vk,
                    user_id,
                    'Привет знатоку в чате-викторине! Начинаем?',
                    ['Да!'])
            elif user_text in ['Да!', 'Новый вопрос', 'Другой вопрос']:
                handle_new_question(vk, user_id, rediser)
            elif user_text in ['Показать ответ']:
                display_answer(vk, user_id, rediser)
            elif user_text in ['Выход']:
                do_exit(vk, user_id)
            else:
                handle_attempt(vk, user_id, user_text, rediser)


def do_reply(vk, user_id, text, buttons=None):
    if buttons is None:
        reply_keyboard = None
    else:
        keyboard = VkKeyboard(one_time=True)
        for button in buttons:
            keyboard.add_button(button, color=VkKeyboardColor.DEFAULT)
        reply_keyboard = keyboard.get_keyboard()
    vk.messages.send(
        user_id=user_id,
        message=text,
        random_id=random.randint(1,1000),
        keyboard=reply_keyboard,
    )


def handle_new_question(vk, user_id, rediser):
    new_question, new_answer = get_question_and_answer()
    rediser.set(user_id, new_answer)
    do_reply(vk, user_id, format_question(new_question))


def handle_attempt(vk, user_id, user_text, rediser):
    attempt = user_text.strip().lower()
    answer = rediser.get(user_id).decode()
    if attempt == format_answer(answer):
        text = 'Правильно! \n\n {}'.format(answer)
        buttons = ['Новый вопрос', 'Выход']
    else:
        text = 'Неверно! Попробуйте еще раз.'
        buttons = ['Показать ответ', 'Другой вопрос', 'Выход']
    do_reply(vk, user_id, text, buttons)


def display_answer(vk, user_id, rediser):
    answer = rediser.get(user_id).decode()
    do_reply(vk, user_id, answer, ['Новый вопрос', 'Выход'])


def do_exit(vk, user_id):
    do_reply(
        vk,
        user_id,
        'До скорой встречи! Чтобы начать заново, нажмите "Старт"',
        ['Старт'])


if __name__ == '__main__':
    token_vk = os.environ['TOKEN_VK']
    rediser = Redis(
                host=os.environ['REDIS_HOST'],
                port=os.environ['REDIS_PORT'],
                db=0,
                password=os.environ['REDIS_PWD'])
    main(token_vk, rediser)
