"""Model lifecycle — the ONE place "deprecated" and "retired" are interpreted at call time.

Ruled by Arman 2026-09-09 (verbatim in
common-docs/systems/agents/ai-models/DECISIONS.md) after deprecating Gemini 3.7
Flash made it vanish platform-wide:

- **deprecated** (`ai.model_definition.is_deprecated`) changes exactly three things:
  it is not offered to a normal user by default, an id already selected anywhere
  still resolves like any other model, and the server logs a warning naming the
  replacement. Everything else runs normally. **Never a substitution.**
- **retired** (`ai.model_definition.retired_at`, null = alive) is the DEAD state — the
  provider no longer serves it. Config and pricing still resolve for history and
  display, but the server refuses to run it, naming the replacement.
- **replacement** = `successor_id` when set (explicit, maintained by the AI Model
  Config Sync agent); otherwise every live `is_primary` model from the same maker
  with the same output modalities (the "same class" fallback — explicit beats inferred,
  and an ambiguous fallback names every candidate rather than picking one).

The warning fires ONCE per model per process (``_DEPRECATION_WARNED``) — a request
storm on a deprecated model must not become a log storm. Every path that routes a
call goes through :func:`gate_model_lifecycle`; TTS tier routing no longer treats
"deprecated" as a reason to reroute.
"""

from __future__ import annotations

from typing import Any

from matrx_utils import vcprint

from matrx_ai.catalog.errors import CatalogRoutingError

_DEPRECATION_WARNED: set[str] = set()


class ModelRetiredError(CatalogRoutingError):
    """The provider no longer serves this model — refuse, naming the replacement."""


def _outputs(state: dict[str, Any]) -> frozenset[str]:
    caps = state.get("capabilities")
    raw = caps.get("output") if isinstance(caps, dict) else None
    if isinstance(raw, str):
        raw = [raw]
    return frozenset(str(v) for v in raw) if isinstance(raw, (list, tuple, set)) else frozenset()


def _label(state: dict[str, Any]) -> str:
    return str(state.get("common_name") or state.get("name") or state.get("id") or "?")


def replacement_candidates(
    model_id: str, states: dict[str, dict[str, Any]]
) -> list[dict[str, Any]]:
    """The model(s) a caller should move to. Explicit ``successor_id`` first; else the
    same-class fallback (same ``provider_id`` + same output modalities + ``is_primary``,
    alive). Empty when nothing qualifies — the caller says so, never invents one."""
    state = states.get(str(model_id)) or {}
    successor = state.get("successor_id")
    if successor and str(successor) in states:
        return [states[str(successor)]]
    provider_id = state.get("provider_id")
    outputs = _outputs(state)
    if not provider_id:
        return []
    out: list[dict[str, Any]] = []
    for sid, candidate in states.items():
        if sid == str(model_id):
            continue
        if str(candidate.get("provider_id") or "") != str(provider_id):
            continue
        if not candidate.get("is_primary"):
            continue
        if candidate.get("is_deprecated") or candidate.get("retired_at"):
            continue
        if _outputs(candidate) != outputs:
            continue
        out.append(candidate)
    out.sort(key=_label)
    return out


def describe_replacement(model_id: str, states: dict[str, dict[str, Any]]) -> str:
    candidates = replacement_candidates(model_id, states)
    if not candidates:
        return (
            "no replacement is named — set ai.model_definition.successor_id on this model "
            "(or mark a live same-maker, same-output model is_primary)"
        )
    state = states.get(str(model_id)) or {}
    if state.get("successor_id"):
        c = candidates[0]
        return f"replacement (successor_id): {_label(c)} ({c.get('id')})"
    names = ", ".join(f"{_label(c)} ({c.get('id')})" for c in candidates)
    return f"replacement (same maker, same outputs, is_primary): {names}"


def gate_model_lifecycle(
    model_id: str,
    states: dict[str, dict[str, Any]],
    *,
    model_name: str | None = None,
) -> None:
    """Refuse a RETIRED model; warn once about a DEPRECATED one; otherwise silent.

    ``states`` is ``ai_catalog_manager``'s per-model state map (id -> row dict with
    ``is_deprecated`` / ``retired_at`` / ``successor_id`` / ``provider_id`` /
    ``is_primary`` / ``capabilities``). Pure: no I/O beyond the log line.
    """
    key = str(model_id)
    state = states.get(key) or {}
    name = model_name or _label(state)
    replacement = describe_replacement(key, states)

    if state.get("retired_at"):
        vcprint(
            f"Model '{name}' ({key}) is RETIRED (retired_at={state.get('retired_at')}): the "
            f"provider no longer serves it, so this call is refused. Move every reference to the "
            f"{replacement}. Deprecated models still run — retired ones never do.",
            title="🚨 AI MODEL RETIRED",
            color="red",
        )
        raise ModelRetiredError(
            f"model '{name}' ({key}) is retired (retired_at={state.get('retired_at')}) and "
            f"cannot be run; {replacement}"
        )

    if state.get("is_deprecated") and key not in _DEPRECATION_WARNED:
        _DEPRECATION_WARNED.add(key)
        vcprint(
            f"Model '{name}' ({key}) is DEPRECATED. It still runs normally (no substitution) "
            f"but is hidden from default selection — move references to the {replacement}. "
            f"This warning prints once per model per process.",
            title="⚠️ AI MODEL DEPRECATED",
            color="yellow",
        )


def reset_deprecation_warnings() -> None:
    """Test seam / catalog-reload hook: allow the once-per-process warning to fire again."""
    _DEPRECATION_WARNED.clear()


__all__ = [
    "ModelRetiredError",
    "describe_replacement",
    "gate_model_lifecycle",
    "replacement_candidates",
    "reset_deprecation_warnings",
]
