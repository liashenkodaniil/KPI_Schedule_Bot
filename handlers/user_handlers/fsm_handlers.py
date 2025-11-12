### --- Модуль обробки діалогів користувача --- ###
from Keyboards import day_inline_kb, para_time_inline_kb, none_link, yes_no_inline_kb
from Keyboards import final_add_inline_kb, events_inline_kb, make_inline_del_keyb
from Database_control import control_database, AddNewLessonCache, DeleteLessonCache
from text_build import menage_text
from filters import IsMessageLinkFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import Router


fsm_router = Router()


#####################################################
### - ОБРОБКА КОМАНД ВІДПОВІДНО АВТОМАТУ СТАНІВ - ###
#####################################################
### - ДІАЛОГ НА ДОДАЧУ ЗАНЯТТЯ - ###
# - Обираємо тиждень
@fsm_router.callback_query(AddNewLessonCache.lesson_week_type)
async def talk_event_week_type(callback: CallbackQuery, state: FSMContext):
    await state.update_data(lesson_week_type = callback.data)
    await callback.message.edit_text(text = "На котрий день тижня ви бажаєте додати заняття?", reply_markup = day_inline_kb)
    await state.set_state(AddNewLessonCache.lesson_day)


# - Обираємо день тижня 
@fsm_router.callback_query(AddNewLessonCache.lesson_day)
async def talk_event_day(callback: CallbackQuery, state: FSMContext):
    await state.update_data(lesson_day = callback.data)
    await callback.message.edit_text(text = "О котрій ваша пара розпочинається?", reply_markup = para_time_inline_kb)
    await state.set_state(AddNewLessonCache.lesson_time)


# - Обираємо час коли розпочинається пара
@fsm_router.callback_query(AddNewLessonCache.lesson_time)
async def talk_event_time(callback: CallbackQuery, state: FSMContext):
    await state.update_data(lesson_time = callback.data)
    await callback.message.edit_text(text = "Введіть назву пари:", reply_markup = None)
    await state.set_state(AddNewLessonCache.lesson_description)


# - Вказуємо конкретно що це за подія
@fsm_router.message(AddNewLessonCache.lesson_description)
async def talk_event_description(message: Message, state: FSMContext):
   await state.update_data(lesson_description = message.text)
   data = await state.get_data()
   await message.delete()
   await message.bot.edit_message_text(
       text = "Вкажіть лінк до вашої пари: ",
       chat_id = data.get("chat_id"),
       message_id = data.get("message_id"),
       reply_markup = none_link
   )
   await state.set_state(AddNewLessonCache.lesson_link)


# - Вказуємо можливий link до події
@fsm_router.message(AddNewLessonCache.lesson_link, IsMessageLinkFilter())
async def talk_event_link(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.delete()
    await message.bot.edit_message_text(
        text = "Ви бажаєте отримувати нагадування до цієї пари?",
        chat_id = data.get("chat_id"),
        message_id = data.get("message_id"),
        reply_markup = yes_no_inline_kb
    )
    await state.set_state(AddNewLessonCache.lesson_remind)


@fsm_router.callback_query(AddNewLessonCache.lesson_link)
async def talk_event_link_callback(callback: CallbackQuery, state: FSMContext):
    await state.update_data(lesson_link = callback.data)
    await callback.message.edit_text(text = "Ви бажаєте отримувати нагадування до цієї пари?", reply_markup = yes_no_inline_kb)
    await state.set_state(AddNewLessonCache.lesson_remind)


# - Вказуємо чи отримувати нагадування чи ні
@fsm_router.callback_query(AddNewLessonCache.lesson_remind)
async def talk_event_remind(callback: CallbackQuery, state: FSMContext):
    await state.update_data(lesson_remind = callback.data)
    data = await state.get_data()
    new_lesson_text = await menage_text.add_lesson_text(data)
    await callback.message.edit_text(text = new_lesson_text, parse_mode = "HTML", reply_markup = final_add_inline_kb)
    await state.set_state(AddNewLessonCache.lesson_end)


# - Завершення діалогу додавання нової події
@fsm_router.callback_query(AddNewLessonCache.lesson_end)
async def talk_event_add_end(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await control_database.add_new_lesson(data, callback.from_user.id)
    await state.clear()
    await state.update_data(
        message_id = callback.message.message_id,
        chat_id = callback.message.chat.id
    )
    await callback.message.edit_text(text = "Бажаєте працювати із розкладом?", reply_markup = events_inline_kb)


### - ДІАЛОГ НА ВИДАЛЕННЯ ЗАНЯТТЯ - ###
# - Обираємо тиждень
@fsm_router.callback_query(DeleteLessonCache.lesson_week_type)
async def talk_event_week_type(callback: CallbackQuery, state: FSMContext):
    await state.update_data(lesson_week_type = callback.data)
    await callback.message.edit_text(text = "Оберіть день тижня: ", reply_markup = day_inline_kb)
    await state.set_state(DeleteLessonCache.lesson_day)


# - Обираємо день тижня 
@fsm_router.callback_query(DeleteLessonCache.lesson_day)
async def talk_event_day(callback: CallbackQuery, state: FSMContext):
    await state.update_data(lesson_day = callback.data)
    data = await state.get_data()
    delete_inline_keyb = await make_inline_del_keyb(await control_database.catch_day_events(data, callback.from_user.id))
    await callback.message.edit_text(text = "Оберіть пару котру бажаєте видалити: ", reply_markup = delete_inline_keyb)
    await state.set_state(DeleteLessonCache.lesson_description)


# - Обираємо заняття
@fsm_router.callback_query(DeleteLessonCache.lesson_description)
async def talk_delete_yes_no(callback: CallbackQuery, state: FSMContext):
    await control_database.delete_lesson(callback.data, callback.from_user.id)
    await state.clear()
    await state.update_data(
        message_id = callback.message.message_id,
        chat_id = callback.message.chat.id
    )
    await callback.message.edit_text(text = "Бажаєте працювати із розкладом?", reply_markup = events_inline_kb)


##################################
### - ХЕНДЛЕРИ СОРТУВАЛЬНИКИ - ###
##################################
# - Використовуємо даний хендлер аби видаляти повідомлення, що не пройшли жодної перевірки
@fsm_router.message()
async def delete_user_rubbish(message: Message):
    await message.delete()