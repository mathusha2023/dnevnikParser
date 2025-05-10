import requests as r
from bs4 import BeautifulSoup
from config import ALL_MARKS_URL, HEADERS


async def parse_all_marks(cookies):
    resp = r.get(ALL_MARKS_URL, headers=HEADERS, cookies=cookies)
    status_code = resp.status_code
    if status_code != 200:
        return None

    parsed_html = BeautifulSoup(resp.content, "html.parser")

    # получаем названия всех предметов
    subjects = list(map(lambda x: x.text.strip(), parsed_html.find_all("div", class_="text-overflow lhCell offset16")))

    res = []

    for subject in subjects:
        d = {"subject": subject}
        str_marks_list = []
        int_marks_list = []
        marks_html = parsed_html.find_all("div", attrs={"name": subject})[1:]  # первый элемент это название предмета, нам нужны только сами оценки
        for mark in marks_html:
            mark = mark.text.strip().replace("\n", "").split(" ")[0]  # получаем непосредственно оценку (в т.ч. 4✕3) или Н
            if mark and mark != "Н":
                str_marks_list.append(mark.replace("✕", "×"))
                if len(mark) == 1:
                    int_marks_list.append(int(mark))
                else:
                    int_marks_list.extend([int(mark[0])] * int(mark[2]))
        d["str_marks"] = str_marks_list
        d["int_marks"] = int_marks_list
        length = len(int_marks_list)
        if length:
            d["average"] = round(sum(int_marks_list) / length, 2)
        else:
            d["average"] = 0.
        d["count"] = length

        res.append(d)
    return res
