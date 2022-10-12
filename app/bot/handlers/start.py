from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from app.database import user
from app.bot.utils import menu


async def start(message: Message, state: FSMContext):
    await user.add(message.from_user.id)
    await message.answer(**await menu.main(state))


async def get_main(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(**await menu.main(state))
    