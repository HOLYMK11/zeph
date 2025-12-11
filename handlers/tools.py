from aiogram import Router
from aiogram.filters import Command
def register_tools(dp):
    router = Router()
    @router.message(Command('tools'))
    async def tools_cmd(m):
        await m.reply('Tools menu')
    dp.include_router(router)

