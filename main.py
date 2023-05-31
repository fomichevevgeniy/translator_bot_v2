from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, CallbackQuery
from keyboards import generate_languages1, generate_languages2
from translate import Translator
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from database import save_data, get_history
from configs import LANGUAGES
TOKEN = 'TOKEN HERE'
bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class GetLanguages(StatesGroup):
    src = State()
    dest = State()
    text = State()



@dp.message_handler(commands=['start'])
async def command_start(message: Message):

    await message.answer('Здравствуйте. Я бот переводчик')
    await get_lang(message)

async def get_lang(message: Message, state=None):
    await GetLanguages.src.set()  # Сейчас будет вопрос
    await message.answer('Выберите язык на который хотите перевести: ',
                                reply_markup=generate_languages1())


@dp.callback_query_handler(lambda call: 'lang1' in call.data, state=GetLanguages.src)
async def get_src_ask_desc(call: CallbackQuery, state: FSMContext):
    # lang1_ru -> ['lang1', 'ru']
    src = call.data.split('_')[1]
    async with state.proxy() as data:
        data['src'] = src
    await GetLanguages.next()
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    await bot.edit_message_text(f'Вы выбрали язык {src}\n\nВыберите язык на который хотите перевести: ',chat_id, message_id,
                                reply_markup=generate_languages2())

@dp.callback_query_handler(lambda call: 'lang2' in call.data, state=GetLanguages.dest)
async def get_dest_ask_text(call: CallbackQuery, state: FSMContext):
    dest = call.data.split('_')[1]
    async with state.proxy() as data:
        data['dest'] = dest
    src = data['src']
    await GetLanguages.next()
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    await bot.edit_message_text(f'Вы выбрали языки {src}->{dest}\n\nВведите текст, который хотите перевести: ',chat_id, message_id)


@dp.message_handler(state=GetLanguages.text)
async def get_text_translate(message: Message, state: FSMContext):
    text = message.text
    async with state.proxy() as data:
        data['text'] = text
    src = data['src']
    dest = data['dest']
    text = data['text']
    kenan = Translator(from_lang=src, to_lang=dest)
    chat_id = message.chat.id
    translated_text = kenan.translate(text=text)
    await bot.send_message(chat_id, translated_text)
    save_data(chat_id=chat_id, src=src, dest=dest,
              translated_text=translated_text, original_text=text)
    await command_start(message)

@dp.message_handler(commands=['history'])
async def get_history_function(message: Message):
    chat_id = message.chat.id
    history = get_history(chat_id)  # [(), ()]
    text = 'Ваша история:\n\n'
    for original_text, src, dest, translated_text in history:
        text += f'''Оригинал текста: {original_text}
Перевод текста: {translated_text}
Язык оригинала: {LANGUAGES[src]}
Язык перевода: {LANGUAGES[dest]}\n\n'''
    await bot.send_message(chat_id, text)
    await command_start(message)

executor.start_polling(dp)
