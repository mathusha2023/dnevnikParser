import os
from all_marks_parser import parse_all_marks
from sign_in import sign_in
from week_parser import parse_week_marks
from bad_subjects_parser import parse_bad_subjects


def main():
    if not os.path.exists("cookies.json"):
        login = input("Введите ваш логин: ")
        password = input("Введите ваш пароль: ")
        get_code_callback = lambda: input("Введите код из СМС: ")

        sign_in(login, password, get_code_callback)

    mode = input("""Какие данные вы хотите получить?
1 - Получить все оценки
2 - Получить все данные за текущую неделю
3 - Получить предметы, по которым нужно подтянуть оценку
Ваш выбор: """)

    while mode not in ("1", "2", "3"):
        mode = input("""Нет такого варианта!
1 - Получить все оценки
2 - Получить все данные за текущую неделю
3 - Получить предметы, по которым нужно подтянуть оценку
Ваш выбор:    """)

    print("\n\n\n")
    if mode == "1":
        parse_all_marks()
    elif mode == "2":
        parse_week_marks()
    elif mode == "3":
        parse_bad_subjects()
    input("Нажмите Enter для продолжения...")


if __name__ == "__main__":
    while True:
        main()

