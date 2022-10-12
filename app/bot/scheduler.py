import asyncio
from fake_useragent import UserAgent
from .loader import scheduler, bot 
from app.database import user
from datetime import datetime
import requests 

INTERVAL = 60

async def parse():
    resp = requests.get('https://www.ukr.net/dat/smart/struct.9.ua.json', headers={'User-Agent': UserAgent().random})
    if resp.status_code != 200:
        return
    data = resp.json()
    if not data:
        return

    news = data[0].get('News')
    now = datetime.now()
    now_seconds = now.hour * 3600 + now.minute * 60

    for new in news:
        print(new.get('Title'))
        hours, minutes = map(int, new.get("Date").split(':'))
        seconds = hours * 3600 + minutes * 60
        if not (now_seconds > seconds and now_seconds - seconds < INTERVAL):
            continue
        print(1)
        users = await user.get_by_phrases(new.get('Title'))
        print(users)
        link = 'https://ukr.net' + new.get('Url')
        message = f'''{new.get('Date')} - <a href="{link}">{new.get('Title')}</a>'''
        for user_id in users:
            try:
                await bot.send_message(user_id, message)
            finally:
                await asyncio.sleep(0.04)
        

scheduler.add_job(parse, 'interval', seconds=INTERVAL)

