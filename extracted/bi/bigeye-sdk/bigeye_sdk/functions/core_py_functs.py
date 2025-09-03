from datetime import datetime, timezone
from enum import Enum
from itertools import chain
from typing import List

# create logger
from bigeye_sdk.log import get_logger

log = get_logger(__name__)


def int_enum_enum_list_joined(enum: Enum.__class__, delimiter: str = '\n') -> str:
    return delimiter.join([f'{t.name}:{t.value}' for t in enum])


def merge_list_of_lists(l: List[list]):
    """
    Flatten a List of lists.

    :param l: A list comprised of other lists.
    :returns: :class:generator

    >>> list(merge_list_of_lists([['str', 'str1'], ['str2']]))
    ['str', 'str1', 'str2']
    """
    for i in l:
        for si in i:
            yield si


def split_list_n_chunks(l: list, n: int):
    """
    Split a list into lists of length n, evenly sized if possible.

    :param l: The list to split
    :param n: The length of the list(s) to return
    :returns: generator

    >>> list(split_list_n_chunks(['str', 'str1', 'str2'], 1))
    [['str'], ['str1'], ['str2']]
    >>> list(split_list_n_chunks(['str', 'str1', 'str2'], 2))
    [['str', 'str1'], ['str2']]
    """
    for i in range(0, len(l), n):
        yield l[i:i + n]


def split_list_in_half(l: list) -> List[list]:
    """
    Split a list of even length in half. For lists of odd lengths, the second list will have more elements.

    :param l: The list to split
    :returns: List[list]

    >>> split_list_in_half(['str', 'str1', 'str2'])
    [['str'], ['str1', 'str2']]
    >>> split_list_in_half(['str', 'str1', 'str2', 'str3'])
    [['str', 'str1'], ['str2', 'str3']]
    """
    middle_ix = len(l) // 2

    data_first_500 = l[:middle_ix]
    data_remainder = l[middle_ix:]

    return [data_first_500, data_remainder]


def dynamic_clz_import(fqc):
    fqc_split = fqc.split('.')
    clz_name = fqc_split.pop()
    module = '.'.join(fqc_split)
    mod = __import__(module, fromlist=[clz_name])
    return getattr(mod, clz_name)


def date_time_2_string(dt: datetime, include_tz_offset: bool = True) -> str:
    """Convert a datetime to a string, with or without a timezone offset

    :param dt: The datetime to convert
    :param include_tz_offset: A boolean to include timezone offset or not.

    :returns: str

    >>> date_time_2_string(datetime(2022, 5, 19, 14, 40, 45, 204489), True)
    '2022-05-19 19:40:45.204489'
    >>> date_time_2_string(datetime(2022, 5, 19, 14, 40, 45, 204489), False)
    '2022-05-19T14:40:45.204489'
    """
    if include_tz_offset:
        return dt.astimezone(tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")
    else:
        return dt.isoformat()


def remove_none(d: dict) -> dict:
    """
    Remove items in a dictionary if the values are None.

    :param d: The dictionary to check.

    :returns: dict

    >>> remove_none({"key": "value", "this_key": None})
    {'key': 'value'}
    """
    return {k: v for k, v in d.items() if v is not None}


def chain_lists(ll: List[list]) -> List:
    """
    Flatten a list of lists.

    :param ll: The list to flatten.

    :returns: List

    >>> chain_lists([['str', 'str1'], ['str2']])
    ['str', 'str1', 'str2']
    """
    return list(chain.from_iterable(ll))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
