from .routes import dp
from .scheduler import scheduler, parse

async def start_bot():
    await parse()
    scheduler.start()
    await dp.start_polling()
