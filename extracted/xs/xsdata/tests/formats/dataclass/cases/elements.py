from typing import Dict, List, Optional, Tuple, Union

cases = [
    (Dict, False),
    (str, ((object,), None, None, False)),
    (List[str], ((object,), list, None, False)),
    (Tuple[str, ...], ((object,), tuple, None, False)),
    (Optional[Union[str, int]], ((object,), None, None, True)),
    (Union[str, int, None], ((object,), None, None, True)),
    (List[Union[List[str], Tuple[str, ...]]], ((object,), list, None, False)),
    (list[str], ((object,), list, None, False)),
    (tuple[str, ...], ((object,), tuple, None, False)),
    (list[Union[list[str], tuple[str, ...]]], ((object,), list, None, False)),
    (str | int | None, ((object,), None, None, True)),
    (list[list[str] | tuple[str, ...]], ((object,), list, None, False)),
]
