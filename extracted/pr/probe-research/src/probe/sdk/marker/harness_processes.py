# ---------------------------------------------------------------------------
# WHICH SESSION RUNS THIS PROCESS, for a harness that does not say.
#
#   <state_dir>/harness-processes/<pid>-<start>.json
#       {"harness": "<registry id>", "session_id": "<uuid>", "updated_at": 1790000000.0}
#
# Claude Code, Codex and pi put the session id in every shell they start; Kimi
# Code puts none there. Its hooks (children of the harness process) write this
# record for the harness process itself, found by the title the harness gives
# its own process (the registry's `process_title`). A `probe` command or a
# training script the harness starts walks up its parents to the same process
# and reads the record. `<start>` is the process's start time, so a recycled pid
# never reads a dead session's record. Linux reads /proc; macOS asks `ps` once.
# ---------------------------------------------------------------------------

HARNESS_PROCESSES_DIRNAME = "harness-processes"
#: How far up a lookup walks: harness -> shell -> (wrappers) -> probe.
_ANCESTOR_LIMIT = 16


def harness_processes_dir() -> Path:
    return state_dir() / HARNESS_PROCESSES_DIRNAME


#: Script runtimes: a process started as `node /usr/local/bin/pi` is pi. Where
#: the script never retitles itself, or the platform does not show the new
#: title (macOS `ps`), the runtime is all the first word says.
_SCRIPT_RUNTIMES = ("node", "nodejs", "bun")


def _title_of(argv: "list[str]") -> str:
    """A process's title from its argv: the script a runtime runs, else argv[0]."""
    if not argv:
        return ""
    if os.path.basename(argv[0]) in _SCRIPT_RUNTIMES and len(argv) > 1 and not argv[1].startswith("-"):
        return argv[1]
    return argv[0]


def _proc_linux(pid: int) -> "tuple[int, str, str] | None":
    """(parent pid, start time, title) from /proc, or None."""
    try:
        with open(f"/proc/{pid}/stat", "rb") as fh:
            stat_line = fh.read().decode("utf-8", "replace")
        with open(f"/proc/{pid}/cmdline", "rb") as fh:
            argv = [part.decode("utf-8", "replace") for part in fh.read().split(b"\0") if part]
    except OSError:
        return None
    argv0 = _title_of(argv)
    # comm may hold spaces and parentheses: the fields start after the LAST ')'.
    fields = stat_line.rsplit(")", 1)[-1].split()
    try:
        return int(fields[1]), fields[19], argv0
    except (IndexError, ValueError):
        return None


def _ps_table() -> "dict[int, tuple[int, str, str]]":
    """Every process as {pid: (parent pid, start time, title)}, from one `ps`."""
    import subprocess  # noqa: PLC0415 -- only off Linux

    try:
        # LC_ALL=C and TZ=UTC: `lstart` is the record key, so it must read the
        # same in the hook and in the command, whatever their locale or zone.
        out = subprocess.run(
            ["ps", "-A", "-ww", "-o", "pid=,ppid=,lstart=,command="],
            capture_output=True, text=True, timeout=3, check=False,
            env={**os.environ, "LC_ALL": "C", "TZ": "UTC"},
        ).stdout
    except (OSError, subprocess.SubprocessError):
        return {}
    table = {}
    for line in out.splitlines():
        parts = line.split(None, 7)  # pid, ppid, 5 words of lstart, command
        if len(parts) < 8:
            continue
        try:
            table[int(parts[0])] = (int(parts[1]), "-".join(parts[2:7]), _title_of(parts[7].split()))
        except ValueError:
            continue
    return table


def _ancestors(pid: "int | None" = None) -> "list[tuple[int, str, str]]":
    """(pid, start time, title) for `pid` (default: this process's parent) and
    each process above it, nearest first. Empty where processes can't be read.

    A hook event run by the warm hook host (`hooks/zygote.py`, plan A0) has the
    host for a parent, not the harness: the host names the harness's process
    in PROBE_HOOK_PARENT_PID, and the walk starts there."""
    if pid is None:
        hosted = os.environ.get("PROBE_HOOK_PARENT_PID", "")
        pid = int(hosted) if hosted.isdigit() and int(hosted) > 1 else os.getppid()
    current = pid
    table = None if os.path.isdir("/proc/self") else _ps_table()
    chain = []
    for _ in range(_ANCESTOR_LIMIT):
        if current <= 1:
            break
        info = _proc_linux(current) if table is None else table.get(current)
        if info is None:
            break
        parent, start, title = info
        chain.append((current, start, title))
        current = parent
    return chain


def _titled(title: str, wanted: str) -> bool:
    return os.path.basename(title) == wanted or title == wanted


def _process_record_path(pid: int, start: str) -> Path:
    return harness_processes_dir() / (f"{pid}-" + re.sub(r"[^A-Za-z0-9]", "", start) + ".json")


def record_harness_process(
    harness: str, session_id: str, process_title: "str | tuple[str, ...] | list[str]",
    loaded: "dict | None" = None,
) -> "Path | None":
    """From a hook: note that the nearest ancestor titled `process_title` (or any
    of several titles) runs `session_id` (replacing what it ran before: a TUI's
    /new and /resume). Also sweeps records of processes that are gone. None when
    no such ancestor exists or the record cannot be written. Never raises.

    Several titles because one harness process reads differently by platform:
    a harness that retitles itself shows the new title in Linux's /proc, while
    macOS's `ps` keeps the name it was started as (the registry's `binary`).

    `loaded`: what the process loaded (Kimi's plugin folders and manifests,
    `probe._shared.kimi_live.loaded_info`). Kimi reads its plugins once, at its
    start, and again only on `/reload`, which reopens the SAME session
    (SessionStart, source `resume`) from the folder it now loads: only that
    (the same session resumed from ANOTHER plugin folder while the one it ran
    from is still there), or a process's first record, writes it. A `/new`
    (source `startup`), a resume of another session, the same session closed
    and reopened (an editor's or server's `kimi acp`/`server`/`web`: no
    reload, the same folder) or any later event keeps it, and so does another
    folder whose old one is gone (the hook entry falls back to the newest one
    then). A first record proves nothing (`late`) when it comes
    LOADED_FIRST_SEEN_S or more after its process started (a `/new` in a
    process older than these hooks), or when anything Kimi read at its start
    (`loaded["read_at_start"]`: its plugin list and folders) changed after it."""
    titles = (process_title,) if isinstance(process_title, str) else tuple(t for t in process_title if t)
    if not (valid_session_id(session_id) and harness and titles):
        return None
    try:
        target = next(
            (
                (pid, start)
                for pid, start, title in _ancestors()
                if any(_titled(title, wanted) for wanted in titles)
            ),
            None,
        )
        if target is None:
            return None
        path = _process_record_path(*target)
        path.parent.mkdir(parents=True, exist_ok=True)
        record = {"harness": harness, "session_id": session_id, "updated_at": time.time()}
        if loaded is not None:
            try:
                previous = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                previous = None
            previous = previous if isinstance(previous, dict) else {}
            before = previous.get("loaded")
            if isinstance(before, dict):
                old_root = before.get("plugin_root")
                reloaded = (loaded.get("source") == "resume" and not loaded.get("late")
                            and previous.get("session_id") == session_id
                            and isinstance(old_root, str) and old_root != loaded.get("plugin_root")
                            and os.path.isdir(old_root))
                if not reloaded:
                    loaded = before
            else:
                age = _process_age(target[1])
                if age is None or age >= LOADED_FIRST_SEEN_S or _changed_since(loaded, time.time() - age):
                    loaded = {**loaded, "late": True}
            record["loaded"] = loaded
        body = json.dumps(record)
        if not _publish_atomically(path, body):
            return None
        _sweep_process_records(keep=path)
        return path
    except Exception:  # noqa: BLE001 -- fail-soft: a hook must never break
        return None


#: A process's first `loaded` record proves what it loaded only this soon after
#: its start (Kimi runs SessionStart within seconds of starting).
LOADED_FIRST_SEEN_S = 120


def _changed_since(loaded: dict, started: float) -> bool:
    """Did anything the process read at its start (`read_at_start`) change
    after `started` (epoch seconds)? A path that cannot be read counts."""
    paths = loaded.get("read_at_start") or []
    for path in paths if isinstance(paths, list) else [paths]:
        try:
            if not isinstance(path, str) or os.stat(path).st_mtime >= started - 1:
                return True
        except OSError:
            return True
    return False


def _process_age(start: str) -> "float | None":
    """Seconds since a process started, from its `_ancestors` start time (Linux:
    clock ticks after boot; else `ps`'s UTC `lstart`), or None."""
    try:
        if start.isdigit():
            with open("/proc/uptime", encoding="ascii") as fh:
                uptime = float(fh.read().split()[0])
            return uptime - int(start) / os.sysconf("SC_CLK_TCK")
        import calendar  # noqa: PLC0415

        return time.time() - calendar.timegm(time.strptime(start, "%a-%b-%d-%H:%M:%S-%Y"))
    except (OSError, ValueError, IndexError, OverflowError):
        return None


#: Off Linux a record cannot be checked against its process: it is kept this long.
_RECORD_MAX_AGE_SECONDS = 14 * 86400


def _sweep_process_records(keep: Path) -> None:
    """Delete records whose process has exited (a pid gone, or reused by a
    process that started later). Off Linux, records older than
    `_RECORD_MAX_AGE_SECONDS` go instead."""
    if not os.path.isdir("/proc/self"):
        try:
            cutoff = time.time() - _RECORD_MAX_AGE_SECONDS
            for entry in harness_processes_dir().glob("*.json"):
                if entry != keep and entry.stat().st_mtime < cutoff:
                    entry.unlink()
        except OSError:
            pass
        return
    try:
        for entry in harness_processes_dir().glob("*.json"):
            if entry == keep:
                continue
            pid_text, _, start_text = entry.stem.partition("-")
            info = _proc_linux(int(pid_text)) if pid_text.isdigit() else None
            if info is None or re.sub(r"[^A-Za-z0-9]", "", info[1]) != start_text:
                entry.unlink()
    except (OSError, ValueError):
        return


def process_environ(pid: int) -> "dict[str, str] | None":
    """A process's own environment (Linux /proc only; None elsewhere or when
    unreadable): what it inherited, as opposed to what was set below it."""
    try:
        with open(f"/proc/{pid}/environ", "rb") as fh:
            raw = fh.read()
    except OSError:
        return None
    out = {}
    for item in raw.split(b"\0"):
        key, sep, value = item.partition(b"=")
        if sep:
            out[key.decode("utf-8", "replace")] = value.decode("utf-8", "replace")
    return out


def harness_launch_environ(
    title: str, pid: "int | None" = None, stop_titles: "tuple[str, ...] | list[str]" = ()
) -> "dict[str, str] | None":
    """The environment the nearest ancestor titled `title` (a harness's binary)
    was started with, or None. A harness may filter what its hooks inherit
    (Codex's `shell_environment_policy` drops `PROBE_SESSION_STATE`, issue
    3620); its own process still has what the researcher launched it with.
    The walk stops at an ancestor titled one of `stop_titles` (another coding
    agent, nearer than one titled `title`: whatever is above it launched that
    agent, not this session), and passes a match it cannot read (the wrapper
    above it was started with the same). Linux /proc only: elsewhere the walk
    would cost a `ps` and read nothing. Never raises."""
    if not title or not os.path.isdir("/proc/self"):
        return None
    try:
        for ancestor, _start, name in _ancestors(pid):
            if _titled(name, title):
                environ = process_environ(ancestor)
                if environ is not None:
                    return environ
            elif any(_titled(name, other) for other in stop_titles):
                return None
    except Exception:  # noqa: BLE001 -- a hook must never break
        return None
    return None


def harness_process(
    pid: "int | None" = None, stop_titles: "tuple[str, ...] | list[str]" = ()
) -> "tuple[str, str, int] | None":
    """(harness id, session id, harness pid) for the nearest recorded harness
    ancestor; see `harness_process_session`. Never raises. No record at all
    (no Kimi Code session on this machine) is None without walking the
    ancestors, which runs `ps` where there is no /proc: every `probe` command
    asks this (`agent_session.adopt_harness_process_session`)."""
    try:
        if not _any_harness_process_record():
            return None
        for ancestor, start, title in _ancestors(pid):
            if any(_titled(title, wanted) for wanted in stop_titles):
                return None
            path = _process_record_path(ancestor, start)
            if not path.is_file():
                continue
            data = json.loads(path.read_text(encoding="utf-8"))
            harness, session_id = data.get("harness"), data.get("session_id")
            if isinstance(harness, str) and harness and valid_session_id(session_id):
                return harness, session_id, ancestor
            return None
    except Exception:  # noqa: BLE001
        return None
    return None


def _any_harness_process_record() -> bool:
    """Whether any harness process is recorded here (`record_harness_process`)."""
    try:
        with os.scandir(harness_processes_dir()) as entries:
            return any(entry.name.endswith(".json") for entry in entries)
    except OSError:
        return False


def harness_process_session(
    pid: "int | None" = None, stop_titles: "tuple[str, ...] | list[str]" = ()
) -> "tuple[str, str] | None":
    """(harness id, session id) a harness's hook recorded for the nearest
    ancestor of this process, or None. The walk stops at an ancestor titled one
    of `stop_titles` (another coding agent, nearer than any recorded one: a
    Claude Code started inside Kimi is Claude Code's). Never raises."""
    try:
        for ancestor, start, title in _ancestors(pid):
            if any(_titled(title, wanted) for wanted in stop_titles):
                return None
            path = _process_record_path(ancestor, start)
            if not path.is_file():
                continue
            data = json.loads(path.read_text(encoding="utf-8"))
            harness, session_id = data.get("harness"), data.get("session_id")
            if isinstance(harness, str) and harness and valid_session_id(session_id):
                return harness, session_id
            return None
    except Exception:  # noqa: BLE001
        return None
    return None


