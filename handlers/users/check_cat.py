from loader import dp
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from . import menu
from aiogram.dispatcher.filters import Command, Text
from states.shop import Shop
from aiogram.dispatcher import FSMContext
from aiogram import types
import copy
from views import find_resault, sql
import pickle

@dp.message_handler(state=Shop.Check_Cat)

async def chose_shop(message: Message, state: FSMContext):
    """
    Opens the store catalog and brands catalog. The structure of the buttons is organized as an embedded dictionary and
      The user shows the keys of this dictionary. When he presses a button, it goes down one level
      nesting, where the contents of the buttons becomes new_dict = DICT [KEY] when it comes to the last level
      The Klludu value becomes the URL address and the program calls functions to create the database and then makes a request to this
       database and displays the result """
    if message.text == "Назад":
        await menu.show_menu(message)
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    context = await state.get_data()
    if message.text == "Бренды":
        with open('keyboards/default/catalog/{}/brands.pickle'.format(context["shop"]), "rb") as f:
            context["catalog"]["Бренды"] = pickle.load(f)
    if message.text == "Назад":
        await menu.show_menu(message)
        return 0

    context['table'] += " " + message.text
    print(context["catalog"])
    catalog = copy.deepcopy(context["catalog"][message.text])
    await state.update_data(catalog=catalog, table=context['table'])
    print(context)
    if isinstance(catalog, str):
        await message.answer("Выполняю поиск, пожалуйста подождите", reply_markup=ReplyKeyboardRemove())
        await Shop.Menu.set()
        print(catalog, context['shop'], context['table'])
        find_resault.create_bd_with_cur_product(catalog, context['shop'], context['table'])
        ans = sql.choose(context['shop'], context['table'])
        if ans:
            for el in ans:
                await message.answer (el)
        else:
            await message.answer (f"В магазине {i} по вашему запросу ничего не найдено")
    else:
        kb.add(*catalog)
        kb.add("Назад")
        if context["shop"] == "Wildberries":
            kb.add("Бренды")

        await message.answer("Выберите категорию товара", reply_markup=kb)
        await Shop.Check_Cat.set()