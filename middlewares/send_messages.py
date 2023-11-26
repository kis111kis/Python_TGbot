import asyncio
import datetime

from data.data_base import db_session
from data.data_base.posts import Post
from data.data_base.users import User
from loader import bot


async def send_messages():
    session = db_session.create_session()
    for post in session.query(Post).all():
        if datetime.datetime(post.year, post.month, post.day, post.hour, post.minute) < datetime.datetime.now():
            data = post.content.split('||')
            content = []
            for i in data:
                content.append(i.split('|'))

            print(content)
            for user in session.query(User).filter(User.mailing == 1):
                print(user.telegram_id)
                try:
                    for i in content:
                        if i[0] == 'text':
                            await bot.send_message(user.telegram_id, i[1])
                        elif i[0] == 'photo':
                            img = open(i[1], 'rb')
                            await bot.send_photo(user.telegram_id, photo=img, caption=i[2] if i[2] != 'None' else '')
                    await asyncio.sleep(0.2)
                except Exception as e:
                    print(e)
            session.delete(post)
    session.commit()

    # print('messages')
