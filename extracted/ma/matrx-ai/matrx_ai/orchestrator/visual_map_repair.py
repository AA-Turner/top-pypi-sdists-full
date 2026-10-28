"""THE VISUAL-MAP REPAIR LOOP — a diagram the model writes is checked, repaired and stamped by the server.

Owner's words: common-docs ``systems/content/visual-maps/VISION.md`` ("iteratively get the diagram to
actually display properly"; "specialists, not one AI"). Plan: common-docs
``projects/legible-diagrams/PLAN.md`` item L4.

When a run is about to finish and its final answer carries a ``visual_map`` value
(``{"__kind": "visual_map", "type", "spec", ...}``), ``visual_map_gate`` runs this loop BEFORE the turn
is persisted:

1. **validate** the spec with the diagram engine (host seam, quality from the knob);
2. errors → hand the diagnostics to a **repair** call point. The host runs the
   ``visual_maps.diagram_repair`` mandate when an agent is bound to it; when none is, the AUTHORING
   model itself gets the diagnostics as a host-written turn in a muted child call and answers with a
   corrected spec. Every call point invocation is captured as a Provision window by the host;
   Before any model call, ``visual_map_fixes.mechanical_fixes`` applies what the engine's evidence fully
   determines. The repairer sees ONE diagnostic group when the list is long and answers with a PATCH that
   code applies to the BEST spec. The loop is MONOTONE: a round is adopted only with fewer errors than the
   best so far, and the next round restarts from the best spec (the notice says so);
3. stop at the first of: no errors · the round knob (default 4) · the stall knob's number of answers in a
   row (default 2) that were not adopted;
4. the LAST round calls **deliver** on the best spec seen (render, headless inspection, screenshot,
   ``render_inspection`` row); every earlier round is saved as a diagnostics-only row;
5. the ``visual_maps.diagram_review`` call point (an image-reading agent) may ADD findings — it can
   never mark a diagram verified; unbound, it is skipped and the round log says so;
6. the server STAMPS ``verified``, ``issues``, ``receipt``, ``inspection_id`` and the stamped value
   replaces the draft in the durable turn text. A model's own values for those four are neutralised at
   parse time by the kind corrector registered below — never trusted.

Never silent: the stream carries ``visual_map_checking`` when the check starts and
``visual_map_checked`` (with the stamped value and the round log) when it ends, plus a
``visual_map_unverified`` warning whenever the final value is not verified.

matrx-ai never imports the host. Everything that needs the database, the diagram service or the mandate
registry arrives through ONE seam: ``configure_ext(visual_map_delivery=...)`` (``VisualMapDelivery``).
Unconfigured → the gate does nothing and says so once in the log.
"""

from __future__ import annotations

import asyncio
import contextvars
import hashlib
import json
import logging
from collections.abc import Awaitable, Callable
from dataclasses import asdict, dataclass, field
from typing import Any, Protocol
from uuid import uuid4

from matrx_utils.knob_fallback import knob_or_declared_default

from matrx_ai.orchestrator.visual_map_fixes import (
    PATCH_INSTRUCTIONS,
    apply_patch,
    identity_fixes,
    mechanical_fixes,
    parse_patch,
    patch_from_whole_spec,
    prompt_diagnostics,
)

logger = logging.getLogger(__name__)

VISUAL_MAP_KIND = "visual_map"
#: The engine's ten diagram types (``@ai-matrx/diagrams`` ``DiagramType``).
DIAGRAM_TYPES: tuple[str, ...] = (
    "architecture",
    "workflow",
    "sequence",
    "dataflow",
    "lifecycle",
    "erd",
    "class",
    "tree",
    "timeline",
    "waterfall",
)
#: The four fields only the server writes.
STAMP_FIELDS: tuple[str, ...] = ("verified", "issues", "receipt", "inspection_id")

HOOK_KEY = "visual_map_delivery"
#: AppContext.metadata flag on the muted child call that repairs a diagram; the gate never runs there.
REPAIR_CHILD_KEY = "visual_map_repair_child"
REPAIR_MANDATE_KEY = "visual_maps.diagram_repair"
REVIEW_MANDATE_KEY = "visual_maps.diagram_review"

#: Stream codes (InfoPayload / WarningPayload ``code``) — the chat renderer's contract.
CHECKING_CODE = "visual_map_checking"
CHECKED_CODE = "visual_map_checked"
UNVERIFIED_CODE = "visual_map_unverified"

#: Knob keys the host resolves (feature ``content.visual_maps``).
KNOB_MAX_ROUNDS = "repair_max_rounds"
KNOB_STALL_ROUNDS = "repair_stall_rounds"
KNOB_QUALITY = "quality"
KNOB_GROUP_MAX = "repair_group_max"
KNOB_REPAIR_MODEL = "repair_model"


@dataclass(frozen=True)
class RepairKnobs:
    max_rounds: int
    stall_rounds: int
    quality: str
    #: More errors than this → the repairer gets one diagnostic group per round. The default is the
    #: package's declared starting value; the host's ``repair_group_max`` knob row governs.
    group_max: int = 6
    #: The model the authoring-model fallback repairs with; "" = the authoring model itself.
    repair_model: str = ""


#: The package's standalone defaults — used ONLY for a key the host's knob rows did not answer
#: (deploy order, or a host without the rows); every such use is named in the round log. The rows
#: (aidream ``content.visual_maps``) govern.
DECLARED_KNOBS = RepairKnobs(max_rounds=4, stall_rounds=2, quality="showcase")


def knobs_from(values: dict[str, Any] | None) -> tuple[RepairKnobs, list[str]]:
    """The effective knobs from the host's answer, and the keys that fell back to the declared default."""
    values = values or {}
    missing: list[str] = []

    def _int(key: str, default: int, floor: int) -> int:
        raw = values.get(key)
        try:
            return max(floor, int(raw))
        except (TypeError, ValueError):
            missing.append(key)
            return default

    max_rounds = _int(KNOB_MAX_ROUNDS, DECLARED_KNOBS.max_rounds, 1)
    stall_rounds = _int(KNOB_STALL_ROUNDS, DECLARED_KNOBS.stall_rounds, 1)
    quality = values.get(KNOB_QUALITY)
    if not isinstance(quality, str) or not quality.strip():
        missing.append(KNOB_QUALITY)
        quality = DECLARED_KNOBS.quality
    group_max = _int(KNOB_GROUP_MAX, DECLARED_KNOBS.group_max, 1)
    repair_model = values.get(KNOB_REPAIR_MODEL)
    if not isinstance(repair_model, str):
        missing.append(KNOB_REPAIR_MODEL)
        repair_model = ""
    return RepairKnobs(max_rounds, stall_rounds, quality.strip(), group_max, repair_model.strip()), missing


def error_count(diagnostics: Any) -> int:
    return sum(1 for d in diagnostics or [] if isinstance(d, dict) and d.get("severity") == "error")


def stop_reason(counts: list[int], knobs: RepairKnobs) -> str | None:
    """Why the loop stops after the round whose error count is ``counts[-1]``, or None to repair again.

    * ``clean`` — no errors left.
    * ``max_rounds`` — the round knob is spent.
    * ``stalled`` — the last ``stall_rounds`` rounds set no new low (errors did not fall).
    """
    if not counts:
        return None
    if counts[-1] == 0:
        return "clean"
    if len(counts) >= knobs.max_rounds:
        return "max_rounds"
    if len(counts) > knobs.stall_rounds:
        before = min(counts[: -knobs.stall_rounds])
        if min(counts[-knobs.stall_rounds :]) >= before:
            return "stalled"
    return None


@dataclass
class RoundRecord:
    round: int
    stage: str  # "validate" | "deliver"
    error_count: int
    warning_count: int
    diagnostics: list[dict[str, Any]] = field(default_factory=list)
    spec_sha256: str = ""
    repaired_by: str | None = None  # "agent" | "authoring_model" | None
    repair_snapshot_id: str | None = None
    persisted_id: str | None = None
    note: str | None = None
    #: True when this round's spec became the best so far (the loop only ever moves to a better spec).
    adopted: bool = True

    def summary(self) -> dict[str, Any]:
        out = asdict(self)
        out.pop("diagnostics", None)
        return out


@dataclass
class RepairOutcome:
    value: dict[str, Any]
    rounds: list[RoundRecord]
    stop_reason: str
    notes: list[str] = field(default_factory=list)
    review: dict[str, Any] | None = None
    #: Labels of first-draft items the delivered spec still does not draw (content/dropped at delivery).
    dropped: list[str] = field(default_factory=list)

    def adopted_counts(self) -> list[int]:
        out: list[int] = []
        for r in self.rounds:
            if r.stage in ("validate", "mechanical"):
                current = r.error_count if (r.adopted or not out) else out[-1]
                out.append(min(current, out[-1]) if out else current)
        return out

    @property
    def verified(self) -> bool:
        return bool(self.value.get("verified"))

    def log(self) -> dict[str, Any]:
        return {
            "stop_reason": self.stop_reason,
            "rounds": [r.summary() for r in self.rounds],
            "error_counts": [r.error_count for r in self.rounds if r.stage == "validate"],
            # The best-so-far error count after each checked round: never rises (the loop is monotone).
            "adopted_counts": self.adopted_counts(),
            "dropped": list(self.dropped),
            "notes": list(self.notes),
            "review": self.review,
        }


@dataclass
class CallPointResult:
    """What the host's call point answered. ``bound`` False = no agent is bound to the mandate."""

    bound: bool
    value: Any = None
    snapshot_id: str | None = None
    note: str | None = None


class VisualMapDelivery(Protocol):
    """The host seam (``configure_ext(visual_map_delivery=...)``). Every method must never raise for a
    bad spec or a down service; a raise is caught by the loop and reported, never swallowed."""

    async def read_knobs(self, *, organization_id: str | None, user_id: str | None) -> dict[str, Any]: ...

    async def validate(self, type: str, spec: dict[str, Any], *, quality: str) -> dict[str, Any]: ...

    async def deliver(
        self, type: str, spec: dict[str, Any], *, organization_id: str | None, subject_ref: str,
        round: int, quality: str,
    ) -> dict[str, Any]: ...

    async def persist_round(
        self, *, organization_id: str | None, subject_ref: str, round: int, spec: dict[str, Any],
        diagnostics: list[dict[str, Any]],
    ) -> str | None: ...

    async def repair(self, provision: dict[str, Any], *, organization_id: str | None) -> CallPointResult: ...

    async def review(self, provision: dict[str, Any], *, organization_id: str | None) -> CallPointResult: ...

    # Optional: the type's authoring card (essential schema rules + one real example) as text. A host
    # without it leaves the repair notice to the diagnostics alone.
    async def authoring_card(self, type: str) -> str | None: ...

    # Optional: the engine's CURRENT ``schema_version`` for a type. A spec that omits ``schema_version``
    # gets it from here before validation; a host without it fills only ``diagram_type``.
    async def schema_version(self, type: str) -> int | None: ...

    # Optional: the spec as the engine reads it. ``visual_map.spec``'s strict JSON Schema writes each open map
    # as ``[{key, value}]`` entries; this turns them back into the map and leaves a map already there (the
    # skill path's free JSON) untouched. A host without it hands the spec to the engine as written.
    def spec_for_engine(self, type: str, spec: dict[str, Any]) -> dict[str, Any]: ...


FallbackRepair = Callable[[dict[str, Any]], Awaitable[Any]]


def spec_sha(spec: Any) -> str:
    return hashlib.sha256(json.dumps(spec, sort_keys=True, default=str).encode()).hexdigest()


def coerce_visual_map(obj: Any, default_type: str) -> tuple[str, dict[str, Any]] | None:
    """(type, spec) from a repair answer: a visual_map value, ``{type, spec}``, a bare spec, or text holding one."""
    if isinstance(obj, str):
        found = find_visual_maps(obj)
        if found:
            return coerce_visual_map(found[-1][2], default_type)
        try:
            obj = json.loads(obj.strip())
        except (ValueError, TypeError):
            return None
    if not isinstance(obj, dict):
        return None
    if isinstance(obj.get("spec"), dict):
        t = obj.get("type") or obj["spec"].get("diagram_type") or default_type
        return (t, obj["spec"]) if t in DIAGRAM_TYPES else None
    if "diagram_type" in obj or "schema_version" in obj:
        t = obj.get("diagram_type") or default_type
        return (t, obj) if t in DIAGRAM_TYPES else None
    return None


def find_visual_maps(text: str) -> list[tuple[int, int, dict[str, Any]]]:
    """Every complete ``visual_map`` object in ``text`` as (start, end, value), in document order.

    Uses the block detector's ONE region finder (balanced JSON objects declaring ``__kind``, in any
    container — fence, artifact body, bare)."""
    if not isinstance(text, str) or VISUAL_MAP_KIND not in text:
        return []
    from matrx_ai.processing.blocks.block_detector import _embedded_kind_json_regions

    out: list[tuple[int, int, dict[str, Any]]] = []
    for start, end, kind in _embedded_kind_json_regions(text):
        if kind != VISUAL_MAP_KIND:
            continue
        try:
            value = json.loads(text[start:end])
        except (ValueError, TypeError):
            continue
        if isinstance(value, dict):
            out.append((start, end, value))
    return out


#: What each diagram type draws (its required top-level lists): how a value with no usable ``type`` is read.
_TYPE_SIGNATURES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("architecture", ("components",)),
    ("sequence", ("participants", "messages")),
    ("dataflow", ("stages", "flows")),
    ("lifecycle", ("states", "transitions")),
    ("erd", ("entities",)),
    ("class", ("types",)),
    ("timeline", ("events",)),
    ("waterfall", ("spans",)),
    ("workflow", ("nodes", "edges")),
    ("tree", ("nodes",)),
)


def infer_identity(value: dict[str, Any]) -> tuple[str | None, dict[str, Any] | None, str | None]:
    """(type, spec, what was inferred) for a visual_map value whose ``type`` is missing or unknown.

    2026-10-23 S5: Haiku wrote ``"type": null`` with a full dataflow spec; the loop answered "unreadable" and
    nothing was checked. The spec's own ``diagram_type``, else the lists it draws, name the type."""
    spec = value.get("spec") if isinstance(value.get("spec"), dict) else None
    type_ = value.get("type") if value.get("type") in DIAGRAM_TYPES else None
    if type_ is not None or spec is None:
        return type_, spec, None
    if spec.get("diagram_type") in DIAGRAM_TYPES:
        return spec["diagram_type"], spec, f"type {spec['diagram_type']} (the spec's diagram_type)"
    for name, keys in _TYPE_SIGNATURES:
        if all(isinstance(spec.get(k), list) for k in keys):
            return name, spec, f"type {name} (the spec draws {', '.join(keys)})"
    return None, spec, None


async def fill_identity(
    delivery: VisualMapDelivery, type_: str, spec: dict[str, Any]
) -> tuple[dict[str, Any], list[str]]:
    """``spec`` with ``diagram_type`` and ``schema_version`` filled from the value's ``type`` when the model
    left them out (2026-10-23 S3: Haiku omitted both; every repair round chased the schema instead of the
    layout), and ``diagram_type`` corrected to ``type`` when it disagrees (the engine's constant).
    Deterministic; a written ``schema_version`` is left to the engine's check. Returns (spec, names filled)."""
    filled: list[str] = []
    out = dict(spec)
    to_engine = getattr(delivery, "spec_for_engine", None)
    if to_engine is not None:
        # Both forms are accepted: entries arrays (a strict Output Schema's answer) become the engine's maps,
        # a map already there is left as written.
        decoded = to_engine(type_, out)
        if isinstance(decoded, dict) and decoded != out:
            out = dict(decoded)
            filled.append("entry maps")
    if out.get("diagram_type") != type_:
        # Each engine schema's diagram_type is the constant of its type, so the value's ``type`` decides;
        # a written "state" / "data_flow" (2026-10-24 S4/S5) can only fail, and the repairer may not edit it.
        out["diagram_type"] = type_
        filled.append("diagram_type")
    if out.get("schema_version") in (None, ""):
        reader = getattr(delivery, "schema_version", None)
        version = None
        if reader is not None:
            try:
                version = await reader(type_)
            except Exception:  # noqa: BLE001 — an unknown version leaves the field to the validator
                logger.exception("[visual_map] schema_version for %s could not be read", type_)
        if isinstance(version, int):
            out["schema_version"] = version
            filled.append("schema_version")
    if filled:
        # The engine reads these two first; keep them at the top of the spec, as the examples write them.
        head = {k: out[k] for k in ("schema_version", "diagram_type") if k in out}
        out = {**head, **{k: v for k, v in out.items() if k not in head}}
    return (out if filled else spec), filled


#: Top-level spec lists that hold geometry or prose about the drawing, not the drawing's content.
_NOT_CONTENT = frozenset({"meta", "layout", "cards", "mainPath", "semanticChecks", "views", "legend",
                          # Grouping containers: regrouping (two stages merged into one) moves content, it
                          # does not drop it (2026-10-23 S5: dataflow allows at most 5 stages).
                          "stages", "lanes", "phases", "groups", "boundaries", "segments", "activations"})


def _item_name(item: dict[str, Any]) -> str | None:
    for key in ("id", "label", "name", "title", "text"):
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    if item.get("from") is not None and item.get("to") is not None:
        return f"{item.get('from')}->{item.get('to')}"
    return None


def content_inventory(spec: Any) -> dict[str, dict[str, str]]:
    """What a spec draws: per top-level list (nodes, edges, states, transitions, messages, ...), each item's
    identity (its id, else its label) mapped to its readable label."""
    out: dict[str, dict[str, str]] = {}
    if not isinstance(spec, dict):
        return out
    for key, value in spec.items():
        if key in _NOT_CONTENT or not isinstance(value, list):
            continue
        items: dict[str, str] = {}
        for item in value:
            if isinstance(item, dict):
                name = _item_name(item)
                if name:
                    label = item.get("label") or item.get("name") or item.get("title") or name
                    items[name] = str(label)
        if items:
            out[key] = items
    return out


def _explained_in_spec(spec: Any, ident: str, label: str) -> bool:
    """A drop is explained when the spec's own visible notes (its ``cards``) name the dropped item."""
    cards = spec.get("cards") if isinstance(spec, dict) else None
    if not cards:
        return False
    text = json.dumps(cards, ensure_ascii=False).lower()
    return any(t and t.lower() in text for t in (ident, label))


def dropped_content(draft: dict[str, dict[str, str]], spec: Any) -> list[dict[str, Any]]:
    """Error diagnostics for every item of the FIRST draft that ``spec`` no longer draws and its notes do
    not explain (2026-10-23 S4: "verified" with 9 of the 11 states; repair had dropped two to pass layout)."""
    now = content_inventory(spec)
    out: list[dict[str, Any]] = []
    for key, items in draft.items():
        kept = now.get(key, {})
        missing = [(i, label) for i, label in items.items() if i not in kept and not _explained_in_spec(spec, i, label)]
        if not missing:
            continue
        names = ", ".join(label for _, label in missing)
        out.append({
            "code": "content/dropped",
            "severity": "error",
            "message": f"content dropped: {key}: {names} (the first draft drew {len(items)} {key}, this one {len(kept)})",
            "subject": {"list": key, "ids": [i for i, _ in missing]},
            "evidence": {"draft_count": len(items), "count": len(kept)},
            "supportedFixes": [
                f"put back {names} in {key}; fix the layout by moving, shortening or regrouping, never by removing content",
                "if the item truly must go, say so in a card of the spec (cards[].items) so the reader is told",
            ],
        })
    return out


def _compact_diagnostics(diagnostics: list[dict[str, Any]]) -> list[dict[str, Any]]:
    keep = ("code", "severity", "message", "subject", "evidence", "supportedFixes")
    return [{k: d.get(k) for k in keep if k in d} for d in diagnostics if isinstance(d, dict)]


def _one_line(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(", ", ": "), default=str)


def _diagnostic_lines(n: int, d: dict[str, Any]) -> list[str]:
    lines = [f"{n}. [{d.get('code') or 'unknown'}] {d.get('message') or ''}".rstrip()]
    if d.get("subject"):
        lines.append(f"   where: {_one_line(d['subject'])}")
    if d.get("evidence"):
        lines.append(f"   evidence: {_one_line(d['evidence'])}")
    fixes = [f for f in d.get("supportedFixes") or [] if isinstance(f, str) and f]
    pins = [p.get("path") for p in (d.get("evidence") or {}).get("conflictingPins") or []
            if isinstance(p, dict) and p.get("path")]
    if not fixes and pins:
        # The engine names the hand-set geometry that conflicts but offers no fix: deleting the pin lets
        # the engine route it (2026-10-21 S6: Haiku re-pinned channelX three rounds running).
        fixes = [f"delete {', '.join(pins)} and let the engine route it"]
    if fixes:
        lines.append(f"   supported fixes: {'; '.join(fixes)}")
    return lines


def _diag_key(d: dict[str, Any]) -> str:
    return _one_line([d.get("code"), d.get("message")])


def repair_notice(provision: dict[str, Any]) -> str:
    """The host-written turn the authoring model reads when it repairs its own diagram.

    Every error diagnostic goes in whole (code, message, subject, evidence, supportedFixes — never
    truncated), the model is told to change ONLY what they name, the earlier rounds' counts show whether
    its last change helped, and the type's authoring card (the engine's rules + a real example) is
    attached so a schema error can be fixed from the schema, not guessed (2026-10-21: the old notice
    said "never add coordinates" while the sequence schema requires ``y``; the model oscillated)."""
    diags = [d for d in provision.get("diagnostics") or [] if isinstance(d, dict)]
    errors = [d for d in diags if d.get("severity") == "error"]
    warnings = len(diags) - len(errors)
    parts = [
        "SYSTEM NOTICE (not from the user): the diagram engine checked the visual_map you just wrote "
        f"(round {provision.get('round')} of at most {provision.get('max_rounds')}) and found "
        f"{len(errors)} error(s)" + (f" and {warnings} warning(s), which you may leave" if warnings else "") + ".",
        "Fix every error below. Change ONLY the fields they name, using the supported fixes listed with "
        "each; keep every other part of your spec exactly as you wrote it. Keep the same diagram type and "
        "meaning. Where an error names a required field or a number, write exactly what the rules below allow. "
        "Prefer deleting hand-set geometry (via, channelX/channelY, labelDx/labelDy, bias, pos) over adding "
        "more: the engine routes and places what you leave out.",
    ]
    total = provision.get("error_count")
    if provision.get("group") and isinstance(total, int) and total > len(errors):
        parts.append(
            f"The diagram has {total} errors in all; this round fixes ONE group of them ({provision['group']}). "
            "The others come in later rounds: leave them alone now."
        )
    prior = [r for r in provision.get("prior_rounds") or [] if isinstance(r, dict) and r.get("stage") == "validate"]
    if prior:
        history = "; ".join(
            f"round {r.get('round')}: {r.get('error_count')} errors" + ("" if r.get("adopted", True) else " (not adopted)")
            for r in prior
        )
        current = f"round {provision.get('round')}: {len(errors)} errors"
        stuck = prior[-1].get("error_count") is not None and len(errors) >= int(prior[-1]["error_count"])
        parts.append(
            f"Earlier rounds: {history}; now {current}."
            + (" Your last change did not reduce the errors: read the rules below and do something different." if stuck else "")
        )
    last = provision.get("last_attempt_errors")
    if isinstance(last, int) and isinstance(total, int) and last >= total:
        parts.append(
            f"Your last answer made it worse ({last} errors, the best is {total}), so it was NOT used. You are "
            f"starting again from the best version (round {provision.get('best_round')}), shown above as your "
            "previous answer. Make a smaller, different change."
        )
    before = {_diag_key(d) for d in provision.get("previous_errors") or [] if isinstance(d, dict)}
    caused = [d for d in errors if before and _diag_key(d) not in before]
    if caused:
        parts.append(
            f"{len(caused)} of these errors are NEW this round (marked NEW): your last change caused them. "
            "When you move one item, keep the spacing the diagnostics name from its neighbours; if there "
            "is no room, move every later item by the same amount instead of squeezing one."
        )
    lines = [f"Errors ({len(errors)}):"]
    for n, d in enumerate(errors, 1):
        block = _diagnostic_lines(n, d)
        if caused and d in caused:
            block[0] = block[0].replace(f"{n}. ", f"{n}. NEW ", 1)
        lines += block
    parts.append("\n".join(lines))
    card = provision.get("authoring_card")
    if isinstance(card, str) and card.strip():
        parts.append(card.strip())
    parts.append(PATCH_INSTRUCTIONS)
    return "\n\n".join(parts)


class _Unavailable(Exception):
    """The diagram service could not be reached while checking a round."""


@dataclass
class _Checked:
    """One spec's check: its errors (validate, or the measured render when validate is clean, plus drops)."""

    type: str
    spec: dict[str, Any]
    errors: int
    diagnostics: list[dict[str, Any]]
    sha: str
    round: int
    note: str | None = None
    canvas_width: float | None = None


def _canvas_width(delivered: dict[str, Any] | None) -> float | None:
    view = ((delivered or {}).get("receipt") or {}).get("viewBox")
    if isinstance(view, list) and len(view) == 4 and isinstance(view[2], (int, float)) and view[2] > 0:
        return float(view[2])
    return None


async def _check(
    delivery: VisualMapDelivery, cache: dict[str, dict[str, Any]], type_: str, spec: dict[str, Any], n: int,
    draft_content: dict[str, dict[str, str]], organization_id: str | None, subject_ref: str, quality: str,
    notes: list[str],
) -> _Checked:
    checked = await delivery.validate(type_, spec, quality=quality)
    if not isinstance(checked, dict) or checked.get("unavailable"):
        raise _Unavailable()
    diags = [d for d in checked.get("diagnostics") or [] if isinstance(d, dict)]
    errors = error_count(diags)
    note: str | None = None
    width: float | None = None
    if errors == 0:
        # The validator is clean: render and MEASURE it now. A clipped label or an overlap only shows in the
        # measured render (2026-10-21 S1: validate [1, 0], delivered with 4 issues and no round left to
        # repair them), so measured defects drive the next repair.
        delivered = await _deliver_once(delivery, cache, type_, spec, organization_id, subject_ref, n, quality, notes)
        width = _canvas_width(delivered)
        if not delivered.get("unavailable") and not delivered.get("verified"):
            measured = [d for d in delivered.get("diagnostics") or []
                        if isinstance(d, dict) and d.get("severity") == "error"]
            measured += [d for d in delivered.get("measured_diagnostics") or [] if isinstance(d, dict)]
            if measured:
                diags = measured
                errors = len(measured)
                note = "the spec validated clean; these errors were measured in the rendered diagram"
    drops = dropped_content(draft_content, spec)
    if drops:
        diags = diags + drops
        errors += len(drops)
    return _Checked(type_, spec, errors, diags, spec_sha(spec), n, note, width)


def _record(c: _Checked, stage: str, adopted: bool, note: str | None = None) -> RoundRecord:
    notes = [x for x in (c.note, note) if x]
    return RoundRecord(
        round=c.round, stage=stage, error_count=c.errors,
        warning_count=sum(1 for d in c.diagnostics if d.get("severity") == "warning"),
        diagnostics=c.diagnostics, spec_sha256=c.sha, adopted=adopted, note="; ".join(notes) or None,
    )


async def run_repair_loop(
    value: dict[str, Any],
    *,
    delivery: VisualMapDelivery,
    knobs: RepairKnobs,
    organization_id: str | None,
    subject_ref: str,
    user_request: str,
    fallback_repair: FallbackRepair | None,
) -> RepairOutcome:
    """Check → mechanical fixes → one diagnostic group to the repairer as a patch → … → deliver → review → stamp.

    MONOTONE: a round is adopted only when it has FEWER errors than the best so far; every repair starts from
    the best spec (and the notice says so), and the delivered spec is always the best one. Never raises (a
    failure is an unverified, stated value)."""
    rounds: list[RoundRecord] = []
    notes: list[str] = []
    type_, spec, inferred = infer_identity(value)
    if inferred:
        notes.append(f"filled from the spec before checking: {inferred}")
    if type_ is None or spec is None:
        notes.append("the value has no known diagram type or no spec object; nothing could be checked")
        return RepairOutcome(_stamp(value, type_, spec, None, False, 0), rounds, "unreadable", notes)

    if not set(spec) - {"schema_version", "diagram_type"}:
        # 2026-10-24 live: a strict decoder forced ``"spec": {}``; checking the filled-in identity answered
        # "/ must have required property 'meta'" for a diagram that was never written. Say what happened.
        notes.append("the spec holds no diagram content (nothing but its identity); nothing could be drawn")
        return RepairOutcome(_stamp(value, type_, spec, None, False, 0), rounds, "empty", notes)

    spec, filled = await fill_identity(delivery, type_, spec)
    if filled:
        notes.append(f"filled from the value's type before checking: {', '.join(filled)}")
    draft_content = content_inventory(spec)
    delivered_by_sha: dict[str, dict[str, Any]] = {}  # a spec is rendered + measured at most once
    best: _Checked | None = None
    reason = "clean"
    n = 0  # validate rounds that count against the round knob (the first check + one per repair answer)
    rejected_streak = 0
    last_attempt: _Checked | None = None
    tried_mechanical: set[str] = set()  # a mechanical candidate is checked once

    async def check(t: str, s: dict[str, Any], rnd: int) -> _Checked:
        return await _check(delivery, delivered_by_sha, t, s, rnd, draft_content, organization_id, subject_ref,
                            knobs.quality, notes)

    async def persist(rec: RoundRecord, c: _Checked) -> None:
        if c.sha in delivered_by_sha:
            rec.persisted_id = delivered_by_sha[c.sha].get("inspection_id")
        else:
            rec.persisted_id = await delivery.persist_round(
                organization_id=organization_id, subject_ref=subject_ref, round=c.round, spec=c.spec,
                diagnostics=c.diagnostics,
            )

    try:
        n = 1
        best = await check(type_, spec, n)
        rec = _record(best, "validate", True)
        rounds.append(rec)
        while True:
            if best.errors == 0:
                reason = "clean"
                break
            # 0. Identity: the engine's constant, which no repairer may write — adopted unconditionally.
            ident_spec, ident_edits = identity_fixes(best.spec, best.diagnostics)
            if ident_edits and spec_sha(ident_spec) not in tried_mechanical:
                tried_mechanical.add(spec_sha(ident_spec))
                await persist(rounds[-1], best) if rounds[-1].persisted_id is None else None
                best = await check(best.type, ident_spec, best.round)
                rounds.append(_record(best, "mechanical", True, "applied: " + "; ".join(ident_edits)))
                notes.append(f"identity set to the engine's constant: {'; '.join(ident_edits)}")
                continue
            # 1. Mechanical: what the engine's own evidence fully determines, no model involved.
            fixed, edits = mechanical_fixes(best.type, best.spec, best.diagnostics)
            if edits and spec_sha(fixed) not in tried_mechanical:
                tried_mechanical.add(spec_sha(fixed))
                candidate = await check(best.type, fixed, best.round)
                # Fewer errors, or as many but every one of them new: the engine reports one route-preset
                # conflict at a time, so clearing it reveals the next (2026-10-23 S3/S6: 1 → 1, a different
                # edge). Never more errors; tried candidates are never re-checked, so this cannot cycle.
                moved_past = candidate.errors == best.errors and not (
                    {_diag_key(d) for d in candidate.diagnostics} & {_diag_key(d) for d in best.diagnostics})
                better = candidate.errors < best.errors or moved_past
                mrec = _record(candidate, "mechanical", better,
                               ("applied: " + "; ".join(edits)) + ("" if better else
                               f"; not adopted ({candidate.errors} errors, best is {best.errors})"))
                if better:
                    # The mechanical spec's own row is written below when it is not the final round.
                    await persist(rounds[-1], best) if rounds[-1].persisted_id is None and rounds[-1].stage != "deliver" else None
                    best = candidate
                    rounds.append(mrec)
                    notes.append(f"mechanical fixes: {'; '.join(edits)}")
                    continue
                rounds.append(mrec)
                await persist(mrec, candidate)
            if n >= knobs.max_rounds:
                reason = "max_rounds"
                break
            if rejected_streak >= knobs.stall_rounds:
                reason = "stalled"
                break
            # 2. Judgment: one diagnostic group to the repairer, starting from the BEST spec.
            await persist(rounds[-1], best) if rounds[-1].persisted_id is None else None
            shown, group = prompt_diagnostics(best.diagnostics, canvas_width=best.canvas_width,
                                              group_max=knobs.group_max)
            provision = {
                "user_request": user_request,
                "diagram_type": best.type,
                "spec": best.spec,
                "diagnostics": shown,
                "error_count": best.errors,
                "group": group,
                "measurements": None,
                "receipt": None,
                "round": n,
                "best_round": best.round,
                "max_rounds": knobs.max_rounds,
                "quality": knobs.quality,
                "repair_model": knobs.repair_model or None,
                "prior_rounds": [r.summary() for r in rounds],
                "subject_ref": subject_ref,
                "authoring_card": await _authoring_card(delivery, best.type),
                "previous_errors": [d for d in (last_attempt.diagnostics if last_attempt else [])
                                    if d.get("severity") == "error"],
                "last_attempt_errors": last_attempt.errors if last_attempt else None,
            }
            answer = await delivery.repair(provision, organization_id=organization_id)
            asking = rounds[-1]
            asking.repair_snapshot_id = answer.snapshot_id
            if answer.bound:
                asking.repaired_by = "agent"
                repaired = answer.value
            elif fallback_repair is not None:
                asking.repaired_by = "authoring_model"
                repaired = await fallback_repair(provision)
            else:
                asking.note = "no agent bound to the repair call point and no authoring model to fall back on"
                reason = "no_repairer"
                break
            n += 1
            try:
                candidate_spec, how = _apply_answer(repaired, best, shown)
            except Exception as exc:  # noqa: BLE001 — one malformed answer is a rejected round, not a lost loop
                logger.exception("[visual_map] repair answer could not be applied")
                candidate_spec, how = None, f"the answer could not be applied: {exc}"
            if candidate_spec is None:
                rounds.append(RoundRecord(round=n, stage="validate", error_count=best.errors, warning_count=0,
                                          note=how if how != "unreadable" else "the repair answer held no readable patch or spec",
                                          adopted=False))
                rejected_streak += 1
                last_attempt = None
                continue
            candidate_spec, filled = await fill_identity(delivery, best.type, candidate_spec)
            if filled:
                how = how + f"; filled {', '.join(filled)}"
            attempt = await check(best.type, candidate_spec, n)
            better = attempt.errors < best.errors
            arec = _record(attempt, "validate", better, how + ("" if better else
                           f"; not adopted ({attempt.errors} errors, best is round {best.round} with {best.errors});"
                           " the next round restarts from the best spec"))
            rounds.append(arec)
            last_attempt = attempt
            if better:
                best = attempt
                rejected_streak = 0
            else:
                rejected_streak += 1
                await persist(arec, attempt)
    except _Unavailable:
        reason = "unavailable"
        notes.append("the diagram service could not be reached; the layout was not checked")
    except Exception as exc:  # noqa: BLE001 — a check failure is stated on the value, never raised
        logger.exception("[visual_map] repair loop failed")
        notes.append(f"the layout check failed: {exc}")
        reason = "failed"

    if reason == "unavailable" or best is None:
        counts = [r.error_count for r in rounds]
        return RepairOutcome(
            _stamp(value, type_, spec, None, False, counts[-1] if counts else 0), rounds, reason, notes
        )

    d_type, d_spec, errors, d_round = best.type, best.spec, best.errors, best.round
    deliver_round = max(r.round for r in rounds) if rounds else 1
    if d_round != deliver_round:
        notes.append(f"round {d_round} had the fewest errors ({errors}); its spec is the one delivered")
    delivered = await _deliver_once(delivery, delivered_by_sha, d_type, d_spec, organization_id, subject_ref,
                                    deliver_round, knobs.quality, notes)
    d_diags = [d for d in delivered.get("diagnostics") or [] if isinstance(d, dict)]
    if isinstance(delivered.get("measured_diagnostics"), list):
        # Distinct defects, the same count the loop compared rounds by (the client's ``issues`` counts a
        # defect once per width x theme capture: S4 2026-10-23 read 14 in the loop and 28 at delivery).
        delivered = {**delivered, "issues": error_count(d_diags) + len(delivered["measured_diagnostics"])}
    rounds.append(
        RoundRecord(
            round=deliver_round, stage="deliver",
            error_count=int(delivered["issues"]) if isinstance(delivered.get("issues"), (int, float))
            else (error_count(d_diags) if d_diags else errors),
            warning_count=sum(1 for d in d_diags if d.get("severity") == "warning"),
            diagnostics=d_diags, spec_sha256=spec_sha(d_spec),
            persisted_id=delivered.get("inspection_id"), adopted=True,
            note="the diagram service could not be reached at delivery" if delivered.get("unavailable") else None,
        )
    )
    if delivered.get("unavailable"):
        notes.append("delivery could not reach the diagram service; the layout was not measured")
        return RepairOutcome(_stamp(value, d_type, d_spec, None, False, errors), rounds, reason, notes)

    verified = bool(delivered.get("verified"))
    issues = delivered.get("issues")
    issues = int(issues) if isinstance(issues, (int, float)) else errors
    drops = dropped_content(draft_content, d_spec)
    dropped_labels: list[str] = []
    if drops:
        # Layout passing by removing content is not a verified diagram of what was asked.
        verified = False
        issues += len(drops)
        rounds[-1].diagnostics = rounds[-1].diagnostics + drops
        rounds[-1].error_count += len(drops)
        notes.extend(d["message"] for d in drops)
        for d in drops:
            ids = (d.get("subject") or {}).get("ids") or []
            labels = draft_content.get((d.get("subject") or {}).get("list"), {})
            dropped_labels.extend(labels.get(i, i) for i in ids)

    review_log: dict[str, Any] | None = None
    shot = delivered.get("screenshot_file_id")
    if shot:
        try:
            reviewed = await delivery.review(
                {
                    "screenshot_file_id": shot,
                    "spec": d_spec,
                    "diagram_type": d_type,
                    "user_request": user_request,
                    "measurements": delivered.get("measurements"),
                    "diagnostics": d_diags,
                    "receipt": delivered.get("receipt"),
                    "inspection_id": delivered.get("inspection_id"),
                    "round": deliver_round,
                    "subject_ref": subject_ref,
                },
                organization_id=organization_id,
            )
        except Exception as exc:  # noqa: BLE001
            logger.exception("[visual_map] review failed")
            reviewed = CallPointResult(bound=False, note=f"review failed: {exc}")
        if reviewed.bound:
            findings = _findings(reviewed.value)
            issues += len(findings)
            if any(f.get("severity") == "error" for f in findings):
                verified = False  # review may fail a diagram; it can NEVER pass one
            review_log = {"bound": True, "findings": findings, "snapshot_id": reviewed.snapshot_id}
        else:
            review_log = {
                "bound": False,
                "snapshot_id": reviewed.snapshot_id,
                "note": reviewed.note or f"review skipped: no agent is bound to {REVIEW_MANDATE_KEY}",
            }
            notes.append(review_log["note"])
    else:
        notes.append("review skipped: delivery returned no screenshot")

    stamped = _stamp(value, d_type, d_spec, delivered, verified, issues)
    return RepairOutcome(stamped, rounds, reason, notes, review_log, dropped=dropped_labels)


def _apply_answer(
    repaired: Any, best: _Checked, shown: list[dict[str, Any]],
) -> tuple[dict[str, Any] | None, str]:
    """The repairer's answer applied to the BEST spec: a patch is applied as written; a whole spec is diffed
    and only the changes the shown diagnostics justify are kept (2026-10-23: whole-spec rewrites turned
    S2 1 error into 11). Returns (candidate spec or None, how it was applied)."""
    changes = parse_patch(repaired)
    how = "patch"
    reverted: list[str] = []
    if changes is None:
        parsed = coerce_visual_map(repaired, best.type)
        if parsed is None:
            return None, "unreadable"
        changes, reverted = patch_from_whole_spec(best.spec, parsed[1], shown)
        how = "whole spec answer, diffed"
    spec, applied, refused = apply_patch(best.spec, changes)
    parts = [f"{how}: {len(applied)} change(s) applied"]
    if reverted:
        parts.append(f"reverted {len(reverted)} change(s) to items no diagnostic named ({', '.join(reverted[:6])})")
    if refused:
        parts.append(f"refused {'; '.join(refused[:4])}")
    return spec, "; ".join(parts)


async def _deliver_once(
    delivery: VisualMapDelivery, cache: dict[str, dict[str, Any]], type_: str, spec: dict[str, Any],
    organization_id: str | None, subject_ref: str, round_: int, quality: str, notes: list[str],
) -> dict[str, Any]:
    """Render + measure + record one spec (once per distinct spec). Never raises."""
    sha = spec_sha(spec)
    if sha in cache:
        return cache[sha]
    try:
        delivered = await delivery.deliver(
            type_, spec, organization_id=organization_id, subject_ref=subject_ref, round=round_, quality=quality,
        )
    except Exception as exc:  # noqa: BLE001
        logger.exception("[visual_map] deliver failed")
        delivered = {"ok": False, "verified": False, "unavailable": True}
        notes.append(f"delivery failed: {exc}")
    delivered = delivered if isinstance(delivered, dict) else {"verified": False, "unavailable": True}
    if not delivered.get("unavailable"):
        cache[sha] = delivered
    return delivered


async def _authoring_card(delivery: VisualMapDelivery, type_: str) -> str | None:
    """The host's card for this type (the engine's rules + one real example), or None if it has none."""
    reader = getattr(delivery, "authoring_card", None)
    if reader is None:
        return None
    try:
        card = await reader(type_)
    except Exception:  # noqa: BLE001 — a missing card never stops a repair; the notice still goes
        logger.exception("[visual_map] authoring card for %s could not be read", type_)
        return None
    return card if isinstance(card, str) and card.strip() else None


def _findings(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, dict):
        value = value.get("findings")
    return [f for f in value or [] if isinstance(f, dict)]


def _stamp(
    value: dict[str, Any], type_: str | None, spec: dict[str, Any] | None,
    delivered: dict[str, Any] | None, verified: bool, issues: int,
) -> dict[str, Any]:
    out: dict[str, Any] = {"__kind": VISUAL_MAP_KIND, "type": type_ or value.get("type"), "spec": spec}
    if spec is None:
        out["spec"] = value.get("spec")
    if delivered and isinstance(delivered.get("receipt"), dict):
        out["receipt"] = delivered["receipt"]
    if delivered and delivered.get("inspection_id"):
        out["inspection_id"] = str(delivered["inspection_id"])
    out["verified"] = bool(verified)
    out["issues"] = max(0, int(issues or 0))
    return out


# ── Server stamps are the only stamps ──────────────────────────────────────────

_stamped: contextvars.ContextVar[frozenset[str]] = contextvars.ContextVar(
    "visual_map_server_stamps", default=frozenset()
)


def _value_sha(value: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, default=str).encode()).hexdigest()


def mark_server_stamped(value: dict[str, Any]) -> None:
    _stamped.set(_stamped.get() | {_value_sha(value)})


def neutralize_model_stamps(value: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    """Kind corrector: a ``visual_map`` the SERVER did not stamp carries no verdict of its own."""
    if _value_sha(value) in _stamped.get():
        return value, []
    claimed = (
        value.get("verified") is True
        or value.get("receipt") is not None
        or value.get("inspection_id") is not None
        or value.get("issues") not in (None, 0)
    )
    if not claimed:
        return value, []
    out = {k: v for k, v in value.items() if k not in ("receipt", "inspection_id")}
    out["verified"] = False
    out["issues"] = 0
    return out, [
        "visual_map: the model's own verified/issues/receipt values were removed — only the server "
        "stamps them after checking the layout"
    ]


def register_visual_map_corrector() -> None:
    from matrx_ai.processing.blocks.kind_correctors import register_kind_corrector

    register_kind_corrector(VISUAL_MAP_KIND, neutralize_model_stamps)


register_visual_map_corrector()


# ── The executor seam ──────────────────────────────────────────────────────────


def _inside_repair_child() -> bool:
    try:
        from matrx_connect.context.app_context import try_get_app_context

        ctx = try_get_app_context()
        return bool(ctx is not None and (getattr(ctx, "metadata", None) or {}).get(REPAIR_CHILD_KEY))
    except Exception:  # noqa: BLE001
        return False


def _host_delivery() -> VisualMapDelivery | None:
    from matrx_ai._ext import get_visual_map_delivery

    return get_visual_map_delivery()


def _last_person_text(messages: Any) -> str:
    from matrx_ai.config.message_config import HOST_AUTHORED_BY

    items = messages.to_list() if hasattr(messages, "to_list") else list(messages or [])
    for message in reversed(items):
        role = getattr(message, "role", None) or (message.get("role") if isinstance(message, dict) else None)
        if role != "user":
            continue
        meta = getattr(message, "metadata", None) or {}
        if isinstance(meta, dict) and meta.get("authored_by") == HOST_AUTHORED_BY:
            continue
        content = getattr(message, "content", None) or []
        texts = [getattr(c, "text", None) for c in content]
        text = "\n".join(t for t in texts if isinstance(t, str) and t)
        if text:
            return text
    return ""


def _assistant_text_parts(current_request: Any, final_response: Any) -> list[Any]:
    parts: list[Any] = []
    seen: set[int] = set()
    config = getattr(current_request, "config", None)
    message = config.messages.get_last_by_role("assistant") if config is not None else None
    candidates = list(getattr(message, "content", None) or []) if message is not None else []
    for msg in getattr(final_response, "messages", None) or []:
        if getattr(msg, "role", None) == "assistant":
            candidates.extend(getattr(msg, "content", None) or [])
    for content in candidates:
        if id(content) in seen or getattr(content, "type", None) != "text":
            continue
        seen.add(id(content))
        if isinstance(getattr(content, "text", None), str):
            parts.append(content)
    return parts


def _render_like(original: str, value: dict[str, Any]) -> str:
    if "\n" in original.strip():
        return json.dumps(value, ensure_ascii=False, indent=2)
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


#: A repair round rewrites the whole spec from named diagnostics: it needs room to write it, not to think.
#: 2026-10-21 live: a Haiku 5.5 child at the run's 8,000-token limit spent all of it thinking about 36
#: diagnostics and wrote nothing ("repair_unreadable" at round 1).
REPAIR_REASONING_EFFORT = "low"
REPAIR_MIN_OUTPUT_TOKENS = 16000


def _repair_budget(config: Any) -> None:
    """Low reasoning effort and at least ``REPAIR_MIN_OUTPUT_TOKENS`` of output for the repair child."""
    config.reasoning_effort = REPAIR_REASONING_EFFORT
    for name in ("thinking_budget", "thinking_level"):
        if hasattr(config, name):
            setattr(config, name, None)
    current = getattr(config, "max_output_tokens", None)
    config.max_output_tokens = max(int(current or 0), REPAIR_MIN_OUTPUT_TOKENS)


def _repair_model(config: Any, provision: dict[str, Any]) -> None:
    """The organization's ``repair_model`` knob, when set, repairs instead of the authoring model."""
    model = provision.get("repair_model")
    if isinstance(model, str) and model.strip():
        config.model = model.strip()


def authoring_model_repairer(current_request: Any) -> FallbackRepair:
    """The authoring model repairs its own diagram: a muted child call on a copy of this turn's
    conversation plus one host-written turn holding the diagnostics. The child shares the parent's
    request id (its cost rolls up to the same user request) and is persisted as a sub-conversation, so
    every repair round is a replayable record."""

    async def _repair(provision: dict[str, Any]) -> Any:
        from matrx_connect.context.app_context import get_app_context, set_app_context
        from matrx_connect.emitters import SilentEmitter

        from matrx_ai.config.message_config import (
            MessageList,
            UnifiedMessage,
            host_authored_user_turn,
            person_authored_user_turn,
        )
        from matrx_ai.config.unified_content import TextContent
        from matrx_ai.orchestrator.executor import _assistant_text_from_response, execute_ai_request

        # A clean three-turn transcript, never the run's raw history: that history can hold tool
        # calls and results (a skill load, a lookup) that this tool-less child may not replay.
        drawn = {"__kind": VISUAL_MAP_KIND, "type": provision.get("diagram_type"),
                 "spec": provision.get("spec"), "verified": False, "issues": 0}
        # A NEW config for a separate child call (its own three-message list, no tools), never a
        # rewrite of the live run's message list: the send-boundary guard keeps that seam closed.
        # Her own request is replayed as hers; with none on record the opener is the host's.
        user_request = provision.get("user_request")
        opener = (
            person_authored_user_turn(user_request)
            if user_request
            else host_authored_user_turn("Draw the diagram.", reason="visual_map_repair")
        )
        config = current_request.config.for_child_call(
            messages=MessageList([
                opener,
                UnifiedMessage(role="assistant", content=[TextContent(text=json.dumps(drawn, ensure_ascii=False))]),
                host_authored_user_turn(repair_notice(provision), reason="visual_map_repair"),
            ]),
            tools=[],
            custom_tools=[],
            tool_choice=None,
        )
        _repair_budget(config)
        _repair_model(config, provision)
        child_id = str(uuid4())

        async def _run() -> Any:
            from matrx_connect.context.app_context import child_agent_context

            # Through THE child funnel: its own conversation AND its own turn (the fork mints
            # the request id; cost cap, admission and stop key on the tree root), its own write
            # scope (the coordinator fork hook) — never a hand-made fork that skips them.
            async with child_agent_context(
                "visual_map_repair", emit_lifecycle=False, conversation_id=child_id
            ):
                child = get_app_context()
                set_app_context(child.with_overrides(
                    emitter=SilentEmitter(),
                    source_feature="visual_map_repair",
                    # The child's answer IS a visual_map: the gate must not check it again inside
                    # the child (that recursion re-ran the whole loop per repair round, 2026-10-21).
                    metadata={**dict(child.metadata or {}), REPAIR_CHILD_KEY: True},
                ))
                completed = await execute_ai_request(
                    config,
                    max_iterations=1,
                    metadata={"visual_map_repair_round": provision.get("round")},
                    conversation_id=child_id,
                    store=True,
                    mandate_key=REPAIR_MANDATE_KEY,
                )
            return _assistant_text_from_response(getattr(completed, "final_response", None))

        # A task copies the context, so the child context never leaks into the parent turn.
        return await asyncio.create_task(_run())

    return _repair


async def visual_map_gate(current_request: Any, final_response: Any, exec_ctx: Any) -> list[RepairOutcome]:
    """Check, repair and stamp every ``visual_map`` in this finishing turn's text. Never raises."""
    try:
        if _inside_repair_child():
            return []
        from matrx_ai.providers.device.route_guard import is_private_device_turn

        if is_private_device_turn(exec_ctx, getattr(current_request, "config", None)):
            # store:false on the person's own computer: the repair child runs a cloud model
            # (the repair_model knob, a bound agent), so the diagram is delivered unchecked.
            return []
        parts = _assistant_text_parts(current_request, final_response)
        if not any(find_visual_maps(p.text) for p in parts):
            return []
        delivery = _host_delivery()
        emitter = getattr(exec_ctx, "emitter", None)
        if delivery is None:
            logger.warning("[visual_map] a visual_map was emitted but no host delivery seam is configured")
            await _warn(emitter, "The diagram's layout could not be checked on this server.", {"configured": False})
            return []
        from matrx_ai.context.app_context import get_app_context

        ctx = get_app_context()
        org_id = getattr(ctx, "organization_id", None) or None
        user_id = getattr(ctx, "user_id", None) or None
        request_id = getattr(ctx, "request_id", None) or getattr(current_request, "request_id", None) or ""
        try:
            knob_values = await knob_or_declared_default(
                lambda: delivery.read_knobs(organization_id=org_id, user_id=user_id),
                declared_default={},
                consequence="Diagram checking uses its built-in settings for this answer.",
            )
        except Exception as exc:  # noqa: BLE001
            logger.warning("[visual_map] knob read failed: %s", exc)
            knob_values = {}
        knobs, missing = knobs_from(knob_values)
        user_request = _last_person_text(current_request.config.messages)
        fallback = authoring_model_repairer(current_request)

        outcomes: list[RepairOutcome] = []
        # Document order across the turn's text parts: ``ordinal`` is how a client finds the drawn draft
        # the checked value replaces (the n-th visual_map of this answer), and the subject_ref suffix.
        located = [(part, find_visual_maps(part.text)) for part in parts]
        total = sum(len(found) for _, found in located)
        first = 0
        for part, found in located:
            if not found:
                continue
            text = part.text
            not_drawn: list[str] = []
            for offset, (start, end, value) in reversed(list(enumerate(found))):  # right to left keeps offsets
                ordinal = first + offset
                subject_ref = f"request:{request_id}#{ordinal}"
                await _info(emitter, CHECKING_CODE, "Checking the diagram's layout", {
                    "subject_ref": subject_ref, "max_rounds": knobs.max_rounds, "quality": knobs.quality,
                })
                outcome = await run_repair_loop(
                    value, delivery=delivery, knobs=knobs, organization_id=org_id,
                    subject_ref=subject_ref, user_request=user_request, fallback_repair=fallback,
                )
                if missing:
                    outcome.notes.append(f"knob row(s) missing, declared default used: {', '.join(missing)}")
                mark_server_stamped(outcome.value)
                text = text[:start] + _render_like(text[start:end], outcome.value) + text[end:]
                if outcome.dropped:
                    not_drawn[:0] = [d for d in outcome.dropped if d not in not_drawn]
                outcomes.append(outcome)
                await _info(emitter, CHECKED_CODE, "Diagram layout checked", {
                    "subject_ref": subject_ref, "ordinal": ordinal, "total": total,
                    "value": outcome.value, "log": outcome.log(),
                })
                if not outcome.verified:
                    issues = outcome.value.get("issues", 0)
                    checked = any(r.stage == "validate" for r in outcome.rounds)
                    await _warn(
                        emitter,
                        f"Layout not verified · {issues} issues" if checked else "Layout not checked",
                        {"subject_ref": subject_ref, "issues": issues, "checked": checked, "log": outcome.log()},
                    )
            first += len(found)
            if not_drawn:
                # D9: the prose around a diagram can promise what the diagram no longer draws ("eleven
                # states" over nine). One plain line says what is missing, so the turn never overclaims.
                text = text.rstrip() + "\n\n" + not_drawn_note(not_drawn)
            part.text = text
            meta = getattr(part, "metadata", None)
            if isinstance(meta, dict):
                meta["visualMapChecks"] = [o.log() for o in outcomes]
        return outcomes
    except Exception as exc:  # noqa: BLE001 — the turn is never lost to its diagram check
        logger.exception("[visual_map] gate failed: %s", exc)
        return []


def not_drawn_note(labels: list[str]) -> str:
    """The one plain line a turn gets when its delivered diagram still leaves out first-draft content."""
    return f"Not drawn in this diagram: {', '.join(labels)}."


async def _info(emitter: Any, code: str, message: str, metadata: dict[str, Any]) -> None:
    if emitter is None:
        return
    from matrx_connect.context.events import InfoPayload

    try:
        await emitter.send_info(InfoPayload(code=code, system_message=message, user_message="", metadata=metadata))
    except Exception as exc:  # noqa: BLE001
        logger.warning("[visual_map] could not emit %s: %s", code, exc)


async def _warn(emitter: Any, message: str, metadata: dict[str, Any]) -> None:
    if emitter is None:
        return
    from matrx_connect.context.events import WarningPayload

    try:
        await emitter.send_warning(
            WarningPayload(
                code=UNVERIFIED_CODE, system_message=message, user_message=message,
                level="low", recoverable=True, metadata=metadata,
            )
        )
    except Exception as exc:  # noqa: BLE001
        logger.warning("[visual_map] could not emit warning: %s", exc)
