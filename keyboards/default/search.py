from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

search = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Искать по всем магазинам")
        ],
        [
            KeyboardButton(text="Искать на Lamoda"),
            KeyboardButton(text="Искать на Wildberries")
        ],
        [
            KeyboardButton(text="Назад")
        ],
    ],
    resize_keyboard=True
)