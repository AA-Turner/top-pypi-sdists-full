"""App key and secret."""

import os

# --- credentials: injected at build time via scripts/update_credentials.py — do not edit ---
def _r(d: tuple[int, ...]) -> str:
    _k = (109, 97, 109, 109, 111, 116, 105, 111, 110, 95, 97, 112, 112)
    return bytes(v ^ _k[i % len(_k)] for i, v in enumerate(d)).decode()

APP_KEY = _r((94, 85, 95, 92, 86, 68, 91, 88))
APP_SECRET = _r((8, 2, 14, 88, 92, 71, 15, 87, 94, 104, 4, 69, 67, 91, 88, 15, 92, 13, 77, 13, 11, 91, 110, 87, 73, 20, 91, 7, 14, 88, 92, 64))
# --- end credentials ---

if not APP_KEY:
    from dotenv import load_dotenv

    load_dotenv()
    APP_KEY = os.environ.get("ALIYUN_APP_KEY", "")
    APP_SECRET = os.environ.get("ALIYUN_APP_SECRET", "")

APP_VERSION = "2.3.2.13"
ALIYUN_DOMAIN = "api.link.aliyun.com"
MAMMOTION_DOMAIN = "https://id.mammotion.com"
MAMMOTION_API_DOMAIN = "https://domestic.mammotion.com"
MAMMOTION_CLIENT_ID = "MADKALUBAS"
MAMMOTION_CLIENT_SECRET = "GshzGRZJjuMUgd2sYHM7"

MAMMOTION_OUATH2_CLIENT_ID = "GxebgSt8si6pKqR"
MAMMOTION_OUATH2_CLIENT_SECRET = "JP0508SRJFa0A90ADpzLINDBxMa4Vj"
