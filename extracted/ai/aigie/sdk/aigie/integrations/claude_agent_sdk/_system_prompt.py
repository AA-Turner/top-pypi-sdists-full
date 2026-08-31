"""``ClaudeAgentOptions.system_prompt`` is a three-armed union, and two arms are objects.

Each arm resolves to whatever text we hold, plus a marker naming where the rest of it
went, so a consumer reading an empty prompt can tell "the author gave none" from "the
author gave one we cannot see".

Every one of those fields is a value the caller chose, so all of them ride the
content-capture switch together. The drift detector is the one exception, and not this
module's to fix: it stores the resolved text on the query root's ``monitoring`` blob
regardless of the switch, for every arm including a plain string.
"""

from __future__ import annotations

from pathlib import PurePath
from typing import Any, NamedTuple

from aigie._system_prompt import system_prompt_text

__all__ = ["OptionsSystemPrompt", "resolve_system_prompt"]

# Where a trustworthy `__str__` for a path may come from. `pathlib._local` is the module
# the stdlib path classes moved to in 3.13; the matrix job on each version is what keeps
# this list honest, since a name missing here silently drops every marker.
_PATHLIB_MODULES = frozenset({"pathlib", "pathlib._local"})


class OptionsSystemPrompt(NamedTuple):
    text: str
    preset: str = ""
    file_path: str = ""

    def stamp_markers(self, metadata: dict[str, Any]) -> None:
        """Record where a prompt we cannot fully see came from.

        Callers gate this on content capture: ``preset`` is typed as a fixed identifier,
        but a ``TypedDict`` is a plain dict at runtime and this is whatever the caller
        put there, so it is suppressed with the rest of the content rather than trusted
        to be one of the framework's own names.
        """
        if self.preset:
            metadata["system_prompt_preset"] = self.preset
        if self.file_path:
            metadata["system_prompt_file"] = self.file_path


def _path_marker(path: Any) -> str:
    """The path the CLI will open, or ``""`` when that cannot be known without asking it.

    The CLI hands ``path`` to ``os.fspath``, so the file it opens is whatever the value's
    own ``__str__`` returns — caller code. Running it here is not an option: this resolves
    inside the host's ``connect()``, and an exception from it is the defect this module
    exists to close. So the marker is only recorded when the rendering belongs to
    ``pathlib`` itself and therefore cannot disagree with what the CLI opens.

    Everything else is dropped rather than guessed at, because a marker naming a different
    file than the one that was read is worse than no marker: a ``UPath`` rendering
    ``s3://bucket/p.md`` would otherwise be recorded as ``/bucket/p.md``, and an
    ``os.PathLike`` that is not a ``PurePath`` only yields its path through the protocol
    we decline to invoke.

    The whole body sits under one ``try`` and one exact-``str`` check rather than a guard
    per hazard. Every line here touches a type the caller owns — ``isinstance`` consults
    ``__class__``, an attribute lookup runs a metaclass, a descriptor rejects an impostor —
    and enumerating those one at a time is how this function acquired a new way to raise
    on each of its previous revisions.
    """
    try:
        if isinstance(path, str):
            # `str.__str__` is the base implementation, so a genuine subclass renders as its
            # own text without dispatch — a `str`-Enum path constant included — leaving an
            # exact `str` in metadata rather than the caller's live object. It rejects an
            # impostor whose `__class__` merely claims `str`, which the `except` then drops.
            rendered = str.__str__(path)
        elif isinstance(path, PurePath) and _renders_as_pathlib(path):
            rendered = type(path).__str__(path)
        else:
            return ""
    except Exception:  # noqa: BLE001 — a path that will not render is not worth a marker
        return ""
    # `PurePath.__str__` reads attributes a subclass can still own, so a result is only
    # trusted once it is an exact string.
    return rendered if type(rendered) is str else ""


def _renders_as_pathlib(path: PurePath) -> bool:
    """Whether both routes to this path's text are pathlib's own.

    ``__str__`` is what the marker reads and ``__fspath__`` is what the CLI opens. They are
    separately overridable, so vetting only one leaves a subclass that displays as one file
    and opens another — which is the disagreement the marker exists to avoid.
    """
    owners = (type(path).__str__, type(path).__fspath__)
    return all(getattr(owner, "__module__", None) in _PATHLIB_MODULES for owner in owners)


def resolve_system_prompt(value: Any) -> OptionsSystemPrompt:
    """Resolve any arm of the union to what a span can carry.

    Callers take ``.text``: the trace-name heuristic runs a regex over it, which raises
    on an object arm. The preset's body is assembled by the ``claude`` CLI, so ``append``
    is the only text on our side, and the file arm is deliberately not read — this runs
    inside the host's own ``connect()``/``query()``, where an unbounded read of a path we
    were merely told about would add both latency and a way for a secrets file to reach a
    span.

    Reading the union at all means running code the caller owns: ``.get`` on a dict
    subclass, ``.text`` on a property. An exception from any of it lands in the host's
    call the same way the original ``TypeError`` did, so nothing here is allowed out — a
    prompt we cannot read resolves to no prompt.
    """
    try:
        return _resolve(value)
    except Exception:  # noqa: BLE001 — a prompt that will not be read is not worth a crash
        return OptionsSystemPrompt("")


def _resolve(value: Any) -> OptionsSystemPrompt:
    if isinstance(value, dict):
        kind = value.get("type")
        if kind == "preset":
            append, preset = value.get("append"), value.get("preset")
            return OptionsSystemPrompt(
                append if isinstance(append, str) else "",
                preset=preset if isinstance(preset, str) else "",
            )
        if kind == "file":
            return OptionsSystemPrompt("", file_path=_path_marker(value.get("path")))
    return OptionsSystemPrompt(system_prompt_text(value))
