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
    catalog = copy.deepcopy(context["catalog"][message.text])
    await state.update_data(catalog=catalog, table=context['table'])
    print(context)
    if isinstance(catalog, str):
        await message.answer("Минуточку", reply_markup=ReplyKeyboardRemove())
        await Shop.Menu.set()
        find_resault.create_bd_with_cur_product(catalog, context['shop'], context['table'])
        ans = sql.choose(context['shop'], context['table'])
        for el in ans:
            await message.answer(el)
        await menu.show_menu(message)
    else:
        kb.add(*catalog)
        kb.add("Назад")
        kb.add("Бренды")

        await message.answer("Выберите категорию товара", reply_markup=kb)
        await Shop.Check_Cat.set()