from aiogram import Router
from aiogram.filters import Command
from random import choice, randint
def register_games(dp):
    router = Router()
    @router.message(Command('rps'))
    async def rps(m):
        user = m.get_command_arg()
        if not user:
            await m.reply('Usage /rps <rock|paper|scissors>')
            return
        bot = choice(['rock','paper','scissors'])
        if user==bot:
            await m.reply(f'Draw. Bot: {bot}')
        elif (user=='rock' and bot=='scissors') or (user=='paper' and bot=='rock') or (user=='scissors' and bot=='paper'):
            await m.reply(f'You win. Bot: {bot}')
        else:
            await m.reply(f'You lose. Bot: {bot}')
    @router.message(Command('dice'))
    async def dice(m):
        v = randint(1,6)
        await m.reply(f'You rolled: {v}')
    dp.include_router(router)
