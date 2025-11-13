### --- Модуль обробки головних команд користувача --- ###
from Keyboards import show_schedule_inline_kb, events_inline_kb, birthday_inline_kb
from filters import ChatTypeFilter, MessageManagerFilter
from middlewares import AntSpamPrivate
from .command_handlers import commands_router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router, F


# - Ініціалізація роутера для обробки головних подій користувача
main_router = Router()
main_router.message.outer_middleware(AntSpamPrivate(1.0))
main_router.message.filter(ChatTypeFilter(["private"]))
main_router.callback_query.filter(ChatTypeFilter(["private"]))
main_router.include_router(commands_router)


###############################################
### - ОБРОБКА ГОЛОВНИХ КОМАНД КОРИСТУВАЧА - ###
###############################################
# - Обробник команди "Переглянути тижневий розклад"
@main_router.message(F.text == "🗓 Переглянути розклад занять", MessageManagerFilter())
async def process_view_schedule_command(message: Message, state: FSMContext):
    await message.delete()
    sent_message = await message.answer(text = "Котрий розклад бажаєте побачити?", reply_markup = show_schedule_inline_kb)
    await state.update_data(
        message_id = sent_message.message_id,
        chat_id = sent_message.chat.id
    )


# - Обробник команди "Події"
@main_router.message(F.text == "✍️ Редагувати розклад", MessageManagerFilter())
async def process_events_command(message: Message, state: FSMContext):
    await message.delete()
    sent_message = await message.answer(text = "🗓 Бажаєте працювати із розкладом?", reply_markup = events_inline_kb)
    await state.update_data(
        message_id = sent_message.message_id,
        chat_id = sent_message.chat.id
    )


# - Обробник команди "Дні народження"
@main_router.message(F.text == "🎂 Дні народження", MessageManagerFilter())
async def process_birthday_command(message: Message, state: FSMContext):
    await message.delete()
    sent_message = await message.answer(text = "🎂 Бажаєте когось привітати?", reply_markup = birthday_inline_kb)
    await state.update_data(
        message_id = sent_message.message_id,
        chat_id = sent_message.chat.id
    )