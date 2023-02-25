from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

inline_buttons = [
    InlineKeyboardButton('Старт', callback_data='start'),
    InlineKeyboardButton('Помощь', callback_data='help'),
    InlineKeyboardButton('Скачать видео', callback_data='video'),
    InlineKeyboardButton('Скачать аудио', callback_data='audio')
]

button = InlineKeyboardMarkup().add(*inline_buttons)