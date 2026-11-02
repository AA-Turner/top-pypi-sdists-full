from contextlib import contextmanager
from pathlib import Path
from typing import IO

import agentic_devtools.cli.ci.dispatch_reservation as module
from agentic_devtools.cli.ci.dispatch_reservation import _locked


class _Operations:
    def __init__(self, handle: IO[str]) -> None:
        self.handle = handle
        self.path: Path | None = None

    @contextmanager
    def locked_file(self, path: Path):
        self.path = path
        yield self.handle


def test_uses_injected_file_operations(tmp_path: Path) -> None:
    handle = (tmp_path / "ledger").open("w+", encoding="utf-8")
    operations = _Operations(handle)
    with _locked(tmp_path / "ledger", operations) as result:
        assert result is handle
    assert operations.path == tmp_path / "ledger"
    handle.close()


def test_uses_rplus_real_lock(monkeypatch, tmp_path: Path) -> None:
    calls: list[tuple[str, bool]] = []

    @contextmanager
    def fake_locked_file(path: Path, mode: str, *, exclusive: bool, encoding: str):
        calls.append((mode, exclusive))
        handle = (tmp_path / "ledger").open("w+", encoding=encoding)
        try:
            yield handle
        finally:
            handle.close()

    monkeypatch.setattr(module, "locked_file", fake_locked_file)
    with _locked(tmp_path / "ledger", None):
        pass
    assert calls == [("r+", True)]
