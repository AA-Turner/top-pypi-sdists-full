"""Cloud Computer idle evidence counts the person's programs, never the platform's."""

from __future__ import annotations

from pathlib import Path

from matrx_scraper.cloud_browser.worker.machine_activity import read_machine_activity


def _proc(root: Path, pid: int, comm: str, state: str, utime: int, stime: int) -> None:
    d = root / str(pid)
    d.mkdir()
    rest = [state] + ["0"] * 10 + [str(utime), str(stime)] + ["0"] * 10
    (d / "stat").write_text(f"{pid} ({comm}) " + " ".join(rest))


def test_only_foreign_processes_count(tmp_path: Path) -> None:
    _proc(tmp_path, 10, "chrome", "R", 900, 100)
    _proc(tmp_path, 11, "Xvfb", "S", 50, 5)
    _proc(tmp_path, 12, "make", "R", 30, 7)
    _proc(tmp_path, 13, "lxterminal", "S", 3, 0)
    got = read_machine_activity(str(tmp_path))
    assert got == {
        "available": True,
        "foreign_cpu_ticks": 40,
        "foreign_running": 1,
        "foreign_processes": ["lxterminal", "make"],
        # No X server on the test host: unknown, never a guessed zero.
        "input_idle_ms": None,
    }


def test_missing_proc_is_unavailable_not_zero(tmp_path: Path) -> None:
    got = read_machine_activity(str(tmp_path / "absent"))
    assert got["available"] is False


def test_a_persons_python_job_counts(tmp_path: Path) -> None:
    _proc(tmp_path, 20, "python3", "R", 70, 1)
    assert read_machine_activity(str(tmp_path))["foreign_cpu_ticks"] == 71
