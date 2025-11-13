### --- Модуль контролю бази даних PostgreSQL --- ###
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.state import State, StatesGroup
import redis.asyncio as aioredis
import datetime
import asyncpg 
import pathlib
import json
import os


# - Машина станів FSM (Стан повідомлення "менеджера")
class MessageManagerCache(StatesGroup):
    # - Дані повідомлення "менеджера"
    message_id = State()
    chat_id = State()


# - Машина станів FSM (Додача нового дня народження)
class AddNewBirthdayCache(StatesGroup):
    birth_member_id = State()
    birth_day = State()
    birth_mounth = State()
    birth_end = State()


# - Машина станів FSM (Видалення дня народження)
class DeleteBirthdayCache(StatesGroup):
    pass


# - Машина станів FSM (Додача нового заняття)
class AddNewLessonCache(StatesGroup):
    lesson_week_type = State()
    lesson_day = State()
    lesson_time = State()
    lesson_description = State()
    lesson_link = State()
    lesson_remind = State()
    lesson_end = State()


# - Машина станів FSM (Видалення заняття)
class DeleteLessonCache(StatesGroup):
    lesson_week_type = State()
    lesson_day = State()
    lesson_description = State()


# - Клас для роботи з основною базою даних
class Databases:
    # - Ініціалізація бази даних
    def __init__(self):
        self.pg_password = os.getenv("POSTGRES_PASSWORD", "11111")
        self.pg_dbname = os.getenv("POSTGRES_NAME", "Schedule")
        self.pg_host = os.getenv("POSTGRES_HOST", "localhost")
        self.pg_user = os.getenv("POSTGRES_USER", "postgres")
        self.pg_port = os.getenv("POSTGRES_PORT", "5432")
        self.redis_host = os.getenv("REDIS_HOST", "redis://localhost/0")
        self.pg_storage = None
        self.redis_pool = None
        self.redis_storage = None
        self.start_data = datetime.datetime.strptime("01.09.2025", "%d.%m.%Y").date()

    # - Створення пулів з'єднань
    async def create_pools(self):
        self.pg_storage = await asyncpg.create_pool(
            password = self.pg_password,
            database = self.pg_dbname,
            host = self.pg_host,
            user = self.pg_user,
            port = self.pg_port,
            min_size = 3,
            max_size = 15
        )
        self.redis_pool = await aioredis.from_url(self.redis_host)
        self.redis_storage = RedisStorage(self.redis_pool)

    # - Функція занесення даних розкладу до Redis
    async def redis_set(self, key, records):
        schedule = [dict(record) for record in records]
        for lesson in schedule:
            lesson["lesson_time"] = str(lesson["lesson_time"])[:5]
        if schedule:
            await self.redis_pool.set(key, json.dumps(schedule), ex = 3600)
        return schedule

    # - Початковий стартовий скрипт для створення бази даних
    async def startpg_script(self): 
        start_script_path = pathlib.Path("sql_scripts/sql_start_script.sql")
        with open(start_script_path, "r", encoding = "utf-8") as file:
            start_script = file.read()
            await self.pg_storage.execute(start_script)

    # - Скрипт на отримання конкретних подій конкретного дня для формування inline-клавіатури
    async def catch_day_events(self, data, user_id):
        script = f'SELECT lesson_id, lesson_time, lesson_description FROM public."Lesson" WHERE chat_member_id = $1 and lesson_week_type = $2 and lesson_day = $3 ORDER BY lesson_time;'
        records = await self.pg_storage.fetch(script, user_id, int(data.get("lesson_week_type")), data.get("lesson_day"))
        inline_list_data = [dict(record) for record in records]
        for lesson in inline_list_data:
            lesson["lesson_time"] = str(lesson["lesson_time"])[:5]
        return inline_list_data

    # - Актуалізація даних редіс
    async def menage_redis(self, id_user):
        if await self.redis_pool.exists(f"schedule:{id_user}:yesterday") == 1:
            await self.redis_pool.delete(f"schedule:{id_user}:yesterday")
            await self.get_yesterday_schedule(id_user)
        else:
            await self.get_yesterday_schedule(id_user)
        if await self.redis_pool.exists(f"schedule:{id_user}:tommorow") == 1:
            await self.redis_pool.delete(f"schedule:{id_user}:tommorow")
            await self.get_tomorrow_schedule(id_user)
        else:
            await self.get_tomorrow_schedule(id_user)
        if await self.redis_pool.exists(f"schedule:{id_user}:today") == 1:
            await self.redis_pool.delete(f"schedule:{id_user}:today")
            await self.get_today_schedule(id_user)
        else:
            await self.get_today_schedule(id_user)

    # - Функція визначення типу тижня
    async def get_week_type(self, number_days):
        if (number_days // 7) % 2 == 0:
            return 1
        else:
            return 2

    # - Перевірка на наявність отриманого ідентифікатора
    async def search_id(self, id):
        search_script = 'SELECT chat_member_id FROM public."Chat member" WHERE chat_member_id = $1;'
        id_result = await self.pg_storage.fetchrow(search_script, id)
        if id_result is None:
            return False
        else:
            return True
    
    # - Додавання нового користувача
    async def add_user(self, id, chat_type, date):
        insert_user_script = 'INSERT INTO public."Chat member" (chat_member_id, chat_type, time_registration) VALUES ($1, $2, $3);'
        await self.pg_storage.execute(insert_user_script, id, chat_type, date)

    # - Додавання нової пари до розкладу
    async def add_new_lesson(self, data, user_id):
        # - Формуємо SQL запит
        add_new_lesson_script = 'INSERT INTO public."Lesson" (chat_member_id, lesson_remind, lesson_week_type, lesson_day, lesson_time, lesson_description, lesson_link) VALUES ($1, $2, $3, $4, $5, $6, $7);'
        # - Парсимо та формуємо час початку пари
        lesson_time = datetime.datetime.strptime(data.get("lesson_time"), "%H:%M").time().replace(tzinfo = datetime.timezone(datetime.timedelta(hours=2)))
        await self.pg_storage.execute(add_new_lesson_script, user_id, data.get("lesson_remind"), int(data.get("lesson_week_type")), data.get("lesson_day"), lesson_time, data.get("lesson_description"), data.get("lesson_link"))
        await self.menage_redis(user_id)

    # - Видалення пари з розкладу
    async def delete_lesson(self, lesson_id, id_user):
        delete_script = 'DELETE FROM public."Lesson" WHERE lesson_id = $1;'
        await self.pg_storage.execute(delete_script, int(lesson_id))
        await self.menage_redis(id_user)

    # - Отримання учорашнього розкладу
    async def get_yesterday_schedule(self, id_user):
        # - Формуємо ключ доступу
        key = f"schedule:{id_user}:yesterday"
        # - Отримуємо тип тижня, день тижня
        yesterday_data = datetime.date.today() - datetime.timedelta(days=1)
        week_type = await self.get_week_type((yesterday_data - self.start_data).days)
        yesterday = (yesterday_data.strftime("%A")).capitalize()
        # - Отримуємо розклад
        if await self.redis_pool.exists(key) == 0:
            script = 'SELECT lesson_time, lesson_description, lesson_link FROM public."Lesson" WHERE chat_member_id = $1 and lesson_week_type = $2 and lesson_day = $3 ORDER BY lesson_time'
            schedule = await self.redis_set(key, await self.pg_storage.fetch(script, id_user, week_type, yesterday))
            return [week_type, yesterday, schedule]
        schedule = json.loads(await self.redis_pool.get(key))
        return [week_type, yesterday, schedule]

    # - Отримання завтрашнього розкладу
    async def get_tomorrow_schedule(self, id_user):
        # - Формуємо ключ доступу
        key = f"schedule:{id_user}:tommorow"
        # - Отримуємо тип тижня, день тижня
        tommorow_data = datetime.date.today() + datetime.timedelta(days=1)
        week_type = await self.get_week_type((tommorow_data - self.start_data).days)
        tommorow = (tommorow_data.strftime("%A")).capitalize()
        # - Отримуємо розклад
        if await self.redis_pool.exists(key) == 0:
            script = 'SELECT lesson_time, lesson_description, lesson_link FROM public."Lesson" WHERE chat_member_id = $1 and lesson_week_type = $2 and lesson_day = $3 ORDER BY lesson_time'
            schedule = await self.redis_set(key, await self.pg_storage.fetch(script, id_user, week_type, tommorow))
            return [week_type, tommorow, schedule]
        schedule = json.loads(await self.redis_pool.get(key))
        return [week_type, tommorow, schedule]
        
    # - Отримання сьогоднішнього розкладу
    async def get_today_schedule(self, id_user):
        # - Формуємо ключ доступу
        key = f"schedule:{id_user}:today"
        # - Отримуємо тип тижня, день тижня
        today_data = datetime.date.today()
        week_type = await self.get_week_type((today_data - self.start_data).days)
        today = (today_data.strftime('%A')).capitalize()
        # - Отримуємо розклад
        if await self.redis_pool.exists(key) == 0:
            script = 'SELECT lesson_time, lesson_description, lesson_link FROM public."Lesson" WHERE chat_member_id = $1 and lesson_week_type = $2 and lesson_day = $3 ORDER BY lesson_time'
            schedule = await self.redis_set(key, await self.pg_storage.fetch(script, id_user, week_type, today))
            return [week_type, today, schedule]
        schedule = json.loads(await self.redis_pool.get(key))
        return [week_type, today, schedule]
    
    # - Отримання списку користувачів котрим необхідно нагадати про початок пари
    async def get_users_remind_lesson(self, time: str):
        data = datetime.date.today()
        day = (data.strftime("%A")).capitalize()
        week_type = await self.get_week_type((data - self.start_data).days)
        get_users_script = 'SELECT chat_member_id, lesson_description, lesson_link FROM public."Lesson" WHERE lesson_remind = $1 and lesson_week_type = $2 and lesson_day = $3 and lesson_time = $4'
        records = await self.pg_storage.fetch(get_users_script, "YES", week_type, day, (datetime.datetime.strptime(time, "%H:%M").time()).replace(tzinfo = datetime.timezone(datetime.timedelta(hours = 2))))
        users = [dict(record) for record in records]
        return users
    
    # - Додавання нового Дня народження
    async def add_birthday(self, new_data, user_id):
        add_script = 'INSERT INTO public."Birthdays" (chat_member_id, birthday_member_id, birthday, birthmounth) VALUES ($1, $2, $3, $4);'
        await self.pg_storage.execute(add_script, user_id, new_data.get("birth_member_id"), int(new_data.get("birth_day")), new_data.get("birth_mounth"))

    # - Отримання списку користувачів, котрим необхідно нагадати за День народження
    async def get_users_remind_birthday(self, today, month):
        get_script = 'SELECT chat_member_id, birthday_member_id FROM public."Birthdays" WHERE birthday = $1 and birthmounth = $2'
        records = await self.pg_storage.fetch(get_script, int(today), str(month))
        users_list = [dict(record) for record in records]
        return users_list

# - Створення екземпляра класу Database для подальшого керування сховищами
control_database = Databases()
