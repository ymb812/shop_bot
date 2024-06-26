import logging
import uuid
from aiogram.types import CallbackQuery, Message, BufferedInputFile
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import ManagedScroll
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Select, Button
from core.states.catalog import CatalogStateGroup
from core.states.cart import CartStateGroup
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


def get_username_or_link(user: User):
    if user.username:
        user_username = f'@{user.username}'
    else:
        user_username = f'<a href="tg://user?id={user.user_id}">ссылка</a>'

    return user_username


class ProductsCallbackHandler:
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
    async def selected_category(
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


    @classmethod
    async def selected_product(
            cls,
            callback: CallbackQuery,
            widget: Select,
            dialog_manager: DialogManager,
            item_id: str,
    ):
        dialog_manager.dialog_data['product_id'] = item_id
        await dialog_manager.switch_to(CartStateGroup.product_interaction)


    @classmethod
    async def delete_from_cart(
            cls,
            callback: CallbackQuery,
            widget: Button,
            dialog_manager: DialogManager,
    ):
        # delete data from db
        await UserProduct.filter(
            product_id=dialog_manager.dialog_data['product_id'],
            user_id=callback.from_user.id,
        ).delete()

        await dialog_manager.switch_to(CartStateGroup.products)


    # handle 3 inputs from cart for order data
    @staticmethod
    async def input_order_data(
            message: Message,
            widget: ManagedTextInput,
            dialog_manager: DialogManager,
            value,
    ):
        if widget.widget.widget_id == 'input_fio':
            dialog_manager.dialog_data['fio'] = value
            await dialog_manager.switch_to(CartStateGroup.input_phone)

        elif widget.widget.widget_id == 'input_phone':
            dialog_manager.dialog_data['phone'] = value
            await dialog_manager.switch_to(CartStateGroup.input_city)

        # start address states
        elif widget.widget.widget_id == 'input_city':
            dialog_manager.dialog_data['address'] = f'{value} '
            await dialog_manager.switch_to(CartStateGroup.input_street)

        elif widget.widget.widget_id == 'input_street':
            dialog_manager.dialog_data['address'] += f'{value} '
            await dialog_manager.switch_to(CartStateGroup.input_house)

        elif widget.widget.widget_id == 'input_house':
            dialog_manager.dialog_data['address'] += f'{value} '
            await dialog_manager.switch_to(CartStateGroup.input_index)

        elif widget.widget.widget_id == 'input_index':
            dialog_manager.dialog_data['address'] += f'{value} '
            await dialog_manager.switch_to(CartStateGroup.input_entrance)

        elif widget.widget.widget_id == 'input_entrance':
            dialog_manager.dialog_data['address'] += f'{value} '
            await dialog_manager.switch_to(CartStateGroup.input_floor)

        elif widget.widget.widget_id == 'input_floor':
            dialog_manager.dialog_data['address'] += f'{value} '
            await dialog_manager.switch_to(CartStateGroup.input_flat)

        # end of address states
        elif widget.widget.widget_id == 'input_flat':
            dialog_manager.dialog_data['address'] += f'{value} '
            await dialog_manager.switch_to(CartStateGroup.confirm)


    # send new order to managers
    @staticmethod
    async def create_order(
            callback: CallbackQuery,
            widget: Button,
            dialog_manager: DialogManager,
    ):
        order = await Order.create(
            id=uuid.uuid4(),
            user_id=callback.from_user.id,
            is_paid=False,
            price=dialog_manager.dialog_data['total_price'],
            product_amount=dialog_manager.dialog_data['product_amount'],
            address=dialog_manager.dialog_data['address'],
        )
        products = await UserProduct.add_cart_to_order(user_id=callback.from_user.id, order_id=order.id)

        # save fio, phone, address to User
        user: User = await order.user
        user.fio = dialog_manager.dialog_data['fio']
        user.phone = dialog_manager.dialog_data['phone']
        user.address = dialog_manager.dialog_data['address']
        await user.save()

        # send info to user and to the managers chat
        await dialog_manager.event.bot.send_message(
            chat_id=settings.managers_chat_id,
            text=_(
                text='ORDER_DATA_FOR_MANAGERS',
                order_id=order.id,
                username=get_username_or_link(user=user),
                products=products,
                product_amount=order.product_amount,
                total_price=order.price,
                fio=dialog_manager.dialog_data['fio'],
                phone=dialog_manager.dialog_data['phone'],
                address=dialog_manager.dialog_data['address'],
            ),
        )
        await callback.message.answer(text=_('ORDER_IS_CREATED', order_id=order.id))
        await dialog_manager.start(MainMenuStateGroup.menu)


class SupportCallbackHandler:
    @classmethod
    async def menu_buttons_handler(
            cls,
            callback: CallbackQuery,
            widget: Button,
            dialog_manager: DialogManager,
    ):
        if callback.data == 'go_to_manager':
            await callback.message.answer(text=_('MANAGER_ACCOUNT', manager_link=settings.manager_link))
        elif callback.data == 'about':
            await callback.message.answer(text=_('ABOUT'))


    # send new support request to managers
    @staticmethod
    async def input_phone(
            message: Message,
            widget: ManagedTextInput,
            dialog_manager: DialogManager,
            value,
    ):
        user = await User.get(user_id=message.from_user.id)
        await dialog_manager.event.bot.send_message(
            chat_id=settings.managers_chat_id,
            text=_(
                text='SUPPORT_REQUEST_FOR_MANAGERS',
                username=get_username_or_link(user=user),
                phone=value,
            ),
        )

        await message.answer(text=_('FEED_BACK_INFO'))
        await dialog_manager.start(MainMenuStateGroup.menu)
