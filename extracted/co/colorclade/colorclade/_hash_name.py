import hashlib


def hash_name(name: str) -> int:
    return int(hashlib.sha256(name.encode("utf-8")).hexdigest(), 16)
