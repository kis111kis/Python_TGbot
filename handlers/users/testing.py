from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from loader import dp
from states.test import Test


@dp.message_handler(Command('test'), state=None)
async def enter_test(message: types.Message):
    await message.answer('Вопрос 1')

    await Test.Q1.set()


@dp.message_handler(state=Test.Q1)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    try:
        int(answer)
        await state.update_data(answer1=answer)

        await message.answer('Вопрос 2')
        await Test.next()
    except Exception:
        await message.answer('Вопрос 1')
        await Test.Q1.set()


@dp.message_handler(state=Test.Q2)
async def answer_q2(message: types.Message, state: FSMContext):
    answer2 = message.text
    data = await state.get_data()
    answer1 = data.get('answer1')
    print(answer1)
    print(answer2)

    await message.answer('Спасибо за ответ')

    await state.finish()
