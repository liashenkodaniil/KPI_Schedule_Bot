from aiogram import BaseMiddleware
from aiogram.types import Message
from cachetools import TTLCache
from typing import Callable, Dict, Awaitable, Any


# - Middleware 
class AntSpamPrivate(BaseMiddleware):
    def __init__(self, slow_mode_delay: float = 1.0):
        self.cache = TTLCache(maxsize = 2500, ttl = slow_mode_delay)

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        if user_id in self.cache:
            await event.delete()
            return
        
        self.cache[user_id] = True
        return await handler(event, data)