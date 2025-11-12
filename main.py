### --- Модуль початкової точки запуску програми --- ###
from handlers.start_actions import start_router
from handlers.user_handlers.main_handlers import main_router
from Database_control import control_database
from reminder import remind_lesson
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher
import asyncio
import locale
import os


# - Визначення української локалі для встановлення часових українських стандартів
locale_name = os.getenv("LOCALE_NAME", "ukrainian")
locale.setlocale(locale.LC_TIME, locale_name)


# - Ініціалізація нагадувача
scheduler = AsyncIOScheduler(timezone = "Europe/Kyiv")


# - Ініціалізація бота та диспетчера
TOKEN_API = os.getenv("TOKEN_API", "7829631908:AAFr-Ef7xu0Om0U4SRCSQ_qGzZ-4JVwCJXI")
bot = Bot(TOKEN_API)


async def main():
    # - Підключення до бази даних
    await control_database.create_pools()
    await control_database.startpg_script()
    disp = Dispatcher(storage = control_database.redis_storage)

    # - Підключення необхідних роутерів
    disp.include_router(start_router)
    disp.include_router(main_router)

    # - Запуск регулярної фонової задачі для надсилання нагадувань про початок самої пари
    scheduler.add_job(remind_lesson, trigger = "cron", hour = 14, minute = 45, kwargs = {'time': '15:00', 'bot': bot})
    scheduler.add_job(remind_lesson, trigger = "cron", hour = 10, minute = 10, kwargs = {'time': '10:25', 'bot': bot})
    scheduler.add_job(remind_lesson, trigger = "cron", hour = 12, minute = 5, kwargs = {'time': '12:20', 'bot': bot})
    scheduler.add_job(remind_lesson, trigger = "cron", hour = 14, minute = 0, kwargs = {'time': '14:15', 'bot': bot})
    scheduler.add_job(remind_lesson, trigger = "cron", hour = 15, minute = 55, kwargs = {'time': '16:10', 'bot': bot})
    scheduler.add_job(remind_lesson, trigger = "cron", hour = 17, minute = 50, kwargs = {'time': '18:05', 'bot': bot})
    scheduler.add_job(remind_lesson, trigger = "cron", hour = 18, minute = 45, kwargs = {'time': '20:00', 'bot': bot})
    scheduler.start()

    # - Запуск бота (подібний варіант придатний для тестування -> необхідно виконати перехід на webhook)
    await bot.delete_webhook(drop_pending_updates = True)
    print("Bot is running ...")
    await disp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
