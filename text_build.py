### --- Модуль для побудови повідомлень на основі отриманих даних --- ###
from aiogram import Bot


class PerfomeText:
    # - Формування тексту розкладу конкретного дня
    async def day_schedule_text(self, type_schedule: str, schedule: list):
        text_schedule = f'''<blockquote><i>{type_schedule}</i></blockquote>'''
        text_schedule += f'''\n<blockquote><b>ТИЖДЕНЬ №{schedule[0]}</b>\n<b>{schedule[1]}:</b></blockquote>'''
        time = ""
        for lesson in schedule[2]:
            if time != lesson["lesson_time"]:
                time = lesson["lesson_time"]
                text_schedule += f'''\n\n<blockquote><b>    {lesson["lesson_time"]}</b></blockquote>'''
            text_schedule += f'''\n<b><i>{lesson["lesson_description"]}</i></b>    '''
            if lesson["lesson_link"] != "None":
                text_schedule += f'''<a href = "{lesson["lesson_link"]}"><i>посилання</i></a>'''
        return text_schedule

    # - Формування тексту інформації додавання нового заняття
    async def add_lesson_text(self, new_data):
        new_lesson_text = f'''<blockquote><b>Нагадування: </b></blockquote>'''
        if new_data.get("lesson_remind") == "YES":
            new_lesson_text += f'''\n✅'''
        else:
            new_lesson_text += f'''\n❌'''
        new_lesson_text += f'''\n\n<blockquote><b>Тиждень: </b></blockquote>'''
        new_lesson_text += f'''\n<i>{new_data.get("lesson_week_type")}</i>'''
        new_lesson_text += f'''\n\n<blockquote><b>День: </b></blockquote>'''
        new_lesson_text += f'''\n<i>{new_data.get("lesson_day")}</i>'''
        new_lesson_text += f'''\n\n<blockquote><b>Час: </b></blockquote>'''
        new_lesson_text += f'''\n<i>{new_data.get("lesson_time")}</i>'''
        new_lesson_text += f'''\n\n<blockquote><b>Пара: </b></blockquote>'''
        new_lesson_text += f'''\n<i>{new_data.get("lesson_description")}</i>'''
        if new_data.get("lesson_link") != "None":
            new_lesson_text += f'''\n\n<blockquote><b>Посилання: </b></blockquote>'''
            new_lesson_text += f'''\n<a href = "{new_data.get("lesson_link")}"><i>Посилання на пару</i></a>'''
        return new_lesson_text

    # - Формування тексту інформації додавання нового дня народження
    async def add_birthday_text(self, new_data, bot: Bot):
        birthday_member = await bot.get_chat(chat_id = int(new_data.get("birth_member_id")))
        birthday_member_photo = (await bot.get_user_profile_photos(user_id = new_data.get("birth_member_id"))).photos[0][-1]
        birthday_text = f'''<blockquote><b>Бажаєте додати нагадування до Дня народження: </b></blockquote>'''
        birthday_text += f'''🥳<blockquote><b>{new_data.get("birth_day")} {new_data.get("birth_mounth")}</b></blockquote>🥳'''
        birthday_text += f'''\n🎂 <b><i>{birthday_member.full_name}</i></b> 🎂\n\n'''
        return [birthday_text, birthday_member_photo.file_id]

    # - Формування тексту повідолмення-нагадування про початок заняття за декілька хвилин до самого заняття
    async def remind_lesson_before_text(self, lesson_description, time):
        remind_text = f'''<blockquote><b>❕УВАГА, через {time} розпочнеться заняття:</b></blockquote>'''
        remind_text += f'''\n\n<i>{lesson_description}</i>'''
        return remind_text

    # - Формування тексту повідомлення-нагадування про конкретний початок заняття
    async def remind_lesson_start_text(self, lesson_description, time):
        remind_text = f'''<blockquote><b>🔔 Розпочалась пара</b></blockquote>'''
        remind_text += f'''\n\n<code><b>{time}</b></code>      <b>{lesson_description}</b>'''
        return remind_text
    
    # - Формування тексту нагадування про День народження
    async def remind_birthday(self, name):
        remind_text = f'''<blockquote>🎉🎉🎉 Сьогодні вітаємо <i>{name}</i> !</blockquote>'''
        remind_text += f'''\n\n<i>У цієї чудової людини сьогодні День народження!\n\n</i>'''
        return remind_text
    
    # - Формування тексту усіх записів днів народжень
    async def all_birthdays_text(self, list_user, user_id, bot: Bot):
        birthdays_text = f'''<blockquote><b>🎂 <i>Ваш список іменинників</i> 🎂</b></blockquote>'''
        for birthday in list_user:
            birthdays_text += f'''\n\n<blockquote><i>🎂 {birthday["birthday"]} {birthday["birthmounth"]}</i></blockquote>'''
            birthdays_text += f'''\n<b><i>{(await bot.get_chat(chat_id = birthday["birthday_member_id"])).full_name}</i></b>'''
        return birthdays_text


menage_text = PerfomeText()