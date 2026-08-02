"""Completion-evidence detector.

Given an :class:`ActionLedger` and the task's deep-planning state, return
an :class:`EvidenceReport` describing whether the agent has already done
the durable work even when plan items aren't all toggled
``completed=True``.

Solves the "restart-after-finish" failure mode: tasks that performed
durable side-effects (writes + verifications) and then got force-retried
because the agent forgot to mark the last plan item complete. The retry's
compaction summary lost the WRITE/VERIFY entries, the agent restarted
from scratch, and the user-facing result was a hung "plan complete" UI.

The detector walks the ledger looking for **write+verify pairs** — a
WRITE entry whose target matches a later VERIFY entry's target, with
matching numeric signatures (e.g. a write reporting ``rows_written=N``
paired with a verify reporting ``count=N``). Each matched pair is one
piece of evidence the corresponding piece of work is durably done.

Conservative bias: missing pairs return ``has_evidence=False`` and the
caller falls back to the existing pre_retry path. We only "skip pre_retry
and finalize" when the evidence is unambiguous AND the number of
uncompleted plan items is small (≤ 2). That cap prevents a single noisy
write+verify on an early step from short-circuiting a large plan.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any, List, Optional, Tuple

from xpander_sdk.models.action_ledger import (
    EvidenceReport,
    LedgerEntry,
    LedgerEntryClass,
)

if TYPE_CHECKING:
    from xpander_sdk.core.context_optimizer.action_ledger import ActionLedger
    from xpander_sdk.models.deep_planning import DeepPlanning


# Number of digits to extract from a signature for cross-checking. A
# write reporting ``rows_written=N`` paired with a verify reporting
# ``count=N`` is one match; mismatched digits suppress the pair.
_SIGNATURE_DIGITS = re.compile(r"=(\d+)\s*$")


def detect_completion_evidence(
    ledger: Optional["ActionLedger"],
    deep_planning: Optional["DeepPlanning"] = None,
) -> EvidenceReport:
    """Return an :class:`EvidenceReport` for the current ledger state.

    Args:
        ledger: The task's :class:`ActionLedger`. ``None`` returns an
            empty report — the caller falls back to existing behavior.
        deep_planning: The task's deep-planning state, if any. The
            detector uses ``deep_planning.tasks`` to count uncompleted
            items and to match plan-item titles against ledger targets.
    """
    if ledger is None:
        return EvidenceReport(has_evidence=False, rationale="no ledger attached")

    entries = ledger.entries
    if not entries:
        return EvidenceReport(has_evidence=False, rationale="ledger empty")

    pairs = _pair_writes_and_verifies(entries)

    uncompleted: List[Any] = []
    if deep_planning and deep_planning.tasks:
        uncompleted = [t for t in deep_planning.tasks if not t.completed]

    matched_items = _match_plan_items(pairs, entries, deep_planning)

    has_evidence = bool(pairs)
    rationale_parts: List[str] = []
    if pairs:
        # ``pairs`` carries durable seq numbers, NOT list indices —
        # the ledger may reload with gaps (corrupt lines skipped) or
        # in non-contiguous order. Use a seq->entry map for lookups
        # so a missing seq falls back to "?" instead of raising.
        by_seq = {e.seq: e for e in entries}
        pair_targets = {
            (by_seq.get(write_seq).target if by_seq.get(write_seq) else None) or "?"
            for write_seq, _ in pairs
        }
        rationale_parts.append(
            f"matched {len(pairs)} write+verify pair(s) on targets: "
            + ", ".join(sorted(t for t in pair_targets if t != "?"))
        )
    else:
        rationale_parts.append("no write+verify pairs found in ledger")
    if matched_items:
        rationale_parts.append(f"{len(matched_items)} plan item(s) covered by evidence")
    rationale_parts.append(f"{len(uncompleted)} uncompleted plan item(s)")

    return EvidenceReport(
        has_evidence=has_evidence,
        write_verify_pairs=pairs,
        matched_plan_items=matched_items,
        uncompleted_count=len(uncompleted),
        rationale="; ".join(rationale_parts),
    )


def _pair_writes_and_verifies(
    entries: List[LedgerEntry],
) -> List[Tuple[int, int]]:
    """Match WRITE entries with later VERIFY entries by canonical target.

    A pair counts when:
      * write.status == "ok" AND verify.status == "ok"
      * write.target == verify.target (case-insensitive, both non-empty)
      * verify.seq > write.seq (verification follows the write)
      * either signatures share a digit suffix, OR the verify target
        matches a write target with no signature (acceptance: the verify
        observed the side-effect at all).

    Returns ``(write.seq, verify.seq)`` tuples — sequence numbers, not
    list indices, so callers can report against the durable record.
    """
    pairs: List[Tuple[int, int]] = []
    by_seq = {e.seq: e for e in entries}
    matched_writes: set = set()

    verifies = [
        e
        for e in entries
        if e.entry_class == LedgerEntryClass.VERIFY and e.status == "ok"
    ]
    writes = [
        e
        for e in entries
        if e.entry_class == LedgerEntryClass.WRITE and e.status == "ok"
    ]

    for v in verifies:
        if not v.target:
            continue
        v_target = v.target.lower()
        v_digits = _digits_from_signature(v.result_signature)
        # Walk writes oldest first; a single write can satisfy at most one verify.
        for w in writes:
            if w.seq in matched_writes:
                continue
            if not w.target:
                continue
            if w.target.lower() != v_target:
                continue
            if v.seq <= w.seq:
                continue
            w_digits = _digits_from_signature(w.result_signature)
            if v_digits and w_digits and v_digits != w_digits:
                # Signatures present but disagree — write claimed N rows,
                # verify saw M. Don't count as evidence.
                continue
            pairs.append((w.seq, v.seq))
            matched_writes.add(w.seq)
            break  # one verify, one write
    # Stable order by write seq, helps tests.
    pairs.sort()
    return pairs


def _digits_from_signature(sig: Optional[str]) -> Optional[str]:
    """Extract the numeric tail of a result signature, e.g.
    ``rows_written=N`` → ``"N"``."""
    if not sig:
        return None
    m = _SIGNATURE_DIGITS.search(sig)
    return m.group(1) if m else None


def _match_plan_items(
    pairs: List[Tuple[int, int]],
    entries: List[LedgerEntry],
    deep_planning: Optional["DeepPlanning"],
) -> List[str]:
    """Return plan-item ids whose title or id appears in a paired target.

    Best-effort string match — production targets are usually
    fully-qualified table names or file paths and titles are short
    human strings. We accept either:
      * substring of plan item title appears in target
      * plan item id appears verbatim in target
    """
    if not deep_planning or not deep_planning.tasks:
        return []
    matched: List[str] = []
    targets = []
    by_seq = {e.seq: e for e in entries}
    for w_seq, _v_seq in pairs:
        e = by_seq.get(w_seq)
        if e and e.target:
            targets.append(e.target.lower())
    if not targets:
        return []
    for item in deep_planning.tasks:
        title = (item.title or "").lower().strip()
        for t in targets:
            if item.id and item.id in t:
                matched.append(item.id)
                break
            if title and len(title) >= 4 and title in t:
                matched.append(item.id)
                break
    return matched
