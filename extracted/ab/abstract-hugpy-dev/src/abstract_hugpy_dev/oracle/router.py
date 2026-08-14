"""Oracle router (k91): goal -> capability -> best eligible route.

Two decisions live here, both DETERMINISTIC and both recorded on the returned
``RouteDecision`` so the receipt can say why:

  1. INTENT — when the goal carries no explicit capability, a small
     input-modality + explicit-ask table picks one (``infer_capability``).
     No model call, no scoring: the table IS the contract, and an explicit
     ``GoalSpec.capability`` always wins over it.
  2. MODEL — within the chosen capability, the model comes from the same
     defaults the existing task handlers use: an explicit request wins
     (``requested``), a single eligible model is taken as-is
     (``only-eligible``), otherwise the dispatcher's own task-default
     resolution (``default``; managers/resolvers TASK_DEFAULTS). No new
     scoring scheme.

Eligibility is the k90 catalog's verdict, never re-derived: an ineligible or
unknown capability routes to ``execution == "gap"`` (the typed CAPABILITY_GAP
shape, catalog reasons echoed — an unmapped task string must land here, never
a KeyError). STUDIO (video.*) capabilities route to ``execution == "deferred"``
— k91 explains the best route via the studio's own verdict but does not run the
render pipeline (that stays with the studio job routes until a later slice).

Import discipline mirrors catalog.py: module top level is contracts + catalog
only; every registry read is lazy inside a module-level provider seam
(``_get_capability`` / ``_task_default_model`` / ``_studio_menu`` /
``_placement_for``) so tests monkeypatch them and need no live fleet.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from . import catalog
from .contracts import ArtifactKind, GoalSpec, InputKind

# ---------------------------------------------------------------------------
# Capability -> canonical dispatch task string (the exact key ml_routes.ML_TASKS
# dispatches on). Inverse-consistent with catalog.LEGACY_TASK_CAPABILITY by
# test: every value here maps back to its key through that table.
# ---------------------------------------------------------------------------

CAPABILITY_TASK: dict[str, str] = {
    "text.chat":        "text-generation",
    "text.summarize":   "text-summarization",
    "text.keywords":    "keyword-extraction",
    "text.embed":       "feature-extraction",
    "text.similarity":  "sentence-similarity",
    "audio.transcribe": "automatic-speech-recognition",
    "image.understand": "image-text-to-text",
    "image.generate":   "text-to-image",
    "image.transform":  "image-to-image",
    "image.depth":      "depth-estimation",
    "image.detect":     "object-detection",
    "image.classify":   "image-classification",
    "image.segment":    "image-segmentation",
    "doc.extract":      "document-extraction",
    "web.fetch":        "url-extraction",
}

# ---------------------------------------------------------------------------
# Intent inference — the input-modality + explicit-ask table.
# ---------------------------------------------------------------------------

# Verbs that read as "change this image" rather than "tell me about this image".
_TRANSFORM_VERBS = (
    "transform", "restyle", "stylize", "repaint", "recolor", "redraw",
    "convert", "turn this", "turn it", "make it", "make this", "edit",
    "remix", "variation", "in the style of",
)
# Verbs that read as "shorten this text".
_SUMMARIZE_VERBS = ("summarize", "summarise", "summary", "tl;dr", "tldr",
                    "condense", "shorten this")
_QUESTION_WORDS = ("what", "who", "where", "when", "why", "how", "which",
                   "describe", "explain", "identify", "is there", "are there",
                   "does", "do you see", "can you see", "tell me")


def _question_like(prompt: str) -> bool:
    p = prompt.strip().lower()
    return "?" in p or any(p.startswith(w) for w in _QUESTION_WORDS)


def _has_any(prompt: str, verbs: tuple[str, ...]) -> bool:
    p = prompt.lower()
    return any(v in p for v in verbs)


def infer_capability(goal: GoalSpec) -> tuple[str, str]:
    """(capability, why) from the deterministic table. First match wins:

      image attached + transform verb, not question-like -> image.transform
      image attached (question-like or anything else)   -> image.understand
      audio attached                                    -> audio.transcribe
      video attached                                    -> audio.transcribe
      url attached                                      -> web.fetch
      no attachment + summarize verb                    -> text.summarize
      default                                           -> text.chat
    """
    prompt = goal.raw_prompt
    kinds = {i.kind for i in goal.inputs}
    if InputKind.IMAGE in kinds:
        if _has_any(prompt, _TRANSFORM_VERBS) and not _question_like(prompt):
            return ("image.transform",
                    "image attached + transform verb, not question-like")
        return ("image.understand",
                "image attached; question-like or descriptive ask")
    if InputKind.AUDIO in kinds:
        return ("audio.transcribe", "audio attached")
    if InputKind.VIDEO in kinds:
        return ("audio.transcribe",
                "video attached; transcription is the only synchronous "
                "capability that accepts video")
    # InputKind has no DOCUMENT member — doc.extract is reached by naming the
    # capability explicitly, never inferred.
    if InputKind.URL in kinds:
        return ("web.fetch", "url attached")
    if _has_any(prompt, _SUMMARIZE_VERBS):
        return ("text.summarize", "no attachment + summarize verb")
    return ("text.chat", "default: no attachment, no routing verb")


# ---------------------------------------------------------------------------
# Provider seams — lazy reads, monkeypatchable in tests.
# ---------------------------------------------------------------------------


def _get_capability(name: str):
    return catalog.get_capability(name)


def _task_default_model(task: str) -> str | None:
    """The dispatcher's OWN default for a task-only request (TASK_DEFAULTS via
    resolve_model_key) — recorded, never re-invented. None when unresolvable."""
    try:
        from abstract_hugpy_dev.managers.resolvers.model_resolver import (
            resolve_model_key)
        return resolve_model_key(task=task)
    except Exception:  # noqa: BLE001 — no default is data, not a fault
        return None


def _studio_menu() -> str:
    """available_menu() — what the studio CAN render, for deferred responses."""
    try:
        from abstract_hugpy_dev.video_intel.studio.presets import available_menu
        return available_menu()
    except Exception:  # noqa: BLE001
        return ""


def _placement_for(model_id: str, task: str) -> str | None:
    """placement.json pin for (model, task), or None for the default route
    (DelegatingRunner: live worker if one serves it, else central-local)."""
    try:
        from abstract_hugpy_dev.managers.resolvers.model_resolver import peer_for
        peer = peer_for(model_id, task)
        return getattr(peer, "name", None) if peer is not None else None
    except Exception:  # noqa: BLE001
        return None


# ---------------------------------------------------------------------------
# The decision.
# ---------------------------------------------------------------------------


class RouteRefusal(ValueError):
    """A typed request-shape refusal (e.g. a requested model that does not
    serve the capability) — the route answers 400, never a traceback."""


@dataclass(frozen=True, slots=True)
class RouteDecision:
    """Where a goal goes and why — the object runtime + scorecard consume.

    ``execution`` is the branch: "execute" (synchronous dispatch), "deferred"
    (video.*: explained, not run), "gap" (typed CAPABILITY_GAP). ``task`` is
    the legacy dispatch task string ("execute" only). ``placement`` names a
    placement.json peer pin, or "auto" for the DelegatingRunner default."""
    capability: str
    execution: str
    source: str = ""
    task: str | None = None
    model_id: str | None = None
    model_rationale: str = ""       # requested | only-eligible | default | deterministic-local
    placement: str = "auto"
    inferred: bool = False
    inference_reason: str = ""
    produces: tuple[ArtifactKind, ...] = ()
    reasons: tuple[str, ...] = ()   # gap reasons / deferred verdict / advisories
    alternatives: str = ""          # studio available_menu (deferred only)
    model_ids: tuple[str, ...] = field(default=())

    def to_dict(self) -> dict[str, Any]:
        return {
            "capability": self.capability,
            "execution": self.execution,
            "source": self.source,
            "task": self.task,
            "model_id": self.model_id,
            "model_rationale": self.model_rationale,
            "placement": self.placement,
            "inferred": self.inferred,
            "inference_reason": self.inference_reason,
            "produces": [k.value for k in self.produces],
            "reasons": list(self.reasons),
            "alternatives": self.alternatives,
            "model_ids": list(self.model_ids),
        }


def resolve_route(goal: GoalSpec, requested_model: str | None = None) -> RouteDecision:
    """Goal -> RouteDecision through the k90 catalog. Never raises for a
    missing/ineligible capability (that is the gap SHAPE); raises RouteRefusal
    only for a request-shape fault (a requested model outside the capability's
    eligible set)."""
    if goal.capability is not None:
        name, inferred, why = goal.capability, False, "explicit capability in request"
    else:
        name, why = infer_capability(goal)
        inferred = True

    view = _get_capability(name)
    if view is None:
        return RouteDecision(
            capability=name, execution="gap", inferred=inferred,
            inference_reason=why,
            reasons=(f"unknown capability {name!r}: not in the unified "
                     f"catalog (GET /oracle/capabilities lists what exists)",))

    if name.startswith("video."):
        # k91 explains the best video route via the studio's own verdict but
        # does not execute it — the studio job routes own that pipeline.
        return RouteDecision(
            capability=name, execution="deferred", source=view.source.value,
            model_id=view.model_ids[0] if view.model_ids else None,
            model_ids=view.model_ids,
            model_rationale="studio-router" if view.model_ids else "",
            inferred=inferred, inference_reason=why,
            produces=view.produces,
            reasons=view.eligibility.reasons or (
                ("servable per the studio capability verdict",)
                if view.eligibility.eligible else ()),
            alternatives=_studio_menu())

    if not view.eligibility.eligible:
        return RouteDecision(
            capability=name, execution="gap", source=view.source.value,
            inferred=inferred, inference_reason=why, produces=view.produces,
            reasons=view.eligibility.reasons)

    task = CAPABILITY_TASK.get(name)
    if task is None:  # a legacy capability outside the dispatch table — drift alarm
        return RouteDecision(
            capability=name, execution="gap", source=view.source.value,
            inferred=inferred, inference_reason=why, produces=view.produces,
            reasons=(f"capability {name!r} has no dispatch task mapping "
                     f"(oracle/router.CAPABILITY_TASK drift)",))

    deterministic = task in catalog.DETERMINISTIC_TASKS
    if requested_model is not None:
        if view.model_ids and requested_model not in view.model_ids:
            raise RouteRefusal(
                f"model {requested_model!r} does not serve capability {name!r} "
                f"on this fleet; eligible: {list(view.model_ids)}")
        model_id, rationale = requested_model, "requested"
    elif deterministic:
        model_id, rationale = None, "deterministic-local"
    elif len(view.model_ids) == 1:
        model_id, rationale = view.model_ids[0], "only-eligible"
    else:
        model_id = _task_default_model(task)
        if model_id not in view.model_ids:
            # default resolution failed or landed outside the eligible set
            # (e.g. the default is operator-blocked) — take the first eligible.
            model_id = view.model_ids[0]
        rationale = "default"

    if deterministic:
        placement = "local"
    elif model_id:
        placement = _placement_for(model_id, task) or "auto"
    else:
        placement = "auto"
    return RouteDecision(
        capability=name, execution="execute", source=view.source.value,
        task=task, model_id=model_id, model_rationale=rationale,
        placement=placement, inferred=inferred, inference_reason=why,
        produces=view.produces, model_ids=view.model_ids,
        reasons=view.eligibility.reasons)  # advisory reasons ride along


__all__ = ["CAPABILITY_TASK", "RouteDecision", "RouteRefusal",
           "infer_capability", "resolve_route"]
