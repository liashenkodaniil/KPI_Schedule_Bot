### --- Модуль для надсилання нагадувань про початок пари --- ###
from Database_control import control_database
from text_build import menage_text
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio


# - Функція нагадування про початок занять
async def remind_lesson(time: str, bot: Bot):
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