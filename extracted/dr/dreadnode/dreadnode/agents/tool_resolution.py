"""Tool-name resolution for trajectory replay and similar retrospective dispatch.

The agent hot path matches the exact ``wire_name`` emitted by the LLM
(see ``Agent._process_tool_call``). This module is for retrospective
resolution — hydrating saved ``tool_call.name`` values from trajectories
that may pre-date the namespacing change.

Under CAP-IDENT-001..-007, a trajectory recorded before namespacing has
bare names in its tool-call records; a trajectory recorded after has
qualified wire names. The resolver handles both cleanly:

1. Exact ``wire_name`` match — post-namespacing trajectories and any
   caller that's already using the wire form.
2. Bare-name match when there is **exactly one** tool with that bare
   name in the effective set — pre-namespacing trajectories replayed in
   a single-capability environment.
3. Ambiguity or no match → ``None``. The caller decides whether to log
   and skip, error the pipeline, or prompt for disambiguation.

We deliberately do **not** pick deterministically on ambiguity: silent
rebinding in training data is the kind of bug that ruins a model
release months later. Callers who want a best-effort pick can inspect
the bare-match candidate list themselves.
"""

import typing as t


def resolve_saved_tool_call(saved_name: str, available: t.Iterable[t.Any]) -> t.Any | None:
    """Resolve a saved ``tool_call.name`` against the current tool set.

    Returns the matching ``Tool`` if resolution is unambiguous, otherwise
    ``None``. ``None`` covers both "not found at all" and "ambiguous"
    — callers can distinguish by falling back to ``bare_name_candidates``
    when they care.
    """
    tools = list(available)
    for tool in tools:
        wire = getattr(tool, "wire_name", None)
        if wire == saved_name:
            return tool

    bare_matches = [tool for tool in tools if getattr(tool, "name", None) == saved_name]
    if len(bare_matches) == 1:
        return bare_matches[0]
    return None


def bare_name_candidates(saved_name: str, available: t.Iterable[t.Any]) -> list[t.Any]:
    """Return every tool whose bare name matches ``saved_name``.

    Helper for callers that want to report ambiguity ("the saved name
    ``connect`` matched N tools: ..."). No wire-name fallback; pure bare
    match.
    """
    return [tool for tool in available if getattr(tool, "name", None) == saved_name]
