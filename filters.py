### --- Модуль експорту власних фільтрів --- ###
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Filter
from aiogram import Bot


# - Фільтр для перевірки типу чату
class ChatTypeFilter(Filter):
    def __init__(self, chat_type: list[str]) -> None:
        self.chat_type = chat_type

    async def __call__(self, obj: Message | CallbackQuery) -> bool:
        if type(obj) == Message:
            return obj.chat.type in self.chat_type
        else:
            return obj.message.chat.type in self.chat_type


# - Фільтр для перевірки чи є користувач адміністратором чату
class AdminFilter(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: Message, bot: Bot) -> bool:
        administrators = await bot.get_chat_administrators(message.chat.id)
        admin_ids = [admin.user.id for admin in administrators]
        return message.from_user.id in admin_ids
    

# - Фільтр для перевірки чи є отримане повідомлення посиланням
class IsMessageLinkFilter(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: Message, bot: Bot, state: FSMContext) -> bool:
        link = None
        if message.entities is None:
            return False
        for entity in message.entities:
            if entity.type == "text_link":
                link = entity.url
                break
            if entity.type == "url":
                link = message.text[entity.offset: entity.offset + entity.length]
                break
        if link is None:
            return False
        await state.update_data(lesson_link = link)
        return True


# - Фільтр для перевірки чи існує повідомлення "менеджер"
class MessageManagerFilter(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: Message, bot: Bot, state: FSMContext):
        data = await state.get_data()
        if data.get("message_id") and data.get("chat_id") is not None:
            try:
                await bot.delete_message(
                    message_id = data.get("message_id"),
                    chat_id = data.get("chat_id")
                )
            except:
                print("Message Manager filter: No message to delete")
                pass
            await state.clear()
        return True