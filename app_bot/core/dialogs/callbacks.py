import logging
from aiogram.types import CallbackQuery, Message, BufferedInputFile
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import ManagedScroll
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Select, Button
from core.states.catalog import CatalogStateGroup
from core.states.main_menu import MainMenuStateGroup
from core.database.models import User, Product, UserProduct, Order
from core.utils.texts import _
from settings import settings


logger = logging.getLogger(__name__)


async def switch_page(dialog_manager: DialogManager, scroll_id: str, message: Message):
    # switch page
    scroll: ManagedScroll = dialog_manager.find(scroll_id)
    current_page = await scroll.get_page()

    if current_page == dialog_manager.dialog_data['pages'] - 1:
        next_page = 0
    else:
        next_page = current_page + 1
    await scroll.set_page(next_page)


class CallBackHandler:
    @classmethod
    async def main_menu_buttons_handler(
            cls,
            callback: CallbackQuery,
            widget: Button,
            dialog_manager: DialogManager,
    ):
        if callback.data == 'faq':
            await callback.message.answer(text=_('FAQ'))
        elif callback.data == 'about':
            await callback.message.answer(text=_('ABOUT'))
        elif callback.data == 'contacts':
            await callback.message.answer(text=_('CONTACTS'))


    @classmethod
    async def selected_product(
            cls,
            callback: CallbackQuery,
            widget: Select,
            dialog_manager: DialogManager,
            item_id: str,
    ):
        dialog_manager.dialog_data['category_id'] = item_id
        await dialog_manager.switch_to(CatalogStateGroup.product_interaction)


    @staticmethod
    async def entered_product_amount(
            message: Message,
            widget: ManagedTextInput,
            dialog_manager: DialogManager,
            value,
    ):
        value: str
        if value.isdigit():
            # add product to cart
            await UserProduct.add_or_update_product_to_the_cart(
                product_id=dialog_manager.dialog_data['current_product_id'],
                user_id=message.from_user.id,
                amount=int(value),
            )

            await dialog_manager.switch_to(state=CatalogStateGroup.add_or_leave)
