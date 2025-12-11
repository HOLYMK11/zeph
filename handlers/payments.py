from aiogram import Router
from aiogram.filters import Command
from services.payments import gen_pid, save, list_all
from services.ocr import parse_url
from ui.keyboards import payment_kb
def register_payments(dp):
    router = Router()
    @router.message(Command('buy'))
    async def buy(m):
        await m.reply('Send payment screenshot and then reply with /verify')
    @router.message(Command('verify'))
    async def verify(m):
        if not m.reply_to_message or not m.reply_to_message.photo:
            await m.reply('Reply to your payment image with /verify')
            return
        f = await m.reply_to_message.photo[-1].get_file()
        url = f.file_path
        pid = gen_pid()
        await m.reply('Parsing image...')
        parsed = await parse_url(url)
        save(pid, {'user': m.from_user.id, 'file': url, 'parsed': parsed})
        kb = payment_kb(pid)
        await m.reply(f'Payment submitted. ID: {pid}', reply_markup=kb)
    dp.include_router(router)
