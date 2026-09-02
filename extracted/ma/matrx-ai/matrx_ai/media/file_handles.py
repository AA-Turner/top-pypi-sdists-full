"""Agent file handles — letting an agent name the files we sent it.

THE PLATFORM PRIMITIVE from ``common-docs/projects/agent-file-handles/PLAN.md``.
When we pass images (or any file) to an agent, the agent must be able to refer
to each one, and we must resolve that reference back to our file ref with
certainty. No provider offers this natively, so we build it:

The four rules (PLAN §2):
  1. **Documented idiom + checksum token.** Each file is labelled
     ``Image N [IMG-XXXX]:`` — the ordinal (what models are tuned for) plus an
     opaque token (what catches a miscount). Ask for BOTH back. Never our UUIDs.
  2. **Adjacency.** The label is its own text block IMMEDIATELY before its
     file — never a preamble list, never the system prompt.
  3. **Resolution is validating, not trusting.** An unknown handle RAISES
     (:class:`UnknownHandleError`) — the agent invented a reference; that is a
     mandate failure, never a warning to swallow.
  4. **Reconcile token against ordinal.** Agreement is recorded on the result
     (:class:`ReconciliationReport`). An ordinal outside ``[1, N]``, or
     duplicated where forbidden, is a failure (:class:`OrdinalError`).

The two failure directions (REVIEW-RESPONSE §3-L adjustment b):
  - **Unknown handle → raise.** Fabrication ships a photo onto the wrong
    product; it must fail the mandate loudly.
  - **Required-but-missing → DEGRADED.** A claim whose schema *requires* a file
    reference (hero image, damage flag) arriving without one is a distinct,
    reportable outcome — collected on the report as :class:`DegradedFinding`,
    not a raise and not a silent pass.

The token alphabet EXCLUDES confusable characters (``0/O/1/I/l``) — models
transcribe handles, and a transcription error must stay detectable, not become
a different valid handle (adjustment a).

This module is deliberately standalone: pure functions + small dataclasses, no
imports from the mandate system, no provider SDKs, no I/O. The integration seam
for the mandate frozen-input builder is exactly two calls:
``inject_file_handles(...)`` when composing the request, and
``resolve_file_handles(...)`` on the structured result.

Open question (PLAN §5.1, unresolved): chunking vs. segmentation under
Anthropic's >20-image dimension cap. Recommended direction: run segmentation on
a high-image-ceiling provider (Gemini) at thumbnail resolution in ONE request.
This module takes no position — it labels whatever ordered list it is given.
"""

from __future__ import annotations

import secrets
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any, Callable

__all__ = [
    "HANDLE_ALPHABET",
    "HANDLE_PREFIX",
    "DegradedFinding",
    "FileHandleError",
    "HandleMap",
    "InjectionResult",
    "OrdinalError",
    "ReconcileSpec",
    "ReconciliationEntry",
    "ReconciliationReport",
    "UnknownHandleError",
    "generate_handle",
    "inject_file_handles",
    "resolve_file_handles",
]

#: Crockford-ish alphabet: uppercase + digits, EXCLUDING the confusables
#: 0/O, 1/I/l (lowercase never appears — the whole alphabet is uppercase).
HANDLE_ALPHABET = "23456789ABCDEFGHJKMNPQRSTUVWXYZ"

HANDLE_PREFIX = "IMG-"
_HANDLE_LEN = 4  # token chars after the prefix; 31^4 ≈ 923k per request-scope


# ─────────────────────────────────────────────────────────── errors ──


class FileHandleError(Exception):
    """Base class for file-handle failures."""


class UnknownHandleError(FileHandleError):
    """The agent returned a handle that was never issued for this request.

    Rule 3: this is a mandate failure — the agent invented a reference and
    downstream code is about to attach a file to the wrong claim.
    """

    def __init__(self, handle: str, field_path: str) -> None:
        self.handle = handle
        self.field_path = field_path
        super().__init__(
            f"Unknown file handle {handle!r} at {field_path!r}: not issued for "
            "this request — the agent fabricated a reference (mandate failure)."
        )


class OrdinalError(FileHandleError):
    """An ordinal is out of ``[1, N]``, non-integer, or duplicated where forbidden."""

    def __init__(self, message: str, field_path: str) -> None:
        self.field_path = field_path
        super().__init__(f"{message} (at {field_path!r})")


# ──────────────────────────────────────────────────── handle issuing ──


def generate_handle(existing: set[str] | None = None, *, prefix: str = HANDLE_PREFIX) -> str:
    """One fresh, collision-free handle like ``IMG-7QK2`` (confusable-free alphabet)."""
    existing = existing or set()
    while True:
        token = "".join(secrets.choice(HANDLE_ALPHABET) for _ in range(_HANDLE_LEN))
        handle = f"{prefix}{token}"
        if handle not in existing:
            return handle


@dataclass(frozen=True)
class HandleMap:
    """Request-scoped ``handle → file_ref`` map plus the issued order.

    ``ordered_handles[i]`` is the handle of ordinal ``i + 1`` — ordinals are
    1-based, exactly as the labels the model saw.
    """

    by_handle: dict[str, Any]
    ordered_handles: tuple[str, ...]

    @property
    def count(self) -> int:
        return len(self.ordered_handles)

    def file_ref(self, handle: str, field_path: str = "<unknown>") -> Any:
        try:
            return self.by_handle[handle]
        except KeyError:
            raise UnknownHandleError(handle, field_path) from None

    def ordinal_of(self, handle: str) -> int:
        """1-based ordinal for an issued handle."""
        return self.ordered_handles.index(handle) + 1


@dataclass(frozen=True)
class InjectionResult:
    content_parts: list[Any]
    handle_map: HandleMap


# ────────────────────────────────────────────── provider text parts ──
# The media part itself is caller-supplied and passed through untouched (it is
# already in the provider's transport shape — bytes/base64/file_id/url block).
# Only the LABEL part is provider-shaped here, because that is the part this
# primitive owns. One interface, three shapes.

_TEXT_PART_BUILDERS: dict[str, Callable[[str], dict[str, Any]]] = {
    # Anthropic Messages API content block.
    "anthropic": lambda text: {"type": "text", "text": text},
    # OpenAI multimodal content part (chat.completions user-content array).
    "openai": lambda text: {"type": "text", "text": text},
    # Gemini generateContent Part.
    "gemini": lambda text: {"text": text},
    # This repo's UnifiedMessage block shape (TextContent).
    "unified": lambda text: {"type": "text", "text": text},
}


def _label(ordinal: int, handle: str, noun: str) -> str:
    return f"{noun} {ordinal} [{handle}]:"


def inject_file_handles(
    files: Sequence[tuple[Any, Any]],
    *,
    provider: str,
    noun: str = "Image",
    prefix: str = HANDLE_PREFIX,
    handles: Sequence[str] | None = None,
) -> InjectionResult:
    """Interleave handle labels with media parts (rules 1 + 2).

    ``files`` is an ORDERED list of ``(file_ref, media_part)``:

    - ``file_ref`` — our identity for the file (file_id / MediaRef / anything
      hashable-by-identity the caller wants back). Never shown to the model.
    - ``media_part`` — the provider-shape transport part for the file's bytes,
      passed through untouched immediately AFTER its label.

    Returns the interleaved ``content_parts`` —
    ``[label_1, media_1, label_2, media_2, …]`` — and the request-scoped
    :class:`HandleMap`. ``handles`` may pre-supply the handle strings (tests /
    deterministic replay); otherwise fresh confusable-free tokens are issued.
    """
    try:
        make_text = _TEXT_PART_BUILDERS[provider]
    except KeyError:
        raise ValueError(
            f"Unknown provider {provider!r}; known: {sorted(_TEXT_PART_BUILDERS)}"
        ) from None
    if handles is not None and len(handles) != len(files):
        raise ValueError("handles, when supplied, must match files 1:1")

    parts: list[Any] = []
    by_handle: dict[str, Any] = {}
    ordered: list[str] = []
    for i, (file_ref, media_part) in enumerate(files):
        handle = handles[i] if handles is not None else generate_handle(set(by_handle), prefix=prefix)
        if handle in by_handle:
            raise ValueError(f"Duplicate handle {handle!r} supplied")
        parts.append(make_text(_label(i + 1, handle, noun)))
        parts.append(media_part)  # adjacency: label immediately before its file
        by_handle[handle] = file_ref
        ordered.append(handle)
    return InjectionResult(
        content_parts=parts,
        handle_map=HandleMap(by_handle=by_handle, ordered_handles=tuple(ordered)),
    )


# ─────────────────────────────────────────────────────── resolution ──


@dataclass(frozen=True)
class ReconcileSpec:
    """One field (or wildcard family of fields) carrying handles to resolve.

    - ``handle_path`` — dotted path, ``*`` wildcards a list, e.g.
      ``"products.*.images.*"`` or ``"best_image"``. The value at the path is a
      handle string (or a list of handle strings when the path lands on a list).
    - ``ordinal_path`` — optional sibling path holding the model's claimed
      1-based position for rule-4 reconciliation (same wildcard arity).
    - ``required`` — a missing/empty value here is a DEGRADED finding
      (adjustment b), never a pass and never a raise.
    - ``forbid_duplicate_ordinals`` — a repeated ordinal across this spec's
      matches is an :class:`OrdinalError` (rule 4).
    """

    handle_path: str
    ordinal_path: str | None = None
    required: bool = False
    forbid_duplicate_ordinals: bool = False


@dataclass(frozen=True)
class ReconciliationEntry:
    field_path: str
    handle: str
    file_ref: Any
    issued_ordinal: int
    claimed_ordinal: int | None
    agreement: str  # "agree" | "disagree" | "token_only"


@dataclass(frozen=True)
class DegradedFinding:
    """A claim whose schema requires a file reference arrived without one."""

    field_path: str
    reason: str


@dataclass
class ReconciliationReport:
    entries: list[ReconciliationEntry] = field(default_factory=list)
    degraded: list[DegradedFinding] = field(default_factory=list)

    @property
    def is_degraded(self) -> bool:
        return bool(self.degraded)

    @property
    def agreement(self) -> str:
        """Overall rule-4 outcome recorded on the result:
        ``"full"`` (every checked pair agrees), ``"partial"``, ``"none"``
        (every checked pair disagrees), or ``"token_only"`` (no ordinals to check).
        """
        checked = [e for e in self.entries if e.claimed_ordinal is not None]
        if not checked:
            return "token_only"
        agree = sum(1 for e in checked if e.agreement == "agree")
        if agree == len(checked):
            return "full"
        return "none" if agree == 0 else "partial"


def _walk(node: Any, segments: list[str], path_so_far: str) -> list[tuple[str, Any, Any, str | int]]:
    """Yield ``(concrete_path, parent, container, key)`` for every match.

    ``container[key]`` is the matched value; missing terminal keys yield the
    parent with a sentinel so callers can distinguish missing from None.
    """
    if not segments:
        return []
    seg, rest = segments[0], segments[1:]
    out: list[tuple[str, Any, Any, str | int]] = []
    if seg == "*":
        if isinstance(node, list):
            for i, item in enumerate(node):
                p = f"{path_so_far}[{i}]" if path_so_far else f"[{i}]"
                if rest:
                    out.extend(_walk(item, rest, p))
                else:
                    out.append((p, node, node, i))
        return out  # non-list under * → no matches
    if isinstance(node, Mapping) and seg in node:
        p = f"{path_so_far}.{seg}" if path_so_far else seg
        if rest:
            out.extend(_walk(node[seg], rest, p))
        else:
            out.append((p, node, node, seg))
    return out


def _matches(result: Any, dotted: str) -> list[tuple[str, Any, str | int]]:
    return [(p, container, key) for p, _parent, container, key in _walk(result, dotted.split("."), "")]


_MISSING = object()


def resolve_file_handles(
    result: Any,
    handle_map: HandleMap,
    specs: Sequence[ReconcileSpec],
) -> tuple[Any, ReconciliationReport]:
    """Walk ``result`` (any dict/list tree), resolve declared handle fields
    in place-of (a deep-copied tree is returned; the input is not mutated),
    reconcile ordinals, and report.

    - Unknown handle → :class:`UnknownHandleError` (raise — rule 3).
    - Required field missing/empty → :class:`DegradedFinding` on the report.
    - Claimed ordinal non-integer / outside ``[1, N]`` / duplicated where
      forbidden → :class:`OrdinalError` (raise — rule 4).
    - Every resolved handle gets a :class:`ReconciliationEntry` with its
      agreement level; the report's ``agreement`` is the recorded outcome.
    """
    import copy

    resolved = copy.deepcopy(result)
    report = ReconciliationReport()
    n = handle_map.count

    for spec in specs:
        matches = _matches(resolved, spec.handle_path)
        if spec.required:
            # Adjustment (b): a claim REQUIRING a file reference that arrives
            # without one is DEGRADED. Cover both "no match at all" and
            # "the parent object exists but the key is missing".
            segments = spec.handle_path.split(".")
            if len(segments) > 1:
                parent_matches = _matches(resolved, ".".join(segments[:-1]))
                matched_parents = {_parent_path(p) for p, _c, _k in matches}
                terminal = segments[-1]
                for p, container, key in parent_matches:
                    if p not in matched_parents:
                        report.degraded.append(
                            DegradedFinding(
                                field_path=f"{p}.{terminal}",
                                reason="required file reference key is missing from the claim",
                            )
                        )
            elif not matches:
                report.degraded.append(
                    DegradedFinding(
                        field_path=spec.handle_path,
                        reason="required file reference is absent from the result",
                    )
                )
        if not matches:
            continue

        ordinal_by_path: dict[str, Any] = {}
        if spec.ordinal_path is not None:
            for p, container, key in _matches(resolved, spec.ordinal_path):
                # Align by positional suffix: strip the last segment, key on the parent path.
                ordinal_by_path[_parent_path(p)] = container[key]

        seen_ordinals: set[int] = set()
        for concrete_path, container, key in matches:
            value = container[key]
            if value is None or value == "" or value == []:
                if spec.required:
                    report.degraded.append(
                        DegradedFinding(
                            field_path=concrete_path,
                            reason="required file reference is null/empty",
                        )
                    )
                continue
            # A list of handles at a non-wildcard terminal: resolve each element.
            if isinstance(value, list):
                container[key] = [
                    _resolve_one(
                        h, f"{concrete_path}[{i}]", handle_map, None, n, report, spec, seen_ordinals
                    )
                    for i, h in enumerate(value)
                ]
                continue
            claimed = ordinal_by_path.get(_parent_path(concrete_path), _MISSING)
            claimed_val = None if claimed is _MISSING else claimed
            container[key] = _resolve_one(
                value, concrete_path, handle_map, claimed_val, n, report, spec, seen_ordinals
            )

    return resolved, report


def _parent_path(p: str) -> str:
    if p.endswith("]"):
        return p[: p.rindex("[")]
    return p.rsplit(".", 1)[0] if "." in p else ""


def _resolve_one(
    handle: Any,
    field_path: str,
    handle_map: HandleMap,
    claimed_ordinal: Any,
    n: int,
    report: ReconciliationReport,
    spec: ReconcileSpec,
    seen_ordinals: set[int],
) -> Any:
    if not isinstance(handle, str):
        raise UnknownHandleError(str(handle), field_path)
    file_ref = handle_map.file_ref(handle, field_path)  # raises UnknownHandleError
    issued = handle_map.ordinal_of(handle)

    agreement = "token_only"
    claimed_int: int | None = None
    if claimed_ordinal is not None:
        if isinstance(claimed_ordinal, bool) or not isinstance(claimed_ordinal, int):
            raise OrdinalError(
                f"Claimed ordinal {claimed_ordinal!r} is not an integer", field_path
            )
        if not 1 <= claimed_ordinal <= n:
            raise OrdinalError(
                f"Claimed ordinal {claimed_ordinal} is outside [1, {n}]", field_path
            )
        if spec.forbid_duplicate_ordinals:
            if claimed_ordinal in seen_ordinals:
                raise OrdinalError(
                    f"Claimed ordinal {claimed_ordinal} is duplicated where the schema forbids it",
                    field_path,
                )
            seen_ordinals.add(claimed_ordinal)
        claimed_int = claimed_ordinal
        agreement = "agree" if claimed_ordinal == issued else "disagree"

    report.entries.append(
        ReconciliationEntry(
            field_path=field_path,
            handle=handle,
            file_ref=file_ref,
            issued_ordinal=issued,
            claimed_ordinal=claimed_int,
            agreement=agreement,
        )
    )
    return file_ref
