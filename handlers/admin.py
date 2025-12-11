from aiogram import Router
from aiogram.filters import Command
from services.payments import list_all, pop
from services.storage import Storage
from config import OWNER_ID, CAPTION_TEXT, PREMIUM_DAYS
def register_admin(dp):
    router = Router()
    @router.message(Command('admin'))
    async def admin(m):
        if m.from_user.id != OWNER_ID:
            await m.reply('Forbidden')
            return
        pend = list_all()
        if not pend:
            await m.reply('No pending payments')
            return
        keys = list(pend.keys())
        await m.reply('Pending: ' + ','.join(keys))
    @router.callback_query(lambda c: c.data and c.data.startswith('approve_'))
    async def approve(cq):
        pid = cq.data.split('_',1)[1]
        p = pop(pid)
        if not p:
            await cq.answer('Already handled')
            return
        storage = cq.bot['storage']
        storage.add_credits(p['user'], 100)
        storage.set_premium(p['user'], PREMIUM_DAYS)
        await cq.message.edit_text('Approved ' + pid)
        await cq.bot.send_message(p['user'], f'Payment {pid} approved. {CAPTION_TEXT}')
    @router.callback_query(lambda c: c.data and c.data.startswith('reject_'))
    async def reject(cq):
        pid = cq.data.split('_',1)[1]
        p = pop(pid)
        if not p:
            await cq.answer('Already handled')
            return
        await cq.message.edit_text('Rejected ' + pid)
        await cq.bot.send_message(p['user'], f'Payment {pid} rejected. {CAPTION_TEXT}')
    dp.include_router(router)
