"""The pending-call ledger seam (S5 §5.6).

A Cloud Browser handoff rides the platform's EXISTING client-delegated tool
path — it must not re-implement the durable pending-call ledger or the
exactly-once completion CAS. Those live in aidream
(``ToolExecutionLogger.log_delegated`` + ``coordinator.finalize`` for the
suspend; ``resolve_client_tool_results`` for the completion). This package
holds ONE injected seam pointing at them, wired exactly like the ``mandates``
resolver.

🚨 THERE IS NO FALLBACK. An unset ledger raises at the boundary — a package
that silently degrades to "no resume" reproduces the mandate-seam failure
class (aidream ``CLAUDE.md`` §Mandates; S5 §5.6). Every deployment shape that
can park a browser run has an authority to resolve it; "nothing could complete
the pending call" is a wiring defect, never a reason to drop a human's return.
"""

from __future__ import annotations

from datetime import datetime
from typing import Protocol, runtime_checkable

from matrx_ai.browser_handoff.models import (
    HandoffResolution,
    HandoffResolutionReceipt,
)


@runtime_checkable
class HandoffLedger(Protocol):
    """The two durable pending-call operations the handoff protocol needs.

    ``delegate`` is P3 of the park sequence — flip the ``chat.tool_call`` row to
    ``status='delegated'`` with ``expires_at`` and run the blocking pre-suspend
    ``coordinator.finalize``. ``resolve`` is R4 of the resume sequence — the
    tool-side exactly-once CAS via ``resolve_client_tool_results``.

    Both are single durable operations against the SAME ledger the desktop /
    browser-tab delegated path uses; the browser flavor adds no columns and no
    second CAS (S5 §4.3, §9 invariant 4).
    """

    async def delegate(
        self,
        *,
        call_id: str,
        conversation_id: str | None,
        execution_id: str,
        handoff_id: str,
        expires_at: datetime,
    ) -> None:
        """P3: durably mark the pending tool call delegated + finalize. Raises
        (aborting the handoff) if the pre-suspend commit fails — better a loud
        failure than telling a human to act against a ledger that does not
        exist (S5 §P3 step 2)."""
        ...

    async def resolve(
        self, resolution: HandoffResolution
    ) -> HandoffResolutionReceipt:
        """R4: complete the pending tool call EXACTLY ONCE. Idempotent under any
        number of duplicate deliveries — the loser is reported ``already_resolved``
        and is a no-op (S5 §4.3)."""
        ...


class HandoffLedgerUnavailable(RuntimeError):
    """Raised when the handoff ledger seam was never wired — a deployment defect,
    never silently swallowed (S5 §5.6; mirrors ``MandateResolutionUnavailable``)."""

    error_type = "browser_handoff_ledger_unavailable"


_LEDGER: HandoffLedger | None = None


def set_handoff_ledger(ledger: HandoffLedger | None) -> None:
    """Host-injection entry point (aidream ``package_integration.py`` /
    ``matrx_ai.configure``). Called once at startup."""
    global _LEDGER
    _LEDGER = ledger


def get_handoff_ledger() -> HandoffLedger:
    """The wired ledger, or a loud raise. NO fallback (S5 §5.6)."""
    if _LEDGER is None:
        raise HandoffLedgerUnavailable(
            "No HandoffLedger is wired. A Cloud Browser handoff cannot durably "
            "delegate or resolve its pending tool call. Wire one via "
            "matrx_ai.browser_handoff.set_handoff_ledger(...) in the host's "
            "package_integration — there is no fallback by design."
        )
    return _LEDGER


def has_handoff_ledger() -> bool:
    return _LEDGER is not None
