import asyncio
from fake_useragent import UserAgent
from .loader import scheduler, bot 
from app.database import user, content
import requests 
import bs4

INTERVAL = 600


def parse_ukrnet():
    news = list()
    ua = UserAgent(use_cache_server=False).random
    # ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36'
    resp = requests.get('https://www.ukr.net/news/main.html', headers={'User-Agent': ua})
    resp.raise_for_status()
    html = resp.text
    soup = bs4.BeautifulSoup(html, 'html.parser')
    for new_item in soup.find('article').find_all('section'):
        time = new_item.find('time').text
        new = new_item.find('a', {'class': 'im-tl_a'})
        title = new.text
        url = new['href']
        news.append(
            {'Title': title, 'Url': url, 'Date': time}
        )

    return news[:10][::-1]

async def parse():

    news = parse_ukrnet()
    for new in news:
        if await content.is_exist(new.get('Title')):
            continue
        users = await user.get_by_phrases(new.get('Title'))
        link = new.get('Url')
        message = f'''{new.get('Date')} - <a href="{link}">{new.get('Title')}</a>'''
        for user_id in users:
            try:
                await bot.send_message(user_id, message, disable_web_page_preview=True)
            finally:
                await asyncio.sleep(0.04)
        

scheduler.add_job(parse, 'interval', seconds=INTERVAL)

