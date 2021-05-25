from loader import dp
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from keyboards.default import menu
from aiogram.dispatcher.filters import Command, Text



@dp.message_handler(Command("menu"))
async def show_menu(message: Message):
    await message.answer("Выберите магазин", reply_markup=menu)


@dp.message_handler(Text(equals=["Wildberries", "Lamoda", "Поиск"]))
async def chose_shop(message: Message):
    if message.answer("Поиск"):
        pass
    else:
        await message.answer(f"Вы выбрали {message.text}, выберите категорию",
reply_markup=ReplyKeyboardRemove())
