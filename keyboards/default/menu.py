from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Поиск")
        ],
        [
            KeyboardButton(text="Wildberries"),
            KeyboardButton(text="Lamoda")
        ],

    ],
    resize_keyboard=True
)