"""Tests for verifying one tracked fixture file."""

import io
import stat
import subprocess
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci.windows_fixture_bytes import _verify_fixture_file

_ROOT = Path("/repo")
_PATH = "tests/fixtures/reviewing-agent-benchmark/space café\n.dat".encode()
_BLOB = b"b" * 40


def test_verify_fixture_file_uses_raw_hashing_and_unset_text(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(Path, "lstat", lambda path: SimpleNamespace(st_mode=stat.S_IFREG | 0o644))
    raw_bytes = b"\r\nfixture\n"
    monkeypatch.setattr(Path, "open", lambda path, mode: io.BytesIO(raw_bytes))

    def run(arguments: list[str], **kwargs: object) -> subprocess.CompletedProcess[bytes]:
        if arguments[3:6] == ["check-attr", "-z", "text"]:
            output = _PATH + b"\0text\0unset\0"
        else:
            output = _BLOB + b"\n"
        return subprocess.CompletedProcess(arguments, 0, stdout=output, stderr=b"")

    git = Mock(side_effect=run)
    monkeypatch.setattr(subprocess, "run", git)

    _verify_fixture_file(_ROOT, _PATH, _BLOB, 40)

    assert git.call_args_list[0].args[0][-2:] == ["--", _PATH.decode()]
    assert git.call_args_list[1].args[0][-4:] == [
        "hash-object",
        "--no-filters",
        "--",
        _PATH.decode(),
    ]


def test_verify_fixture_file_rejects_non_byte_attribute_output(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(Path, "lstat", lambda path: SimpleNamespace(st_mode=stat.S_IFREG | 0o644))
    monkeypatch.setattr(Path, "open", lambda path, mode: io.BytesIO(b"\r\n"))
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.windows_fixture_bytes._run_git",
        lambda root, arguments: "not bytes",
    )

    with pytest.raises(ValueError, match="Malformed text attribute result"):
        _verify_fixture_file(_ROOT, _PATH, _BLOB, 40)


def test_verify_fixture_file_preserves_missing_file_error_during_open(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(Path, "lstat", lambda path: SimpleNamespace(st_mode=stat.S_IFREG | 0o644))
    monkeypatch.setattr(Path, "open", Mock(side_effect=FileNotFoundError("disappeared")))

    with pytest.raises(FileNotFoundError, match="Tracked fixture is missing"):
        _verify_fixture_file(_ROOT, _PATH, _BLOB, 40)
