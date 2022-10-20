from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


def cancel():
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.add(KeyboardButton('ОТМЕНА'))
    return m


def admin_menu():
    m = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    m.insert(InlineKeyboardButton('Рассылка сообщений', callback_data='sndd'))
    m.insert(InlineKeyboardButton('Скачать базу пользователей', callback_data='dwnld'))
    m.insert(InlineKeyboardButton('Обновить приветственный пост', callback_data='wlcm_post'))
    return m