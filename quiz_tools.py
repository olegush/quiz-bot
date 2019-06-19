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
    questions = [section for section in sections if section.find('Вопрос') == 0]
    answers = [section for section in sections if section.find('Ответ') == 0]
    pairs = list(zip(questions, answers))
    # Check if pair list is empty
    try:
        prog = re.compile("""
                            \(pic.+\)  # Картинка в вопросе
                          """, re.VERBOSE)
        pairs = [(question, answer)
                for (question, answer) in pairs
                if prog.search(question) is None]
        return random.choice(pairs)
    except IndexError:
        pass
