import asyncio
from .loader import scheduler, bot 
from app.database import user, content
import aiohttp 
import bs4

INTERVAL = 600


async def parse_ukrnet():
    news = list()
    async with aiohttp.ClientSession() as session:
        async with session.get('https://my.ua/') as resp:
            resp.raise_for_status()
            html = await resp.text()
            soup = bs4.BeautifulSoup(html, 'html.parser')
            items = soup.find('main').find_all('a', {'data-internal': "true"})
            for i in items:
                text_item = i.find('h4')
                if not text_item:
                    continue
                text = text_item.text
                url = i['href']
                news.append(
                    {'Title': text, 'Url': 'https://my.ua' + url, 'Date': ''}
                )
            return news[:10][::-1]

async def parse():

    news = await parse_ukrnet()
    for new in news:
        if await content.is_exist(new.get('Title')):
            continue
        users = await user.get_by_phrases(new.get('Title'))
        link = new.get('Url')
        message = f'''<a href="{link}">{new.get('Title')}</a>'''
        for user_id in users:
            try:
                await bot.send_message(user_id, message, disable_web_page_preview=False)
            finally:
                await asyncio.sleep(0.04)
        

scheduler.add_job(parse, 'interval', seconds=INTERVAL)

