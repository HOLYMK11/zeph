import aiohttp
from config import OCR_SPACE_KEY
OCR_URL = "https://api.ocr.space/parse/image"
async def parse_url(url:str):
    data = aiohttp.FormData()
    data.add_field("apikey", OCR_SPACE_KEY)
    data.add_field("url", url)
    async with aiohttp.ClientSession() as s:
        async with s.post(OCR_URL, data=data) as r:
            js = await r.json()
            if js.get("IsErroredOnProcessing"):
                return {"ok":False,"error":js.get("ErrorMessage")}
            parsed = js.get("ParsedResults",[{}])[0]
            text = parsed.get("ParsedText","")
            return {"ok":True,"text":text,"raw":parsed}
