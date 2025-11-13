### --- Модуль для надсилання нагадувань про початок пари --- ###
from Database_control import control_database
from Keyboards import ok_inline_kb
from text_build import menage_text
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import datetime
import asyncio


# - Функція нагадування про День народження
async def remind_birthday(bot: Bot):
    today_date = datetime.date.today()
    month_number = today_date.month 
    months_lookup = [
        "Січень", "Лютий", "Березень", "Квітень", "Травень", "Червень",
        "Липень", "Серпень", "Вересень", "Жовтень", "Листопад", "Грудень"
    ]
    mounth = months_lookup[month_number - 1]
    today = today_date.day
    users = await control_database.get_users_remind_birthday(today, mounth)
    for user in users:
        photo = (await bot.get_user_profile_photos(user_id = user["birthday_member_id"])).photos[0][-1]
        name = await bot.get_chat(chat_id = user["birthday_member_id"])
        text = await menage_text.remind_birthday(name.full_name)
        await bot.send_photo(chat_id = user["chat_member_id"], photo = photo.file_id, caption = text, parse_mode = "HTML", reply_markup = ok_inline_kb)


# - Функція нагадування про початок занять
async def remind_lesson(time: str, bot: Bot):
    delete_list = []
    users = await control_database.get_users_remind_lesson(time)

    for user in users:
        user_id = user["chat_member_id"]
        remind_text = await menage_text.remind_lesson_before_text(user["lesson_description"], "15хв.")
        message = await bot.send_message(chat_id = user_id, text = remind_text, parse_mode = "HTML")
        delete_list.append((user_id, message.message_id))
    await asyncio.sleep(600)
    for message in delete_list:
        await bot.delete_message(chat_id = message[0], message_id = message[1])

    delete_list = []
    users = await control_database.get_users_remind_lesson(time)

    for user in users:
        user_id = user["chat_member_id"]
        remind_text = await menage_text.remind_lesson_before_text(user["lesson_description"], "5хв.")
        message = await bot.send_message(chat_id = user_id, text = remind_text, parse_mode = "HTML")
        delete_list.append((user_id, message.message_id))
    await asyncio.sleep(300)
    for message in delete_list:
        await bot.delete_message(chat_id = message[0], message_id = message[1])

    delete_list = []
    users = await control_database.get_users_remind_lesson(time)

    for user in users:
        user_id = user["chat_member_id"]
        remind_text = await menage_text.remind_lesson_start_text(user["lesson_description"], time)
        if user["lesson_link"] != None:
            link_keyb = InlineKeyboardMarkup(
                inline_keyboard = [
                    [InlineKeyboardButton(text = "🤙 Бігом на пару", url = user["lesson_link"])]
                ]
            )
            message = await bot.send_message(chat_id = user["chat_member_id"], text = remind_text, reply_markup = link_keyb, disable_web_page_preview = True, parse_mode = "HTML")
            delete_list.append((user_id, message.message_id))
            continue
        message = await bot.send_message(chat_id = user["chat_member_id"], text = remind_text, parse_mode = "HTML")
        delete_list.append((user_id, message.message_id))
    await asyncio.sleep(3600)
    for message in delete_list:
        await bot.delete_message(chat_id = message[0], message_id = message[1])