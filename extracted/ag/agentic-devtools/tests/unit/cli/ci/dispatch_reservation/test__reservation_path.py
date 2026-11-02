from pathlib import Path

import agentic_devtools.cli.ci.dispatch_reservation as module
from agentic_devtools.cli.ci.dispatch_reservation import _reservation_path


def test_returns_state_directory_ledger_path(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(module, "get_state_dir", lambda: tmp_path)
    assert _reservation_path() == tmp_path / "dispatch-ordinals.json"
