from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
                           ReplyKeyboardMarkup, KeyboardButton, InlineQueryResultPhoto, InlineQueryResultArticle,
                           InputTextMessageContent, InlineQueryResult)
from typing import Dict, List
from aiogram.utils.markdown import hide_link


def ReplyKeyboard(*data: Dict[str, str], resize_keyboard=None):
    """
    All buttons are passed as arguments, NOT list:
    {'text': 'Button text', 'type': 'type of button'}, ...
        types:
            reply - simple button
            location - button to send location request
            contact - button to send contact request
    """
    resize_keyboard = True if resize_keyboard is None else resize_keyboard
    buttons = ReplyKeyboardMarkup(resize_keyboard=resize_keyboard)

    for btn in data:
        text = btn.get("text")
        typ = btn.get("type")

        if typ == "reply":
            button = KeyboardButton(text)
        elif typ == "location":
            button = KeyboardButton(text, request_location=True)
        elif typ == "contact":
            button = KeyboardButton(text, request_contact=True)
        else:
            button = KeyboardButton(f"{text}, error")

        buttons.add(button)

    return buttons


def InlineKeyboard(*data: Dict[str, str]):
    """
    All buttons are passed as arguments, NOT list:
    {'text': 'Button text', 'data': 'Callback_data or Url'}, ...
    """
    buttons = InlineKeyboardMarkup()

    for btn in data:
        text = str(btn.get("text"))
        bid = str(btn.get("data"))
        if bid.startswith("http"):
            button = InlineKeyboardButton(text, url=bid)
        elif bid.startswith('inline_'):
            button = InlineKeyboardButton(text, switch_inline_query_current_chat=bid.split('_', maxsplit=1)[1])
        else:
            button = InlineKeyboardButton(text, callback_data=bid)
        buttons.add(button)

    return buttons


def HardInlineKeyboard(mask: List[List]):
    buttons = InlineKeyboardMarkup()

    for layer in mask:
        button = list()
        for btn in layer:
            text = str(btn.get('text'))
            bid = str(btn.get('data'))
            if bid.startswith("http"):
                button.append(InlineKeyboardButton(text, url=bid))
            else:
                button.append(InlineKeyboardButton(text, callback_data=bid))

        buttons.add(*button)

    return buttons


def InlineQueryKeyboard(inline_items, default_keyboard: list):
    items = list()
    for item in inline_items:
        temp_keyboard = default_keyboard.copy()
        for button in temp_keyboard:
            button['data'] = button.get('data').format(id=item.get('id'))

        items.append(
            InlineQueryResultArticle(id=item.get('id'),
                                     thumb_url=item.get('photo_url'),
                                     description=item.get('disc'),
                                     title=item.get('title'),
                                     input_message_content=InputTextMessageContent(
                                         message_text=f"{item.get('title')}\n"
                                                      f"{item.get('disc')}{hide_link(item.get('photo_url'))}"),
                                     reply_markup=InlineKeyboard(*temp_keyboard)))

    return items
