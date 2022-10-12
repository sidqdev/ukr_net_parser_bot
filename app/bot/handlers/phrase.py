from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher.storage import FSMContext
from app.bot.utils import menu
from app.database import user
from app.bot.loader import bot


async def add_phrase(message: Message, state: FSMContext):
    resp = await user.add_phrase(message.text, message.from_user.id)
    if resp == 'already_exist':
        await message.answer('Таке слово вже є')
    if resp == 'too_many_phrases':
        await message.answer('Забагато слів')
        
    data = await state.get_data()
    await message.delete()
    await bot.delete_message(message.from_user.id, data.get('message_id'))
    msg = await message.answer(**await menu.phrases(message.from_user.id, state))
    await state.update_data({'message_id': msg.message_id})


async def delete_phrase(callback: CallbackQuery, state: FSMContext):
    if not callback.data.startswith('delete_'):
        return
    
    phrase_id = int(callback.data.split("_")[-1])
    await user.delete_phrase(phrase_id, callback.from_user.id)
    msg = await callback.message.edit_text(**await menu.phrases(callback.from_user.id, state))
    await state.update_data({'message_id': msg.message_id})


async def fast_add_phrase(message: Message, state: FSMContext):
    await state.update_data({'phrase': message.text})
    await message.answer(**await menu.fast_add_phrase(state))


async def fast_add_phrase_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await user.add_phrase(data.get('phrase'), callback.from_user.id)
    msg = await callback.message.edit_text(**await menu.phrases(callback.from_user.id, state))
    await state.update_data({'message_id': msg.message_id})