from typing import Dict, List

def deep_search(
    d: Dict,
    key: str
) -> List:
    """Recursively search for all values of a key in a nested Dict/List."""
    results = []
    if isinstance(d, Dict):
        for k, v in d.items():
            if k == key:
                results.append(v)
            elif isinstance(v, (Dict, List)):
                results.extend(deep_search(v, key))
    elif isinstance(d, List):
        for item in d:
            results.extend(deep_search(item, key))
    return results