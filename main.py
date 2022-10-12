from dotenv import load_dotenv

load_dotenv()

import asyncio
from app.bot.builder import start_bot

loop = asyncio.get_event_loop()
loop.create_task(start_bot())
loop.run_forever()
