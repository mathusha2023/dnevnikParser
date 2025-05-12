import json
import requests as r
from bs4 import BeautifulSoup
import sys


def parse_all_marks():
    url = "https://dnevnik.admin-smolensk.ru/journal-student-grades-action?mode=print"

    headers = {"Content-Type": "application/octet-stream",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"}

    try:
        with open("cookies.json") as file:
            cookies = json.load(file)
    except FileNotFoundError:
        print("Что то пошло не так (попробуйте удалить файл cookies.json или вручную пропишите куки в файле)")
        sys.exit()

    resp = r.get(url, headers=headers, cookies=cookies)
    status_code = resp.status_code
    if status_code != 200:
        print(f"Error: {status_code=}")
        sys.exit()

    parsed_html = BeautifulSoup(resp.content, "html.parser")

    # получаем названия всех предметов
    subjects = list(map(lambda x: x.text.strip(), parsed_html.find_all("div", class_="text-overflow lhCell offset16")))

    d = {}

    for subject in subjects:
        marks_list = []
        marks_html = parsed_html.find_all("div", attrs={"name": subject})[1:]  # первый элемент это название предмета, нам нужны только сами оценки
        for mark in marks_html:
            mark = mark.text.strip().replace("\n", "").split(" ")[0]  # получаем непосредственно оценку (в т.ч. 4✕3) или Н
            if mark and mark != "Н":
                marks_list.append(mark)
        d[subject] = marks_list

    for sub in d:
        marks = d[sub]
        summa = 0
        count = 0
        for str_mark in marks:
            if len(str_mark) == 1:
                summa += int(str_mark)
                count += 1
            else:
                m = int(str_mark[0])
                k = int(str_mark[2])
                summa += m * k
                count += k

        print(sub)
        print(*marks)
        if count:
            print(f"Средняя: {round(summa / count, 2)}")
        print()
