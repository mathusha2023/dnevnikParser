import json
import requests as r
from bs4 import BeautifulSoup
import sys

url = "https://dnevnik.admin-smolensk.ru/journal-student-grades-action"

headers = {"Content-Type": "application/octet-stream",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"}

with open("cookies.json") as file:
    cookies = json.load(file)

resp = r.get(url, headers=headers, cookies=cookies)
status_code = resp.status_code
if status_code != 200:
    print(f"Error: {status_code=}")
    sys.exit()

parsed_html = BeautifulSoup(resp.content, "html.parser")
print(parsed_html)
