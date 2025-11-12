### --- Модуль занесення початкових даних до бази даних --- ###
from Database_control import control_database
from filters import MessageManagerFilter
from Keyboards import main_kb
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Router


# - Ініціалізація роутера для обробки команди /start
start_router = Router()


# - Початковий текст привітання та загальної інформації
WELCOME_TEXT = """
Вітаємо!

Даний телеграм-бот був створений із метою
упорядкування ваших життєвих подій та
покращення вашого тижневого розкладу!

Даний бот здатен працювати як і з подіями
конкретного користувача, так і з подіями,
що стосуються конкретного чату.

Якщо ви бажате працювати з ботом особисто,
можете скористатися головним меню нижче.

Якщо ви бажаєте працювати з ботом у рамках
конкретного чату, дотримуйтесь інструкцій,
описаних нижче:
1) Ви маєте бути адміністратором чату.
2) Додайте бота до вашого чату.
3) Надішліть команду /start
     безпосередньо у вашому чаті.
4) Налаштуйте бота відповідно до 
     ваших потреб за допомогою
     доступних вам команд.

Список доступних команд можна отримати
за допомогою команди /help

Бажаємо приємного корситування!
"""


# - Повідомлення про подяку за повторний запуск
RETURNING_TEXT = """
Дякуємо вам за повернення!
Ваші основні дані були збережені.
"""


# - Обробник команди /start
@start_router.message(CommandStart(), MessageManagerFilter())
async def process_start_command(message: Message, state: FSMContext):
    await message.delete()
    # - Отримання зовнішнього ідентифікатора 
    if message.chat.type == "private":
        new_id = message.from_user.id
    if message.chat.type in ["group", "supergroup", "channel"]:
        # - Перевірка чи є користувач адміністратором чату:
        administrators = await message.chat.get_administrators()
        admin_ids = [admin.user.id for admin in administrators]
        if message.from_user.id in admin_ids:
            new_id = message.chat.id
        else:
            await message.answer("Лише адміністратори чатів можуть ініціювати роботу ;(")
            return
    # - Перевірка на наявність отриманого ідентифікатора у базі даних
    search_result = await control_database.search_id(new_id)
    if search_result is False:
        # - Додавання нового користувача до бази даних
        await control_database.add_user(new_id, message.chat.type, message.date)
        await message.answer(WELCOME_TEXT, reply_markup = main_kb)
    if search_result is True:
        # - Надсилаємо інформаціне повідомлення
        await message.answer(RETURNING_TEXT, reply_markup = main_kb)