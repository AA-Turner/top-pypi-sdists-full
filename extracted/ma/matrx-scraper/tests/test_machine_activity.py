"""Cloud Computer idle evidence counts the person's programs, never the platform's."""

from __future__ import annotations

from pathlib import Path

from matrx_scraper.cloud_browser.worker.machine_activity import read_machine_activity


def _proc(root: Path, pid: int, comm: str, state: str, utime: int, stime: int, *, ppid: int = 0,
          io: int | None = None) -> None:
    d = root / str(pid)
    d.mkdir(exist_ok=True)
    rest = [state, str(ppid)] + ["0"] * 9 + [str(utime), str(stime)] + ["0"] * 10
    (d / "stat").write_text(f"{pid} ({comm}) " + " ".join(rest))
    if io is not None:
        (d / "io").write_text(f"rchar: {io}\nwchar: 0\nsyscr: 1\n")


def _net(root: Path, rx: int, tx: int) -> None:
    (root / "net").mkdir(exist_ok=True)
    (root / "net/dev").write_text(
        "Inter-|   Receive\n face |bytes\n"
        "    lo: 999999 0 0 0 0 0 0 0 999999 0 0 0 0 0 0 0\n"
        f"  eth0: {rx} 0 0 0 0 0 0 0 {tx} 0 0 0 0 0 0 0\n"
    )


def test_only_foreign_processes_count(tmp_path: Path) -> None:
    _proc(tmp_path, 10, "chrome", "R", 900, 100)
    _proc(tmp_path, 11, "Xvfb", "S", 50, 5)
    _proc(tmp_path, 12, "make", "R", 30, 7)
    _proc(tmp_path, 13, "lxterminal", "S", 3, 0)
    got = read_machine_activity(str(tmp_path), sample={})
    assert {k: got[k] for k in ("available", "foreign_cpu_ticks", "foreign_running",
                                "foreign_processes", "input_idle_ms")} == {
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


def test_the_idle_desktop_baseline_is_not_the_person(tmp_path: Path) -> None:
    """Break (2026-10-17 live): pcmanfm (desktop icons), the container init and
    the entrypoint's runuser were counted, so an empty desktop read as work."""
    _proc(tmp_path, 1, "init", "S", 14, 31)
    _proc(tmp_path, 7, "runuser", "S", 2, 0)
    _proc(tmp_path, 161, "pcmanfm", "R", 100, 48)
    _proc(tmp_path, 162, "tint2", "S", 36, 104)
    _proc(tmp_path, 89, "openbox", "S", 26, 34)
    _proc(tmp_path, 85, "bash", "S", 0, 0)
    got = read_machine_activity(str(tmp_path))
    assert got["foreign_cpu_ticks"] == 0 and got["foreign_running"] == 0


def test_a_download_that_uses_no_cpu_still_reads_as_work(tmp_path: Path) -> None:
    """Break (review D7, 2026-10-18): a download, a sleep in a build, an upload
    burn almost no CPU, so the build move read the machine as quiet and stopped
    it mid-job. Its I/O and the machine's network traffic are now in the reading."""
    clock = iter([100.0, 110.0])
    sample: dict[str, float] = {}
    _proc(tmp_path, 30, "curl", "S", 1, 0, io=1_000_000)
    _net(tmp_path, 5_000_000, 100_000)
    first = read_machine_activity(str(tmp_path), clock=lambda: next(clock), sample=sample)
    assert first["foreign_io_bytes_per_second"] is None  # one reading is no rate
    _proc(tmp_path, 30, "curl", "S", 1, 0, io=51_000_000)
    _net(tmp_path, 55_000_000, 200_000)
    second = read_machine_activity(str(tmp_path), clock=lambda: next(clock), sample=sample)
    assert second["foreign_cpu_ticks"] == 1  # what the CPU-only check saw: nothing
    assert second["foreign_io_bytes_per_second"] == 5_000_000
    assert second["net_bytes_per_second"] == 5_010_000  # loopback excluded


def test_agent_shell_work_counts_every_process_under_the_daemon(tmp_path: Path) -> None:
    _proc(tmp_path, 40, "python3", "S", 0, 0, ppid=1)       # the agent daemon
    _proc(tmp_path, 41, "bash", "S", 0, 0, ppid=40)         # an agent command
    _proc(tmp_path, 42, "sleep", "S", 0, 0, ppid=41)        # what it waits on
    _proc(tmp_path, 50, "lxterminal", "S", 0, 0, ppid=1)    # not the agent's
    got = read_machine_activity(str(tmp_path), agent_pid=40, sample={})
    assert got["agent_jobs"] == 2 and got["work_signals"] == 1
    assert read_machine_activity(str(tmp_path), sample={})["agent_jobs"] is None
