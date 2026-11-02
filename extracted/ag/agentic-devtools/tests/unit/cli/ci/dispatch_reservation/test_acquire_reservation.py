import json
from contextlib import AbstractContextManager
from pathlib import Path
from typing import IO, cast

import pytest

import agentic_devtools.cli.ci.dispatch_reservation as reservation_module
from agentic_devtools.cli.ci.dispatch_reservation import (
    AcquiredResult,
    ExhaustedResult,
    LostRaceResult,
    acquire_reservation,
)
from agentic_devtools.file_locking import locked_file

SHA = "a" * 40


class _FileOps:
    def __init__(self, path: Path, *, lose_read_back: bool = False, other_owner: bool = False) -> None:
        self.path = path
        self.lose_read_back = lose_read_back
        self.other_owner = other_owner
        self.reads = 0

    def locked_file(self, path: Path):
        return cast(
            AbstractContextManager[IO[str]],
            _InterleavedFile(path, self, locked_file(path, "a+", exclusive=True, encoding="utf-8")),
        )


class _InterleavedFile:
    def __init__(self, path: Path, ops: _FileOps, context) -> None:
        self._path = path
        self._ops = ops
        self._context = context
        self._handle: IO[str] | None = None

    def __enter__(self) -> IO[str]:
        self._handle = self._context.__enter__()
        return cast(IO[str], self)

    def __exit__(self, *args: object) -> object:
        return self._context.__exit__(*args)

    def seek(self, offset: int, whence: int = 0) -> int:
        assert self._handle is not None
        return self._handle.seek(offset, whence)

    def read(self, size: int = -1) -> str:
        assert self._handle is not None
        self._ops.reads += 1
        value = self._handle.read(size)
        if (self._ops.lose_read_back or self._ops.other_owner) and self._ops.reads == 2:
            self._handle.seek(0)
            replacement = "{}"
            if self._ops.other_owner:
                replacement = value.replace("456-1-a1b2c3d4", "789-1-deadbeef")
            self._handle.write(replacement)
            self._handle.truncate()
            self._handle.flush()
            self._handle.seek(0)
            return replacement
        return value

    def write(self, value: str) -> int:
        assert self._handle is not None
        return self._handle.write(value)

    def truncate(self) -> int:
        assert self._handle is not None
        return self._handle.truncate()

    def flush(self) -> None:
        assert self._handle is not None
        self._handle.flush()


def _use_tmp_path(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(reservation_module, "get_state_dir", lambda: tmp_path)


def test_acquires_and_is_idempotent_for_owner(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    _use_tmp_path(monkeypatch, tmp_path)

    first = acquire_reservation("owner/repo", 123, SHA, 1, "456-1-a1b2c3d4")
    second = acquire_reservation("owner/repo", 123, SHA, 1, "456-1-a1b2c3d4")

    assert isinstance(first, AcquiredResult)
    assert second == first
    store = json.loads((tmp_path / "dispatch-ordinals.json").read_text())
    assert store["reservations"]["owner/repo|123|" + SHA + "|1"]["owner"] == "456-1-a1b2c3d4"


def test_competing_owner_loses_without_overwriting(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    _use_tmp_path(monkeypatch, tmp_path)

    acquire_reservation("owner/repo", 123, SHA, 1, "456-1-a1b2c3d4")
    result = acquire_reservation("owner/repo", 123, SHA, 1, "789-1-deadbeef")

    assert result == LostRaceResult("already_reserved")


def test_read_back_loss_is_not_reported_as_acquired(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    _use_tmp_path(monkeypatch, tmp_path)
    ops = _FileOps(tmp_path / "dispatch-ordinals.json", lose_read_back=True)

    result = acquire_reservation("owner/repo", 123, SHA, 1, "456-1-a1b2c3d4", file_ops=ops)

    assert result == LostRaceResult("read_back_failed")


def test_read_back_other_owner_is_not_reported_as_acquired(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    _use_tmp_path(monkeypatch, tmp_path)
    ops = _FileOps(tmp_path / "dispatch-ordinals.json", other_owner=True)

    result = acquire_reservation("owner/repo", 123, SHA, 1, "456-1-a1b2c3d4", file_ops=ops)

    assert result == LostRaceResult("read_back_failed")


def test_exhausted_ordinal_does_not_create_store(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    _use_tmp_path(monkeypatch, tmp_path)

    result = acquire_reservation("owner/repo", 123, SHA, 4, "456-1-a1b2c3d4")

    assert isinstance(result, ExhaustedResult)
    assert not (tmp_path / "dispatch-ordinals.json").exists()


@pytest.mark.parametrize(
    "args",
    [
        ("repo", 123, SHA, 1, "456-1-a1b2c3d4"),
        ("owner/repo", 0, SHA, 1, "456-1-a1b2c3d4"),
        ("owner/repo", 123, "A" * 40, 1, "456-1-a1b2c3d4"),
        ("owner/repo", 123, SHA, 1, "bad"),
    ],
)
def test_rejects_invalid_request(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, args: tuple[object, ...]) -> None:
    _use_tmp_path(monkeypatch, tmp_path)

    with pytest.raises(ValueError):
        acquire_reservation(*args)  # type: ignore[arg-type]


def test_rejects_malformed_and_duplicate_store(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    _use_tmp_path(monkeypatch, tmp_path)
    path = tmp_path / "dispatch-ordinals.json"
    path.write_text("{", encoding="utf-8")
    with pytest.raises(ValueError):
        acquire_reservation("owner/repo", 123, SHA, 1, "456-1-a1b2c3d4")

    path.write_text('{"schema_version": 1, "reservations": []}', encoding="utf-8")
    with pytest.raises(ValueError):
        acquire_reservation("owner/repo", 123, SHA, 1, "456-1-a1b2c3d4")

    path.write_text(
        '{"schema_version": 1, "reservations": {"wrong": "not a reservation"}}',
        encoding="utf-8",
    )
    with pytest.raises(ValueError):
        acquire_reservation("owner/repo", 123, SHA, 1, "456-1-a1b2c3d4")

    path.write_text(
        '{"schema_version": 1, "reservations": {"wrong": '
        + json.dumps(
            {
                "repo": "owner/repo",
                "pull_request_id": 123,
                "sha": SHA,
                "ordinal": 1,
                "owner": "456-1-a1b2c3d4",
                "state": "reserved",
                "created_at": "2026-08-19T12:34:56.123456Z",
                "schema_version": 1,
            }
        )
        + "}}",
        encoding="utf-8",
    )
    with pytest.raises(ValueError):
        acquire_reservation("owner/repo", 123, SHA, 1, "456-1-a1b2c3d4")

    path.write_text('{"schema_version": 1, "reservations": {}}', encoding="utf-8")
    path.write_text(
        '{"schema_version": 1, "schema_version": 1, "reservations": {}}',
        encoding="utf-8",
    )
    with pytest.raises(ValueError):
        acquire_reservation("owner/repo", 123, SHA, 1, "456-1-a1b2c3d4")
