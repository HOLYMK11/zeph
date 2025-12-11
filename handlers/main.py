from aiogram import Router
from aiogram.filters import Command
from ui.keyboards import main_menu
from ui.style import box
def register_main(dp):
    router = Router()
    @router.message(Command('start'))
    async def start_cmd(m):
        storage = m.bot['storage']
        u = storage.ensure_user(m.from_user.id, m.from_user.username)
        text = f"Hello @{m.from_user.username or m.from_user.first_name}!\nCredits: {u.credits}\nPremium: {bool(u.premium_until)}\nDaily AI: {u.daily_ai}/10"
        await m.answer(box('ZEPH MAIN MENU', text), reply_markup=main_menu())
    @router.message(Command('help'))
    async def help_cmd(m):
        await m.reply('/play <song> - plays song\n/ytmp3 <url> - download audio\n/ytmp4 <url> - download video\n/redeem <code> - redeem coupon')
    dp.include_router(router)
