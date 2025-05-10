from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from selenium.common import TimeoutException
import parser.sign_in
from database import database
from states import LoginStates

router = Router()


@router.message(Command("auth"))
async def enter_name(message: Message, state: FSMContext):
    await message.answer("Введите ваш логин:")
    await state.set_state(LoginStates.enter_login)


@router.callback_query(F.data == "logout")
async def logout(callback: CallbackQuery):
    user_id = callback.from_user.id
    database.logout(user_id)
    await callback.message.answer("Успешно")
    await callback.answer()


@router.callback_query(F.data == "login")
async def enter_name_by_callback(callback: CallbackQuery, state: FSMContext):
    await enter_name(callback.message, state)
    await callback.answer()


@router.message(LoginStates.enter_login, F.text)
async def enter_password(message: Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.answer("Введите ваш пароль:")
    await state.set_state(LoginStates.enter_password)


@router.message(LoginStates.enter_password, F.text)
async def first_step_sign_in(message: Message, state: FSMContext):
    data = await state.get_data()
    login = data["login"]
    password = message.text
    auth = parser.sign_in.Auth(message.from_user.id)
    try:
        await auth.first_step_sign_in(login, password)
        await message.answer("Пришлите код из СМС: ")
        await state.update_data(auth=auth)
        await state.set_state(LoginStates.enter_code)
    except TimeoutException:
        await message.answer("Введены неверные данные! Попробуйте снова с помощью команды /auth")
        await state.clear()
        await auth.close()


@router.message(LoginStates.enter_code, F.text)
async def second_step_sign_in(message: Message, state: FSMContext):
    data = await state.get_data()
    auth = data["auth"]
    code = message.text
    await message.answer("Подождите немного, идет авторизация...")
    auth_result = await auth.second_step_sign_in(code)
    if not auth_result:
        await message.answer("Неверный код! Попробуйте снова:")
        return
    await message.answer("Успешно")
    await auth.close()
    await state.clear()
