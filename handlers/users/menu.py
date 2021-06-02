from loader import dp
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from keyboards.default import menu, catalog
from aiogram.dispatcher.filters import Command, Text
from states.shop import Shop
from aiogram.dispatcher import FSMContext
import pickle

@dp.message_handler(Command("menu"), state="*")
async def show_menu(message: Message):
    await message.answer("Выберите магазин или можете ввести название товара", reply_markup=menu)
    await Shop.Menu.set()


@dp.message_handler(Text(equals=["Wildberries", "Lamoda", "Поиск"]), state=Shop.Menu)
async def chose_shop(message: Message, state: FSMContext):
    if message.text == "Поиск":
        await Shop.Search.set()
        await message.answer("Введите название товара", reply_markup=ReplyKeyboardRemove())

    else:
        key = []
        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        kb.add()
        table = ''
        with open('keyboards/default/catalog/{}/catalog.pickle'.format(message.text), "rb") as f:
            catalog = pickle.load(f)
        await state.update_data(catalog=catalog[message.text], table=table, shop=message.text)
        kb.add(*catalog[message.text])
        kb.add("Назад")
        kb.add ("Бренды")

        await message.answer(f"Вы выбрали {message.text}, выберите категорию",
reply_markup=kb)
        await Shop.Check_Cat.set()

