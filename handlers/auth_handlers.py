from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from states import LoginStates

router = Router()


@router.callback_query(F.data == "login")
async def enter_name(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите ваш логин:")
    await state.set_state(LoginStates.enter_login)
    await callback.answer()


@router.message(LoginStates.enter_login, F.text)
async def enter_name(message: Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.answer("Введите ваш пароль:")
    await state.set_state(LoginStates.enter_password)


@router.message(LoginStates.enter_password, F.text)
async def enter_name(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
