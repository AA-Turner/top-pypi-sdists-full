from itertools import chain
from random import choice
from typing import Union, List, Iterator, Optional, Any, Type

from spotipyio.logic.consts.typing_consts import EnumType


def chain_iterable(iterable_of_iterable: Union[List[list], Iterator[list]]) -> list:
    return list(chain.from_iterable(iterable_of_iterable))


def safe_nested_get(dct: dict, paths: list, default: Optional[Any] = None) -> Any:
    value = dct.get(paths[0], {})

    for path in paths[1:]:
        if not isinstance(value, dict):
            value = {}

        value = value.get(path, {})

    return value if value != {} else default


def random_enum_value(enum_: Type[EnumType]) -> EnumType:
    enum_values = get_all_enum_values(enum_)
    return choice(enum_values)


def get_all_enum_values(enum_: Type[EnumType]) -> List[EnumType]:
    return [v for v in enum_]
