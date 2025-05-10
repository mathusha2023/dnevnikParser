from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time
import json

def sign_in(login, password, get_code_callback):

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    driver.get("https://dnevnik.admin-smolensk.ru/journal-esia-action/")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "login")))
    login_field = driver.find_element(By.ID, "login")
    login_field.clear()
    login_field.send_keys(login)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password")))
    password_field = driver.find_element(By.ID, "password")
    password_field.clear()
    password_field.send_keys(password)

    continue_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Войти')]")
    continue_btn.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "empty")))

    buttons = driver.find_elements(By.TAG_NAME, "input")
    code = get_code_callback()

    for button, char in zip(buttons, code):
        button.send_keys(char)

    time.sleep(20)
    full_cookies = driver.get_cookies()
    cookies = {x["name"]: x["value"] for x in full_cookies}

    with open("cookies.json", "w") as file:
        json.dump(cookies, file)

    print("Авторизация прошла успешно!")
    driver.quit()
