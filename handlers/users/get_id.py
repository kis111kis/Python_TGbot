from aiogram import types

from loader import dp
from aiogram.dispatcher.filters import Command


@dp.message_handler(Command('get_id'))
async def get_id(message: types.Message):
    await message.answer('Ваш id: ' + str(message.from_user.id), reply_markup=types.ReplyKeyboardRemove())
