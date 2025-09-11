from __future__ import annotations
from typing import Any, Callable, Iterable, Iterator, List, Tuple, Union, Dict
import re

JSONLike = Union[dict, list, tuple, set, str, int, float, bool, None]
PathType = Tuple[Union[str, int], ...]  # ('window_title',) or ('tabs', 2, 'name'), etc.

def iter_values(obj: JSONLike, path: PathType = ()) -> Iterator[Tuple[PathType, Any]]:
    """
    Depth-first walk of nested dict/list/tuple/set. Yields (path, value) for every leaf.
    Path items are str (dict key) or int (list index).
    """
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from iter_values(v, path + (k,))
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            yield from iter_values(v, path + (i,))
    elif isinstance(obj, set):
        for v in obj:
            # sets are unordered/no index – use a pseudo-key
            yield from iter_values(v, path + ('<setitem>',))
    else:
        # leaf (scalar)
        yield path, obj

def _mk_predicate(
    terms: Iterable[str] | None = None,
    *,
    case_insensitive: bool = True,
    substring: bool = True,
    regex: bool = False
) -> Callable[[Any], bool]:
    """
    Build a predicate that checks a scalar value against terms.
    """
    terms = list(terms or [])
    if regex:
        flags = re.IGNORECASE if case_insensitive else 0
        patterns = [re.compile(t, flags) for t in terms]
        def pred(value: Any) -> bool:
            if not isinstance(value, str):
                return False
            return any(p.search(value) for p in patterns)
        return pred

    # string contains (or equals)
    def pred(value: Any) -> bool:
        if not isinstance(value, str):
            return False
        v = value.lower() if case_insensitive else value
        for t in terms:
            t2 = t.lower() if case_insensitive else t
            if (t2 in v) if substring else (t2 == v):
                return True
        return False

    return pred

def search_values(
    obj: JSONLike,
    *,
    terms: Iterable[str],
    case_insensitive: bool = True,
    substring: bool = True,
    regex: bool = False,
) -> List[Tuple[PathType, Any]]:
    """
    Return all (path, value) where value matches any term.
    """
    pred = _mk_predicate(terms, case_insensitive=case_insensitive, substring=substring, regex=regex)
    results: List[Tuple[PathType, Any]] = []
    for p, v in iter_values(obj):
        if pred(v):
            results.append((p, v))
    return results

def any_match(
    obj: JSONLike,
    *,
    terms: Iterable[str],
    **kw
) -> bool:
    """Fast boolean check."""
    pred = _mk_predicate(terms, **kw)
    for _, v in iter_values(obj):
        if pred(v):
            return True
    return False
def get_first_match(obj: JSONLike, *, terms: Iterable[str], **kw) -> Optional[Any]:
    """Return just the first matching value, or None."""
    pred = _mk_predicate(terms, **kw)
    for _, v in iter_values(obj):
        if pred(v):
            return v
    return None

def get_all_match(obj: JSONLike, *, terms: Iterable[str], **kw) -> List[Any]:
    """Return all matching values as a flat list."""
    pred = _mk_predicate(terms, **kw)
    results: List[Any] = []
    for _, v in iter_values(obj):
        if pred(v):
            results.append(v)
    return results
