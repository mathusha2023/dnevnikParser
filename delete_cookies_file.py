import os


def delete_cookies_file():
    if not os.path.exists("cookies.json"):
        print("Файл cookies.json не существует!")
        return
    os.remove("cookies.json")
    print("Файл cookies.json успешно удален!")
