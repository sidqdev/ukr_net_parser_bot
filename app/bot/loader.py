import os 
import aiogram
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from apscheduler.schedulers.asyncio import AsyncIOScheduler


bot = Bot(token=os.getenv('bot_token'), parse_mode='html')
storage = RedisStorage2(host=os.getenv('redis_host'), port=int(os.getenv('redis_port')), db=int(os.getenv('redis_db')))
dp = Dispatcher(bot=bot, storage=storage)

scheduler = AsyncIOScheduler()
