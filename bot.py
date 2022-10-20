from sqlite3 import IntegrityError

import aiogram
from aiogram import Bot
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils import executor

import button
import config
import db
import write_excel

storage = MemoryStorage()
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=storage)


async def on_startup(_):
    print('Bot activated')
    db.start_db()


class MassSend(StatesGroup):
    sendd = State()


class PostSend(StatesGroup):
    post_sendd = State()


@dp.message_handler(commands='start')
async def strt(message: types.Message):
    for admn in config.ADMIN_ID:
        if message.from_user.id == admn:
            await bot.send_message(message.from_user.id, text='Вы администратор, добро пожаловать!',
                                   reply_markup=button.admin_menu())
        else:
            try:
                if message.from_user.id not in db.get_tg_id():
                    db.db_add(message.from_user.id, message.from_user.first_name, message.from_user.last_name,
                              message.from_user.username)
            except IntegrityError:
                pass
            ids = db.post_data()
            ids2 = ids[0]
            await bot.copy_message(message.chat.id, ids2[0], ids2[1])


@dp.callback_query_handler(text='sndd')
async def snd(message: types.Message):
    if message.from_user.id not in config.ADMIN_ID:
        await bot.send_message(message.from_user.id, text="В доступе отказано!")
    else:
        await bot.send_message(message.from_user.id, text=f"Напишите и отправьте сообщение для "
                                                          f"рассылки оно будет отправлено {len(db.all_user())} "
                                                          f"пользователям", reply_markup=button.cancel())
        await message.answer()
        await MassSend.sendd.set()


@dp.message_handler(text='ОТМЕНА', state=MassSend.sendd)
async def cncl(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id, 'Рассылка отменена', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(content_types=aiogram.types.ContentType.ANY,
                    state=MassSend.sendd)
async def send(message: types.Message, state: FSMContext):
    good, bad = 0, 0
    await state.finish()
    errors_list = []
    for i in db.all_user():
        try:
            await bot.copy_message(i[0], message.chat.id, message.message_id)
            good += 1
        except Exception as e:
            bad += 1
            errors_list.append(e)
    await bot.send_message(message.from_user.id, 'Рассылка завершена успешно\n'
                                                 f'Доставлено: {good}\n'
                                                 f'Не доставлено: {bad}\n'
                                                 f'Ошибки {set(errors_list)}', reply_markup=ReplyKeyboardRemove())


@dp.callback_query_handler(text='dwnld')
async def find_id_message(message: types.Message):
    if message.from_user.id in config.ADMIN_ID:
        write_excel.excel()
        await bot.send_document(message.from_user.id, open(config.path_to_result, 'rb'))
        await message.answer()
    else:
        await bot.send_message(message.from_user.id, text="У нет прав, обратитесь к администратору!")


@dp.callback_query_handler(text='wlcm_post')
async def welcome_post(message: types.Message):
    await bot.send_message(message.from_user.id, text=f"Перешлите сюда сообщение, "
                                                      f"бот будет использовать его как приветствие",
                           reply_markup=button.cancel())
    await message.answer()
    await PostSend.post_sendd.set()


@dp.message_handler(text='ОТМЕНА', state=PostSend.post_sendd)
async def cncl(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id, 'Отменено', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(content_types=aiogram.types.ContentType.ANY,
                    state=PostSend.post_sendd)
async def send(message: types.Message, state: FSMContext):
    db.create_post_db()
    db.db_post(message.chat.id, message.message_id)
    await state.finish()
    await bot.send_message(message.from_user.id, text='Пост установлен', reply_markup=ReplyKeyboardRemove())


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
