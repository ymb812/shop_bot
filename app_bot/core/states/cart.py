from aiogram.fsm.state import State, StatesGroup


class CartStateGroup(StatesGroup):
    products = State()
    product_interaction = State()
    input_fio = State()
    input_phone = State()
    input_address = State()
    confirm = State()

