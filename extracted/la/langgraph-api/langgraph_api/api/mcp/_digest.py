import hashlib

import orjson
from pydantic import JsonValue

KEY_DIGEST_LENGTH = 16


def digest(*parts: JsonValue) -> str:
    encoded = orjson.dumps(parts, option=orjson.OPT_SORT_KEYS)
    return hashlib.sha256(encoded).hexdigest()[:KEY_DIGEST_LENGTH]
