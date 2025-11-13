### --- Модуль експорту клавіатур користувача --- ###
from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from Database_control import control_database


############################################
### - ІНІЦІАЛІЗАЦІЯ ГОЛОВНИХ КЛАВІАТУР - ###
############################################
# - Ініціалізація клавіатури головного меню
main_kb = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton(text = "🗓 Переглянути розклад занять")],
        [KeyboardButton(text = "✍️ Редагувати розклад")],
        [KeyboardButton(text = "🎂 Дні народження")]
    ],
    resize_keyboard = True
)


######################################
### - ІНІЦІАЛІЗАЦІЯ ПІДКЛАВІАТУР - ###
######################################
# - Ініціалізація підклавіатури роботи зі святами
birthday_inline_kb = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text = "🗓 Переглянути дні народження 🎂", callback_data = "look_birth_call")],
        [InlineKeyboardButton(text = "✍️ Додати день народження 🎂", callback_data = "add_birth_call")],
        [InlineKeyboardButton(text = "🗑 Видалити день народження 🎂", callback_data = "delete_birth_call")],
        [InlineKeyboardButton(text = "❌ Обірвати процес", callback_data = "end_call")]
    ]
)


# - Ініціалізація підклавіатури місяців
mounth_inline_kb = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text = "Січ.", callback_data = "Січня"),
            InlineKeyboardButton(text = "Лют.", callback_data = "Лютого"),
            InlineKeyboardButton(text = "Бер.", callback_data = "Березня"),
            InlineKeyboardButton(text = "Квіт.", callback_data = "Квітня"),
            InlineKeyboardButton(text = "Трав.", callback_data = "Травня"),
            InlineKeyboardButton(text = "Черв.", callback_data = "Червня"),
        ],
        [
            InlineKeyboardButton(text = "Лип.", callback_data = "Липня"),
            InlineKeyboardButton(text = "Серп.", callback_data = "Серпня"),
            InlineKeyboardButton(text = "Вер.", callback_data = "Вересня"),
            InlineKeyboardButton(text = "Жовт.", callback_data = "Жовтня"),
            InlineKeyboardButton(text = "Лист.", callback_data = "Листопада"),
            InlineKeyboardButton(text = "Груд.", callback_data = "Грудня"),
        ]
    ]
)

# - Ініціалізація підклавіатури підтвердження додавання нового Дня народження
add_new_birthday_inline_kb = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text = "✅ Додати новий День народження", callback_data = "add_new_birthday_final")]
    ]
)

# - Ініціалізація підклавіатури перегляду тижневого розкладу
show_schedule_inline_kb = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text = "◀️ Учорашній розклад", callback_data = "yesterday_call"), 
         InlineKeyboardButton(text = "Завтрашній розклад ▶️", callback_data = "tomorrow_call")],
        [InlineKeyboardButton(text = "🔽 Сьогоднішній розклад", callback_data = "today_call")],
        [InlineKeyboardButton(text = "❌ Обірвати процес", callback_data = "end_call")]
    ]
)


# - Ініціалізація підклавіатури роботи з подіями
events_inline_kb = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text = "✅ Додати нове заняття", callback_data = "add_call")],
        [InlineKeyboardButton(text = "🗑 Видалити заняття", callback_data = "delete_call")],
        [InlineKeyboardButton(text = "❌ Обірвати процес", callback_data = "end_call")]
    ]
)


# - Ініціалізація підклавіатури додаткових опцій
additional_options_inline_kb = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text = "Додаткові команди", callback_data = "help_call")],
        [InlineKeyboardButton(text = "❌ Обірвати процес", callback_data = "end_call")]
    ]
)


###################################################
### - ІНІЦІАЛІЗАЦІЯ КЛАВІАТУР АВТОМАТІВ СТАНУ - ###
###################################################
# - Ініціалізація клавіатури типу тижня
week_type_inline_kb = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text = "Тиждень 1️⃣", callback_data = "1"),
         InlineKeyboardButton(text = "Тиждень 2️⃣", callback_data = "2")]
    ]
)


# - Ініціалізація клавіатури днів тижня
day_inline_kb = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text = "Понеділок", callback_data = "Понеділок")],
        [InlineKeyboardButton(text = "Вівторок", callback_data = "Вівторок")],
        [InlineKeyboardButton(text = "Середа", callback_data = "Середа")],
        [InlineKeyboardButton(text = "Четверг", callback_data = "Четвер")],
        [InlineKeyboardButton(text = "П'ятниця", callback_data = "П'ятниця")],
        [InlineKeyboardButton(text = "Субота", callback_data = "Субота")],
        [InlineKeyboardButton(text = "Неділя", callback_data = "Неділя")]
    ]
)


# - Ініціалізація клавіатури часу початку пари
para_time_inline_kb = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text = "08:30", callback_data = "08:30"), InlineKeyboardButton(text = "10:25", callback_data = "10:25"),
         InlineKeyboardButton(text = "12:20", callback_data = "12:20"), InlineKeyboardButton(text = "14:15", callback_data = "14:15")],
        [InlineKeyboardButton(text = "16:10", callback_data = "16:10"), InlineKeyboardButton(text = "18:05", callback_data = "18:05"),
         InlineKeyboardButton(text = "20:00", callback_data = "20:00")]
    ]
)


# - Ініціалізація клавіатури варіантів вибору Так/Ні
yes_no_inline_kb = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text = "✅ Так", callback_data = "YES"), InlineKeyboardButton(text = "❌ Ні", callback_data = "NO")]
    ]
)


# - Ініціалізація клавіатури затвердження додавання події
final_add_inline_kb = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text = "✅ Додати заняття", callback_data = "final_add_event")]
    ]
)

# - Ініціалізація клавіатури відсутності link
none_link = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text = "🚫 Без посилання", callback_data = "None")]
    ]
)


# - Ініціалізація клавіатури повернення на попередній стан
back_inline_kb = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text = "👈 Назад", callback_data = "back")]
    ]
)


# - Функція створення динамічної клавіатури для видалення заняття
async def make_inline_del_keyb(list_lessons):
    delete_keyb = []
    for lesson in list_lessons:
        delete_keyb.append([InlineKeyboardButton(text = lesson["lesson_time"] + " 👉 " + lesson["lesson_description"], callback_data = str(lesson["lesson_id"]))])
    return InlineKeyboardMarkup(inline_keyboard = delete_keyb)