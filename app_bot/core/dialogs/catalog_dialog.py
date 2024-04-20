from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.kbd import PrevPage, NextPage, CurrentPage, Start, Column, StubScroll, Button, Row, \
    FirstPage, LastPage, SwitchTo, Select
from aiogram_dialog.widgets.input import TextInput
from core.dialogs.getters import get_products_by_category, get_categories
from core.dialogs.callbacks import ProductsCallbackHandler
from core.dialogs.custom_content import CustomPager
from core.states.main_menu import MainMenuStateGroup
from core.states.catalog import CatalogStateGroup
from core.states.cart import CartStateGroup
from core.utils.texts import _
from settings import settings


catalog_dialog = Dialog(
    # categories
    Window(
        Const(text=_('PICK_CATEGORY')),
        CustomPager(
            Select(
                id='_category_select',
                items='categories',
                item_id_getter=lambda item: item.id,
                text=Format(text='{item.name}'),
                on_click=ProductsCallbackHandler.selected_category,
            ),
            id='categories_group',
            height=settings.categories_per_page_height,
            width=settings.categories_per_page_width,
            hide_on_single_page=True,
        ),
        Start(Const(text=_('BACK_BUTTON')), id='go_to_menu', state=MainMenuStateGroup.menu),
        getter=get_categories,
        state=CatalogStateGroup.categories,
    ),


    # products
    Window(
        DynamicMedia(selector='media_content'),
        Format(text=_(
            text='PRODUCT_PAGE',
            name='{product.name}',
            description='{product.description}',
            price='{product.price}',
        )),
        StubScroll(id='product_scroll', pages='pages'),

        # cycle pager
        Row(
            LastPage(scroll='product_scroll', text=Const('<'), when=F['current_page'] == 0),
            PrevPage(scroll='product_scroll', when=F['current_page'] != 0),
            Button(text=Format('{current_page}'), id='current_page_button'),
            NextPage(scroll='product_scroll', when=F['current_page'] != F['pages'] - 1),
            FirstPage(scroll='product_scroll', text=Const('>'), when=F['current_page'] == F['pages'] - 1),
            when=F['pages'] > 1,
        ),

        Column(
            SwitchTo(Const(text=_('PICK_BUTTON')), id='go_to_amount', state=CatalogStateGroup.product_amount),
            SwitchTo(Const(text=_('BACK_BUTTON')), id='go_to_categories', state=CatalogStateGroup.categories),
        ),
        getter=get_products_by_category,
        state=CatalogStateGroup.product_interaction,
    ),

    # input amount
    Window(
        Const(text=_('INPUT_AMOUNT')),
        TextInput(
            id='product_amount',
            type_factory=str,
            on_success=ProductsCallbackHandler.entered_product_amount
        ),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='go_to_product', state=CatalogStateGroup.product_interaction),
        state=CatalogStateGroup.product_amount,
    ),

    # add or leave
    Window(
        Const(text=_('PICK_ACTION')),
        Column(
            SwitchTo(Const(text=_('ADD_MORE_BUTTON')), id='go_to_categories', state=CatalogStateGroup.categories),
            Start(Const(text=_('MY_PRODUCTS_BUTTON')), id='go_to_my_products', state=CartStateGroup.products),
        ),
        state=CatalogStateGroup.add_or_leave
    ),
)
