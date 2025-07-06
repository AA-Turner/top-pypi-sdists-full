import collections.abc
from typing import Any, Dict, List, Mapping


def make_cf_tags(tags: Dict[str, str]) -> List[Dict[str, str]]:
    _tags = []
    for key, value in tags.items():
        _tags.append({"Key": key, "Value": value})
    return _tags


def nested_update(d: Dict[Any, Any], u: Mapping[Any, Any]):
    for key, value in u.items():
        if isinstance(value, collections.abc.Mapping):
            d[key] = nested_update(d.get(key, {}), value)
        else:
            d[key] = value
    return d
