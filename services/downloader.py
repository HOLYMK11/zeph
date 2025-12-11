import asyncio, tempfile, os, shutil, subprocess
from yt_dlp import YoutubeDL
from config import TEMP_DIR
def ffmpeg_available():
    try:
        subprocess.check_output(["ffmpeg","-version"])
        subprocess.check_output(["ffprobe","-version"])
        return True
    except:
        return False
def _download_audio(url,outtmpl):
    opts = {"format":"bestaudio/best","outtmpl":outtmpl,"quiet":True,"no_warnings":True,"postprocessors":[{"key":"FFmpegExtractAudio","preferredcodec":"mp3","preferredquality":"192"}]}
    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
    return info
def _download_video(url,outtmpl):
    opts = {"format":"bestvideo[height<=480]+bestaudio/best/best[height<=480]","merge_output_format":"mp4","outtmpl":outtmpl,"quiet":True}
    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
    return info
async def download_audio(query):
    outdir = TEMP_DIR
    outtmpl = os.path.join(outdir, "%(id)s.%(ext)s")
    loop = asyncio.get_running_loop()
    info = await loop.run_in_executor(None, _download_audio, query, outtmpl)
    files = [f for f in os.listdir(outdir) if info.get("id") in f]
    path = None
    for f in files:
        if f.endswith(".mp3"):
            path = os.path.join(outdir,f); break
    return {"info":info,"file":path,"thumbnail":info.get("thumbnail")}
async def download_video(query):
    outdir = TEMP_DIR
    outtmpl = os.path.join(outdir, "%(id)s.%(ext)s")
    loop = asyncio.get_running_loop()
    info = await loop.run_in_executor(None, _download_video, query, outtmpl)
    files = [f for f in os.listdir(outdir) if info.get("id") in f]
    path = None
    for f in files:
        if f.endswith(".mp4"):
            path = os.path.join(outdir,f); break
    return {"info":info,"file":path,"thumbnail":info.get("thumbnail")}
