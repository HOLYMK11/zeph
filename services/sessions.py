import time, threading
from config import SESSION_TIMEOUT_SECONDS, PAYMENT_SESSION_TIMEOUT
class SessionManager:
    def __init__(self):
        self.sessions = {}
        self.lock = threading.Lock()
    def start(self, tg_id:int, chat_id:int, mode:str, wait_msg_id:int=None, timeout: int = None):
        if timeout is None:
            timeout = SESSION_TIMEOUT_SECONDS if mode != "payment" else PAYMENT_SESSION_TIMEOUT
        entry = {"chat_id":chat_id,"mode":mode,"wait_msg_id":wait_msg_id,"start":time.time(),"timeout":timeout}
        with self.lock:
            self.sessions[tg_id] = entry
    def get(self, tg_id:int):
        with self.lock:
            s = self.sessions.get(tg_id)
            if not s: return None
            if time.time() - s["start"] > s["timeout"]:
                del self.sessions[tg_id]
                return None
            return s
    def end(self, tg_id:int):
        with self.lock:
            if tg_id in self.sessions:
                del self.sessions[tg_id]
    def cleanup(self):
        now = time.time()
        with self.lock:
            stale = [k for k,v in self.sessions.items() if now - v["start"] > v["timeout"]]
            for k in stale:
                del self.sessions[k]
