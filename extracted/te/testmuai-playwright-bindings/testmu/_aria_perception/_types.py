"""The mode-owned types the portable capture builds.

The ``AxNode`` / ``FrameCapture`` / ``FrameForest`` classes, the AX serializer
and the interactive-role table live in the mode package (``testmu._v4._helpers``),
and shared code must not import a mode package, so the mode passes its own
``ModeTypes`` in (see ``testmu._v4._helpers.aria_perception``).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class ModeTypes:
    AxNode: type
    FrameCapture: type
    FrameForest: type
    serialize_ax_tree: Callable[..., Any]
    interactive_roles: frozenset
    # Marks ``[cursor=pointer]`` nodes clickable, as the CDP capture does.
    annotate_pointer: Callable[[Any], Any] | None = None
