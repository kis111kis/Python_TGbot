from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data.data_base import db_session
from data.data_base.users import User
from middlewares.add_update_user import add_update_User
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await add_update_User(message)
    await message.answer(f"""Привет, {message.from_user.full_name}!
/help - список команд""", reply_markup=types.ReplyKeyboardRemove())
