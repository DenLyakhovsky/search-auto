from aiogram.fsm.state import StatesGroup, State


class Search(StatesGroup):
    start = State()
    search = State()
    stop_search = State()
