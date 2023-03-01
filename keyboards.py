from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

inline_buttons = [
    InlineKeyboardButton('Старт', callback_data='start'),
    InlineKeyboardButton('Помощь', callback_data='help'),
    InlineKeyboardButton('Скачать видео', callback_data='video'),
    InlineKeyboardButton('Скачать аудио', callback_data='audio')
]

button = InlineKeyboardMarkup().add(*inline_buttons)

share_keyboards = [
    KeyboardButton('Поделиться контактом', request_contact=True),
    KeyboardButton('Отправить геолокацию', request_location=True)
]

share_button = ReplyKeyboardMarkup().add(*share_keyboards)