from __future__ import annotations

from typing import Any

from matrx_utils.fancy_prints import vcprint
from pydantic import BaseModel


def _find_bytes_paths(obj: Any, path: str = "root") -> list[tuple[str, bytes]]:
    if isinstance(obj, bytes):
        return [(path, obj)]
    if isinstance(obj, dict):
        found: list[tuple[str, bytes]] = []
        for key, value in obj.items():
            found.extend(_find_bytes_paths(value, f"{path}.{key}"))
        return found
    if isinstance(obj, list):
        found: list[tuple[str, bytes]] = []
        for index, value in enumerate(obj):
            found.extend(_find_bytes_paths(value, f"{path}[{index}]"))
        return found
    return []


def model_dump_json(model: BaseModel, *, context: str = "") -> dict[str, Any]:
    """``model_dump(mode='json')`` with a loud pre-flight scan for raw bytes.

    Pydantic cannot JSON-serialize invalid UTF-8 ``bytes`` nested in ``Any``
    fields (Google ``thought_signature`` is the common case). Scan the
    Python-mode dump first so the failure is diagnosable before it raises.
    """
    py_dump = model.model_dump()
    blockers = _find_bytes_paths(py_dump)
    if blockers:
        label = context or type(model).__name__
        vcprint(
            f"[model_dump_json] {label}: model_dump(mode='json') will fail — "
            f"{len(blockers)} raw bytes field(s)",
            color="red",
        )
        for path, raw in blockers[:25]:
            hint = ""
            if ".signature" in path:
                hint = " (likely thinking/thought_signature — use to_storage_dict)"
            vcprint(
                f"  {path}: len={len(raw)} head={raw[:32]!r}{hint}",
                color="yellow",
            )
    return model.model_dump(mode="json")
