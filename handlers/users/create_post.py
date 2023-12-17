import datetime
import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, ReplyKeyboardRemove

from data.data_base import db_session
from data.data_base.posts import Post
from keyboards.inline.aiogramcalendar import create_calendar, calendar_callback, process_calendar_selection
from loader import dp
from states.create_post import Create_Post

keyboard_1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_1.add(
    types.KeyboardButton(text="Завершить заполнение поста"))

keyboard_2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_2.add(types.KeyboardButton(text='Отправить сейчас'))
keyboard_2.add(types.KeyboardButton(text='Выбрать дату и время для отпраления'))

keyboard_3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_3.add(types.KeyboardButton(text='С помощью анимированного календаря'))
keyboard_3.add(types.KeyboardButton(text='Ввести дату вручную'))


@dp.message_handler(Command('create_post'), state=None)
async def start_creating_post(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['year'] = datetime.datetime.now().year
        data['month'] = datetime.datetime.now().month
        data['day'] = datetime.datetime.now().day
        data['hour'] = datetime.datetime.now().hour
        data['minute'] = datetime.datetime.now().minute
        data['content'] = []
        data['theme'] = ''
        data['created_by'] = ''
    await message.answer('Когда вы хотите сделать расслыку?', reply_markup=keyboard_2)
    await Create_Post.Choose_Method_Of_Input_Date_1.set()


@dp.message_handler(state=Create_Post.Choose_Method_Of_Input_Date_1)
async def select_dispatch_date(message: types.Message, state: FSMContext):
    if message.text == 'Отправить сейчас':
        async with state.proxy() as data:
            data['year'] = datetime.datetime.now().year
            data['month'] = datetime.datetime.now().month
            data['day'] = datetime.datetime.now().day
            data['hour'] = datetime.datetime.now().hour
            data['minute'] = datetime.datetime.now().minute

        await message.answer('''Теперь введите информацию для рассылки
(Здесь вы можете отправлять картинки и текст)''',
                             reply_markup=keyboard_1)
        await Create_Post.Information.set()
        return

    elif message.text == 'Выбрать дату и время для отпраления':
        await message.answer('Как именно вы хотите ввести дату?', reply_markup=keyboard_3)
        await Create_Post.Choose_Method_Of_Input_Date_2.set()
    else:
        await message.answer('Что-то пошло не так, выберите заново', reply_markup=keyboard_2)
        await Create_Post.Choose_Method_Of_Input_Date_1.set()


@dp.message_handler(state=Create_Post.Choose_Method_Of_Input_Date_2)
async def choose_method_of_input_date(message: types.Message, state: FSMContext):
    if message.text == 'С помощью анимированного календаря':
        await message.answer('Выберите дату', reply_markup=create_calendar())
        await Create_Post.Calendar.set()
    elif message.text == 'Ввести дату вручную':
        await message.answer('Введите дату в формате DD.MM.YYYY (год не является обязательным параметром')
        await Create_Post.Enter_Date.set()
    else:
        await message.answer('Что-то пошло не так, выберите заново', reply_markup=keyboard_3)
        await Create_Post.Choose_Method_Of_Input_Date_2.set()


@dp.message_handler(state=Create_Post.Enter_Date)
async def input_date(message: types.Message, state: FSMContext):
    content = message.text.replace(':', ' ').replace(';', ' ').replace('.', ' ').split(' ')
    try:
        if len(content) == 2:
            if datetime.datetime(datetime.datetime.now().year, int(content[1]), int(content[0])) >= datetime.datetime(
                    datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day):
                async with state.proxy() as data:
                    data['year'] = datetime.datetime.now().year
                    data['month'] = int(content[1])
                    data['day'] = int(content[0])
                await message.answer('Введите время для публикации в формате HH:MM')
                await Create_Post.Time.set()
                return

            else:
                await message.answer('Вы ввели дату ранеше текущей, введите снова')
                await Create_Post.Enter_Date.set()
                return
        elif len(content) == 3:
            if len(content[2]) == 2:
                content[2] = '20' + content[2]
            if datetime.datetime(int(content[2]), int(content[1]), int(content[0])) >= datetime.datetime(
                    datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day):
                async with state.proxy() as data:
                    data['year'] = int(content[2])
                    data['month'] = int(content[1])
                    data['day'] = int(content[0])
                    await message.answer('Введите время для публикации в формате HH:MM')
                    await Create_Post.Time.set()
                    return
            else:
                await message.answer('Вы ввели дату ранеше текущей, введите снова')
                await Create_Post.Enter_Date.set()
                return
        else:
            await message.answer('Вы ввели дату неправильно, введите снова')
            await Create_Post.Enter_Date.set()
            return
    except Exception:
        await message.answer('Вы что-то ввели неверно, введите еще раз')
        await Create_Post.Enter_Date.set()


@dp.callback_query_handler(calendar_callback.filter(),
                           state=Create_Post.Calendar)  # handler is processing only calendar_callback queries
async def select_data_with_calendar(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await process_calendar_selection(callback_query, callback_data)
    if selected:
        now = datetime.datetime.now()
        if int(datetime.datetime.toordinal(date)) < int(datetime.datetime.toordinal(datetime.datetime.now())):
            await callback_query.message.answer('Вы выбрали неверную дату',
                                                reply_markup=create_calendar(now.year, now.month))
        else:
            await callback_query.message.answer(f'Вы выбрали {date.strftime("%d/%m/%Y")}',
                                                reply_markup=ReplyKeyboardRemove())
            day, month, year = map(int, date.strftime("%d/%m/%Y").split('/'))
            async with state.proxy() as data:
                data['year'] = year
                data['month'] = month
                data['day'] = day
                print(data)
            await callback_query.message.answer('Введите время для публикации в формате HH:MM')
            await Create_Post.Time.set()


@dp.message_handler(state=Create_Post.Time)
async def select_date(message: types.Message, state: FSMContext):
    answer = message.text
    try:
        hour, minute = map(int, answer.replace(':', ' ').replace(';', ' ').replace('.', ' ').split(' '))
        data = await state.get_data()
        print(data, 'state')
        year, month, day = data['year'], data['month'], data['day']
        print(year, month, day, hour, minute)
        print(datetime.datetime(year, month, day, hour, minute))
        if datetime.datetime(year, month, day, hour, minute) >= datetime.datetime.now():
            async with state.proxy() as data:
                data['hour'] = hour
                data['minute'] = minute
            await message.answer('Дата и время установлены\nВведите краткую тему поста')
            await Create_Post.Theme.set()
        else:
            await message.answer('Вы пытаетесь задать дату ранее настоящей, введите время заново')
            await Create_Post.Time.set()
    except Exception as e:
        await message.answer('Вы ввели дату в неверном формате')

        await Create_Post.Time.set()

    print(answer)


@dp.message_handler(state=Create_Post.Theme)
async def input_theme(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['theme'] = message.text
        data['created_by'] = message.from_user.full_name + ' ' + str(message.from_user.id)
    await message.answer('Теперь введите информацию для рассылки\n(Здесь вы можете отправить картинки и текст)',
                         reply_markup=keyboard_1)

    await Create_Post.Information.set()


@dp.message_handler(state=Create_Post.Information, content_types=["text", "photo"])
async def enter_information(message: types.Message, state: FSMContext):
    if message.content_type == 'text' and message.text == 'Завершить заполнение поста':
        await message.answer('Заполнение завершено', reply_markup=types.ReplyKeyboardRemove())
        async with state.proxy() as data:
            print(data)
            session = db_session.create_session()
            for i in data['content']:
                if i[0] == 'text':
                    await message.answer(i[1])
                elif i[0] == 'photo':
                    img = open(i[1], 'rb')
                    await message.answer_photo(photo=img, caption=i[2])
            await message.answer(
                'Этот пост будет отправлен\n' + str(
                    datetime.datetime(data['year'], data['month'], data['day'], data['hour'],
                                      data['minute'])))
            post = Post()
            post.year = data['year']
            post.month = data['month']
            post.day = data['day']
            post.hour = data['hour']
            post.minute = data['minute']
            post.theme = data['theme']
            post.created_by = data['created_by']
            content = ''
            for i in data['content']:
                for j in i:
                    content += str(j)
                    content += '|'
                content += '|'
            print(content)
            post.content = content
            session.add(post)
            session.commit()
            print('post created')
        await state.finish()
        return

    # print(message.content_type)
    # print(message.photo)
    if message.content_type == 'text':
        async with state.proxy() as data:
            print(data)
            data['content'].append(['text', message.text])
            # await message.answer(data['content'][-1])
    else:
        # print(message.caption)
        photo = message.photo.pop()
        await photo.download()
        url = await photo.get_url()
        async with state.proxy() as data:
            print(data)
            data['content'].append(
                ['photo', 'photos/' + url.split('/')[-1], message.caption])

        # img = open(await photo.get_url(), 'rb')
        # await message.answer_photo(photo=img)
    print(await state.get_data())
    await Create_Post.Information.set()
