from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Моя успеваемость", callback_data="all_marks"))
    builder.row(InlineKeyboardButton(text="Выйти из аккаунта", callback_data="logout"))
    return builder.as_markup()
