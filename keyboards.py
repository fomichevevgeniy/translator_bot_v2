from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from configs import LANGUAGES


def generate_languages1():
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for lang_code, lang_name in LANGUAGES.items(): # [Русский] -> lang1_ru
        btn = InlineKeyboardButton(text=lang_name, callback_data=f'lang1_{lang_code}')
        buttons.append(btn)
    markup.add(*buttons)
    return markup

def generate_languages2():
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for lang_code, lang_name in LANGUAGES.items(): # [Русский] -> lang1_ru
        btn = InlineKeyboardButton(text=lang_name, callback_data=f'lang2_{lang_code}')
        buttons.append(btn)
    markup.add(*buttons)
    return markup