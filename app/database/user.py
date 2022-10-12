from ._core import connection
from asyncpg import Connection


@connection
async def add(id: int, conn: Connection = None):
    q = '''INSERT INTO bot_user(id)
           VALUES($1)
           ON CONFLICT(id) DO NOTHING'''

    await conn.execute(q, id)


@connection
async def get_by_phrases(text: str, conn: Connection = None):
    q = '''SELECT DISTINCT usr.id
           FROM bot_user AS usr
           INNER JOIN bot_phrase AS phrase ON phrase.user_id = usr.id
           WHERE $1 LIKE '%' || phrase.text || '%'
           '''
    return [x.get('id') for x in await conn.fetch(q, text.lower())]


@connection
async def get_phrases(user_id: int, conn: Connection = None):
    q = '''SELECT phrase.id, phrase.text
           FROM bot_user AS usr
           INNER JOIN bot_phrase AS phrase ON phrase.user_id = usr.id
           WHERE usr.id = $1
           '''
    return [dict(x) for x in await conn.fetch(q, user_id)]


@connection
async def add_phrase(phrase: str, user_id: int, conn: Connection = None):
    q = '''INSERT INTO bot_phrase(user_id, text)
           SELECT usr.id, $1
           FROM bot_user AS usr
           WHERE usr.id = $2'''
    await conn.execute(q, phrase.lower(), user_id)


@connection
async def delete_phrase(phrase_id: int, user_id: int, conn: Connection = None):
    q = '''DELETE FROM bot_phrase
           WHERE id = $1 AND user_id = $2'''
    await conn.execute(q, phrase_id, user_id)

