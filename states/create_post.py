from aiogram.dispatcher.filters.state import StatesGroup, State


class Create_Post(StatesGroup):
    Start_Enter = State()
    Choose_Method_Of_Input_Date_1 = State()
    Choose_Method_Of_Input_Date_2 = State()

    Calendar = State()
    Enter_Date = State()
    Time = State()

    Theme = State()
    Information = State()
    Save_Information = State()
    Exit = State()
