import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from data.data_base import db_session
from data.data_base.posts import Post
from loader import dp
from aiogram.dispatcher.filters import Command

from states.delete_post import Delete_Post

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(types.KeyboardButton(text='Завершить удаление'))


@dp.message_handler(Command('delete_post'))
async def delete_post(message: types.Message, state: FSMContext):
    session = db_session.create_session()
    posts = []
    index = 1
    for post in session.query(Post).all():
        posts.append(
            str(index) + '. Тема : ' + post.theme + '\nДата: ' + str(
                datetime.datetime(post.year, post.month, post.day, post.hour,
                                  post.minute)) + '\nАвтор: ' + post.created_by)
        index += 1
    if len(posts) == 0:
        posts = ['Будущих постов для публикации нет']
    await message.answer('\n\n'.join(posts))
    if index > 1:
        await message.answer(
            'Введите номер поста для удаления( так же можно перечислить несколько постов через запятую ) ',
            reply_markup=keyboard)
        await Delete_Post.Delete.set()


@dp.message_handler(state=Delete_Post.Delete)
async def delete_post(message: types.Message, state: FSMContext):
    if message.text == 'Завершить удаление':
        await message.answer('Удаление отменено', reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
        return
    try:
        set(list(map(int, message.text.replace(',', ' ').replace('  ', ' ').split())))
    except Exception:
        await message.answer('Вы ввели что-то неправильно, введите заново', reply_markup=keyboard)
        await Delete_Post.Delete.set()
        return
    index = 1
    ls = set(list(map(int, message.text.replace(',', ' ').replace('  ', ' ').split())))
    session = db_session.create_session()
    for post in session.query(Post).all():
        if index in ls:
            session.delete(post)
            await message.answer(str(index) + '. Тема : ' + post.theme + '\nДата: ' + str(
                datetime.datetime(post.year, post.month, post.day, post.hour,
                                  post.minute)) + '\nУдален')
            ls.discard(index)
            index += 1
            session.commit()
            if len(ls) == 0:
                await message.answer('Все посты удалены', reply_markup=types.ReplyKeyboardRemove())
            await state.finish()
        return
    else:
        await message.answer('У меня не получилось удалить все посты', reply_markup=keyboard)
