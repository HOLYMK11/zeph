import json, os, random, string, time
from config import COUPONS_DB
os.makedirs(os.path.dirname(COUPONS_DB), exist_ok=True)
if not os.path.exists(COUPONS_DB):
    with open(COUPONS_DB,"w") as f: json.dump({},f)
def gen_coupon(amount, uses=1):
    code = "ZEPH-" + ''.join(random.choices(string.ascii_uppercase+string.digits,k=8))
    d = json.load(open(COUPONS_DB))
    d[code] = {"amount":amount,"uses":uses,"ts":int(time.time())}
    json.dump(d, open(COUPONS_DB,"w"), indent=2)
    return code
def redeem(code):
    d = json.load(open(COUPONS_DB))
    if code not in d: return None
    entry = d[code]
    if entry["uses"] <= 0: return None
    entry["uses"] -= 1
    amount = entry["amount"]
    if entry["uses"] <= 0:
        del d[code]
    json.dump(d, open(COUPONS_DB,"w"), indent=2)
    return amount
