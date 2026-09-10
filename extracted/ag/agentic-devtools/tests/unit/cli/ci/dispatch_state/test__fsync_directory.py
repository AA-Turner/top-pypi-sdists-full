from pathlib import Path

import pytest

from agentic_devtools.cli.ci import dispatch_state as dispatch_state_module


def test_tolerates_missing_o_directory(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delattr(dispatch_state_module.os, "O_DIRECTORY", raising=False)

    dispatch_state_module._fsync_directory(tmp_path)


def test_skips_directory_fsync_when_directory_handles_are_unsupported(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(dispatch_state_module.os, "name", "nt")
    monkeypatch.delattr(dispatch_state_module.os, "O_DIRECTORY", raising=False)

    def unexpected_open(target: str | Path, flags: int, mode: int = 0o777) -> int:
        raise AssertionError(f"os.open should not be called for {target} with flags {flags} and mode {mode}")

    monkeypatch.setattr(dispatch_state_module.os, "open", unexpected_open)

    dispatch_state_module._fsync_directory(tmp_path)


def test_fails_closed_on_open_failures(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    original_open = dispatch_state_module.os.open

    def flaky_open(target: str | Path, flags: int, mode: int = 0o777) -> int:
        if Path(target) == tmp_path:
            raise OSError("fsync unavailable")
        return original_open(target, flags, mode)

    monkeypatch.setattr(dispatch_state_module.os, "open", flaky_open)

    with pytest.raises(OSError, match="failed to fsync directory"):
        dispatch_state_module._fsync_directory(tmp_path)
