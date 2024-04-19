from aiogram.fsm.state import State, StatesGroup


class SupportStateGroup(StatesGroup):
    menu = State()
    manager = State()
    input_phone = State()
