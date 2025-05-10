from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database import database
from keyboards import login_keyboard, menu_keyboard

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    user_id = message.from_user.id
    user_first_name = message.from_user.first_name
    database.add_user_if_not_exists(user_id, user_first_name)
    if database.is_logged_in(user_id):
        text = f"Здравствуй, {user_first_name}!"
        await message.answer(text, reply_markup=menu_keyboard())
    else:
        text = f"Здравствуй, {user_first_name}! Чтобы пользоваться этим ботом, тебе необходимо войти в свой дневник через Госуслуги!"
        await message.answer(text, reply_markup=login_keyboard())

