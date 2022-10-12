from aiogram.types import CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from app.bot.utils import menu


async def main(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'info':
        await callback.message.edit_text(**await menu.info(state))
        return

    if callback.data == 'phrases':
        message = await callback.message.edit_text(**await menu.phrases(callback.from_user.id, state))
        await state.update_data({'message_id': message.message_id})
        return
        