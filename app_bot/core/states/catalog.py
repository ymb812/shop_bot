from aiogram.fsm.state import State, StatesGroup


class CatalogStateGroup(StatesGroup):
    categories = State()
    product_interaction = State()
    product_amount = State()
    add_or_leave = State()
