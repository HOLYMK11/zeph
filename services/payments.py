import json, os, random, string, time
from config import PENDING_PAYMENTS_DB
os.makedirs(os.path.dirname(PENDING_PAYMENTS_DB), exist_ok=True)
if not os.path.exists(PENDING_PAYMENTS_DB):
    with open(PENDING_PAYMENTS_DB,"w") as f: json.dump({},f)
def gen_pid():
    return "ZPH" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
def save(pid, obj):
    d = json.load(open(PENDING_PAYMENTS_DB))
    d[pid] = obj
    json.dump(d, open(PENDING_PAYMENTS_DB,"w"), indent=2)
def pop(pid):
    d = json.load(open(PENDING_PAYMENTS_DB))
    if pid in d:
        val = d.pop(pid)
        json.dump(d, open(PENDING_PAYMENTS_DB,"w"), indent=2)
        return val
    return None
def list_all():
    return json.load(open(PENDING_PAYMENTS_DB))
