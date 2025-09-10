from pathlib import Path
from typing import Union


class PathOutsideBase(Exception):
    pass

def safe_join(base: Union[str, Path], *parts: Union[str, Path], must_exist: bool = False) -> Path:
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
