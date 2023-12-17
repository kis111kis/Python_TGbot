import asyncio
from aiogram import executor


async def f():
    await asyncio.sleep(0.1)
    print('hi')


asyncio.run(f())
