"""The tool-trace file sink never grows without bound on a long-lived server (C80, 2026-11-10: the task disk filled)."""

from __future__ import annotations

from pathlib import Path

import pytest

from matrx_ai.tools import _debug_log as sink


@pytest.fixture
def small_sink(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setenv("MATRX_TOOL_DEBUG_LOG_DIR", str(tmp_path))
    monkeypatch.setattr(sink, "_log_file_path", None)
    monkeypatch.setattr(sink, "_switches", {})
    monkeypatch.setattr(sink, "FILE_CAP_BYTES", 4_000)
    monkeypatch.setattr(sink, "FILE_KEEP", 3)
    monkeypatch.setattr(sink, "_SIZE_CHECK_EVERY", 5)
    monkeypatch.setattr(sink, "_writes_since_check", 0)
    return tmp_path


def test_the_file_sink_rolls_and_keeps_only_the_newest_files(small_sink: Path) -> None:
    with sink.trace_sinks_enabled():
        for i in range(2_000):
            sink.log_event("DISPATCH", tool="t", call=f"call-{i}", body="x" * 200)
        active = sink.log_path()
    files = sorted(small_sink.glob("tool-trace-*.log"))
    total = sum(f.stat().st_size for f in files)
    assert len(files) <= sink.FILE_KEEP, [f.name for f in files]
    # 2,000 events of ~250 bytes = ~500 KB written; the directory holds at most KEEP files of about the cap each.
    assert total < (sink.FILE_KEEP + 1) * (sink.FILE_CAP_BYTES + sink._SIZE_CHECK_EVERY * 400), total
    current = (small_sink / "current.log").resolve()
    assert active is not None and current.exists() and current.name == active.name
    assert any("call-1999" in f.read_text() for f in small_sink.glob("tool-trace-*.log"))
