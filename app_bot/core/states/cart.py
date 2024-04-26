from aiogram.fsm.state import State, StatesGroup


class CartStateGroup(StatesGroup):
    products = State()
    product_interaction = State()
    input_fio = State()
    input_phone = State()

    input_city = State()
    input_street = State()
    input_house = State()
    input_index = State()
    input_entrance = State()
    input_floor = State()
    input_flat = State()

    confirm = State()
