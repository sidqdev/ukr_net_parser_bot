from .routes import dp
from .scheduler import scheduler

async def start_bot():
    scheduler.start()
    await dp.start_polling()
