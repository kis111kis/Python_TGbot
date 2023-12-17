import logging

from aiogram import Dispatcher

from data.config import ADMINS, MAIN_ADMINS


async def on_startup_notify(dp: Dispatcher):
    print(ADMINS, MAIN_ADMINS)
    # for admin in ADMINS:
    #     try:
    #         await dp.bot.send_message(admin, "Бот Запущен")
    #
    #     except Exception as err:
    #         logging.exception(err)
    for admin in MAIN_ADMINS:
        if admin != '':
            try:
                await dp.bot.send_message(admin, "Бот Запущен")
            except Exception as err:
                logging.exception(err)
