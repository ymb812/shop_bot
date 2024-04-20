from aiogram.fsm.state import State, StatesGroup


class SupportStateGroup(StatesGroup):
    menu = State()
    input_phone = State()
