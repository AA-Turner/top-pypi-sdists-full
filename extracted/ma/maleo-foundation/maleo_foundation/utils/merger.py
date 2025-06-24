from collections.abc import Mapping
from typing import Dict

def deep_merge(*obj: Dict) -> Dict:
    def merge_dicts(
        a: Dict,
        b: Dict
    ) -> Dict:
        result = dict(a)
        for key, value in b.items():
            if (
                key in result
                and isinstance(result[key], Mapping)
                and isinstance(value, Mapping)
            ):
                result[key] = merge_dicts(result[key], value)
            else:
                result[key] = value
        return result

    merged = {}
    for ob in obj:
        merged = merge_dicts(merged, ob)
    return merged