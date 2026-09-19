"""Tests for the hook-path flow spool file."""

import json
import os
import sys
import time

import pytest

from runlayer_cli import flow_spool
from runlayer_cli.flow_contract import MAX_FLOWS_PER_ENVELOPE
from tests.hostile_inputs import DEEP_NESTING_BYTES


@pytest.fixture(autouse=True)
def _spool_in_tmp(monkeypatch, tmp_path):
    monkeypatch.setattr(flow_spool, "get_runlayer_dir", lambda: tmp_path)
    return tmp_path


def _summary(n: int, ts: int | None = None) -> dict:
    return {
        "operation": "cli.hook_event",
        "status": "ok",
        "n": n,
        "ts": ts if ts is not None else int(time.time()),
    }


class TestSpoolAppendDrain:
    def test_drain_missing_file_returns_none(self):
        assert flow_spool.spool_drain() is None

    def test_append_drain_roundtrip(self):
        flow_spool.spool_append(_summary(1))
        flow_spool.spool_append(_summary(2))
        envelope = flow_spool.spool_drain()
        assert envelope is not None
        assert [f["n"] for f in envelope["flows"]] == [1, 2]
        assert envelope["dropped"] == 0
        # Drained: spool is empty for the next invocation.
        assert flow_spool.spool_drain() is None

    def test_file_truncated_after_drain(self, _spool_in_tmp):
        flow_spool.spool_append(_summary(1))
        flow_spool.spool_drain()
        assert (_spool_in_tmp / "flow-spool.jsonl").stat().st_size == 0

    def test_malformed_trailing_line_skipped(self, _spool_in_tmp):
        flow_spool.spool_append(_summary(1))
        with open(_spool_in_tmp / "flow-spool.jsonl", "ab") as f:
            f.write(b'{"operation": "cli.hook_ev')  # crash mid-append
        envelope = flow_spool.spool_drain()
        assert envelope is not None
        assert [f["n"] for f in envelope["flows"]] == [1]
        assert envelope["dropped"] == 1

    def test_non_dict_line_skipped(self, _spool_in_tmp):
        with open(_spool_in_tmp / "flow-spool.jsonl", "wb") as f:
            f.write(b"[1, 2]\n")
        assert flow_spool.spool_drain() is None

    def test_deep_nested_row_dropped_siblings_kept(self, _spool_in_tmp):
        """A poisoned row raises RecursionError, not JSONDecodeError (ISS-01).

        It must count as one ``dropped`` and leave its siblings shippable.
        Before, it escaped ``_partition`` to ``spool_drain``'s outer ``except``:
        the drain returned ``None`` forever and the spool stayed wedged.
        """
        path = _spool_in_tmp / "flow-spool.jsonl"
        with open(path, "wb") as f:
            f.write(json.dumps(_summary(1)).encode() + b"\n")
            f.write(DEEP_NESTING_BYTES + b"\n")
            f.write(json.dumps(_summary(2)).encode() + b"\n")
        envelope = flow_spool.spool_drain()
        assert envelope is not None
        assert [f["n"] for f in envelope["flows"]] == [1, 2]
        assert envelope["dropped"] == 1
        assert path.stat().st_size == 0

    def test_stale_entries_pruned(self):
        old_ts = int(time.time()) - flow_spool._MAX_AGE_SECONDS - 60
        flow_spool.spool_append(_summary(1, ts=old_ts))
        flow_spool.spool_append(_summary(2))
        envelope = flow_spool.spool_drain()
        assert envelope is not None
        assert [f["n"] for f in envelope["flows"]] == [2]
        assert envelope["dropped"] == 1

    def test_newest_win_beyond_cap(self):
        for n in range(MAX_FLOWS_PER_ENVELOPE + 3):
            flow_spool.spool_append(_summary(n))
        envelope = flow_spool.spool_drain()
        assert envelope is not None
        assert len(envelope["flows"]) == MAX_FLOWS_PER_ENVELOPE
        assert envelope["flows"][0]["n"] == 3
        assert envelope["dropped"] == 3

    def test_oversized_line_not_written(self, _spool_in_tmp):
        flow_spool.spool_append({"operation": "cli.hook_event", "pad": "x" * 5000})
        assert not (_spool_in_tmp / "flow-spool.jsonl").exists()

    def test_size_cap_stops_appends(self, _spool_in_tmp):
        path = _spool_in_tmp / "flow-spool.jsonl"
        with open(path, "wb") as f:
            f.write(b"x" * (flow_spool._MAX_SPOOL_BYTES + 1))
        size_before = path.stat().st_size
        flow_spool.spool_append(_summary(1))
        assert path.stat().st_size == size_before

    @pytest.mark.skipif(sys.platform == "win32", reason="fcntl lock simulation")
    def test_contended_lock_returns_none_without_blocking(self, _spool_in_tmp):
        import fcntl

        flow_spool.spool_append(_summary(1))
        lock_fd = os.open(
            str(_spool_in_tmp / "flow-spool.lock"), os.O_CREAT | os.O_RDWR
        )
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_EX)
            start = time.monotonic()
            assert flow_spool.spool_drain() is None
            assert time.monotonic() - start < 0.5
        finally:
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
            os.close(lock_fd)
        # Data still spooled for the next, uncontended drain.
        envelope = flow_spool.spool_drain()
        assert envelope is not None
        assert [f["n"] for f in envelope["flows"]] == [1]

    def test_append_failure_is_silent(self, monkeypatch):
        monkeypatch.setattr(
            flow_spool, "_spool_path", lambda: (_ for _ in ()).throw(OSError("ro fs"))
        )
        flow_spool.spool_append(_summary(1))  # must not raise

    def test_lines_are_valid_json(self, _spool_in_tmp):
        flow_spool.spool_append(_summary(1))
        raw = (_spool_in_tmp / "flow-spool.jsonl").read_bytes()
        assert raw.endswith(b"\n")
        assert json.loads(raw.decode())["n"] == 1


def _hosted(n: int, host: str | None, ts: int | None = None) -> dict:
    summary = _summary(n, ts)
    if host is not None:
        summary["target_host"] = host
    return summary


def _remaining(spool_dir) -> list[int]:
    lines = (spool_dir / "flow-spool.jsonl").read_text().splitlines()
    return [json.loads(line)["n"] for line in lines]


class TestPerHostDrain:
    def test_drains_target_host_and_legacy_keeps_foreign(self, _spool_in_tmp):
        flow_spool.spool_append(_hosted(1, "a.example.com"))
        flow_spool.spool_append(_hosted(2, "b.example.com"))
        flow_spool.spool_append(_hosted(3, None))  # older CLI: no target_host
        flow_spool.spool_append(_hosted(4, "a.example.com"))

        # Records are stamped pre-normalized; only the argument is lowercased.
        envelope = flow_spool.spool_drain(target_host="A.Example.COM")
        assert envelope is not None
        assert [f["n"] for f in envelope["flows"]] == [1, 3, 4]
        assert envelope["dropped"] == 0
        # B's line survives verbatim for a later POST to B; A is fully drained.
        assert _remaining(_spool_in_tmp) == [2]
        assert flow_spool.spool_drain(target_host="a.example.com") is None

        envelope_b = flow_spool.spool_drain(target_host="B.example.com")
        assert envelope_b is not None
        assert [f["n"] for f in envelope_b["flows"]] == [2]
        assert flow_spool.spool_drain() is None

    def test_foreign_only_spool_returns_none_and_keeps_lines(self, _spool_in_tmp):
        flow_spool.spool_append(_hosted(1, "b.example.com"))
        assert flow_spool.spool_drain(target_host="a.example.com") is None
        assert _remaining(_spool_in_tmp) == [1]

    def test_stale_foreign_lines_pruned(self, _spool_in_tmp):
        old_ts = int(time.time()) - flow_spool._MAX_AGE_SECONDS - 60
        flow_spool.spool_append(_hosted(1, "b.example.com", ts=old_ts))
        flow_spool.spool_append(_hosted(2, "a.example.com"))

        envelope = flow_spool.spool_drain(target_host="a.example.com")
        assert envelope is not None
        assert [f["n"] for f in envelope["flows"]] == [2]
        assert envelope["dropped"] == 1
        assert _remaining(_spool_in_tmp) == []

    def test_foreign_lines_byte_capped_newest_kept(self, _spool_in_tmp):
        line_bytes = len(json.dumps(_hosted(0, "b.example.com")).encode()) + 1
        count = flow_spool._MAX_FOREIGN_BYTES // line_bytes + 20
        for n in range(count):
            flow_spool.spool_append(_hosted(n, "b.example.com"))
        flow_spool.spool_append(_hosted(999, "a.example.com"))

        envelope = flow_spool.spool_drain(target_host="a.example.com")
        assert envelope is not None
        assert [f["n"] for f in envelope["flows"]] == [999]
        assert envelope["dropped"] == 0  # foreign trims are B's loss, not A's
        spool = _spool_in_tmp / "flow-spool.jsonl"
        assert 0 < spool.stat().st_size <= flow_spool._MAX_FOREIGN_BYTES
        kept = _remaining(_spool_in_tmp)
        assert kept[-1] == count - 1  # newest kept
        assert kept[0] > 0  # oldest trimmed first
        # The live host can still append after the write-back.
        flow_spool.spool_append(_hosted(1000, "a.example.com"))
        assert _remaining(_spool_in_tmp)[-1] == 1000

    def test_no_target_host_drains_everything(self, _spool_in_tmp):
        flow_spool.spool_append(_hosted(1, "a.example.com"))
        flow_spool.spool_append(_hosted(2, "b.example.com"))
        flow_spool.spool_append(_hosted(3, None))

        envelope = flow_spool.spool_drain()
        assert envelope is not None
        assert [f["n"] for f in envelope["flows"]] == [1, 2, 3]
        assert _remaining(_spool_in_tmp) == []
