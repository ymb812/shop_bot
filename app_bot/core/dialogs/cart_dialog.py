from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.kbd import Start, Button, Select, SwitchTo
from aiogram_dialog.widgets.input import TextInput
from core.dialogs.custom_content import CustomPager
from core.dialogs.getters import get_products_by_user, get_product_data, get_order_data
from core.dialogs.callbacks import ProductsCallbackHandler
from core.states.cart import CartStateGroup
from core.states.main_menu import MainMenuStateGroup
from core.utils.texts import _
from settings import settings


cart_dialog = Dialog(
    # products by cart
    Window(
        Const(text=_('PRODUCTS_IN_CART'), when=F['products']),
        Const(text=_('CART_IS_EMPTY'), when=~F['products']),
        CustomPager(
            Select(
                id='_products_in_cart_select',
                items='products',
                item_id_getter=lambda item: item.id,
                text=Format(text='{item.name}'),
                on_click=ProductsCallbackHandler.selected_product,
            ),
            id='products_by_cart_group',
            height=settings.categories_per_page_height,
            width=settings.categories_per_page_width,
            hide_on_single_page=True,
        ),
        SwitchTo(Const(text=_('CREATE_ORDER_BUTTON')), id='switch_to_fio', state=CartStateGroup.input_fio,
                 when=F['products']),
        Start(Const(text=_('BACK_BUTTON')), id='go_to_menu', state=MainMenuStateGroup.menu),
        getter=get_products_by_user,
        state=CartStateGroup.products,
    ),


    # products interactions
    Window(
        DynamicMedia(selector='media_content'),
        Format(text=_(
            text='PRODUCT_PAGE',
            name='{product.name}',
            description='{product.description}',
            price='{product.price}',
        )),
        Button(Const(text=_('DELETE_BUTTON')), id='delete_from_cart', on_click=ProductsCallbackHandler.delete_from_cart),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='switch_to_cart', state=CartStateGroup.products),
        getter=get_product_data,
        state=CartStateGroup.product_interaction,
    ),


    # input fio
    Window(
        Const(text=_('INPUT_FIO')),
        TextInput(
            id='input_fio',
            type_factory=str,
            on_success=ProductsCallbackHandler.input_order_data
        ),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='switch_to_products', state=CartStateGroup.products),
        state=CartStateGroup.input_fio,
    ),


    # input phone
    Window(
        Const(text=_('INPUT_PHONE')),
        TextInput(
            id='input_phone',
            type_factory=str,
            on_success=ProductsCallbackHandler.input_order_data
        ),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='switch_to_fio', state=CartStateGroup.input_fio),
        state=CartStateGroup.input_phone,
    ),


    # input address
    Window(
        Const(text=_('INPUT_ADDRESS')),
        TextInput(
            id='input_address',
            type_factory=str,
            on_success=ProductsCallbackHandler.input_order_data
        ),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='switch_to_phone', state=CartStateGroup.input_phone),
        state=CartStateGroup.input_address,
    ),


    # confirm order
    Window(
        Format(text=_('CONFIRM_ORDER',
                      product_types_amount='{product_types_amount}',
                      product_amount='{product_amount}',
                      total_price='{total_price}')
               ),
        Button(Const(text=_('CONFIRM_BUTTON')), id='create_order', on_click=ProductsCallbackHandler.create_order),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='switch_to_address', state=CartStateGroup.input_address),
        getter=get_order_data,
        state=CartStateGroup.confirm,
    ),
)
