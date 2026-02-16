from collections.abc import Iterable, Sequence
from typing import Dict, List, Optional, Set, Tuple, Union

tokens = [
    (Set, False),
    (Dict[str, int], False),
    (Tuple[str, str], False),
    (List[str], ((str,), None, list, False)),
    (Optional[List[str]], ((str,), None, list, True)),
    (Tuple[str, ...], ((str,), None, tuple, False)),
    (List[List[str]], ((str,), list, list, False)),
    (Optional[List[List[Union[str, int]]]], ((str, int), list, list, True)),
    (List[Tuple[str, ...]], ((str,), list, tuple, False)),
    (Iterable[Iterable[str, ...]], ((str,), list, list, False)),
    (Sequence[Sequence[str, ...]], ((str,), list, list, False)),
    (Tuple[List[str], ...], ((str,), tuple, list, False)),
    (Optional[Tuple[List[str], ...]], ((str,), tuple, list, True)),
    (list[str], ((str,), None, list, False)),
    (tuple[str, ...], ((str,), None, tuple, False)),
    (list[list[str]], ((str,), list, list, False)),
    (list[tuple[str, ...]], ((str,), list, tuple, False)),
    (tuple[list[str], ...], ((str,), tuple, list, False)),
]

not_tokens = [
    (Set, False),
    (Dict[str, int], False),
    (Tuple[str, int], False),
    (List[List[str]], False),
    (List[Tuple[str, ...]], False),
    (Tuple[List[str], ...], False),
    (str, ((str,), None, None, False)),
    (List[str], ((str,), list, None, False)),
    (List[Union[str, int]], ((str, int), list, None, False)),
    (Optional[List[Union[str, int]]], ((str, int), list, None, True)),
    (Tuple[str, ...], ((str,), tuple, None, False)),
    (list[str], ((str,), list, None, False)),
    (tuple[str, ...], ((str,), tuple, None, False)),
]
