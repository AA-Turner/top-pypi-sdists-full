from .imports import (
    re,
    string,
    Any,
    Callable,
    Optional,
    Tuple,
    Union,
    Iterable,
    Iterator,
    Dict,
    List,
    SequenceMatcher,
)
JSONLike = Union[dict, list, tuple, set, str, int, float, bool, None]
PathType = Tuple[Union[str, int], ...]


