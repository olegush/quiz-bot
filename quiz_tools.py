import os
import re
import random

PATH_TO_QUESTIONS_DIR = 'quiz-questions'

def format_answer(answer):
    prog = re.compile("""
                        \w+:\n|             # Ответ:\n
                        [\s]|               # Пробелы
                        (?=\()(.+)(?<=\))|  # Круглые скобки
                        (?=\[)(.+)(?<=\])|  # Квадратные скобки
                        [\"]|               # Кавычки
                        [.]                 # Точки
                        """, re.VERBOSE)
    answer = prog.sub(' ', answer)
    return re.sub(r'[ ]{2,}',' ', answer).strip().lower()


def format_question(question):
    prog = re.compile("""
                        ^.+:\n|             # Вопрос :\n
                        [\s]                # Пробелы
                        """, re.VERBOSE)
    question = prog.sub(' ', question)
    return re.sub(r'[ ]{2,}',' ', question).strip()


def get_question_and_answer():
    file_name = random.choice(os.listdir(PATH_TO_QUESTIONS_DIR))
    file_path = os.path.join(PATH_TO_QUESTIONS_DIR, file_name)
    with open(file_path, encoding='KOI8-R') as file:
        content = file.read()
        sections = content.split('\n\n')
    try:
        answers = [section for section in sections if section.find('Ответ') == 0]
        questions = [section for section in sections if section.find('Вопрос') == 0]
    except (TypeError, ValueError):
        pass
    pairs = list(zip(questions, answers))
    while True:
        rand_num = random.randint(0, len(pairs) - 1)
        pair = pairs[rand_num]
        prog = re.compile("""
                            \(pic.+\)  # Картинка в вопросе
                          """, re.VERBOSE)
        if prog.search(pair[0]):
            continue
        return pair
