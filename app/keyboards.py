from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


menu_btn = InlineKeyboardBuilder()
menu_btn.row(
    types.InlineKeyboardButton(
        text="Статистика",
        callback_data="statistics")
)
menu_btn.row(
    types.InlineKeyboardButton(
        text="Поменять id чата",
        callback_data="chat")
)
menu_btn.row(
    types.InlineKeyboardButton(
        text="Поменять id поста",
        callback_data="post")
)
menu_btn.row(
    types.InlineKeyboardButton(
        text="Поменять ключевое слово",
        callback_data="words")
)
menu_btn.row(
    types.InlineKeyboardButton(
        text="Поменять max_tokens",
        callback_data="tokens")
)
menu_btn.row(
    types.InlineKeyboardButton(
        text="Поменять temperature",
        callback_data="temperature")
)
menu_btn.row(
    types.InlineKeyboardButton(
        text="Поменять prompt",
        callback_data="prompt")
)
menu_btn = menu_btn.as_markup()

back_btn = InlineKeyboardBuilder()
back_btn.row(
    types.InlineKeyboardButton(
        text="Назад",
        callback_data="menu")
)
back_btn = back_btn.as_markup()