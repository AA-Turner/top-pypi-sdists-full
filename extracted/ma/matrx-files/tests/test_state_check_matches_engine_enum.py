"""`files.sync_mappings.state` mirrors the engine's honest-state enum, verbatim.

C3: there is ONE honest-state enum, owned by the engine and emitted from its
single Rust declaration as ``crates/matrx-sync/contracts/honest_states.json``.
The server's CHECK constraint is a MIRROR of the mapping-scoped subset -- not a
second opinion about it.

Why this is a test and not a promise: ten of those values (``offline``,
``polling_fallback``, ``permission_denied``, ``watcher_exhausted``,
``over_quota``, ``disk_low``, ``pending``, ``removed``, ``root_missing``,
``daemon_older_than_app``) are written by an ORDINARY heartbeat. A CHECK missing
any one of them raises 23514 on that heartbeat and silently freezes the browser's
device list in exactly the conditions the table exists to report. An earlier
hand-written draft of this list was missing all ten.

It fails on divergence in EITHER direction, and if the artifact is missing it
fails LOUDLY rather than skipping — a guard that disappears when its input does
is not a guard.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

_REQUIRED_ENV = ("SUPABASE_MATRIX_HOST", "SUPABASE_MATRIX_PASSWORD")

#: FS-C2's build artifact (SPEC-ENGINE E16), shaped
#: [{"value", "scopes": ["session"|"device"|"mapping"], "title", "remedy_action"}]
ARTIFACT = Path(
    "/Users/armanisadeghi/code/matrx-local/crates/matrx-sync/contracts/honest_states.json"
)


def _skip_without_db() -> None:
    missing = [n for n in _REQUIRED_ENV if not os.environ.get(n)]
    if missing:
        pytest.skip(f"live platform database unavailable: {', '.join(missing)} unset")


def _engine_mapping_states() -> set[str]:
    assert ARTIFACT.exists(), (
        f"the honest-state artifact is missing at {ARTIFACT}. This test does NOT skip: "
        "without it nothing proves the server's CHECK still mirrors the engine's enum, "
        "and a divergence costs a silently frozen device list. Build matrx-sync (the "
        "artifact is generated from the single Rust declaration) or fix the path."
    )
    entries = json.loads(ARTIFACT.read_text())
    assert entries, "the artifact is empty"
    return {e["value"] for e in entries if "mapping" in e.get("scopes", [])}


async def _live_check_values() -> set[str]:
    from matrx_orm import acquire_connection

    from matrx_files.db import bootstrap_db

    async with acquire_connection(bootstrap_db()) as conn:
        src = await conn.fetchval(
            """
            SELECT pg_get_constraintdef(c.oid)
              FROM pg_constraint c
              JOIN pg_class t ON t.oid = c.conrelid
              JOIN pg_namespace n ON n.oid = t.relnamespace
             WHERE n.nspname = 'files' AND t.relname = 'sync_mappings'
               AND c.contype = 'c'
               -- exactly the `state` CHECK: `desired_state` has its own, and a
               -- LIKE '%state%' happily returns that one instead (it did).
               AND c.conname = 'sync_mappings_state_check'
            """
        )
    assert src, "no CHECK constraint on files.sync_mappings.state"
    return set(re.findall(r"'([a-z_]+)'::text", src))


async def test_the_check_equals_the_engine_enums_mapping_subset():
    _skip_without_db()
    engine = _engine_mapping_states()
    live = await _live_check_values()
    only_engine = sorted(engine - live)
    only_db = sorted(live - engine)
    assert not only_engine and not only_db, (
        "THE HONEST-STATE ENUM HAS DIVERGED. The engine declares but the server's CHECK "
        f"refuses: {only_engine} (each of these raises 23514 the moment a daemon reports "
        f"it). The server's CHECK allows but the engine never emits: {only_db}. "
        "Regenerate the CHECK from crates/matrx-sync/contracts/honest_states.json; never "
        "hand-edit either side."
    )


async def test_every_value_a_heartbeat_writes_is_present():
    """The ten an ordinary heartbeat reports, named so a regression is obvious."""
    _skip_without_db()
    live = await _live_check_values()
    heartbeat = {
        "offline",
        "polling_fallback",
        "permission_denied",
        "watcher_exhausted",
        "over_quota",
        "disk_low",
        "pending",
        "removed",
        "root_missing",
        "daemon_older_than_app",
    }
    assert heartbeat <= live, f"missing from the CHECK: {sorted(heartbeat - live)}"


async def test_session_only_values_are_not_mapping_scoped():
    """`signed_in` is a session fact, not a mapping's state. It must not be here."""
    _skip_without_db()
    live = await _live_check_values()
    assert "signed_in" not in live
