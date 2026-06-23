"""LangGraph metadata extraction helpers.

Pulls ``langgraph_node`` / ``langgraph_step`` / ``langgraph_path`` out of the
callback's ``metadata`` and ``tags``, and merges user metadata alongside.
Pure functions, split out of ``native_callback`` to keep that file focused.
"""

from __future__ import annotations

import contextlib

# Keys that ``extract_langgraph_metadata`` consumes (and that we therefore
# don't want passing through twice into the chain-span metadata).
_LG_META_KEYS = frozenset(
    {"langgraph_node", "langgraph_step", "langgraph_path", "node", "step", "graph_node", "path"}
)


def extract_langgraph_metadata(  # noqa: C901, PLR0915 — multi-source (metadata + 3 tag patterns)
    *,
    metadata: dict[str, object] | None,
    tags: list[object] | None,
) -> dict[str, object]:
    """Pull langgraph_node/langgraph_step/langgraph_path from metadata and tags."""
    out: dict[str, object] = {}

    if metadata:
        node = metadata.get("langgraph_node") or metadata.get("node") or metadata.get("graph_node")
        step = metadata.get("langgraph_step") or metadata.get("step")
        path = metadata.get("langgraph_path") or metadata.get("path")
        if node:
            out["langgraph_node"] = node
        if step is not None:
            out["langgraph_step"] = step
        if path:
            out["langgraph_path"] = path

    if tags:
        for tag in tags:
            if not isinstance(tag, str):
                continue
            if tag.startswith(("graph:", "langgraph:")):
                parts = tag.split(":")
                if len(parts) >= 3 and parts[1] == "step":
                    out.setdefault("langgraph_node", parts[2])
            elif tag.startswith("seq:step:"):
                with contextlib.suppress(ValueError, IndexError):
                    out.setdefault("langgraph_step", int(tag.split(":")[2]))
            elif tag.startswith("node:"):
                out.setdefault("langgraph_node", tag.split(":", 1)[1])

    return out


def passthrough_metadata(
    user_metadata: dict[str, object] | None,
    lg_meta: dict[str, object],
) -> dict[str, object]:
    """Keep non-langgraph user metadata keys alongside our langgraph_* fields."""
    if not user_metadata:
        return lg_meta
    out = dict(lg_meta)
    for k, v in user_metadata.items():
        if k not in _LG_META_KEYS and k not in out:
            out[k] = v
    return out
