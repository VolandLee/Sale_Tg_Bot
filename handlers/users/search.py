from loader import dp
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from keyboards.default import menu, catalog
from aiogram.dispatcher.filters import Command, Text
from states.shop import Shop
from aiogram.dispatcher import FSMContext
from views import find_resault, sql
from . import menu

@dp.message_handler(state=Shop.Search)
async def show_menu(message: Message):
    await message.answer("Минуточку", reply_markup=ReplyKeyboardRemove())
    url = find_resault.search(message.text)
    find_resault.create_bd_with_cur_product(url, shop='Shop', table=message.text)
    ans = sql.choose(shop="Shop", table=message.text)
    for el in ans:
        await message.answer(el)
    await Shop.Menu.set()
    await menu.show_menu(message)
