
from typing import Any

def add_attribute(attributes: dict, key: str, value: Any):
    if key is None:
        return
    if value is None or value == "None":
        return
    if attributes is None:
        return
    attributes[key] = value

