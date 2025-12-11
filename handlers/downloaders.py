from aiogram import Router
from aiogram.filters import Command
from services.downloader import download_audio, download_video, ffmpeg_available
from services.thumbnail import fetch, cleanup
def register_downloader(dp):
    router = Router()
    @router.message(Command('play'))
    async def play(m):
        arg = m.get_command_arg()
        if not arg:
            await m.reply('Usage: /play <song name>')
            return
        query = arg if arg.startswith('http') else f'ytsearch1:{arg}'
        pmsg = await m.reply('Processing ' + '⚙️')
        if not ffmpeg_available():
            await pmsg.edit_text('ffmpeg/ffprobe not found. Install ffmpeg.')
            return
        res = await download_audio(query)
        if not res or not res.get('file'):
            await pmsg.edit_text('No result found.')
            return
        thumb = res.get('thumbnail')
        if thumb:
            tpath = fetch(thumb)
            if tpath:
                await m.answer_photo(open(tpath,'rb'))
                cleanup(tpath)
        await m.answer_audio(open(res['file'],'rb'), caption=res['info'].get('title',''))
        try:
            cleanup(res['file'])
        except:
            pass
        await pmsg.delete()
    @router.message(Command('ytmp4'))
    async def ytmp4(m):
        arg = m.get_command_arg()
        if not arg:
            await m.reply('Usage: /ytmp4 <url or query>')
            return
        query = arg if arg.startswith('http') else f'ytsearch1:{arg}'
        pmsg = await m.reply('Processing ' + '⚙️')
        if not ffmpeg_available():
            await pmsg.edit_text('ffmpeg/ffprobe not found. Install ffmpeg.')
            return
        res = await download_video(query)
        if not res or not res.get('file'):
            await pmsg.edit_text('No result found.')
            return
        thumb = res.get('thumbnail')
        if thumb:
            tpath = fetch(thumb)
            if tpath:
                await m.answer_photo(open(tpath,'rb'))
                cleanup(tpath)
        await m.answer_video(open(res['file'],'rb'), caption=res['info'].get('title',''))
        try:
            cleanup(res['file'])
        except:
            pass
        await pmsg.delete()
    dp.include_router(router)
