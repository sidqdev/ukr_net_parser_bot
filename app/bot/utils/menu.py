from .buttons import InlineKeyboard, HardInlineKeyboard
from aiogram.dispatcher.storage import FSMContext
from app.database import user


async def main(state: FSMContext):
    text = 'Головне меню'
    buttons = [
        {'text': 'Про бот', 'data': 'info'},
        {'text': 'Ключові слова', 'data': 'phrases'}
    ]
    await state.set_state('main')
    return {
        'text': text,
        'reply_markup': InlineKeyboard(*buttons)
    }
    

async def info(state: FSMContext):
    text = 'Якась инфа про бот'
    buttons = [
        {'text': 'Назад', 'data': 'main'},
    ]
    await state.set_state('info')
    return {
        'text': text,
        'reply_markup': InlineKeyboard(*buttons)
    }


async def phrases(user_id: int, state: FSMContext):
    await state.set_state('phrases')
    text = 'Ваші ключові слова, щоб добавити просто напішіть'
    user_phrases = await user.get_phrases(user_id)
    buttons = []
    for phrase in user_phrases:
        buttons.append(
            [{'text': phrase.get('text'), 'data': None}, {'text': 'Видалити', 'data': f'delete_{phrase.get("id")}'}]
        )

    buttons.append([
        {'text': 'Додати ключевое слово', 'data': 'add_phrase'},
    ])
    buttons.append([
        {'text': 'Назад', 'data': 'main'},
    ])
    return {
        'text': text,
        'reply_markup': HardInlineKeyboard(buttons)
    }


async def add_phrase(state: FSMContext):
    await state.set_state('add_phrase')
    text = 'Відправте ключове слово'
    return {
        'text': text
    }