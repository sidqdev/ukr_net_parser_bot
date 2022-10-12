from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher.storage import FSMContext
from app.bot.utils import menu
from app.database import user
from app.bot.loader import bot


async def add_phrase(message: Message, state: FSMContext):
    await user.add_phrase(message.text, message.from_user.id)
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