from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor

API_TOKEN = "8542451616:AAGxhKtMu50rdjHYjy9nwQABg8abtoZmTtw"
ADMIN_ID = 8261093250

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_requests = {}

def main_menu():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Bikes", callback_data="bikes"))
    return kb

def bikes_menu():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("E-Bikes", callback_data="ebikes"))
    return kb

def ebikes_menu():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Modell A", callback_data="produkt_a"))
    return kb

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Wähle:", reply_markup=main_menu())

@dp.callback_query_handler(lambda c: c.data == "bikes")
async def bikes(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Bikes:", reply_markup=bikes_menu())

@dp.callback_query_handler(lambda c: c.data == "ebikes")
async def ebikes(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "E-Bikes:", reply_markup=ebikes_menu())

@dp.callback_query_handler(lambda c: c.data == "produkt_a")
async def produkt(callback_query: types.CallbackQuery):
    user_requests[callback_query.from_user.id] = "Modell A"

    await bot.send_message(callback_query.from_user.id, "Bitte Namen eingeben:")

@dp.message_handler()
async def name_input(message: types.Message):
    if message.from_user.id in user_requests:

        produkt = user_requests[message.from_user.id]

        text = f"Neue Anfrage!\nName: {message.text}\nProdukt: {produkt}"

        await bot.send_message(ADMIN_ID, text)

        await message.answer("Gesendet ✅")

        del user_requests[message.from_user.id]

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)