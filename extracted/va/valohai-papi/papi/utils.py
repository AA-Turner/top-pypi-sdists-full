def compact_dict(dct: dict) -> dict:
    return {key: value for (key, value) in dct.items() if key and value}
