from aiogram import Router
from aiogram.filters import Command
from services.ai_api import openai_chat
def register_ai(dp):
    router = Router()
    @router.message(Command('jarvis'))
    async def jarvis(m):
        arg = m.get_command_arg()
        if not arg:
            await m.reply('Usage /jarvis <prompt>')
            return
        res = await openai_chat(arg)
        await m.reply(res)
    dp.include_router(router)
