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

AUTHORING time is the one place that resolves rather than runs — see
:func:`resolve_authoring_model_id` at the bottom of this module. Writing a NEW
reference is a different question from running an existing one, and conflating
the two refused two live agent builds on 2026-09-12.

The warning fires ONCE per model per process (``_DEPRECATION_WARNED``) — a request
storm on a deprecated model must not become a log storm. Every path that routes a
call goes through :func:`gate_model_lifecycle`; TTS tier routing no longer treats
"deprecated" as a reason to reroute.
"""

from __future__ import annotations

from typing import Any

from matrx_utils import vcprint

from matrx_ai.catalog.errors import CatalogRoutingError
from matrx_ai.catalog.knobs import catalog_knob

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


# --- AUTHORING-TIME RESOLUTION ------------------------------------------------
# Call time and authoring time are different questions, and conflating them is
# what broke the Masterwork Conductor's `workflow_plan build_agent` twice on
# 2026-09-12: the builder's frozen catalog snapshot authored Gemini 3.7 Flash
# (deprecated, successor Gemini 3.8 Flash) and the birth gate — which asks the
# live catalog for NON-deprecated models only — refused the whole build.
#
# * CALL time keeps Arman's 2026-09-09 ruling exactly: a deprecated id already
#   selected somewhere runs, never substituted (``gate_model_lifecycle``).
# * AUTHORING time is a WRITE of a brand-new reference. Nothing should be born
#   pointing at a model the platform has already moved off, and a housekeeping
#   flag must never stop an author mid-build. So a deprecated or retired id is
#   resolved ALONG THE EXPLICIT ``successor_id`` CHAIN — bounded and cycle-safe
#   — and only a dead end fails, loudly, naming the replacement work to do.
#
# The chain is explicit-only on purpose: the same-class fallback is a GUESS, and
# a guess must never be written into a stored definition. It is still reported in
# the failure message so the author knows what to pick.

#: How far the successor chain is followed before it is called a defect. Two or
#: three generations is a normal model family; twenty is a broken catalog.
#: KNOB MIRROR of platform.feature_knob "agents.model_catalog" "authoring_successor_hop_limit" —
#: the standalone default; the host binds the live row through configure_catalog_knobs.
AUTHORING_SUCCESSOR_HOP_LIMIT = 5


class ModelNotAuthorableError(CatalogRoutingError):
    """This model id may not be written into a new/updated definition."""


class AuthoringModelResolution:
    """The model id a write should persist, plus how it got there."""

    __slots__ = ("model_id", "requested_model_id", "chain", "note")

    def __init__(
        self,
        *,
        model_id: str,
        requested_model_id: str,
        chain: tuple[str, ...],
        note: str,
    ) -> None:
        self.model_id = model_id
        self.requested_model_id = requested_model_id
        self.chain = chain
        self.note = note

    @property
    def substituted(self) -> bool:
        return self.model_id != self.requested_model_id

    def __repr__(self) -> str:  # pragma: no cover - debug aid
        return (
            f"AuthoringModelResolution(model_id={self.model_id!r}, "
            f"requested_model_id={self.requested_model_id!r}, chain={self.chain!r})"
        )


def resolve_authoring_model_id(
    model_id: str,
    states: dict[str, dict[str, Any]],
    *,
    hop_limit: int | None = None,
) -> AuthoringModelResolution:
    """THE resolver every authoring write goes through. Pure; no I/O.

    A live id returns unchanged. A deprecated or retired id follows
    ``successor_id`` until a live model is reached. Raises
    :class:`ModelNotAuthorableError` when the id is unknown, when the chain dead
    ends (no successor, or one that is not in the catalog), when it cycles, or
    when it is longer than ``hop_limit`` — never a silent pick.
    """
    if hop_limit is None:
        hop_limit = int(catalog_knob("authoring_successor_hop_limit", AUTHORING_SUCCESSOR_HOP_LIMIT))
    requested = str(model_id or "").strip()
    if not requested:
        raise ModelNotAuthorableError("no model_id was supplied")
    if requested not in states:
        raise ModelNotAuthorableError(
            f"model {requested} is not in the live model catalog"
        )

    chain: list[str] = [requested]
    seen: set[str] = {requested}
    current = requested

    for _ in range(hop_limit):
        state = states.get(current) or {}
        if not state.get("is_deprecated") and not state.get("retired_at"):
            if len(chain) == 1:
                note = ""
            else:
                note = (
                    f"authored model {_label(states.get(requested) or {})} ({requested}) is "
                    f"{'retired' if (states.get(requested) or {}).get('retired_at') else 'deprecated'}; "
                    f"resolved along successor_id to {_label(state)} ({current})"
                )
            return AuthoringModelResolution(
                model_id=current,
                requested_model_id=requested,
                chain=tuple(chain),
                note=note,
            )

        successor = str(state.get("successor_id") or "").strip()
        lifecycle = "retired" if state.get("retired_at") else "deprecated"
        if not successor:
            raise ModelNotAuthorableError(
                f"model {_label(state)} ({current}) is {lifecycle} and names no successor_id, "
                f"so there is nothing to write instead — {describe_replacement(current, states)}"
            )
        if successor not in states:
            raise ModelNotAuthorableError(
                f"model {_label(state)} ({current}) is {lifecycle} and its successor_id "
                f"{successor} is not in the live model catalog"
            )
        if successor in seen:
            raise ModelNotAuthorableError(
                "successor_id chain cycles through "
                f"{' -> '.join([*chain, successor])}; fix ai.model_definition.successor_id"
            )
        seen.add(successor)
        chain.append(successor)
        current = successor

    raise ModelNotAuthorableError(
        f"successor_id chain from {requested} is longer than {hop_limit} hops "
        f"({' -> '.join(chain)}) and never reached a live model"
    )


__all__ = [
    "AUTHORING_SUCCESSOR_HOP_LIMIT",
    "AuthoringModelResolution",
    "ModelNotAuthorableError",
    "ModelRetiredError",
    "describe_replacement",
    "gate_model_lifecycle",
    "replacement_candidates",
    "reset_deprecation_warnings",
    "resolve_authoring_model_id",
]
