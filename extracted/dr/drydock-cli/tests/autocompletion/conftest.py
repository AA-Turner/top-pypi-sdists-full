from __future__ import annotations

from pathlib import Path

import pytest

from drydock.core.config.harness_files import (
    init_harness_files_manager,
    reset_harness_files_manager,
)


@pytest.fixture(autouse=True)
def _isolate_skills(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Prevent bundled drydock skills from appearing in autocomplete tests.

    The skill loader reads DRYDOCK_ROOT / "skills" unconditionally.  Pointing
    DRYDOCK_ROOT at a temp dir (no skills/ subdir) keeps slash-command
    ordering deterministic so tests like "tab on /co → /compact" don't
    break when new bundled skills are added whose aliases sort earlier.
    """
    monkeypatch.setattr("drydock.DRYDOCK_ROOT", tmp_path)
    # Re-init the harness manager so it picks up the patched DRYDOCK_ROOT
    reset_harness_files_manager()
    init_harness_files_manager("user", "project")
    yield
    reset_harness_files_manager()
