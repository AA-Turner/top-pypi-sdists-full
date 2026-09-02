"""The judge accuracy ledger — one row per invocation, plus the agreement bit.

``platform.judge_verdict`` is the durable half of "a judge has its own accuracy
tracking" (Engram VISION §3.3). Two writes make it work:

* :func:`record_verdict` — every invocation, at the moment it happens. Not
  sampled, not opt-in: a judge whose verdicts are only sometimes recorded has an
  accuracy record that is only sometimes true.
* :func:`record_agreement` — later, when an **authoritative** signal about the
  same subject arrives (a human verdict via ``platform.output_feedback``, a
  replay outcome, a gate result). That is the row that turns a pile of opinions
  into a measurable track record.

Placement of the table (``platform.``, not ``hindsight.``) is argued in the
migration `db/migrations/0373_judge_verdict_ledger.sql`.

A ledger write NEVER fails a judgement. It screams and returns ``None`` — a lost
accuracy row is a real loss, but killing a paid, already-completed judgement to
punish it would be worse.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from matrx_utils import vcprint

if TYPE_CHECKING:  # pragma: no cover
    from matrx_ai.evaluators.judge import (
        AuthorityKind,
        JudgeContract,
        JudgeOutcome,
        JudgeSubject,
    )

logger = logging.getLogger("matrx_ai.evaluators.ledger")


def _model() -> Any | None:
    """The host-injected ``platform.judge_verdict`` model, or None standalone."""
    from matrx_ai.db._registry import DBNotConfiguredError, get_model

    try:
        return get_model("JudgeVerdict")
    except DBNotConfiguredError:
        return None


def _warn_unconfigured(what: str) -> None:
    vcprint(
        f"[judge-ledger] {what} NOT RECORDED — the host has not injected the "
        "'JudgeVerdict' model (platform.judge_verdict). Judge accuracy cannot be "
        "measured while this is true; wire it in the host's matrx_ai.configure().",
        color="red",
    )
    logger.warning("judge ledger unavailable: JudgeVerdict model not registered (%s)", what)


def verdict_payload(
    *,
    contract: JudgeContract,
    subject: JudgeSubject,
    reference: JudgeSubject | None,
    outcome: JudgeOutcome,
    invocation: dict[str, Any],
    organization_id: str | None,
    user_id: str | None,
    candidate_refs: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """The ledger row as plain data, without writing it.

    Exists because a caller does not always run on the database the row belongs
    on. A Hindsight replay contained on the MIRROR (D-25) must not write its
    accuracy row there — nobody reads the mirror, and the row's id would be a
    mirror id masquerading as a live one. Such a caller carries this payload
    back across the boundary and :func:`write_verdict` lands it on live.
    """
    return {
        "judge_key": contract.key,
        "judge_version": contract.version,
        "mode": contract.mode,
        "question": contract.question,
        "subject_kind": contract.subject_kind,
        "subject_ref_type": subject.ref.ref_type,
        "subject_ref_id": subject.ref.ref_id,
        "reference_ref_type": reference.ref.ref_type if reference else None,
        "reference_ref_id": reference.ref.ref_id if reference else None,
        "candidate_refs": candidate_refs or [],
        "verdict": outcome.verdict,
        "confidence": outcome.confidence,
        "reasoning": outcome.reasoning,
        "rubric_name": contract.rubric_name,
        "rubric_provenance": contract.rubric_provenance,
        "rubric_fingerprint": contract.rubric_fingerprint,
        "rubric_author": contract.rubric_author,
        "mandate": contract.mandate,
        "model": invocation.get("model") or contract.model,
        "consumer": contract.consumer,
        "invocation": invocation,
        "organization_id": organization_id,
        "created_by": user_id,
        "updated_by": user_id,
        "metadata": {"evidence": outcome.evidence},
    }


async def write_verdict(payload: dict[str, Any]) -> str | None:
    """Land a :func:`verdict_payload` on THIS process's database."""
    model = _model()
    judge_key = payload.get("judge_key")
    if model is None:
        _warn_unconfigured(f"verdict for judge {judge_key!r}")
        return None
    if not payload.get("organization_id"):
        # organization_id is NOT NULL on the ledger (canonical entity contract) and
        # a NULL org is never "global" — a row without one would be invisible.
        vcprint(
            f"[judge-ledger] verdict for judge {judge_key!r} NOT RECORDED — no "
            "organization_id was supplied. Pass the caller's resolved org; a judge "
            "verdict with no org cannot be read back by anyone.",
            color="red",
        )
        logger.warning("judge ledger skipped for %s: no organization_id", judge_key)
        return None
    try:
        row = await model.create(**payload)
        return str(row.id)
    except Exception as exc:  # noqa: BLE001 — a ledger write never sinks a verdict
        logger.exception("judge ledger write failed for %s", judge_key)
        vcprint(
            f"[judge-ledger] WRITE FAILED for judge {judge_key!r}: "
            f"{type(exc).__name__}: {exc} — the verdict stands, its accuracy row is lost.",
            color="red",
        )
        return None


async def record_verdict(
    *,
    contract: JudgeContract,
    subject: JudgeSubject,
    reference: JudgeSubject | None,
    outcome: JudgeOutcome,
    invocation: dict[str, Any],
    organization_id: str | None,
    user_id: str | None,
    candidate_refs: list[dict[str, Any]] | None = None,
) -> str | None:
    """Record one invocation on THIS database. Returns the row id, or None.

    Build-then-write, in one call. A caller that is NOT on the database the row
    belongs on (a mirror-contained replay) uses :func:`verdict_payload` and
    :func:`write_verdict` separately instead.
    """
    return await write_verdict(
        verdict_payload(
            contract=contract,
            subject=subject,
            reference=reference,
            outcome=outcome,
            invocation=invocation,
            organization_id=organization_id,
            user_id=user_id,
            candidate_refs=candidate_refs,
        )
    )


async def record_agreement(
    *,
    ledger_id: str,
    authority_kind: AuthorityKind,
    authority_verdict: str,
    agreed: bool,
    authority_ref_type: str | None = None,
    authority_ref_id: str | None = None,
) -> bool:
    """Stamp the agreement bit on one ledger row once ground truth arrives."""
    model = _model()
    if model is None:
        _warn_unconfigured(f"agreement for ledger row {ledger_id}")
        return False
    try:
        await model.update_where(
            {"id": ledger_id},
            authority_kind=authority_kind,
            authority_verdict=authority_verdict,
            authority_ref_type=authority_ref_type,
            authority_ref_id=authority_ref_id,
            agreed=agreed,
            agreement_at=datetime.now(UTC),
        )
        return True
    except Exception as exc:  # noqa: BLE001
        logger.exception("judge ledger agreement write failed for %s", ledger_id)
        vcprint(
            f"[judge-ledger] AGREEMENT WRITE FAILED for row {ledger_id}: "
            f"{type(exc).__name__}: {exc}",
            color="red",
        )
        return False


__all__ = ["record_agreement", "record_verdict", "verdict_payload", "write_verdict"]
