from aiogram import Bot, types, Dispatcher, executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv
from pytube import YouTube
import logging
import time
import os

from keyboards import button
from start_db import CustomDB
from custom_states import DownloadAudio, DownloadVideo, Mail

db = CustomDB()
connect = db.connect
db.connect_db()

load_dotenv(".env")

bot = Bot(os.environ.get('TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())
storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)

def url_valid(url):
    try:
        YouTube(url).streams.first()
        return True
    except:
        return False

@dp.message_handler(commands=['start'])
async def start(message:types.Message):
    cursor = connect.cursor()
    cursor.execute(f"SELECT id FROM users WHERE id = {message.from_user.id};")
    res = cursor.fetchall()
    if res == []:
        cursor.execute(f"INSERT INTO users VALUES ('{message.from_user.username}', '{message.from_user.first_name}', '{message.from_user.last_name}', {message.from_user.id}, '{time.ctime()}');")
    await message.answer(f'Здравствуйте {message.from_user.full_name}')
    await message.answer("Этот бот способен скачивать видео или аудио с платформы Youtube.")
    await message.answer("Если запутаетесь в командах напишите /help", reply_markup=button)
    connect.commit()

@dp.callback_query_handler(lambda call: call)
async def all(call):
    if call.data == "start":
        await start(call.message)
    elif call.data == "help":
        await helper(call.message)
    elif call.data == "audio":
        await audio(call.message)
    elif call.data == "video":
        await video(call.message)

@dp.message_handler(commands=['help'])
async def helper(message:types.Message):
    await message.answer("Вот список команд бота:\n/video - для скачивания видеороликов\n/audio - для скачивания аудио из видеороликов")

@dp.message_handler(commands=['audio'])
async def audio(message:types.Message):
    await message.reply("Отправьте ссылку на аудио и оно будет скачано.")
    await DownloadAudio.downloadaud.set()

@dp.message_handler(state=DownloadAudio.downloadaud)
async def download_audio(message:types.Message, state:FSMContext):
    if url_valid(message.text) == True:
        await message.answer("Скачиваем аудио")
        aud_yt = YouTube(message.text)
        await message.reply(f'{aud_yt.title}')
        audio = aud_yt.streams.filter(only_audio=True).first().download('audio', f'{aud_yt.title}.mp3')
        try:
            await message.answer("Отправляем аудио...")
            with open(audio, 'rb') as down_audio:
                await message.answer_audio(down_audio)
                os.remove(audio)
        except:
            await message.answer("Произошла ошибка при скачивании")
            os.remove(audio)
        await state.finish()
    else:
            await message.reply("Отправленная вами ссылка недействительна. Отправьте ссылку на Youtube видео.")

@dp.message_handler(commands=['video'])
async def video(message:types.Message):
    await message.reply("Отправьте ссылку на видео и оно будет скачано.")
    await DownloadVideo.download.set()

@dp.message_handler(state=DownloadVideo.download)
async def download_video(message:types.Message, state:FSMContext):
    if url_valid( message.text) == True:
        await message.answer("Скачиваем видео")
        yt = YouTube(message.text)
        await message.reply(f'{yt.title}')
        video = yt.streams.filter(progressive=True, file_extension="mp4").order_by('resolution').desc().first().download('video', f"{yt.title}.mp4")
        try:
            await message.answer("Отправляем видео...")
            with open(video, 'rb') as down_video:
                await message.answer_video(down_video)
                os.remove(video)
        except:
            await message.answer("Произошла ошибка при скачивании")
            os.remove(video)
        await state.finish()
    else:
        await message.reply("Отправленная вами ссылка недействительна. Отправьте ссылку на Youtube видео.")

@dp.message_handler(commands=['mailing'])
async def mailing(message:types.Message):
    if message.from_user.id == 731982105:
        await message.answer("Введите текст для рассылки: ")
        await Mail.title.set()
    else:
        await message.answer("Нет доступа")

@dp.message_handler(state=Mail.title)
async def send_mailing(message:types.Message, state:FSMContext):
    cursor = connect.cursor()
    cursor.execute(f"SELECT id FROM users;")
    users_id = cursor.fetchall()
    await message.answer(f"{users_id}")
    for id in users_id:
        await bot.send_message(id[0], message.text)
    await message.answer("Рассылка окончена")
    await state.finish()

@dp.message_handler()
async def nothing(message:types.Message):
    await message.reply("Я вас не понял, введите /help для просмотра доступных функций.")

executor.start_polling(dp)