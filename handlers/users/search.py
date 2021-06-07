from loader import dp
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from keyboards.default import menu, catalog, search
from loader import dp
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from keyboards.default import menu, catalog, search
from aiogram.dispatcher.filters import Command, Text
from states.shop import Shop
from aiogram.dispatcher import FSMContext
import pickle
from views import find_resault, sql
from . import menu
@dp.message_handler(state=Shop.Request)
async def show_menu(message: Message, state: FSMContext):
    await message.answer("Выполняю поиск, пожалуйста подождите")
    """Вызывает функции, чтобы создать бд и далее делает запрос к этой бд и выводит результат"""
    shop = await state.get_data()
    for i in shop['shop']:
        print(i)
        url = find_resault.search(i, message.text)
        find_resault.create_bd_with_cur_product (url, i, message.text)
        ans = sql.choose(i, message.text)
        if ans:
            for el in ans:
                await message.answer(el)
        else:
            await message.answer(f"В магазине {i} по вашему запросу ничего не найдено")
    await Shop.Menu.set()
    await menu.show_menu(message)

@dp.message_handler(state=Shop.Search)
async def show_menu(message: Message, state: FSMContext):
    if message.text == "Назад":
        await menu.show_menu(message)
    else:
        if message.text == "Искать по всем магазинам":
            shop = ["Lamoda", "Wildberries"]
        elif message.text == "Искать на Lamoda":
            shop = ["Lamoda"]
        else:
            shop = ["Wildberries"]
        await state.update_data(shop=shop)
        await Shop.Request.set()
        await message.answer("Введите название товара", reply_markup=ReplyKeyboardRemove())

