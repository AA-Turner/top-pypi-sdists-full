"""Tests for exact-commit raw benchmark fixture verification."""

import io
import stat
import subprocess
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci.windows_fixture_bytes import verify_fixture_bytes

_ROOT = Path("/repo")
_COMMIT = "a" * 40
_BLOB = "b" * 40
_PREFIX = b"tests/fixtures/reviewing-agent-benchmark/"


def _record(
    path: bytes,
    *,
    blob: bytes = _BLOB.encode(),
    mode: bytes = b"100644",
    entry_type: bytes = b"blob",
) -> bytes:
    return mode + b" " + entry_type + b" " + blob + b"\t" + path + b"\0"


def _install_filesystem(
    monkeypatch: pytest.MonkeyPatch,
    *,
    missing: set[str] | None = None,
    non_regular: set[str] | None = None,
    unreadable: set[str] | None = None,
) -> list[bytes]:
    missing = missing or set()
    non_regular = non_regular or set()
    unreadable = unreadable or set()
    opened_contents: list[bytes] = []
    monkeypatch.setattr(Path, "exists", lambda path: path == _ROOT)
    monkeypatch.setattr(Path, "is_dir", lambda path: path == _ROOT)

    def lstat(path: Path) -> SimpleNamespace:
        if str(path.relative_to(_ROOT)).replace("\\", "/") in missing:
            raise FileNotFoundError(str(path))
        mode = stat.S_IFDIR if str(path.relative_to(_ROOT)).replace("\\", "/") in non_regular else stat.S_IFREG
        return SimpleNamespace(st_mode=mode | 0o644)

    def open_file(path: Path, mode: str = "r") -> io.BytesIO:
        if str(path.relative_to(_ROOT)).replace("\\", "/") in unreadable:
            raise PermissionError(f"cannot read {path}")
        assert mode == "rb"
        content = b"\r\nfixture bytes\n"
        opened_contents.append(content)
        return io.BytesIO(content)

    monkeypatch.setattr(Path, "lstat", lstat)
    monkeypatch.setattr(Path, "open", open_file)
    return opened_contents


def _install_git(
    monkeypatch: pytest.MonkeyPatch,
    paths: list[bytes],
    *,
    commit: str = _COMMIT,
    blob: bytes = _BLOB.encode(),
    tree: bytes | None = None,
    attributes: dict[bytes, bytes] | None = None,
    hashes: dict[bytes, bytes] | None = None,
) -> Mock:
    attributes = attributes or {path: b"unset" for path in paths}
    hashes = hashes or {path: blob + b"\n" for path in paths}
    tree = tree if tree is not None else b"".join(_record(path, blob=blob) for path in paths)
    calls: list[list[str]] = []

    def run(arguments: list[str], **kwargs: object) -> subprocess.CompletedProcess[bytes]:
        calls.append(arguments)
        assert kwargs["check"] is True
        assert kwargs["shell"] is False
        assert kwargs["capture_output"] is True
        if arguments[3:] == ["rev-parse", "--show-toplevel"]:
            output = b"/repo\n"
        elif arguments[3:] == ["rev-parse", "HEAD"]:
            output = commit.encode() + b"\n"
        elif arguments[3:6] == ["ls-tree", "-r", "-z"]:
            output = tree
        elif arguments[3:6] == ["check-attr", "-z", "text"]:
            path = arguments[-1].encode()
            output = path + b"\0text\0" + attributes.get(path, b"unset") + b"\0"
        elif arguments[3:5] == ["hash-object", "--no-filters"]:
            path = arguments[-1].encode()
            output = hashes.get(path, _BLOB.encode() + b"\n")
        else:
            raise AssertionError(f"Unexpected git invocation: {arguments!r}")
        return subprocess.CompletedProcess(arguments, 0, stdout=output, stderr=b"")

    mock = Mock(side_effect=run)
    monkeypatch.setattr(subprocess, "run", mock)
    mock.calls_seen = calls
    return mock


def test_verify_fixture_bytes_checks_raw_hashes_and_preserves_path_arguments(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    path = _PREFIX + "space café\nfixture.dat".encode()
    opened_contents = _install_filesystem(monkeypatch)
    git = _install_git(monkeypatch, [path])

    assert verify_fixture_bytes(_COMMIT, _ROOT) == 1
    assert opened_contents == [b"\r\nfixture bytes\n"]

    calls = git.calls_seen
    assert calls[0] == ["git", "-C", str(_ROOT), "rev-parse", "--show-toplevel"]
    assert calls[1] == ["git", "-C", str(_ROOT), "rev-parse", "HEAD"]
    assert calls[2] == [
        "git",
        "-C",
        str(_ROOT),
        "ls-tree",
        "-r",
        "-z",
        "--full-tree",
        _COMMIT,
        "--",
        "tests/fixtures/reviewing-agent-benchmark",
    ]
    assert calls[3] == [
        "git",
        "-C",
        str(_ROOT),
        "check-attr",
        "-z",
        "text",
        "--",
        path.decode(),
    ]
    assert calls[4] == [
        "git",
        "-C",
        str(_ROOT),
        "hash-object",
        "--no-filters",
        "--",
        path.decode(),
    ]


def test_verify_fixture_bytes_accepts_sha256_object_ids(monkeypatch: pytest.MonkeyPatch) -> None:
    commit = "c" * 64
    blob = b"d" * 64
    path = _PREFIX + b"sha256-fixture"
    _install_filesystem(monkeypatch)
    _install_git(monkeypatch, [path], commit=commit, blob=blob)

    assert verify_fixture_bytes(commit, _ROOT) == 1


@pytest.mark.parametrize("commit", ["a" * 39, "A" * 40, "g" * 40, "a" * 41])
def test_verify_fixture_bytes_rejects_invalid_commit_ids(commit: str) -> None:
    with pytest.raises(ValueError, match="full lowercase"):
        verify_fixture_bytes(commit, _ROOT)


def test_verify_fixture_bytes_rejects_missing_root(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(Path, "exists", lambda path: False)
    with pytest.raises(FileNotFoundError, match="does not exist"):
        verify_fixture_bytes(_COMMIT, _ROOT)


def test_verify_fixture_bytes_rejects_non_directory_root(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(Path, "exists", lambda path: True)
    monkeypatch.setattr(Path, "is_dir", lambda path: False)
    with pytest.raises(NotADirectoryError, match="not a directory"):
        verify_fixture_bytes(_COMMIT, _ROOT)


def test_verify_fixture_bytes_rejects_repository_subdirectory(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_filesystem(monkeypatch)
    git = _install_git(monkeypatch, [])
    git.side_effect = [
        subprocess.CompletedProcess([], 0, stdout=b"/other\n", stderr=b""),
    ]
    with pytest.raises(ValueError, match="repository top-level"):
        verify_fixture_bytes(_COMMIT, _ROOT)


def test_verify_fixture_bytes_rejects_head_mismatch(monkeypatch: pytest.MonkeyPatch) -> None:
    _install_filesystem(monkeypatch)
    git = _install_git(monkeypatch, [])
    git.side_effect = [
        subprocess.CompletedProcess([], 0, stdout=b"/repo\n", stderr=b""),
        subprocess.CompletedProcess([], 0, stdout=b"c" * 40 + b"\n", stderr=b""),
    ]
    with pytest.raises(ValueError, match="HEAD does not match"):
        verify_fixture_bytes(_COMMIT, _ROOT)


@pytest.mark.parametrize(
    ("tree", "message"),
    [
        (b"", "empty"),
        (b"100644 blob " + _BLOB.encode() + b"\t" + _PREFIX + b"cut", "truncated"),
        (b"\0", "Malformed"),
        (b"100644 blob " + _BLOB.encode() + b" " + _BLOB.encode() + b"\tx\0", "metadata"),
        (_record(_PREFIX + b"x") + _record(_PREFIX + b"x"), "Duplicate"),
        (_record(b"outside/x"), "Malformed fixture path"),
        (_record(_PREFIX + b"x", mode=b"120000"), "Unsupported"),
        (_record(_PREFIX + b"x", entry_type=b"commit"), "Unsupported"),
        (
            b"100644 blob " + b"g" * 40 + b"\t" + _PREFIX + b"x\0",
            "Unsupported",
        ),
    ],
)
def test_verify_fixture_bytes_rejects_invalid_tree_inventories(
    monkeypatch: pytest.MonkeyPatch, tree: bytes, message: str
) -> None:
    _install_filesystem(monkeypatch)
    _install_git(monkeypatch, [], tree=tree)
    with pytest.raises(ValueError, match=message):
        verify_fixture_bytes(_COMMIT, _ROOT)


def test_verify_fixture_bytes_rejects_missing_fixture(monkeypatch: pytest.MonkeyPatch) -> None:
    path = _PREFIX + b"missing"
    _install_filesystem(monkeypatch, missing={path.decode()})
    _install_git(monkeypatch, [path])
    with pytest.raises(FileNotFoundError, match="missing"):
        verify_fixture_bytes(_COMMIT, _ROOT)


def test_verify_fixture_bytes_rejects_non_regular_fixture(monkeypatch: pytest.MonkeyPatch) -> None:
    path = _PREFIX + b"directory"
    _install_filesystem(monkeypatch, non_regular={path.decode()})
    _install_git(monkeypatch, [path])
    with pytest.raises(ValueError, match="not a regular file"):
        verify_fixture_bytes(_COMMIT, _ROOT)


def test_verify_fixture_bytes_rejects_unreadable_fixture(monkeypatch: pytest.MonkeyPatch) -> None:
    path = _PREFIX + b"unreadable"
    _install_filesystem(monkeypatch, unreadable={path.decode()})
    _install_git(monkeypatch, [path])
    with pytest.raises(ValueError, match="not readable"):
        verify_fixture_bytes(_COMMIT, _ROOT)


@pytest.mark.parametrize(
    ("attribute", "message"),
    [(b"set", "observed 'set'"), (b"unspecified", "observed 'unspecified'")],
)
def test_verify_fixture_bytes_rejects_non_unset_attributes(
    monkeypatch: pytest.MonkeyPatch, attribute: bytes, message: str
) -> None:
    path = _PREFIX + b"fixture"
    _install_filesystem(monkeypatch)
    _install_git(monkeypatch, [path], attributes={path: attribute})
    with pytest.raises(ValueError, match=message):
        verify_fixture_bytes(_COMMIT, _ROOT)


@pytest.mark.parametrize(
    "attribute_output",
    [b"", b"wrong\0text\0unset\0", b"fixture\0text\0unset", b"fixture\0other\0unset\0"],
)
def test_verify_fixture_bytes_rejects_malformed_attribute_results(
    monkeypatch: pytest.MonkeyPatch, attribute_output: bytes
) -> None:
    path = _PREFIX + b"fixture"
    _install_filesystem(monkeypatch)
    git = _install_git(monkeypatch, [path])
    git.side_effect = [
        subprocess.CompletedProcess([], 0, stdout=b"/repo\n", stderr=b""),
        subprocess.CompletedProcess([], 0, stdout=_COMMIT.encode() + b"\n", stderr=b""),
        subprocess.CompletedProcess([], 0, stdout=_record(path), stderr=b""),
        subprocess.CompletedProcess([], 0, stdout=attribute_output, stderr=b""),
    ]
    with pytest.raises(ValueError, match="attribute result"):
        verify_fixture_bytes(_COMMIT, _ROOT)


def test_verify_fixture_bytes_rejects_raw_hash_mismatch(monkeypatch: pytest.MonkeyPatch) -> None:
    path = _PREFIX + b"fixture"
    _install_filesystem(monkeypatch)
    _install_git(monkeypatch, [path], hashes={path: b"c" * 40 + b"\n"})
    with pytest.raises(ValueError, match="blob mismatch"):
        verify_fixture_bytes(_COMMIT, _ROOT)


@pytest.mark.parametrize("bad_hash", [b"", b"short\n", b"C" * 40 + b"\n"])
def test_verify_fixture_bytes_rejects_malformed_hash_results(monkeypatch: pytest.MonkeyPatch, bad_hash: bytes) -> None:
    path = _PREFIX + b"fixture"
    _install_filesystem(monkeypatch)
    _install_git(monkeypatch, [path], hashes={path: bad_hash})
    with pytest.raises(ValueError, match="Malformed raw hash"):
        verify_fixture_bytes(_COMMIT, _ROOT)


@pytest.mark.parametrize("failure_at", ["top-level", "head", "tree", "attribute-command", "hash-command"])
def test_verify_fixture_bytes_propagates_git_failures(monkeypatch: pytest.MonkeyPatch, failure_at: str) -> None:
    path = _PREFIX + b"fixture"
    _install_filesystem(monkeypatch)
    failure_signatures = {
        "top-level": ["rev-parse", "--show-toplevel"],
        "head": ["rev-parse", "HEAD"],
        "tree": ["ls-tree", "-r", "-z"],
        "attribute-command": ["check-attr", "-z", "text"],
        "hash-command": ["hash-object", "--no-filters"],
    }

    def run(arguments: list[str], **kwargs: object) -> subprocess.CompletedProcess[bytes]:
        command = arguments[3:]
        if command[: len(failure_signatures[failure_at])] == failure_signatures[failure_at]:
            raise subprocess.CalledProcessError(2, arguments, stderr=b"git failed")
        if command == ["rev-parse", "--show-toplevel"]:
            output = b"/repo\n"
        elif command == ["rev-parse", "HEAD"]:
            output = _COMMIT.encode() + b"\n"
        elif command[:3] == ["ls-tree", "-r", "-z"]:
            output = _record(path)
        elif command[:3] == ["check-attr", "-z", "text"]:
            output = path + b"\0text\0unset\0"
        else:
            output = _BLOB.encode() + b"\n"
        return subprocess.CompletedProcess(arguments, 0, stdout=output, stderr=b"")

    monkeypatch.setattr(subprocess, "run", run)
    with pytest.raises(subprocess.CalledProcessError) as error:
        verify_fixture_bytes(_COMMIT, _ROOT)
    assert error.value.stderr == b"git failed"


def test_verify_fixture_bytes_rejects_malformed_git_outputs(monkeypatch: pytest.MonkeyPatch) -> None:
    _install_filesystem(monkeypatch)
    git = _install_git(monkeypatch, [])
    git.side_effect = [subprocess.CompletedProcess([], 0, stdout="not bytes", stderr=b"")]
    with pytest.raises(ValueError, match="malformed repository top-level"):
        verify_fixture_bytes(_COMMIT, _ROOT)


def test_verify_fixture_bytes_rejects_non_byte_tree_inventory(monkeypatch: pytest.MonkeyPatch) -> None:
    _install_filesystem(monkeypatch)
    git = _install_git(monkeypatch, [])
    git.side_effect = [
        subprocess.CompletedProcess([], 0, stdout=b"/repo\n", stderr=b""),
        subprocess.CompletedProcess([], 0, stdout=_COMMIT.encode() + b"\n", stderr=b""),
        subprocess.CompletedProcess([], 0, stdout="not bytes", stderr=b""),
    ]
    with pytest.raises(ValueError, match="malformed fixture tree inventory"):
        verify_fixture_bytes(_COMMIT, _ROOT)


def test_verify_fixture_bytes_propagates_git_startup_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    _install_filesystem(monkeypatch)
    monkeypatch.setattr(subprocess, "run", Mock(side_effect=OSError("git unavailable")))
    with pytest.raises(OSError, match="git unavailable"):
        verify_fixture_bytes(_COMMIT, _ROOT)
