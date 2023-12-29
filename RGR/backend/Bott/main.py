from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from localsettings import BOT_TOKEN
#from states import States
from api import profile_exists,create_profile,ask_question1, ask_question2,ask_question3,send_answers
from api import ask_subscription,set_subscription
from aiogram.dispatcher.filters.state import State, StatesGroup

class States(StatesGroup):
    AWAITING_RESIDENCE = State()
    QUESTION1 = State()
    QUESTION2 = State()
    QUESTION3 = State()
    SUBSCRIBE = State()

API_TOKEN = BOT_TOKEN
API_BASE_URL = 'http://localhost:8000/api/'  

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot,storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=['start'], state = "*")
async def start_command(message: types.Message):
    external_id = message.chat.id
    await message.reply("Привет, я-бот, который помогает выбрать вуз")
    await message.reply("Идет проверка на существование профиля")
    user_exist = await profile_exists(bot, external_id)
    if user_exist==False:
        await States.AWAITING_RESIDENCE.set()
        # Ожидаем ответа от пользователя с клавиатуры
        markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add(KeyboardButton("Левый"))
        markup.add(KeyboardButton("Правый"))
        await bot.send_message(external_id, "На каком берегу вы живете? (Левый/Правый)", reply_markup=markup)
    else:
        await ask_question1(bot,external_id)
        await States.QUESTION1.set()


@dp.message_handler(state=States.AWAITING_RESIDENCE)
async def handle_residence_choice(message: types.Message,state: FSMContext):
    external_id = message.chat.id
    name = message.from_user.username
    user_answer = message.text.lower()
    await create_profile(bot, external_id, name, user_answer)
    await state.finish()
    await ask_question1(bot,external_id)
    await States.QUESTION1.set()

@dp.message_handler(state=States.QUESTION1)
async def QUESTION1(message: types.Message,state: FSMContext):
    external_id = message.chat.id
    answer1 = message.text.lower()
    await state.update_data(answer1=answer1)
    await ask_question2(bot,external_id)
    await States.QUESTION2.set()
@dp.message_handler(state=States.QUESTION2)
async def QUESTION2(message: types.Message,state: FSMContext):
    external_id = message.chat.id
    answer2 = message.text.lower()
    await state.update_data(answer2=answer2)
    await ask_question3(bot,external_id)
    await States.QUESTION3.set()
@dp.message_handler(state=States.QUESTION3)
async def QUESTION3(message: types.Message,state: FSMContext):
    external_id = message.chat.id
    answer3 = message.text.lower()
    await state.update_data(answer3=answer3)
    await send_answers(bot,external_id,state)
    await ask_subscription(bot,external_id)
    await States.SUBSCRIBE.set()
@dp.message_handler(state=States.SUBSCRIBE)
async def SUBSCRIBE(message: types.Message,state: FSMContext):
    external_id = message.chat.id
    if message.text.lower() == 'да':
        subscribe = True
    else:
        subscribe = False
    await set_subscription(bot,external_id, subscribe)
    await state.finish()


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)