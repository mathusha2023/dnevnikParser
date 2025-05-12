import json
import requests as r
from bs4 import BeautifulSoup
import sys


def parse_week_marks():
    url = "https://dnevnik.admin-smolensk.ru/journal-app/week.0"

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

    columns = parsed_html.find_all("div", class_="dnevnik-day")
    if columns:
        for day in columns:
            title = day.find("div", class_="dnevnik-day__title").text.strip()
            print(title)
            lessons = day.find_all("div", class_="dnevnik-lesson")
            for lesson in lessons:
                number = lesson.find("div", class_="dnevnik-lesson__number").text.strip()
                subject = lesson.find("span", class_="js-rt_licey-dnevnik-subject").text.strip()
                task = lesson.find("div", class_="dnevnik-lesson__task")
                if task is None:
                    str_task = "Без задания"
                else:
                    children = task.children
                    for i in range(2):
                        children.__next__()
                    str_task = children.__next__().text.strip()

                mark = lesson.find("div", class_="dnevnik-mark")
                if mark is None:
                    str_mark = "-"
                else:
                    weight = mark.find("span", class_="dnevnik-mark__weight")
                    if weight:
                        str_weight = weight.text.strip()
                    else:
                        str_weight = ""
                    str_mark = f"{mark.text.strip()[0]}{str_weight}"
                print(number, subject, str_mark, str_task)
            print()
    else:
        print("Что то пошло не так (попробуйте удалить файл cookies.json или вручную пропишите куки в файле)")
