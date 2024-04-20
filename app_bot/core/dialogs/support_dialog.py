from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Button, SwitchTo
from aiogram_dialog.widgets.input import TextInput
from core.dialogs.callbacks import SupportCallbackHandler
from core.states.support import SupportStateGroup
from core.states.main_menu import MainMenuStateGroup
from core.utils.texts import _


support_dialog = Dialog(
    # menu
    Window(
        Const(text=_('PICK_ACTION')),
        Button(Const(text=_('WRITE_BUTTON')), id='go_to_manager', on_click=SupportCallbackHandler.menu_buttons_handler),
        SwitchTo(Const(text=_('FEED_BACK_BUTTON')), id='go_to_feed_back', state=SupportStateGroup.input_phone),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='switch_to_menu', state=MainMenuStateGroup.menu),
        state=SupportStateGroup.menu,
    ),

    # input phone
    Window(
        Const(text=_('INPUT_PHONE')),
        TextInput(
            id='input_phone',
            type_factory=str,
            on_success=SupportCallbackHandler.input_phone,
        ),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='switch_to_support', state=SupportStateGroup.menu),
        state=SupportStateGroup.input_phone,
    ),
)
