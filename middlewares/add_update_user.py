from data.data_base import db_session
from data.data_base.users import User


async def add_update_User(message):
    session = db_session.create_session()
    if not session.query(User).filter(User.telegram_id == message.from_user.id).first():
        user = User()
        user.telegram_id = message.from_user.id
        user.first_name = message.from_user.first_name
        user.last_name = message.from_user.last_name
        session.add(user)
        session.commit()
    else:
        user = session.query(User).filter(User.telegram_id == message.from_user.id).first()
        user.last_name = message.from_user.last_name
        user.first_name = message.from_user.first_name
        session.commit()
