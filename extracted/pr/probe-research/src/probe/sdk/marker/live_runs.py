# ---------------------------------------------------------------------------
# Liveness: which of this session's runs are executing right now
# ---------------------------------------------------------------------------


def _fcntl():
    """The flock provider: `probe.foundation.os_backend.os_backend` (fcntl on POSIX, msvcrt on
    Windows). The vendored hook copy has no `probe` package to import; there it
    is fcntl itself, or None on a platform without it."""
    try:
        from probe.foundation.os_backend import os_backend  # noqa: PLC0415

        return os_backend
    except ImportError:
        pass
    try:  # an older CLI keeps it at its old path
        import importlib  # noqa: PLC0415

        return importlib.import_module("probe._shared.oscompat")  # restructure-guard-ok: older CLIs
    except ImportError:
        pass
    try:
        import fcntl  # noqa: PLC0415

        return fcntl
    except ImportError:
        return None


def _lease_run_id(path: Path, now: float) -> str | None:
    """The run a `.lease` entry names, if the lease has not expired.

    Malformed or unreadable reads as NOT live, which INVERTS
    `probe.cli.run_lock`. That module fails closed because applying an
    auto-update into a live run costs somebody's afternoon. Here the cost is
    reversed: the only thing downstream is a word on a status line, and
    printing "running" when nothing is running is a confident lie. Uncertainty
    should say less, not more.
    """
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict):
        return None
    try:
        if float(data.get("expires_at", 0)) <= now:
            return None
    except (TypeError, ValueError):
        return None
    run = data.get("run")
    return run if isinstance(run, str) and run else None


def _flock_run_id(path: Path) -> str | None:
    """The run a `.flock` entry names, if somebody still holds the lock.

    READ-ONLY, unlike `run_lock._flock_is_held`, which deletes the entry when it
    finds it unheld. That cleanup is right on a command path that runs
    occasionally and wrong here: this executes on every status-line render, so
    it would race a starting run's own acquire and delete state it does not own.
    Probing takes the lock non-blocking and releases immediately; a second
    `open()` is a new open file description, so this reads correctly even when
    the holder is this process.
    """
    module = _fcntl()
    if module is None:
        return None  # cannot prove liveness on this platform: say nothing
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict):
        return None
    run = data.get("run")
    if not (isinstance(run, str) and run):
        return None
    try:
        handle = open(path, "a+")  # noqa: SIM115 -- closed below
    except OSError:
        return None
    try:
        module.flock(handle.fileno(), module.LOCK_EX | module.LOCK_NB)
    except BlockingIOError:
        return run  # somebody holds it: a live run
    except (OSError, ValueError):
        return None
    else:
        try:
            module.flock(handle.fileno(), module.LOCK_UN)
        except (OSError, ValueError):
            pass
        return None  # nobody held it; leave the leftover for run_lock to reap
    finally:
        handle.close()


def live_run_ids() -> set[str]:
    """Run ids currently executing on THIS machine, from the run-lock directory.

    Bounded and non-mutating. `probe.cli.run_lock` owns the format and the
    cleanup; this only looks.
    """
    live = set()
    try:
        directory = state_dir() / "runs"
        entries = sorted(directory.iterdir())
    except OSError:
        return live
    now = time.time()
    for entry in entries[:512]:  # sanity bound, mirroring run_lock.MAX_SCAN_ENTRIES
        try:
            if entry.suffix == ".lease":
                found = _lease_run_id(entry, now)
            elif entry.suffix == ".flock":
                found = _flock_run_id(entry)
            else:
                continue
        except OSError:
            continue
        if found:
            live.add(found)
    return live


def is_live(state: dict | None) -> bool:
    """Whether a run this session opened is executing. TWO SOURCES, OR'd.

    **The server is the source of truth.** `active_run_ids` is what
    `GET /v1/runs?foreign_key=<agent>_session_id:<id>&active=true` said, and it is
    the only one of the two that can see a run executing on a CLUSTER: that run
    holds its lock on the machine running it, not on this laptop. Reading only
    local locks made a remote training job — much of what this team actually runs
    — indistinguishable from no run at all.

    **The local locks are a fast path, not a fallback.** They are ground truth for
    a local process (the kernel releases an flock on SIGKILL and OOM, which no
    heartbeat can promise) and they are current between refreshes, so a run
    started seconds ago shows before the next fetch lands. The intersection with
    `run_ids` is what keeps that honest: "a run is live on this box" is
    `run_lock`'s question and would light up for a colleague's sweep in another
    terminal.

    OR rather than AND because the two see different things and neither is
    complete. Both false is the only "not running".
    """
    if not isinstance(state, dict):
        return False

    active = state.get("active_run_ids")
    if isinstance(active, list) and any(isinstance(run_id, str) and run_id for run_id in active):
        return True

    run_ids = state.get("run_ids")
    if not isinstance(run_ids, list) or not run_ids:
        return False
    return bool(set(run_ids) & live_run_ids())


#: A session's gap file (`probe.service.capture_gate`): the stretches of its
#: transcript written while Probe was off, which are never to be uploaded.
GAPS_SUFFIX = ".gaps"
#: What a kept session keeps: its gap file and its switch (what says it was off).
KEPT_SUFFIXES = (GAPS_SUFFIX, ".state")
#: A gap file that names no transcript (or does not read) goes after this long.
UNKNOWN_TRANSCRIPT_KEEP_SECONDS = 90 * 86400


def _keeps_gaps(path: str, mtime: float, now: float) -> bool:
    """Does this gap file still hold a gap of a transcript that still exists?
    One whose transcript is gone is done with. One that names no transcript,
    or does not read, is kept for UNKNOWN_TRANSCRIPT_KEEP_SECONDS from its
    last write."""
    try:
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, ValueError):
        data = None
    if isinstance(data, dict) and isinstance(data.get("gaps"), list) and not data["gaps"]:
        return False
    transcript = data.get("transcript") if isinstance(data, dict) else None
    if isinstance(transcript, str) and transcript:
        return os.path.exists(transcript)
    return now - mtime < UNKNOWN_TRANSCRIPT_KEEP_SECONDS


def prune(max_age_seconds: float = MAX_AGE_SECONDS) -> None:
    """Drop markers for sessions long finished. Never raises.

    os.scandir rather than a `find` shell-out, for the reason the telemetry
    hook's prune already documents: `find /tmp` on macOS matches the symlink
    and silently descends into nothing.

    A session whose gap file still holds a gap (`_keeps_gaps`) keeps that file
    and its `.state` (what says it was off) whatever their age; its other
    files go as any session's do. A gap file that is done with goes now. A
    `.home` stays while its session lives (`_keeps_home`).
    """
    try:
        now = time.time()
        cutoff = now - max_age_seconds
        with os.scandir(sessions_dir()) as listing:
            entries = list(listing)
        kept: set[str] = set()
        for entry in entries:
            if not entry.name.endswith(GAPS_SUFFIX):
                continue
            try:
                if not entry.is_file():
                    continue
                if _keeps_gaps(entry.path, entry.stat().st_mtime, now):
                    kept.add(entry.name[: -len(GAPS_SUFFIX)])
                else:
                    os.unlink(entry.path)
            except OSError:
                continue
        for entry in entries:
            try:
                suffix = next((s for s in KEPT_SUFFIXES if entry.name.endswith(s)), None)
                if suffix is not None and entry.name[: -len(suffix)] in kept:
                    continue
                if entry.is_file() and entry.stat().st_mtime < cutoff and not _keeps_home(entry.name, cutoff):
                    os.unlink(entry.path)
            except OSError:
                continue
    except OSError:
        pass


def _keeps_home(name: str, cutoff: float) -> bool:
    """Is this an old `.home` whose session still lives? A home never expires on its own,
    so it stays while the session's marker, daemon lease or scope was written in the window."""
    if not name.endswith(HOME_SUFFIX):
        return False
    session_id = name[: -len(HOME_SUFFIX)]
    for path in (marker_path(session_id), lease_path(session_id), scope_path(session_id)):
        try:
            if path.stat().st_mtime >= cutoff:
                return True
        except OSError:
            continue
    return False


