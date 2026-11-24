"""After stored code is saved, the host stores its CSS (project stored-code-styling, VISION item 8).

A kind component, a kind component layer and a ``tool.ui`` renderer are code in the database: the app's build
never saw their classes, so the host compiles their CSS once, at save, and stores it for every reader. The package
never compiles anything and never decides which code parts a reader draws: after a successful write it reads the
saved row's code columns and hands them to the host hook, which applies the one parts rule and stores the CSS.

Unconfigured (a bare install) nothing happens. A failing hook never fails the save: it is counted, logged and
filed as a ``stored_css_save_failed`` system error, and the reader's on-demand compile still styles the code.
"""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from typing import Any

logger = logging.getLogger(__name__)

#: The kinds of stored code a hook receives (the host maps each to its parts rule).
ROW_KIND_COMPONENT = "kind_component"
ROW_TOOL_UI = "tool_ui"

#: The code columns of each row kind, read back from the saved row.
CODE_COLUMNS: dict[str, tuple[str, ...]] = {
    ROW_KIND_COMPONENT: ("component_source", "props_transform"),
    ROW_TOOL_UI: ("inline_code", "overlay_code", "utility_code", "header_extras_code", "header_subtitle_code"),
}

#: ``hook(row_kind, code_columns) -> anything``; it raises on failure.
StoredCodeSavedHook = Callable[[str, dict[str, str | None]], Awaitable[Any]]

_hook: StoredCodeSavedHook | None = None
_failures = 0


def configure_stored_code_saved(hook: StoredCodeSavedHook | None) -> None:
    """Install (or clear, with ``None``) the host's after-save CSS hook."""
    global _hook
    _hook = hook


def stored_code_saved_failures() -> int:
    """How many after-save CSS hooks failed since boot."""
    return _failures


def code_columns(row_kind: str, row: Any) -> dict[str, str | None]:
    """The code columns of a saved row (a model instance or a dict)."""
    get = row.get if isinstance(row, dict) else (lambda name: getattr(row, name, None))
    return {name: get(name) for name in CODE_COLUMNS[row_kind]}


async def stored_code_saved(row_kind: str, row: Any, *, row_id: str | None = None) -> bool:
    """Hand a saved row's code to the host hook. Returns whether the CSS was stored; never raises."""
    global _failures
    if _hook is None or row is None:
        return False
    try:
        await _hook(row_kind, code_columns(row_kind, row))
        return True
    except Exception as exc:  # noqa: BLE001 — the save stands; the reader's on-demand compile still styles it
        _failures += 1
        logger.error(
            "[stored-code-styling] the CSS for saved %s %s was not stored (%s failures since boot): %r",
            row_kind,
            row_id or "?",
            _failures,
            exc,
        )
        try:
            from matrx_utils import capture_error

            await capture_error(exc, kind="stored_css_save_failed", context={"row_kind": row_kind, "row_id": row_id})
        except Exception:  # noqa: BLE001 — the report never breaks the save
            logger.warning("could not file the stored_css_save_failed system error", exc_info=True)
        return False


def saved_component_id(result: Any, args: dict[str, Any]) -> str | None:
    """The id of the row a successful ``*_component`` write tool saved (its receipt, else the args)."""
    if not getattr(result, "success", False):
        return None
    output = result.output
    save = output.model_dump(mode="json") if hasattr(output, "model_dump") else output
    if isinstance(save, dict) and isinstance(save.get("save"), dict):
        save = save["save"]
    found = save.get("component_id") if isinstance(save, dict) else None
    found = found or args.get("component_id")
    return str(found).strip() or None if found else None
