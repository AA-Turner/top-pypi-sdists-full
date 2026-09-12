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

import importlib
import sys
from pathlib import Path
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


def test_seam_baseline_loads_an_arbitrary_unloaded_module(tmp_path, monkeypatch):
    """A plugin seam remains lazy and generic, rather than becoming a fixed list."""
    from matrx_ai.testing import host_isolation

    module_name = "host_seam_extension"
    (tmp_path / f"{module_name}.py").write_text("value = {'pristine': True}\n")
    monkeypatch.syspath_prepend(str(tmp_path))
    importlib.invalidate_caches()
    monkeypatch.setattr(host_isolation, "_SEAMS", ((module_name, ("value",)),))

    assert module_name not in sys.modules
    baseline = host_isolation.capture_baseline()
    module = sys.modules[module_name]
    module.value["polluted"] = True

    host_isolation.restore_baseline(baseline)

    assert module.value == {"pristine": True}


def test_seam_baseline_never_duplicates_a_module_its_parent_already_imported(
    tmp_path, monkeypatch
):
    """A seam is PROCESS-GLOBAL state, so two module objects for it is the bug.

    Every real seam lives inside a package whose ``__init__`` re-exports it
    (``matrx_ai.persistence`` does ``from .registry import register_table``).
    ``importlib.util.find_spec()`` imports that parent, which imports the child
    — so a loader that only checks ``sys.modules`` BEFORE ``find_spec`` then
    executes the spec anyway installs a SECOND copy over the real one. The
    coordinator then reads an empty table registry while the tests populate the
    original, and every queued write is dropped as ``unregistered_table``.
    """
    from matrx_ai.testing import host_isolation

    pkg = tmp_path / "host_seam_pkg"
    pkg.mkdir()
    (pkg / "__init__.py").write_text("from . import child\n")
    (pkg / "child.py").write_text("value = {'pristine': True}\n")
    monkeypatch.syspath_prepend(str(tmp_path))
    importlib.invalidate_caches()
    monkeypatch.setattr(host_isolation, "_SEAMS", (("host_seam_pkg.child", ("value",)),))

    for name in ("host_seam_pkg", "host_seam_pkg.child"):
        monkeypatch.delitem(sys.modules, name, raising=False)
        assert name not in sys.modules

    host_isolation.capture_baseline()

    parent = sys.modules["host_seam_pkg"]
    child = sys.modules["host_seam_pkg.child"]
    assert child is parent.child, (
        "capture_baseline() loaded a second copy of the seam module — the "
        "process now has two sets of that module's globals"
    )


def test_host_seam_loader_has_no_unresolved_dynamic_import():
    """The canonical scanner must see the entire host-isolation import graph."""
    from matrx_mandate_scan.adapters.python import scan_source

    source_path = Path(__file__).parents[1] / "matrx_ai/testing/host_isolation.py"
    result = scan_source(source_path.read_text(encoding="utf-8"), source_path.as_posix())

    assert [finding for finding in result.findings if finding.code == "UNRESOLVED_IMPORT"] == []


@pytest.mark.parametrize("_repeat", [1, 2])
def test_e_still_pristine_after_repeated_pollution(_repeat: int):
    """Every test gets the same pristine start, not just the one after a leak."""
    assert _seam_state() == {"durable_vfs": False, "tracker": False}


# ---------------------------------------------------------------------------
# Seam drift, the direction capture_baseline() cannot see
# ---------------------------------------------------------------------------


def test_every_seam_configure_wires_is_declared():
    """A new host seam cannot reach main undeclared.

    ``capture_baseline()`` raises when a DECLARED seam disappears. The way the
    ordering bug actually comes back is the opposite move: wiring a NEW
    process-global into ``matrx_ai.configure`` and forgetting ``_SEAMS``.
    Nothing would restore it, matrx-ai's tests would silently go
    order-dependent again, and the next cross-suite run would be red for a
    reason nobody can find. This reads the real ``configure()`` and says so at
    the commit that adds the seam instead.
    """
    from matrx_ai.testing.host_isolation import undeclared_seam_modules

    source_path = Path(__file__).parents[1] / "matrx_ai/__init__.py"
    undeclared = undeclared_seam_modules(source_path.read_text(encoding="utf-8"))

    assert not undeclared, (
        "matrx_ai.configure() wires these modules, but nothing declares or "
        "waives them, so the test isolation would NOT restore them:\n  "
        + "\n  ".join(undeclared)
        + "\n\nAdd each to _SEAMS in matrx_ai/testing/host_isolation.py with the "
        "globals it writes — or, if it truly holds no process-global state, to "
        "_NO_PROCESS_GLOBAL_STATE with the reason."
    )


def test_undeclared_seam_detector_catches_a_planted_seam():
    """The detector above must be able to FAIL — plant a seam and prove it.

    A guard that cannot be shown failing is not a guard: without this leg,
    ``test_every_seam_configure_wires_is_declared`` would pass identically if
    the scanner silently measured nothing.
    """
    from matrx_ai.testing.host_isolation import undeclared_seam_modules

    planted = (
        "def _helper():\n"
        "    from matrx_ai.brand_new.seam import set_thing\n"
        "    set_thing(None)\n"
        "\n"
        "def configure(**kwargs):\n"
        "    from matrx_ai._ext import configure_ext\n"
        "    configure_ext(**kwargs)\n"
        "    _helper()\n"
    )

    assert undeclared_seam_modules(planted) == ["matrx_ai.brand_new.seam"], (
        "the detector missed a seam wired through a helper configure() calls"
    )


def test_undeclared_seam_detector_screams_when_it_measures_nothing():
    """A scan that cannot find ``configure`` must raise, never return clean."""
    from matrx_ai.testing.host_isolation import HostSeamDriftError, undeclared_seam_modules

    with pytest.raises(HostSeamDriftError):
        undeclared_seam_modules("def something_else():\n    pass\n")
