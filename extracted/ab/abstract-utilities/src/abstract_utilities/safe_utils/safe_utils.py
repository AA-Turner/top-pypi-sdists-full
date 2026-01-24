"""
abstract_safeops.py
-------------------
Utility functions for safely splitting, slicing, and retrieving elements from iterable or string objects
without raising exceptions on invalid input or out-of-range indices.

Designed for compatibility with the abstract_ ecosystem (e.g. abstract_utilities, abstract_math, etc.).
"""

from .imports import *
_BASE_DIR = get_caller_dir()

class PathOutsideBase(Exception):
    pass

def safe_join_base(base: Union[str, Path], *parts: Union[str, Path], must_exist: bool = False) -> Path:
    """
    Join base with parts, normalize, and ensure the result lives under base.
    Prevents '../' traversal and ignores leading slashes in parts.
    """
    base = Path(base).resolve(strict=True)
    # Disallow absolute/drive-anchored parts by stripping their anchors before joining.
    cleaned = []
    for p in parts:
        p = Path(p)
        # Convert absolute to relative (security: we won't allow escaping base anyway)
        if p.is_absolute():
            p = Path(*p.parts[1:])  # drop leading '/'
        cleaned.append(p)

    # Build and resolve (non-strict so missing files are allowed unless must_exist=True)
    target = (base.joinpath(*cleaned)).resolve(strict=False)

    # Containment check (works even if target doesn't exist)
    try:
        target.relative_to(base)
    except ValueError:
        raise PathOutsideBase(f"{target} escapes base {base}")

    if must_exist and not target.exists():
        raise FileNotFoundError(target)

    return target
def safe_split(
    string: Any,
    char: Any,
    i: Optional[int] = None,
    default: Union[bool, Any] = False
) -> Union[str, List[str], Any, None]:
    """
    Safely split a string by a character and optionally return index i.

    Args:
        string: Input string (or any object convertible to string).
        char: Delimiter to split on.
        i: Optional index to retrieve from the split result.
        default: If True, return the original string on error. 
                 If any other value, return that instead of raising.

    Returns:
        The split list, or the element at index i, or default behavior on error.
    """
    if string is None or char is None:
        return string

    s, c = str(string), str(char)
    if c not in s:
        return string

    parts = s.split(c)

    if i is None:
        return parts

    if is_number(i):
        idx = int(i)
        if 0 <= idx < len(parts):
            return parts[idx]

    if default:
        return string if default is True else default

    return None


def safe_slice(
    obj: Any,
    i: Optional[int] = None,
    k: Optional[int] = None,
    default: Union[bool, Any] = False
) -> Any:
    """
    Safely slice an iterable object or string, with fallback behavior on invalid indices.

    Args:
        obj: Iterable or string-like object.
        i: Start index (can be negative).
        k: End index (can be negative).
        default: If True, returns the original object on error.
                 If any other value, return that value on error.

    Returns:
        The sliced object, or default behavior on error.
    """
    # Null or invalid base case
    if obj is None or isinstance(obj, bool):
        return obj if default is True else default if default else None

    # Non-iterable guard
    if not hasattr(obj, "__getitem__"):
        return obj if default is True else default if default else None

    obj_len = len(obj)

    # Normalize negative indices
    if isinstance(i, int) and i < 0:
        i = obj_len + i
    if isinstance(k, int) and k < 0:
        k = obj_len + k

    # Bound indices
    if i is not None:
        i = max(0, min(i, obj_len))
    if k is not None:
        k = max(0, min(k, obj_len))

    try:
        return obj[i:k]
    except Exception:
        return obj if default is True else default if default else None

def safe_join(*paths):
    paths = list(paths)
    paths = [path for path in paths if path]
    return os.path.join(*paths)
def safe_get(
    obj: Any,
    key: Union[int, str, None] = None,
    default: Union[bool, Any] = False
) -> Any:
    """
    Generalized safe getter for both indexable and mapping types.

    Args:
        obj: The object to access (list, dict, string, etc.).
        key: Index or key to retrieve.
        default: Fallback value or True for "return obj".

    Returns:
        Retrieved element, or default value on failure.
    """
    if obj is None or key is None:
        return obj if default is True else default if default else None

    try:
        if isinstance(obj, dict):
            return obj.get(key, obj if default is True else default if default else None)
        return obj[key]
    except Exception:
        return obj if default is True else default if default else None
def get_slash(path):
    if '/' in path:
        return '/'
    else:
        return '//'
join_path=safe_join
