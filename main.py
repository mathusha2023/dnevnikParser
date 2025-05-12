import os

from all_marks_parser import parse_all_marks
from sign_in import sign_in
from week_parser import parse_week_marks

if not os.path.exists("cookies.json"):
    login = input("Введите ваш логин: ")
    password = input("Введите ваш пароль: ")
    get_code_callback = lambda: input("Введите код из СМС: ")

    sign_in(login, password, get_code_callback)

mode = input("""Какие данные вы хотите получить?
1 - Получить все оценки
2 - Получить все данные за текущую неделю
Ваш выбор: """)

while mode not in ("1", "2"):
    mode = input("""Нет такого варианта!
1 - Получить все оценки
2 - Получить все данные за текущую неделю
Ваш выбор:    """)

print("\n\n\n")
if mode == "1":
    parse_all_marks()
elif mode == "2":
    parse_week_marks()
input()
