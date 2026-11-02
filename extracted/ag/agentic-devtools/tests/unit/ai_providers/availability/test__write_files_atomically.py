import os
import stat
import sys
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.ai_providers.availability import _write_files_atomically


def _set_mode(
    monkeypatch: pytest.MonkeyPatch, target: Path, mode: int, *, fallback: bool = False
) -> tuple[MagicMock, MagicMock]:
    windows = sys.platform == "win32"
    original_stat, original_chmod = Path.stat, os.chmod
    if windows:
        monkeypatch.setattr(
            Path,
            "stat",
            lambda self, *args, **kwargs: (
                MagicMock(st_mode=stat.S_IFREG | mode) if self == target else original_stat(self, *args, **kwargs)
            ),
        )
    else:
        os.chmod(target, mode)
    fchmod = MagicMock(side_effect=AttributeError if fallback else None)
    if windows or fallback:
        monkeypatch.setattr(os, "fchmod", fchmod, raising=False)
    chmod = MagicMock(wraps=None if windows else original_chmod)
    if fallback:
        monkeypatch.setattr(os, "chmod", chmod)
    return fchmod, chmod


def _fail_second_replace(message: str) -> Any:
    original_replace = os.replace
    call_count = 0

    def failing_replace(src: str, dst: str) -> None:
        nonlocal call_count
        call_count += 1
        if call_count == 2:
            raise OSError(message)
        original_replace(src, dst)

    return failing_replace


def test_write_files_atomically_writes_all_files(tmp_path: Path) -> None:
    a = tmp_path / "a.txt"
    b = tmp_path / "sub" / "b.txt"

    _write_files_atomically({a: "hello", b: "world"})

    assert a.read_text() == "hello"
    assert b.read_text() == "world"


def test_write_files_atomically_preserves_existing_mode(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    target = tmp_path / "a.txt"
    target.write_text("original")
    original_mode = 0o640

    mock_fchmod, _ = _set_mode(monkeypatch, target, original_mode)
    _write_files_atomically({target: "updated"})

    if sys.platform == "win32":
        assert mock_fchmod.call_args.args[1] == original_mode
    else:
        assert stat.S_IMODE(target.stat().st_mode) == original_mode


def test_write_files_atomically_falls_back_to_chmod_when_fchmod_unavailable(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "a.txt"
    target.write_text("original")
    original_mode = 0o640
    _, mock_chmod = _set_mode(monkeypatch, target, original_mode, fallback=True)
    _write_files_atomically({target: "updated"})

    assert target.read_text() == "updated"
    assert any(call.args[1] == original_mode for call in mock_chmod.call_args_list)
    if sys.platform != "win32":
        assert stat.S_IMODE(target.stat().st_mode) == original_mode


def test_write_files_atomically_rolls_back_read_only_target_on_replace_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    a.write_text("original-a")
    b.write_text("original-b")
    read_only_mode = 0o444
    mock_fchmod, _ = _set_mode(monkeypatch, a, read_only_mode)
    failing_replace = _fail_second_replace("simulated replace failure")

    with patch("agentic_devtools.ai_providers.availability.os.replace", side_effect=failing_replace):
        with pytest.raises(OSError, match="simulated replace failure"):
            _write_files_atomically({a: "new-a", b: "new-b"})

    if sys.platform == "win32":
        assert mock_fchmod.call_args_list[2].args[1] == read_only_mode
    assert a.read_text() == "original-a"
    assert b.read_text() == "original-b"
    if sys.platform != "win32":
        assert stat.S_IMODE(a.stat().st_mode) == read_only_mode
    # Temp files must be cleaned up by the finally block.
    assert not any(tmp_path.glob("tmp*")), "stale temp files found after rollback"


def test_write_files_atomically_removes_new_file_on_replace_failure(tmp_path: Path) -> None:
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"

    failing_replace = _fail_second_replace("simulated replace failure for new file")

    with patch("agentic_devtools.ai_providers.availability.os.replace", side_effect=failing_replace):
        with pytest.raises(OSError):
            _write_files_atomically({a: "content-a", b: "content-b"})

    assert not a.exists()


def test_write_files_atomically_preserves_original_error_when_new_file_rollback_unlink_fails(
    tmp_path: Path,
) -> None:
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"

    original_replace = os.replace
    call_count = [0]

    def failing_replace(src: str, dst: str) -> None:
        call_count[0] += 1
        if call_count[0] == 2:
            raise OSError("simulated replace failure for new file")
        original_replace(src, dst)

    original_unlink = Path.unlink

    def failing_unlink(self: Path, missing_ok: bool = False) -> None:
        if self == a:
            raise PermissionError("rollback unlink failure")
        original_unlink(self, missing_ok=missing_ok)

    with (
        patch("agentic_devtools.ai_providers.availability.os.replace", side_effect=failing_replace),
        patch.object(Path, "unlink", new=failing_unlink),
    ):
        with pytest.raises(OSError, match="simulated replace failure for new file"):
            _write_files_atomically({a: "content-a", b: "content-b"})


def test_write_files_atomically_rolls_back_with_chmod_fallback_on_replace_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    a.write_text("original-a")
    b.write_text("original-b")
    original_mode = 0o444
    _, mock_chmod = _set_mode(monkeypatch, a, original_mode, fallback=True)
    failing_replace = _fail_second_replace("replace failed after first target")

    with patch("agentic_devtools.ai_providers.availability.os.replace", side_effect=failing_replace):
        with pytest.raises(OSError, match="replace failed after first target"):
            _write_files_atomically({a: "new-a", b: "new-b"})

    assert a.read_text() == "original-a"
    assert b.read_text() == "original-b"
    assert mock_chmod.call_args_list[2].args[1] == original_mode
    if sys.platform != "win32":
        assert stat.S_IMODE(a.stat().st_mode) == original_mode


def test_write_files_atomically_preserves_original_error_when_rollback_restore_fails(tmp_path: Path) -> None:
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    a.write_text("original-a")
    b.write_text("original-b")
    failing_replace = _fail_second_replace("simulated replace failure")

    original_fdopen = os.fdopen
    fdopen_call_count = [0]

    def failing_fdopen(*args: Any, **kwargs: Any):
        fdopen_call_count[0] += 1
        if fdopen_call_count[0] >= 3:
            raise OSError("rollback fdopen failure")
        return original_fdopen(*args, **kwargs)

    with (
        patch("agentic_devtools.ai_providers.availability.os.replace", side_effect=failing_replace),
        patch("agentic_devtools.ai_providers.availability.os.fdopen", side_effect=failing_fdopen),
    ):
        with pytest.raises(OSError, match="simulated replace failure"):
            _write_files_atomically({a: "new-a", b: "new-b"})

    assert a.read_text() == "new-a"
    assert b.read_text() == "original-b"


def test_write_files_atomically_rollback_cleanup_swallows_close_and_unlink_errors(tmp_path: Path) -> None:
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    a.write_text("original-a")
    b.write_text("original-b")

    original_replace = os.replace
    replace_call_count = [0]

    def failing_replace(src: str, dst: str) -> None:
        replace_call_count[0] += 1
        if replace_call_count[0] == 2:
            raise OSError("simulated replace failure")
        original_replace(src, dst)

    original_fdopen = os.fdopen
    fdopen_call_count = [0]

    def failing_fdopen(*args: Any, **kwargs: Any):
        fdopen_call_count[0] += 1
        if fdopen_call_count[0] >= 3:
            raise OSError("rollback fdopen failure")
        return original_fdopen(*args, **kwargs)

    with (
        patch("agentic_devtools.ai_providers.availability.os.replace", side_effect=failing_replace),
        patch("agentic_devtools.ai_providers.availability.os.fdopen", side_effect=failing_fdopen),
        patch("agentic_devtools.ai_providers.availability.os.close", side_effect=OSError("EBADF")),
        patch("agentic_devtools.ai_providers.availability.os.unlink", side_effect=FileNotFoundError),
    ):
        with pytest.raises(OSError, match="simulated replace failure"):
            _write_files_atomically({a: "new-a", b: "new-b"})


def test_write_files_atomically_cleans_up_temp_on_write_failure(tmp_path: Path) -> None:
    target = tmp_path / "out.txt"

    with patch("agentic_devtools.ai_providers.availability.os.fdopen", side_effect=OSError("write fail")):
        with pytest.raises(OSError, match="write fail"):
            _write_files_atomically({target: "data"})

    assert not target.exists()


def test_write_files_atomically_preserves_write_error_when_temp_cleanup_unlink_fails(tmp_path: Path) -> None:
    target = tmp_path / "out.txt"

    with (
        patch("agentic_devtools.ai_providers.availability.os.fdopen", side_effect=OSError("write fail")),
        patch("agentic_devtools.ai_providers.availability.os.unlink", side_effect=PermissionError("unlink fail")),
    ):
        with pytest.raises(OSError, match="write fail"):
            _write_files_atomically({target: "data"})


def test_write_files_atomically_write_failure_cleanup_swallows_close_errors(tmp_path: Path) -> None:
    target = tmp_path / "out.txt"

    mock_fh = MagicMock()
    mock_fh.__enter__ = MagicMock(return_value=mock_fh)
    mock_fh.__exit__ = MagicMock(return_value=False)
    mock_fh.write.side_effect = OSError("write error")

    with (
        patch("agentic_devtools.ai_providers.availability.os.fdopen", return_value=mock_fh),
        patch("agentic_devtools.ai_providers.availability.os.close", side_effect=OSError("EBADF")),
    ):
        with pytest.raises(OSError, match="write error"):
            _write_files_atomically({target: "data"})


def test_write_files_atomically_closes_fd_on_fdopen_failure(tmp_path: Path) -> None:
    target = tmp_path / "out.txt"

    with (
        patch("agentic_devtools.ai_providers.availability.os.fdopen", side_effect=OSError("fdopen fail")),
        patch("agentic_devtools.ai_providers.availability.os.close") as mock_close,
    ):
        with pytest.raises(OSError, match="fdopen fail"):
            _write_files_atomically({target: "data"})

    mock_close.assert_called_once()


def test_write_files_atomically_cleans_up_temp_on_keyboard_interrupt_during_write(tmp_path: Path) -> None:
    target = tmp_path / "out.txt"

    with patch("agentic_devtools.ai_providers.availability.os.fdopen", side_effect=KeyboardInterrupt):
        with pytest.raises(KeyboardInterrupt):
            _write_files_atomically({target: "data"})

    assert not target.exists()
    assert not any(tmp_path.glob("tmp*")), "stale temp files found after KeyboardInterrupt"


def test_write_files_atomically_rolls_back_on_keyboard_interrupt_during_rename(tmp_path: Path) -> None:
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    a.write_text("original-a")
    b.write_text("original-b")

    original_replace = os.replace
    call_count = [0]

    def ki_on_second(src: str, dst: str) -> None:
        call_count[0] += 1
        if call_count[0] == 2:
            raise KeyboardInterrupt
        original_replace(src, dst)

    with patch("agentic_devtools.ai_providers.availability.os.replace", side_effect=ki_on_second):
        with pytest.raises(KeyboardInterrupt):
            _write_files_atomically({a: "new-a", b: "new-b"})

    assert a.read_text() == "original-a"
    assert b.read_text() == "original-b"
    assert not any(tmp_path.glob("tmp*")), "stale temp files found after KeyboardInterrupt rollback"


def test_write_files_atomically_preserves_replace_error_when_final_cleanup_unlink_fails(tmp_path: Path) -> None:
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    a.write_text("original-a")
    b.write_text("original-b")

    original_replace = os.replace
    call_count = [0]

    def failing_replace(src: str, dst: str) -> None:
        call_count[0] += 1
        if call_count[0] == 2:
            raise OSError("simulated replace failure")
        original_replace(src, dst)

    with (
        patch("agentic_devtools.ai_providers.availability.os.replace", side_effect=failing_replace),
        patch("agentic_devtools.ai_providers.availability.os.unlink", side_effect=PermissionError("unlink fail")),
    ):
        with pytest.raises(OSError, match="simulated replace failure"):
            _write_files_atomically({a: "new-a", b: "new-b"})
