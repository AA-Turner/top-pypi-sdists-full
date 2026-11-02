"""The Files cookie mint never gives up while aidream is still inside its own authority budget.

Sibling of matrx-connect's ``test_remote_authority_budget_alignment`` (Files cannot import another
package's tests). 2026-10-21: the mint allowed 5 s for its two remote calls together and 3 s for the
source check, while each endpoint behind them runs aidream's own login check with a 15.9 s budget.
"""

from __future__ import annotations

from matrx_connect.middleware.authority_retry import (
    DEFAULT_SESSION_ATTEMPT_SECONDS,
    authority_budget_seconds,
)
from matrx_files.standalone.remote_mint import RemoteFileSessionMint

INNER_TOTAL = authority_budget_seconds(DEFAULT_SESSION_ATTEMPT_SECONDS)
MINT = "https://authority.example/files/session/mint"
STATUS = "https://authority.example/auth/file-session/status"


def test_each_remote_call_of_the_mint_outlasts_the_inner_budget() -> None:
    mint = RemoteFileSessionMint(MINT, STATUS, b"synthetic-signing-key")
    assert mint.timeout_seconds > INNER_TOTAL, f"mint call gives up at {mint.timeout_seconds}s; inner {INNER_TOTAL:.2f}s"
    assert mint._authority.timeout_seconds > INNER_TOTAL, (
        f"source check gives up at {mint._authority.timeout_seconds}s; inner {INNER_TOTAL:.2f}s")


def test_the_whole_mint_deadline_covers_both_calls() -> None:
    mint = RemoteFileSessionMint(MINT, STATUS, b"synthetic-signing-key")
    whole = getattr(mint, "whole_seconds", mint.timeout_seconds)
    assert whole > mint.timeout_seconds + mint._authority.timeout_seconds, (
        f"one {whole}s deadline wraps two calls of {mint.timeout_seconds}s and {mint._authority.timeout_seconds}s")
