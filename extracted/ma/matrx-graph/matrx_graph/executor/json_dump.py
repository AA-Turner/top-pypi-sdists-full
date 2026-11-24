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
    """``model_dump(mode='json')``; when it fails, a loud scan names every raw-bytes path.

    Pydantic cannot JSON-serialize invalid UTF-8 ``bytes`` nested in ``Any``
    fields (Google ``thought_signature`` is the common case). The scan runs only
    on that failure: on success it would dump the model a second time and walk
    every leaf on the event loop (a top event-loop stall on 2026-11-02, up to
    54 s on one large step output).
    """
    try:
        return model.model_dump(mode="json")
    except Exception:
        blockers = _find_bytes_paths(model.model_dump())
        if blockers:
            label = context or type(model).__name__
            vcprint(
                f"[model_dump_json] {label}: model_dump(mode='json') failed — "
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
        raise
