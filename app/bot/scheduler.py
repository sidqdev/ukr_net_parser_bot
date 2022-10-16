import asyncio
from .loader import scheduler, bot 
from app.database import user, content
import requests 
import bs4

INTERVAL = 600


def parse_ukrnet():
    news = list()
    ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
    resp = requests.get('https://my.ua/', headers={'User-Agent': ua})
    resp.raise_for_status()
    html = resp.text
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

    news = parse_ukrnet()
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

