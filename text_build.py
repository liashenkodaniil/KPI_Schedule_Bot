### --- Модуль для побудови повідомлень на основі отриманих даних --- ###


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

    # - Формування тексту повідомлення-нагадування
    async def remind_lesson_start_text(self, lesson_description, time):
        remind_text = f'''<blockquote><b>🔔 Розпочалась пара</b></blockquote>'''
        remind_text += f'''\n\n<code><b>{time}</b></code>      <b>{lesson_description}</b>'''
        return remind_text


menage_text = PerfomeText()