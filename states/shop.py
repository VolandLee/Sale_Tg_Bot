from aiogram.dispatcher.filters.state import StatesGroup, State


class Shop(StatesGroup):

    Menu = State()
    Check_Cat = State()
    Search = State()
    Find = State()
