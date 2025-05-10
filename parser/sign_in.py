import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import asyncio
from config import AUTH_URL
from database import database


class Auth:
    def __init__(self, user_id):
        options = Options()
        # options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        self.user_id = user_id

    async def first_step_sign_in(self, login, password):
        self.driver.get(AUTH_URL)

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "login")))
        login_field = self.driver.find_element(By.ID, "login")
        login_field.clear()
        login_field.send_keys(login)

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "password")))
        password_field = self.driver.find_element(By.ID, "password")
        password_field.clear()
        password_field.send_keys(password)

        continue_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Войти')]")
        continue_btn.click()

        WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "empty")))


    async def second_step_sign_in(self, code: str):
        buttons = self.driver.find_elements(By.TAG_NAME, "input")
        if not code.isdigit():
            return False
        if len(buttons) != len(code):
            return False

        for button, char in zip(buttons, code):
            button.send_keys(char)

        await asyncio.sleep(2)
        if self.driver.find_elements(By.CLASS_NAME, "empty"):
            return False

        await asyncio.sleep(20)
        full_cookies = self.driver.get_cookies()
        cookies = {x["name"]: x["value"] for x in full_cookies}

        database.write_cookies(self.user_id, cookies)

        logging.info("Авторизация прошла успешно!")
        return True

    async def close(self):
        self.driver.quit()
