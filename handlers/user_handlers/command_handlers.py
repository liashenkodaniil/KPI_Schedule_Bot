### --- Модуль обробки підкоманд користувача --- ###
from Keyboards import week_type_inline_kb, back_inline_kb, show_schedule_inline_kb, make_inline_del_birth_keyb, back_birth_inline_kb
from Keyboards import birthday_inline_kb
from Database_control import control_database, AddNewLessonCache, DeleteLessonCache, AddNewBirthdayCache, DeleteBirthdayCache
from text_build import menage_text
from .fsm_handlers import fsm_router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F


commands_router = Router()
commands_router.include_router(fsm_router)


#########################################
### - ОБРОБКА ПІДКОМАНД КОРИСТУВАЧА - ###
#########################################
### --- ПІДКОМАНДИ ДНЯ НАРОДЖЕННЯ --- ###
# - Підкоманда перегляду урочистих подій
@commands_router.callback_query(F.data == "look_birth_call")
async def echo_look_birth(callback: CallbackQuery):
    birthdays_text = await menage_text.all_birthdays_text(await control_database.get_info_birthdays(callback.message.chat.id), callback.message.chat.id, callback.message.bot)
    await callback.message.edit_text(text = birthdays_text, parse_mode = "HTML", reply_markup = back_birth_inline_kb)


# - Підкоманда додавання дня народження
@commands_router.callback_query(F.data == "add_birth_call")
async def echo_add_birth(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text = "🥳 Введіть <b>id</b> іменинника: ", reply_markup = None, parse_mode = "HTML")
    await state.set_state(AddNewBirthdayCache.birth_member_id)


# - Підкоманда видалення дня народження
@commands_router.callback_query(F.data == "delete_birth_call")
async def echo_delete_birth(callback: CallbackQuery, state: FSMContext):
    del_keyb = await make_inline_del_birth_keyb(await control_database.get_info_birthdays(callback.from_user.id), callback.message.bot)
    await callback.message.edit_text(text = "<blockquote><b>Кого ви бажаєте видалити ? 😭</b></blockquote>", parse_mode = "HTML", reply_markup = del_keyb)
    await state.set_state(DeleteBirthdayCache.del_moment)


# - Підкоманда повернення назад до операцій днів народження
@commands_router.callback_query(F.data == "back_birth")
async def echo_back_birth(callback: CallbackQuery):
    await callback.message.edit_text(text = "🎂 Бажаєте когось привітати?", reply_markup = birthday_inline_kb)


### --- ПІДКОМАНДИ ПЕРЕГЛЯДУ РОЗКЛАДУ --- ###
# - Підкоманда учорашнього розкладу
@commands_router.callback_query(F.data == "yesterday_call")
async def echo_yesterday(callback: CallbackQuery):
    schedule_info = await menage_text.day_schedule_text("Учорашній розклад", await control_database.get_yesterday_schedule(callback.from_user.id))
    await callback.message.edit_text(text = schedule_info, parse_mode = "HTML", reply_markup = back_inline_kb, disable_web_page_preview = True)


# - Підкоманда завтрашнього розкладу
@commands_router.callback_query(F.data == "tomorrow_call")
async def echo_tomorrow(callback: CallbackQuery):
    schedule_info = await menage_text.day_schedule_text("Завтрашній розклад", await control_database.get_tomorrow_schedule(callback.from_user.id))
    await callback.message.edit_text(text = schedule_info, parse_mode = "HTML", reply_markup = back_inline_kb, disable_web_page_preview = True)


# - Підкоманда сьогоднішнього розкладу
@commands_router.callback_query(F.data == "today_call")
async def echo_today(callback: CallbackQuery):
    schedule_info = await menage_text.day_schedule_text("Сьогоднішній розклад", await control_database.get_today_schedule(callback.from_user.id))
    await callback.message.edit_text(text = schedule_info, parse_mode = "HTML", reply_markup = back_inline_kb, disable_web_page_preview = True)


# - Підкоманда повернення до меню варіацій розкладів
@commands_router.callback_query(F.data == "back")
async def echo_schedule_back(callback: CallbackQuery):
    await callback.message.edit_text(text = "Котрий розклад бажаєте побачити?", reply_markup = show_schedule_inline_kb)


### -------- ПІДКОМАНДИ РЕДАГУВАННЯ РОЗКЛАДУ ------- ###
# - Підкоманда додання нової події
@commands_router.callback_query(F.data == "add_call")
async def echo_add(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text = "На котрий тиждень бажаєте додати заняття?", reply_markup = week_type_inline_kb)
    await state.set_state(AddNewLessonCache.lesson_week_type)


# - Підкоманда видалення події
@commands_router.callback_query(F.data == "delete_call")
async def echo_delete(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text = "На котрому тижні ви бажаєте видалити заняття?", reply_markup = week_type_inline_kb)
    await state.set_state(DeleteLessonCache.lesson_week_type)


### -------- ЗАГАЛЬНІ СПІЛЬНІ ПІДКОМАНДИ ------- ###
# - Підкоманда обривання процесу
@commands_router.callback_query(F.data == "end_call")
async def echo_end(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
