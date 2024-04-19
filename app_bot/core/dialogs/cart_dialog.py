from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.kbd import Back, Button, Select, SwitchTo
from aiogram_dialog.widgets.input import TextInput
from core.dialogs.custom_content import CustomPager
from core.dialogs.getters import get_products_by_user, get_product_data, get_order_data
from core.dialogs.callbacks import CallBackHandler
from core.states.dialogs import CartStateGroup
from core.utils.texts import _
from settings import settings


cart_dialog = Dialog(
    # products by cart
    Window(
        Const(text=_('PRODUCTS_IN_CART')),
        CustomPager(
            Select(
                id='_products_in_cart_select',
                items='products',
                item_id_getter=lambda item: item.id,
                text=Format(text='{item.name}'),
                on_click=CallBackHandler.selected_content,
            ),
            id='products_by_cart_group',
            height=settings.products_per_page_height,
            width=settings.products_per_page_width,
            hide_on_single_page=True,
        ),
        SwitchTo(Const(text=_('CREATE_ORDER_BUTTON')), id='switch_to_delivery', state=CartStateGroup.delivery),
        getter=get_products_by_user,
        state=CartStateGroup.products,
    ),

    # products interactions
    Window(
        DynamicMedia(selector='media_content'),
        Format(text=_('PRODUCT_PAGE',
                      product_name='{product.name}',
                      product_description='{product.description}',
                      product_price='{product.price}')
               ),
        Button(Const(text=_('DELETE_BUTTON')), id='delete_from_cart', on_click=CallBackHandler.delete_from_cart),
        Back(Const(text=_('BACK_BUTTON'))),
        getter=get_product_data,
        state=CartStateGroup.product_interaction,
    ),

    # input delivery data
    Window(
        Const(text=_('INPUT_DELIVERY_DATA')),
        TextInput(
            id='delivery_data',
            type_factory=str,
            on_success=CallBackHandler.get_delivery_data
        ),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='switch_to_delivery', state=CartStateGroup.products),
        state=CartStateGroup.delivery,
    ),

    # payment
    Window(
        Format(text=_('CONFIRM_ORDER',
                      product_types_amount='{product_types_amount}',
                      product_amount='{product_amount}',
                      total_price='{total_price}')
               ),
        Button(Const(text=_('PAY_BUTTON')), id='pay_order', on_click=CallBackHandler.order_payment),
        Back(Const(text=_('BACK_BUTTON'))),
        getter=get_order_data,
        state=CartStateGroup.payment,
    ),
)
