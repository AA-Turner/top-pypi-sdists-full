# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.


from dataclasses import asdict
from typing import Any


def as_camel_dict(data):
    return asdict(data, dict_factory=lower_camel_case_keyed_dict_factory)


def lower_camel_case_keyed_dict_factory(kvs: list[tuple[str, Any]]) -> dict[str, Any]:
    return {lower_snake_to_camel(k): v for k, v in kvs if v is not None}


def lower_snake_to_camel(snake_str: str) -> str:
    return "".join(
        word if i == 0 else word.capitalize()
        for i, word in enumerate(snake_str.split("_"))
    )
