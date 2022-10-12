from aiogram import types

from app.bot.loader import dp
from app.bot import handlers


dp.register_message_handler(handlers.start, commands=['start', 'menu'], state='*')
dp.register_callback_query_handler(handlers.get_main, lambda e: e.data == 'main', state='*')

dp.register_callback_query_handler(handlers.main, state='main')

dp.register_message_handler(handlers.add_phrase, state='phrases')
dp.register_callback_query_handler(handlers.delete_phrase, state='phrases')