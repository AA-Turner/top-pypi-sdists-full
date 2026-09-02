"""🚨 matrx-ai's own tests never read the HOST's wiring.

THE ORDERING DEFECT THIS PINS
-----------------------------
``matrx_ai.configure(...)`` writes process-global package state — the ``_ext``
host-seam registry, the durable VFS backend, the Mandate resolver, the browser
handoff ledger, the host model catalog, the capability registry. A host calls
it once at startup, which is correct at runtime and a landmine under pytest:
aidream's bootstrap (``configure_packages()``) fires as an IMPORT-TIME side
effect while pytest is COLLECTING an aidream test module, so every matrx-ai
test collected after it ran against a host-configured package.

    uv run pytest packages/matrx-ai/tests -q
        -> 4153 passed
    uv run pytest aidream/services/mandates/tests packages/matrx-ai/tests -q
        -> 13 failed          (same code, same assertions, different order)

Thirteen red tests that were not defects. That is the real cost: a full-repo
run that reports fake failures teaches everyone to ignore red.

The fix is the leaking globals, not the thirteen assertions —
``matrx_ai/testing/host_isolation.py`` snapshots the pristine package
configuration at conftest import (before any host bootstrap can fire) and
``packages/matrx-ai/conftest.py`` restores it around every matrx-ai test.

WHAT THIS FILE PROVES
---------------------
That the restore actually happens, without needing aidream in the run: the
first test installs host-style seams exactly as a host bootstrap would, and the
second asserts the package is pristine again. Delete the autouse fixture and
the second test goes red — that is what makes this a guard and not a comment.

The full ordering pairing (``pytest aidream/services/mandates/tests
packages/matrx-ai/tests``) runs in CI as the ``host-seam-isolation`` suite in
.github/workflows/test.yml, which is the end-to-end version of this guard.
"""

from __future__ import annotations

from typing import Any

import pytest

_FAKE_TRACKER_KEY = "internal_run_tracker"


class _FakeVfsBackend:
    """Stand-in for aidream's durable code_files backend."""

    async def read(self, *args: Any, **kwargs: Any) -> bytes:  # pragma: no cover
        raise AssertionError("the fake host backend is never used, only installed")


def _seam_state() -> dict[str, Any]:
    from matrx_ai import _ext
    from matrx_ai.tools.vfs.workspace import has_durable_backend

    return {
        "durable_vfs": has_durable_backend(),
        "tracker": _ext.has_ext(_FAKE_TRACKER_KEY),
    }


def test_a_host_bootstrap_installs_process_global_seams():
    """Establish that a host bootstrap really does mutate package globals.

    Without this leg the next test could pass because nothing ever writes the
    seams, which would make the guard unfalsifiable.
    """
    import matrx_ai

    assert _seam_state() == {"durable_vfs": False, "tracker": False}

    matrx_ai.configure(
        vfs_backend=_FakeVfsBackend(),
        **{_FAKE_TRACKER_KEY: object()},
    )

    assert _seam_state() == {"durable_vfs": True, "tracker": True}, (
        "matrx_ai.configure no longer installs these seams — this guard is "
        "measuring nothing. Re-point it at a seam configure() still writes."
    )


def test_b_the_next_test_sees_the_pristine_package():
    """The leak from the previous test does NOT reach this one.

    This is the whole contract. If it fails, the autouse
    ``_pristine_matrx_ai_host_seams`` fixture in packages/matrx-ai/conftest.py
    is gone or a NEW host seam was added to ``matrx_ai.configure`` without
    being added to ``_SEAMS`` in matrx_ai/testing/host_isolation.py.
    """
    assert _seam_state() == {"durable_vfs": False, "tracker": False}, (
        "A host seam installed by the previous test survived into this one. "
        "matrx-ai tests are order-dependent again — see "
        "matrx_ai/testing/host_isolation.py."
    )


def test_c_workspace_identity_stays_per_conversation_without_a_host():
    """The exact assertion the durable-backend leak broke.

    ``workspace_id_for`` drops the conversation suffix once a durable backend is
    installed, so a leaked host backend turned "alice:session-1" into "alice"
    in tests/vfs/test_package_isolation.py — a real failure with no real defect.
    """
    from dataclasses import dataclass

    from matrx_ai.tools.vfs import workspace_id_for

    @dataclass
    class _Ctx:
        user_id: str | None
        conversation_id: str | None

    assert workspace_id_for(_Ctx(user_id="alice", conversation_id="session-1")) == (
        "alice:session-1"
    )


def test_d_a_test_that_configures_a_seam_is_restored_for_its_neighbours():
    """Symmetry check: restore happens BEFORE the test too, not only after.

    A polluted process (a host bootstrap that fired during collection, before
    any fixture ran) is corrected on the way in — otherwise the very first
    matrx-ai test in a mixed run would still read the host's wiring.
    """
    import matrx_ai

    assert not _seam_state()["durable_vfs"]
    matrx_ai.configure(vfs_backend=_FakeVfsBackend())
    assert _seam_state()["durable_vfs"]


@pytest.mark.parametrize("_repeat", [1, 2])
def test_e_still_pristine_after_repeated_pollution(_repeat: int):
    """Every test gets the same pristine start, not just the one after a leak."""
    assert _seam_state() == {"durable_vfs": False, "tracker": False}
