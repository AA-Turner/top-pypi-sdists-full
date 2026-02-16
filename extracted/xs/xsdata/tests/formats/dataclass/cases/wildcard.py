from collections.abc import Iterable, Sequence
from typing import Dict, List, Literal, Optional, Set, Tuple

cases = [
    (int, False),
    (Dict[int, int], False),
    (Dict, False),
    (Set, False),
    (Literal["foo"], False),
    (object, ((object,), None, None, False)),
    (List[object], ((object,), list, None, False)),
    (Tuple[object, ...], ((object,), tuple, None, False)),
    (Iterable[object, ...], ((object,), list, None, False)),
    (Sequence[object, ...], ((object,), list, None, False)),
    (Optional[object], ((object,), None, None, True)),
    (list[object], ((object,), list, None, False)),
    (tuple[object, ...], ((object,), tuple, None, False)),
    (object | None, ((object,), None, None, True)),
]
