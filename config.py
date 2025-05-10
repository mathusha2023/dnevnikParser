import os
from dotenv import load_dotenv

load_dotenv(".env")

BOT_TOKEN = os.getenv("BOT_TOKEN")
AUTH_URL = "https://dnevnik.admin-smolensk.ru/journal-esia-action/"
ALL_MARKS_URL = "https://dnevnik.admin-smolensk.ru/journal-student-grades-action?mode=print"
WEEK_DATA_URL = lambda x: f"https://dnevnik.admin-smolensk.ru/journal-app/week.{x}"
DATABASE_FILE = "data.json"
HEADERS = {
    "Content-Type": "application/octet-stream",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
}
