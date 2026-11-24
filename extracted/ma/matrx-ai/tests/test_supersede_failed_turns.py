"""A successful turn never hides the failed attempts before it (P-160, lead's ruling 2026-11-04).

The person's history keeps a failed attempt; the client draws it collapsed as resolved ("An earlier attempt failed;
a later reply went through · What failed"). The server used to flip such rows to ``is_visible_to_user=False`` once a
later reply landed (``_hide_superseded_failed_turns``), so the collapsed line could never draw: live, W4 2026-11-04,
a "too long" failure vanished from the transcript the moment the next reply succeeded.
"""

from __future__ import annotations

from matrx_utils.source_guard import stable_source

import matrx_ai.orchestrator.executor as _executor_mod  # noqa: F401 -- load order (persistence <-> executor)
import matrx_ai.db.persistence as persist_mod  # noqa: E402


def test_no_hider_of_recovered_failures_exists() -> None:
    assert not hasattr(persist_mod, "_hide_superseded_failed_turns")


def test_the_final_commit_never_flips_a_failed_row_out_of_the_persons_view() -> None:
    source = stable_source(persist_mod)
    # The one shape the old hider queued: a failed row's user visibility turned off after a success.
    assert 'status="failed",\n        is_visible_to_user=True' not in source
    assert "Superseded" not in source
