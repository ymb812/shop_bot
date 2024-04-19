from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Column, Url, SwitchTo, Button, Start
from core.states.main_menu import MainMenuStateGroup
from core.utils.texts import _
from core.dialogs.callbacks import CallBackHandler
from core.states.catalog import CatalogStateGroup
from core.states.cart import CartStateGroup
from core.states.support import SupportStateGroup


main_menu_dialog = Dialog(
    # menu
    Window(
        Const(text=_('PICK_ACTION')),
        Column(
            Start(Const(text=_('ORDER_BUTTON')), id='go_to_new_order', state=CatalogStateGroup.categories),
            Start(Const(text=_('MY_PRODUCTS_BUTTON')), id='go_to_my_products', state=CartStateGroup.products),
            Button(Const(text=_('FAQ_BUTTON')), id='faq', on_click=CallBackHandler.main_menu_buttons_handler),
            Button(Const(text=_('ABOUT_BUTTON')), id='about', on_click=CallBackHandler.main_menu_buttons_handler),
            Button(Const(text=_('CONTACTS_BUTTON')), id='contacts', on_click=CallBackHandler.main_menu_buttons_handler),
            Start(Const(text=_('SUPPORT_BUTTON')), id='go_to_support', state=SupportStateGroup.menu),
        ),
        state=MainMenuStateGroup.menu,
    ),
)
