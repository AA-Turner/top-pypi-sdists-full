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
#
# The same walk names the agent running a process when two agents' variables are
# set (a Codex started from a Claude Code shell inherits Claude Code's): the
# agents above it, nearest first (`find_agent_ancestors`,
# `agent_session.harness_process_env`).
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


_PIDPATH: list = []  # macOS `proc_pidpath`, loaded once (`_get_executable_path`)


def _get_executable_path(pid: int) -> "str | None":
    """The file a process runs, from the macOS kernel (`proc_pidpath`); None
    elsewhere. The hooks' copy of this module cannot import
    `probe.foundation.service_api.procid.get_executable_path`, its twin."""
    import sys  # noqa: PLC0415

    if sys.platform != "darwin":
        return None
    try:
        import ctypes  # noqa: PLC0415

        if not _PIDPATH:
            for library in ("/usr/lib/libproc.dylib", "/usr/lib/libSystem.B.dylib"):
                try:
                    pidpath = ctypes.CDLL(library).proc_pidpath
                except (OSError, AttributeError):
                    continue
                pidpath.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_uint32]
                pidpath.restype = ctypes.c_int
                _PIDPATH.append(pidpath)
                break
            else:
                _PIDPATH.append(None)
        if _PIDPATH[0] is None:
            return None
        buffer = ctypes.create_string_buffer(4096)  # PROC_PIDPATHINFO_MAXSIZE
        if _PIDPATH[0](pid, buffer, 4096) <= 0:
            return None
        return buffer.value.decode("utf-8", "replace") or None
    except Exception:  # noqa: BLE001 -- a Python without ctypes: the `ps` title stands
        return None


def _get_walk_start(pid: "int | None") -> "tuple[int | None, bool]":
    """(the process a walk from `pid` starts at, whether it is the caller a Probe
    service child serves): `pid`, else PROBE_CALLER_PID, else the hook host's
    PROBE_HOOK_PARENT_PID, else (None, False): the caller's own default (`_ancestors`:
    this process's parent; the namespace check: this process)."""
    if pid is not None:
        return pid, False
    caller = os.environ.get("PROBE_CALLER_PID", "")
    if caller.isascii() and caller.isdigit() and int(caller) > 1:
        return int(caller), True
    hosted = os.environ.get("PROBE_HOOK_PARENT_PID", "")
    if hosted.isascii() and hosted.isdigit() and int(hosted) > 1:
        return int(hosted), False
    return None, False


def _ancestors(pid: "int | None" = None) -> "list[tuple[int, str, str]]":
    """(pid, start time, title) for `pid` (default: this process's parent) and
    each process above it, nearest first. Empty where processes can't be read.

    A hook event run by the warm hook host (`hooks/zygote.py`, plan A0) has the
    host for a parent, not the harness: the host names the harness's process
    in PROBE_HOOK_PARENT_PID, and the walk starts there. A `probe` command the
    Probe service runs (`cli.run`) has the service's CLI host for a parent: the
    service names the shim it serves in PROBE_CALLER_PID (`probe.foundation.caller`),
    and the walk is that shim's parents. It ends with pid 1 of this process
    namespace: a sandboxed Codex shell's whole view is itself and pid 1,
    `codex-linux-sandbox`."""
    if pid is None:
        start, is_caller = _get_walk_start(None)
        if is_caller:
            return _ancestors(start)[1:]
        pid = start if start is not None else os.getppid()
    current = pid
    table = None if os.path.isdir("/proc/self") else _ps_table()
    chain = []
    for _ in range(_ANCESTOR_LIMIT):
        if current < 1:
            break
        info = _proc_linux(current) if table is None else table.get(current)
        if info is None:
            break
        parent, start, title = info
        if table is not None:
            # `ps` cannot say where a path with a space ends: the Claude app keeps
            # Claude Code under `~/Library/Application Support/`, read as
            # `Application`. The kernel's path, when it starts with that word.
            path = _get_executable_path(current)
            if path and path.startswith(title + " "):
                title = path
        chain.append((current, start, title))
        current = parent
    return chain


def _titled(title: str, wanted: str) -> bool:
    return os.path.basename(title) == wanted or title == wanted


#: The machine's own pid namespace: the kernel gives it this fixed inode (PROC_PID_INIT_INO).
_ROOT_PID_NAMESPACE = "pid:[4026531836]"


def _is_in_child_pid_namespace() -> bool:
    """Whether this process runs in a child pid namespace (a sandbox, a container):
    its pid 1 is not the machine's, and a pid another agent exported means nothing
    here. `NSpid` cannot say so where the sandbox mounted its own /proc; the
    namespace's identity can. Elsewhere (macOS: no /proc), False."""
    try:
        return os.readlink("/proc/self/ns/pid") != _ROOT_PID_NAMESPACE
    except OSError:
        return False


def _get_pid_namespace(pid: int) -> "str | None":
    """Another process's pid namespace (`pid:[<inode>]`), or None when unreadable."""
    try:
        return os.readlink(f"/proc/{pid}/ns/pid")
    except OSError:
        return None


def _is_walk_in_child_pid_namespace(pid: "int | None") -> bool:
    """Whether the walk from `pid` (default: this process, the caller a Probe service
    child serves (PROBE_CALLER_PID), or the hook host's harness pid
    (PROBE_HOOK_PARENT_PID): `_get_walk_start`) runs in a child pid namespace. The
    service child sits in the machine's namespace while its caller may be in a
    sandbox's, where an exported pid is numbered differently; an unreadable start
    process (another user's) counts as one, unproven."""
    if _is_in_child_pid_namespace():
        return True
    start, _is_caller = _get_walk_start(pid)
    if start is None or not os.path.isdir("/proc/self"):
        return False
    return _get_pid_namespace(start) != _ROOT_PID_NAMESPACE


def find_agent_ancestors(
    names: "dict[str, tuple[str, ...]]", pid: "int | None" = None, pids: "dict[int, str] | None" = None
) -> "tuple[list[tuple[str, int, bool]], bool]":
    """([(agent id, pid, sandbox)], complete): each ancestor titled one of `names`
    ({agent id: the names its process goes by}), else whose pid `pids` names
    ({pid: agent id}, the pid an agent exports: `CLAUDE_PID`), nearest first, and
    whether the walk read every process up to the machine's pid 1. `sandbox`: the
    namespace's pid 1 under a helper's name (`<name>-…`), as a sandboxed Codex
    shell sees only `codex-linux-sandbox` above it. In a child pid namespace (this
    process's or the walk's start process's, `_get_walk_start`) no pid is matched and
    the walk is never complete.
    ([], False) when unreadable. Never raises."""
    found = []
    try:
        nested = _is_walk_in_child_pid_namespace(pid)
        pids = {} if nested else (pids or {})
        chain = _ancestors(pid)
        for ancestor, _start, title in chain:
            helper = os.path.basename(title) if ancestor == 1 else ""
            named = next((agent for agent, wanted in names.items()
                          if any(_titled(title, name) for name in wanted)), None)
            if named is not None:
                found.append((named, ancestor, False))
            elif ancestor in pids:
                found.append((pids[ancestor], ancestor, False))
            else:
                helper_of = next((agent for agent, wanted in names.items()
                                  if any(helper.startswith(name + "-") for name in wanted)), None)
                if helper_of is not None:
                    found.append((helper_of, ancestor, True))
        return found, not nested and bool(chain) and chain[-1][0] == 1
    except Exception:  # noqa: BLE001 -- attribution must never break a command
        return [], False


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


