from ._core import connection
from asyncpg import Connection


@connection
async def is_exist(text: str, conn: Connection = None):
    q = '''SELECT *
           FROM bot_oldnews
           WHERE content = $1'''
    a = bool(await conn.fetchval(q, text.lower()))
    if a:
        return True

    q = '''INSERT INTO bot_oldnews(content)
           VALUES($1)'''
    await conn.execute(q, text.lower())