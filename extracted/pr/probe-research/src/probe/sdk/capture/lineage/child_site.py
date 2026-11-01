"""give `probe exec`'s child a stdlib read hook: the child-site source, sitecustomize chaining, handing rules to the launcher."""

from __future__ import annotations
import functools
import json
import os
import sys
from pathlib import Path
from typing import Any
from ...recording_rules import ignore as _ignore
from ....foundation.safe_warn import safe_warn as _diagnostics
from probe.sdk.capture.lineage.exclusions import (
    _CACHE_ENVS,
    _CODE_SUFFIXES,
    _CREDENTIAL_PARTS,
    _ROOT_PREFIXES,
    _SYSTEM_ALLOWED,
    _SYSTEM_PREFIXES,
    _TOOL_CACHE_PARTS,
    _WRITE_ONLY_PARTS,
    _ignored,
)
from probe.sdk.capture.lineage.lineage import (
    BIND_CHECK_S,
    BIND_ENV,
    CHILD_DIR_ENV,
    OUTPUTS_ENV,
    OWNER_CHECK_S,
    OWNER_PID_ENV,
    READS_ENV,
    _PROBE_FRAME_DEPTH,
    _client_url,
    _env_on,
    _token_id,
    _without_probe_sites,
    enabled,
)
from probe.sdk.capture.lineage.spool.spool import (
    MAX_PATHS,
    _host,
    _mark_live,
    _write_owner,
    internal,
    run_dir,
    run_folder,
)
#: ``PROBE_CAPTURE_WRITES=0`` turns off write recording alone.
WRITES_ENV = "PROBE_CAPTURE_WRITES"


# -- probe exec: the child's hook ---------------------------------------------


def _readers_source() -> str:
    """`c_readers`' source, for the child hook (which cannot import Probe);
    empty when it cannot be read (the child then has no wrappers)."""
    try:
        return (Path(__file__).parent / "c_readers.py").read_text(encoding="utf-8")
    except OSError:
        return ""


#: The ``sitecustomize.py`` ``probe exec`` puts first on a Python child's path.
#: Stdlib only (the child's environment may not have Probe installed), no
#: hashing (the launcher hashes), and it chains to any sitecustomize the
#: environment already had -- never to another Probe hook, so a nested
#: ``probe exec`` installs one hook, not one per level. Its state is published
#: as ``sys._probe_reads_state`` so ``probe.init(capture_reads=False)`` in the
#: child can switch it off (``capture_outputs=False``: its writes), and
#: ``probe.init(ignore=[...])`` can give it a ``skip`` test
#: (:func:`hand_to_launcher`). It notes writes (and renames of them) exactly
#: as the in-process hook does. The exclusion lists are this module's, filled
#: in below, so the two recorders cannot drift.
CHILD_SITE_CODE = r"""
import os, sys, json, socket, threading, time, uuid
from datetime import datetime, timezone
try:
    import fcntl
except ImportError:
    fcntl = None

def _probe_site_dir(p):
    p = os.path.abspath(p or ".")
    return (p.endswith(os.sep + "site")
            and (os.sep + "probe" + os.sep + "reads" + os.sep) in p)

def _probe_run_of(spool_dir):
    # The run a spool folder is for: its name, unescaped (`inputs.run_folder`
    # escapes what a folder name cannot carry: `local:<key>` is `local%3A<key>`).
    name = os.path.basename(os.path.normpath(spool_dir))
    if "%" in name:
        from urllib.parse import unquote
        name = unquote(name)
    return name

def _probe_reads_install():
    spool_dir = os.environ.get("PROBE_READS_DIR")
    if not spool_dir or not hasattr(sys, "addaudithook"):
        return
    owner = os.environ.get("PROBE_READS_OWNER_PID") or ""
    if owner == str(os.getpid()):
        return  # the process that bound its workers (F5) records itself
    def env_off(name):
        return (os.environ.get(name) or "1").strip().lower() in ("0", "false", "off", "no")
    if env_off("PROBE_CAPTURE_READS"):
        return
    if getattr(sys, "_probe_reads_state", None) is not None:
        return
    skip_prefixes = set()
    for p in (sys.prefix, sys.base_prefix, sys.exec_prefix):
        if p and p not in __ROOTS__:
            skip_prefixes.add(os.path.abspath(p) + os.sep)
    try:
        import site, sysconfig
        libs = [sysconfig.get_paths().get(n) for n in ("stdlib", "platstdlib", "purelib", "platlib")]
        for p in list(site.getsitepackages()) + [site.getusersitepackages()] + libs:
            if p:
                skip_prefixes.add(os.path.abspath(p) + os.sep)
    except Exception:
        pass
    skip_prefixes.add(os.path.abspath(spool_dir) + os.sep)
    # Probe's own folders: its state and the outbox.
    state_home = os.environ.get("XDG_STATE_HOME") or os.path.join(os.path.expanduser("~"), ".local", "state")
    for p in (os.path.join(state_home, "probe"), os.environ.get("PROBE_OUTBOX_DIR")):
        if p:
            skip_prefixes.add(os.path.abspath(p) + os.sep)
    skip_prefixes = tuple(skip_prefixes)
    write_skip = tuple(os.path.abspath(os.environ[n]) + os.sep for n in __CACHE_ENVS__ if os.environ.get(n))
    write_parts = __WRITE_PARTS__
    system = __SYSTEM__
    allowed = __ALLOWED__
    parts = __PARTS__
    code = __CODE__
    max_paths = __MAX_PATHS__
    depth = __DEPTH__
    host = "".join(c if c.isalnum() or c in "-_" else "_" for c in (socket.gethostname() or "host"))
    wbits = os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND
    local = threading.local()
    bind_check = __BIND_CHECK__
    owner_check = __OWNER_CHECK__
    state = {"pid": None, "fh": None, "seen": {}, "count": 0, "off": False,
             "writes_off": env_off("PROBE_CAPTURE_WRITES") or env_off("PROBE_CAPTURE_OUTPUTS"),
             "written": {}, "wcount": 0,
             # The run this process spools into, and whose close takes the spool.
             "dir": spool_dir, "run": _probe_run_of(spool_dir),
             "owner": int(owner) if owner.isdigit() else None,
             # A worker bound through its owner's binding file (F5) follows it.
             "bind": os.environ.get("PROBE_READS_BIND"), "bind_next": 0.0, "bind_sig": None,
             "bind_writes": True}
    sys._probe_reads_state = state

    def probe_calling(frame):
        for _ in range(depth):
            if frame is None:
                return False
            name = frame.f_globals.get("__name__", "")
            if (name == "probe" or name.startswith("probe.")) and name != "probe.sdk.capture.lineage.c_readers":
                return True
            frame = frame.f_back
        return False

    def spool():
        pid = os.getpid()
        if state["pid"] != pid or state["fh"] is None:
            state["fh"] = open(os.path.join(state["dir"], "%s.%d.jsonl" % (host, pid)), "a",
                               buffering=1, encoding="utf-8")
            state["pid"] = pid
            # At every open: the run what follows is bound to, whose close
            # takes it, and whether that is a binding owner this one follows.
            state["fh"].write(json.dumps({"run": state["run"], "owner": state["owner"],
                                          "follows": bool(state["bind"])}) + "\n")
        return state["fh"]

    def owner_alive():
        # The owner holds its binding's lock exclusively while it lives: a
        # shared lock on it can be had only once it ended (a crash too).
        path = state["bind"][:-len(".json")] + ".lock"
        if fcntl is None:
            try:
                os.kill(state["owner"], 0)
            except ProcessLookupError:
                return False
            except Exception:
                return True
            return True
        try:
            fd = os.open(path, os.O_RDONLY)
        except OSError:
            return False
        try:
            try:
                fcntl.flock(fd, fcntl.LOCK_SH | fcntl.LOCK_NB)
            except BlockingIOError:
                return True
            except OSError:
                return True
            fcntl.flock(fd, fcntl.LOCK_UN)
            return False
        finally:
            os.close(fd)

    def follow():
        # The owner's binding file, looked at most every `bind_check`: gone,
        # nothing more is recorded; another run, its folder is spooled into;
        # its owner dead (its lock free), nothing more, for good. True while
        # bound to a run. (Only for a worker bound through one.)
        path = state["bind"]
        if not path:
            return True
        now = time.monotonic()
        if now < state["bind_next"] or state.get("bind_dead"):
            return state["run"] is not None
        state["bind_next"] = now + bind_check
        try:
            st = os.stat(path)
            sig = (st.st_ino, st.st_mtime_ns, st.st_size)
        except OSError:
            sig = None
        alive = True
        if sig is not None and now >= state.get("alive_next", 0.0):
            state["alive_next"] = now + owner_check
            alive = owner_alive()
        if not alive:
            state["bind_dead"] = True
            sig = None
        elif sig == state["bind_sig"]:
            return state["run"] is not None
        state["bind_sig"] = sig
        run = where = None
        writes = True
        if sig is not None:
            try:
                with open(path, encoding="utf-8") as fh:
                    record = json.load(fh)
                run, where, writes = record.get("run"), record.get("dir"), record.get("writes", True)
            except Exception:
                run = None
        if not (isinstance(run, str) and isinstance(where, str)):
            run = where = None
        if run != state["run"]:
            if state["fh"] is not None:
                try:
                    state["fh"].close()
                except Exception:
                    pass
            state.update(fh=None, pid=None, run=run, dir=where, seen={}, count=0, capped=False,
                         written={}, wcount=0, wcapped=False)
        state["bind_writes"] = bool(writes)
        return run is not None

    def as_path(p):
        if isinstance(p, bytes):
            return os.fsdecode(p)
        if p is not None and not isinstance(p, str):
            p = os.fspath(p)
            if isinstance(p, bytes):
                return os.fsdecode(p)
        return p if isinstance(p, str) else None

    def never(path):
        return (path.endswith(code) or path.startswith(skip_prefixes)
                or (path.startswith(system) and not path.startswith(allowed))
                or any(part in path for part in parts))

    real_dirs = {}

    def resolved(path):
        # realpath, with the folder's resolution cached while the folder is
        # the same entry (a link retargeted on the way is another one).
        import stat as _stat
        head, tail = os.path.split(path)
        try:
            st = os.lstat(head)
        except OSError:
            return os.path.realpath(path)
        link = _stat.S_ISLNK(st.st_mode)
        key = (st.st_dev, st.st_ino, link, st.st_ctime_ns if link else 0)
        cached = real_dirs.get(head)
        if cached is not None and cached[1] == key:
            real = cached[0]
        else:
            real = os.path.realpath(head)
            if len(real_dirs) >= 4096:
                real_dirs.clear()
            real_dirs[head] = (real, key)
        candidate = os.path.join(real, tail) if tail else real
        return os.path.realpath(candidate) if os.path.islink(candidate) else candidate

    def never_written(path):
        def no(p):
            return (never(p) or p.startswith(write_skip)
                    or any(part in p for part in write_parts))
        if no(path):
            return True
        real = resolved(path)
        return real != path and no(real)

    def before(path):
        try:
            st = os.stat(path)
        except OSError:
            return None
        import stat as _stat
        if not _stat.S_ISREG(st.st_mode):
            return None
        return [st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns]

    def note_write(path, first):
        if path in state["written"]:
            return
        if state["wcount"] >= max_paths:
            if not state.get("wcapped"):
                state["wcapped"] = True
                spool().write(json.dumps({"wtruncated": True}) + "\n")
            return
        state["written"][path] = first
        state["wcount"] += 1
        spool().write(json.dumps({"w": path, "t": first[0], "n": first[1],
                                  "o": uuid.uuid4().hex, "b": before(path)}) + "\n")

    def fresh_pid():
        if state.get("for_pid") != os.getpid():
            # A forked worker records its own reads and writes, from zero, in
            # its own spool.
            state.update(seen={}, count=0, capped=False, written={}, wcount=0, wcapped=False,
                         for_pid=os.getpid())

    def cut():
        if not state.get("capped") and state["fh"] is not None:
            state["capped"] = True
            state["fh"].write(json.dumps({"truncated": True}) + "\n")

    def note(path, writing, frame):
        # One open of `path` -- by `open`, or by a wrapped C reader -- made by
        # the code at `frame`.
        if state["off"] or getattr(local, "busy", False):
            return
        try:
            local.busy = True
            fresh_pid()
            if not follow():
                return
            if writing and (state["writes_off"] or not state["bind_writes"]):
                return
            if not writing and state["count"] >= max_paths:
                cut()
                return
            path = as_path(path)
            if path is None:
                return
            path = os.path.abspath(path)
            if writing and path in state["written"]:
                return
            if writing and state["wcount"] >= max_paths:
                note_write(path, None)  # past the cap: says so once, judges nothing
                return
            if never_written(path) if writing else never(path):
                return
            skip = state.get("skip")
            if skip is not None and skip(path):
                return
            if probe_calling(frame):
                return
            if writing:
                note_write(path, (datetime.now(timezone.utc).isoformat(), time.time_ns()))
                return
            st = os.stat(path)
            import stat as _stat
            if not _stat.S_ISREG(st.st_mode):
                return
            ident = (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns)
            if state["seen"].get(path) == ident:
                return
            state["seen"][path] = ident
            state["count"] += 1
            spool().write(json.dumps({
                "p": path, "d": st.st_dev, "i": st.st_ino, "s": st.st_size,
                "m": st.st_mtime_ns, "c": st.st_ctime_ns,
                "t": datetime.now(timezone.utc).isoformat()}) + "\n")
        except Exception:
            pass
        finally:
            local.busy = False

    def hook(event, args):
        if (event != "open" and event != "os.rename") or state["off"] or getattr(local, "busy", False):
            return
        fresh_pid()
        if event == "os.rename":
            if state["writes_off"]:
                return
            try:
                local.busy = True
                if not follow() or not state["bind_writes"]:
                    return
                if any(fd not in (None, -1) for fd in args[2:4]):
                    return
                src, dst = as_path(args[0]), as_path(args[1])
                if src is None or dst is None:
                    return
                first = state["written"].get(os.path.abspath(src))
                if first is None:
                    return
                dst = os.path.abspath(dst)
                skip = state.get("skip")
                if state["wcount"] < max_paths and (
                        never_written(dst) or (skip is not None and skip(dst))):
                    return
                note_write(dst, first)
            except Exception:
                pass
            finally:
                local.busy = False
            return
        try:
            path, mode, flags = args
        except Exception:
            return
        if isinstance(mode, str) and mode:
            writing = any(c in mode for c in "wax+")
        elif isinstance(flags, int):
            writing = bool(flags & wbits)
        else:
            return
        try:
            frame = sys._getframe(1)
        except ValueError:  # no Python code on the stack: the main script's open
            frame = None
        note(path, writing, frame)

    sys.addaudithook(hook)

    # Readers that open files from C, and torch.save (`probe.sdk.capture.lineage.c_readers`,
    # the same source): patched as they are imported.
    def active():
        # Whether anything records now (a wrapper with a cost asks first).
        if state["off"] or getattr(local, "busy", False):
            return False
        try:
            local.busy = True
            return follow()
        except Exception:
            return False
        finally:
            local.busy = False

    readers = __READERS__
    if readers:
        try:
            space = {"__name__": "_probe_readers"}
            exec(compile(readers, "<probe readers>", "exec"), space)
            space["install"](lambda p, f: note(p, False, f), lambda p, f: note(p, True, f), cut, active)
        except Exception:
            pass

_probe_reads_install()

def _probe_chain_sitecustomize():
    try:
        import importlib.machinery, importlib.util
        rest = [p for p in sys.path if not _probe_site_dir(p)]
        spec = importlib.machinery.PathFinder.find_spec("sitecustomize", rest)
        if spec is None or spec.loader is None:
            return
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception:
        pass

_probe_chain_sitecustomize()
"""
for _name, _value in (
    ("__SYSTEM__", _SYSTEM_PREFIXES),
    ("__ALLOWED__", _SYSTEM_ALLOWED),
    ("__PARTS__", _TOOL_CACHE_PARTS + _CREDENTIAL_PARTS),
    ("__CODE__", _CODE_SUFFIXES),
    ("__MAX_PATHS__", MAX_PATHS),
    ("__DEPTH__", _PROBE_FRAME_DEPTH),
    ("__ROOTS__", _ROOT_PREFIXES),
    ("__CACHE_ENVS__", _CACHE_ENVS),
    ("__WRITE_PARTS__", _WRITE_ONLY_PARTS),
    ("__READERS__", _readers_source()),
    ("__BIND_CHECK__", BIND_CHECK_S),
    ("__OWNER_CHECK__", OWNER_CHECK_S),
):
    CHILD_SITE_CODE = CHILD_SITE_CODE.replace(_name, repr(_value))
del _name, _value


def hand_to_launcher(run_id: str, rules: Any) -> bool:
    """Under ``probe exec``: give the launcher this process's ``.probeignore``
    ``rules`` (plan (n), #2045 review) -- a child's own ``ignore=`` patterns,
    which the launcher that collects the child's reads never saw.

    Two halves. The child's stdlib hook takes them as its ``skip`` test, so a
    read they exclude from now on is not even spooled (a forked worker
    inherits it). And one line in this process's spool carries the rules, so
    the launcher's :func:`collect` -- or a recovery's -- also drops what was
    spooled before ``probe.init()`` ran, or by a spawned worker's hook. The
    spool is the channel that already runs from child to launcher; nothing
    else is. Returns whether the rules were handed over; never raises."""
    try:
        spool_dir = os.environ.get(CHILD_DIR_ENV)
        if rules is None or not spool_dir or os.path.basename(os.path.normpath(spool_dir)) != run_folder(run_id):
            return False
        record = _ignore.to_record(rules)
        if record is None:
            return False
        state = getattr(sys, "_probe_reads_state", None)
        if isinstance(state, dict):
            state["skip"] = functools.partial(_ignored, rules)
        with internal():
            with open(os.path.join(spool_dir, f"{_host()}.{os.getpid()}.jsonl"), "a", encoding="utf-8") as fh:
                fh.write(json.dumps({"ignore": record}) + "\n")
        return True
    except Exception:  # noqa: BLE001 -- filtering is never a reason to fail init
        return False


def _is_probe_site(path: str) -> bool:
    path = os.path.abspath(path or ".")
    return path.endswith(os.sep + "site") and (os.sep + "probe" + os.sep + "reads" + os.sep) in path


def prepare_child(
    run_id: str,
    env: dict[str, str],
    *,
    client: Any = None,
    base_url: str | None = None,
    ignore: Any = None,
    capture_outputs: bool | None = None,
) -> bool:
    """Give ``probe exec``'s child a read hook: a ``sitecustomize.py`` first on
    ``PYTHONPATH`` and the spool folder in ``PROBE_READS_DIR``. Harmless for a
    child that is not Python (it never reads either). Returns whether it was
    installed; the launcher then finalizes the reads after the child exits.
    Off when the launcher OR the child's own environment opts out. ``ignore``
    (the run's ``.probeignore`` rules) is recorded for a recovery: the child's
    hook spools every read, and the launcher may never collect them. The hook
    notes writes too unless ``capture_outputs=False`` (which the caller also
    puts in the child's environment) or either environment turns them off."""
    if not enabled(None) or not _env_on(env.get(READS_ENV)):
        return False
    try:
        directory = run_dir(run_id)
        site_dir = _write_site(run_id)
        if capture_outputs is False:
            env[WRITES_ENV] = "0"  # the child's hook reads its environment
        # What the child's hook will do: it reads only its environment.
        writes = _env_on(env.get(WRITES_ENV)) and _env_on(env.get(OUTPUTS_ENV))
        _write_owner(
            run_id,
            base_url=base_url or _client_url(client),
            token_id=_token_id(client),
            ignore=ignore,
            writes=writes,
        )
        _mark_live(run_id)
    except OSError as exc:
        _diagnostics.warn(f"probe: read capture for the child could not start: {exc}")
        return False
    # An outer `probe exec`'s hook folder is dropped: one hook per process.
    # Every other entry stays as given (an empty one is the working folder).
    env["PYTHONPATH"] = os.pathsep.join([str(site_dir), *_without_probe_sites(env.get("PYTHONPATH"))])
    env[CHILD_DIR_ENV] = str(directory)
    # A launcher whose own workers are bound (F5) runs this child as a plain
    # `probe exec` child: its launcher, not a binding, collects it.
    env.pop(OWNER_PID_ENV, None)
    env.pop(BIND_ENV, None)
    return True


def _write_site(run_id: str) -> Path:
    """The run's ``site`` folder holding the child hook's ``sitecustomize.py``."""
    site_dir = run_dir(run_id) / "site"
    with internal():
        site_dir.mkdir(parents=True, exist_ok=True)
        (site_dir / "sitecustomize.py").write_text(CHILD_SITE_CODE, encoding="utf-8")
    return site_dir
