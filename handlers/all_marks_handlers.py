from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from database import database

router = Router()


@router.message(Command("marks"))
async def all_marks(message: Message):
    user_id = message.from_user.id
    marks = await database.get_all_marks(user_id)
    text = ""
    for i in marks:
        text += f"{i["subject"]}\n"
        text += f"{" ".join(i["str_marks"])}\n"
        text += f"Средняя: {i["average"]}\n"
        text += "\n"
    await message.answer(text)


@router.callback_query(F.data == "all_marks")
async def enter_name_by_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    marks = await database.get_all_marks(user_id)
    text = ""
    for i in marks:
        text += f"{i["subject"]}\n"
        text += f"{" ".join(i["str_marks"])}\n"
        text += f"Средняя: {i["average"]}\n"
        text += "\n"
    await callback.message.answer(text)
    await callback.answer()
