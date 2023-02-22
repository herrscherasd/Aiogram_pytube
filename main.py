from aiogram import Bot, types, Dispatcher, executor
from dotenv import load_dotenv
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from pytube import YouTube
import os
import logging

load_dotenv(".env")

buttons = [
    KeyboardButton('/start'),
    KeyboardButton('/help'),
    KeyboardButton('/video'),
    KeyboardButton('/audio')
]

button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(*buttons)

bot = Bot(os.environ.get('TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())
storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=['start'])
async def start(message:types.Message):
    await message.answer(f'Здравствуйте {message.from_user.full_name}', reply_markup=button)

class DownloadVideo(StatesGroup):
    download = State()



@dp.message_handler(commands=['video'])
async def video(message:types.Message):
    await message.reply("Отправьте ссылку на видео и оно будет скачано.")
    await DownloadVideo.download.set()

@dp.message_handler(state=DownloadVideo.download)
async def download_video(message:types.Message, state:FSMContext):
    await message.answer("Скачиваем видео")
    yt = YouTube(message.text)
    await message.reply(f'{yt.title}')
    video = yt.streams.filter(progressive=True, file_extension="mp4").order_by('resolution').desc().first().download('video', f"{yt.title}.mp4")

    try:
        await message.answer("Отправляем видео...")
        with open(video, 'rb') as down_video:
            await message.answer_video(down_video)
    except:
        await message.answer("Произошла ошибка при скачивании")
    await state.finish()


@dp.message_handler()
async def nothing(message:types.Message):
    await message.reply("Я вас не понял, введите /help для просмотра доступных функций.")



executor.start_polling(dp)