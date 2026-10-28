"""The uninstall's finisher: deletes the CLI itself, which `probe uninstall` cannot do from inside it.

FROZEN. Digest-pinned by `agent/tests/test_uninstall_finisher.py`: a copy of it
is what finishes an uninstall the CLI can no longer run (the env it ran from is
gone), so a change to it is deliberate. To change it, raise FINISHER_VERSION
and re-pin the digest (the test says how).

`probe uninstall` (plan clean-uninstall-reinstall, U-T9) does everything it can
in its own code, phase by phase, under the uninstall barrier and the install
lock. What is left is the code it runs from: the CLI's env generations, the
`probe*` shims uv made for them, and the `probe-versions/` bookkeeping. At phase
"finishing" it copies this file to `S/uninstall/finisher.py` (S =
`~/.local/state/probe`, never moved by XDG) and becomes it (`os.execv`: same
pid, same terminal, the install lock's fd inherited through
PROBE_INSTALL_LOCK_FD), run by the base interpreter the env was made from,
never the env being deleted:

    <base python> -I -S S/uninstall/finisher.py --plan S/uninstall/plan.json [--json]

It deletes only what the plan names, and only while it is still what the plan
saw (generation-bound): a file or a link whose inode and mtime still match, a
folder whose inode still matches (a folder's own mtime moves with whatever is
written inside it) and whose `witness`, when the plan names one (an env's
`pyvenv.cfg`: a folder made again can get its old inode back), is still the
same file or gone. Anything else is another install's now, and is kept. Entries marked `empty_only` are removed
only once empty. Paths are never followed through a symlink. Then, last,
`S/uninstall/` itself (the barrier with it), and S when that left it empty
(never `~/.local/state` or anything above it).

    exit 0   done: one summary line
    exit 1   partial: what is left, and the command that finishes it (this
             file and the plan stay, so it can be run again: it resumes from
             whatever is still there)
    exit 2   usage, or a plan it cannot read

With `--json` it ends the event stream the CLI began (`probe.core.events`):
its own `step` (`uninstall_finish`), then the `result` and `done` events the
CLI left in `S/uninstall/tail.json`, completed with its outcome. On exit 1 the
`result` carries the CLI's `reason` shape: `{"code": "partial", "resumed",
"resume": <the command that finishes it>, "phase": "finishing"}`, or `{"code":
"busy", "resumed"}` when another install held the lock. Its human line goes
to stderr there, as every run's text does.

Stdlib only, imports nothing of `probe`, runs with `-I -S` on any Python >= 3.8.
"""

from __future__ import annotations

import json
import os
import shutil
import stat
import sys
import time

FINISHER_VERSION = 1
PLAN_VERSION = 1
#: The install lock's fd, handed across the exec (`probe._shared.handoff.LOCK_FD_ENV`).
LOCK_FD_ENV = "PROBE_INSTALL_LOCK_FD"
#: What the CLI leaves for `--json`: the run's steps and result rows so far.
TAIL_NAME = "tail.json"
STEP_NAME = "uninstall_finish"
#: Windows: a file of the env the CLI ran from stays open a moment after the exec.
BUSY_RETRY_S = 5.0
#: How long a resume run (no inherited lock) waits for the install lock.
LOCK_WAIT_S = 30.0

KIND_FILE = "file"
KIND_LINK = "link"
KIND_DIR = "dir"

GONE = "gone"
REMOVED = "removed"
CHANGED = "changed"
FAILED = "failed"
KEPT = "kept"


def _say(text: str, *, json_mode: bool) -> None:
    stream = sys.stderr if json_mode else sys.stdout
    try:
        stream.write(text + "\n")
        stream.flush()
    except (OSError, ValueError):
        pass


def _sane(path: str) -> bool:
    """Never `/`, a top-level folder, HOME, or an ancestor of HOME."""
    if not isinstance(path, str) or not os.path.isabs(path):
        return False
    norm = os.path.normpath(path)
    parts = [p for p in norm.replace("\\", "/").split("/") if p]
    if len(parts) < 2:
        return False
    home = os.path.normpath(os.path.expanduser("~"))
    if norm == home or home.startswith(norm.rstrip(os.sep) + os.sep):
        return False
    return True


def _matches(entry: dict, st: os.stat_result) -> bool:
    """Is what is at the path still what the plan saw?"""
    kind = entry.get("kind")
    if kind == KIND_LINK and not stat.S_ISLNK(st.st_mode):
        return False
    if kind == KIND_FILE and not stat.S_ISREG(st.st_mode):
        return False
    if kind == KIND_DIR and not stat.S_ISDIR(st.st_mode):
        return False
    inode = entry.get("inode")
    if isinstance(inode, int) and not isinstance(inode, bool) and inode != st.st_ino:
        return False
    if kind in (KIND_FILE, KIND_LINK):
        mtime = entry.get("mtime")
        if isinstance(mtime, (int, float)) and not isinstance(mtime, bool) and mtime != st.st_mtime:
            return False
    if hasattr(os, "getuid") and st.st_uid != os.getuid():
        return False
    return kind != KIND_DIR or _witness_matches(entry.get("witness"))


def _witness_matches(witness: object) -> bool:
    """A folder's witness: a file made once with it (an env's `pyvenv.cfg`),
    since a folder made again may get the same inode back. Still there, it
    must be the same file; gone, the folder is the one the plan saw, part
    deleted (an earlier run of this) or broken."""
    if not isinstance(witness, dict) or not isinstance(witness.get("path"), str):
        return True
    try:
        st = os.lstat(witness["path"])
    except FileNotFoundError:
        return True
    except OSError:
        return False
    return st.st_ino == witness.get("inode") and st.st_mtime == witness.get("mtime")


def _retrying(action, path: str):
    deadline = time.monotonic() + (BUSY_RETRY_S if os.name == "nt" else 0.0)
    while True:
        try:
            return action(path)
        except PermissionError:
            if time.monotonic() >= deadline:
                raise
            time.sleep(0.2)


def _rmtree(path: str) -> None:
    def retry(function, failed, _info):
        # A read-only folder in the way: open it up and try again. Never
        # through a symlink (chmod follows one, to whatever it names).
        if not os.path.islink(failed):
            try:
                os.chmod(failed, stat.S_IWRITE | stat.S_IREAD | stat.S_IEXEC)
            except OSError:
                pass
        function(failed)

    if sys.version_info >= (3, 12):
        shutil.rmtree(path, onexc=retry)
    else:
        shutil.rmtree(path, onerror=retry)


def remove(entry: dict) -> str:
    """Delete one plan entry if it is still the plan's. Returns GONE (nothing
    there), REMOVED, CHANGED (another install's now: kept), KEPT (an
    `empty_only` folder that is not empty) or FAILED."""
    path = entry.get("path")
    if entry.get("owner", "probe") != "probe" or not _sane(path):
        return CHANGED
    try:
        st = os.lstat(path)
    except FileNotFoundError:
        return GONE
    except OSError:
        return FAILED
    if not _matches(entry, st):
        return CHANGED
    try:
        if stat.S_ISDIR(st.st_mode):
            if entry.get("empty_only"):
                try:
                    _retrying(os.rmdir, path)
                except OSError:
                    return KEPT if os.path.isdir(path) and os.listdir(path) else FAILED
            else:
                _retrying(_rmtree, path)
        else:
            _retrying(os.unlink, path)
    except FileNotFoundError:
        return GONE
    except OSError:
        return FAILED
    return REMOVED


def _depth(entry: dict) -> int:
    return len(os.path.normpath(str(entry.get("path") or "")).split(os.sep))


def ordered(entries: list) -> list:
    """Files and links first (the shims before the env they point into), then
    folders deepest first, `empty_only` folders last of all."""
    items = [e for e in entries if isinstance(e, dict) and e.get("kind") in (KIND_FILE, KIND_LINK, KIND_DIR)]
    files = [e for e in items if e.get("kind") != KIND_DIR]
    dirs = sorted((e for e in items if e.get("kind") == KIND_DIR and not e.get("empty_only")), key=_depth, reverse=True)
    empties = sorted((e for e in items if e.get("kind") == KIND_DIR and e.get("empty_only")), key=_depth, reverse=True)
    return files + dirs + empties


def finishing(entries: list) -> list:
    """The finisher's entries: `stage` "finish" (the CLI's own `state` phase
    removes the rest; an entry without a stage is the finisher's)."""
    return [e for e in entries if isinstance(e, dict) and e.get("stage", "finish") == "finish"]


def _lock(plan: dict):
    """Hold the install lock: inherited from the CLI, else taken here (a resume
    run by hand), waiting up to LOCK_WAIT_S. Returns (fd or None, busy)."""
    raw = os.environ.get(LOCK_FD_ENV, "")
    if raw.isdigit():
        return int(raw), False
    path = plan.get("install_lock")
    if not isinstance(path, str) or not os.path.isfile(path):
        return None, False
    try:
        import fcntl
    except ImportError:
        return None, False
    try:
        fd = os.open(path, os.O_RDWR)
    except OSError:
        return None, False
    deadline = time.monotonic() + LOCK_WAIT_S
    while True:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return fd, False
        except BlockingIOError:
            if time.monotonic() >= deadline:
                os.close(fd)
                return None, True
            time.sleep(0.5)
        except OSError:
            return fd, False  # a filesystem without locks: go on, as every install does


def _read_json(path: str):
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, ValueError):
        return None


def _reason(tail: dict, code: str, resume: str = "") -> dict:
    """The `result` event's `reason` for an exit 1 (`probe.cli.uninstall.reason_record`'s shape)."""
    out = {"code": code, "resumed": bool(tail.get("resumed"))}
    if code == "partial":
        out.update(resume=resume, phase="finishing")
    return out


def _events(tail: dict, *, ok: bool, message: str, exit_code: int, reason: dict | None = None) -> list:
    """The `step`, `result` and `done` events that end the CLI's stream."""
    record = {"name": STEP_NAME, "status": "done" if ok else "failed", "message": message, "agent": None}
    steps = [s for s in (tail.get("steps") or []) if isinstance(s, dict) and s.get("name") != STEP_NAME]
    steps.append(record)
    out = [{"v": 1, "event": "step", **record}]
    unfinished = any(s.get("status") in ("failed", "skipped") for s in steps)
    rows = [r for r in (tail.get("rows") or []) if isinstance(r, dict)]
    rows_ok = all(r.get("ok") for r in rows)
    incomplete = bool(tail.get("incomplete"))
    if tail.get("action"):
        result = {"v": 1, "event": "result", "action": tail["action"], "agents": rows,
                  "complete": rows_ok and not (incomplete or unfinished)}
        if reason is not None:
            result["reason"] = reason
        out.append(result)
    if exit_code != 0:
        out.append({"v": 1, "event": "error", "code": "failed", "message": message})
    out.append({"v": 1, "event": "done", "ok": exit_code == 0,
                "complete": exit_code == 0 and rows_ok and not (incomplete or unfinished),
                "exit_code": exit_code, "steps": steps})
    return out


def _emit(events: list) -> None:
    for event in events:
        try:
            sys.stdout.write(json.dumps(event) + "\n")
            sys.stdout.flush()
        except (OSError, ValueError):
            return


def _arg(args: list, name: str):
    for index, token in enumerate(args):
        if token == name and index + 1 < len(args):
            return args[index + 1]
        if token.startswith(name + "="):
            return token.split("=", 1)[1]
    return None


def resume_command(plan_path: str) -> str:
    here = os.path.join(os.path.dirname(os.path.abspath(plan_path)), "finisher.py")
    return f"python3 {here} --plan {plan_path}"


def run(plan_path: str, *, json_mode: bool = False) -> int:
    plan = _read_json(plan_path)
    if not isinstance(plan, dict) or plan.get("v") != PLAN_VERSION or not isinstance(plan.get("paths"), list):
        _say(f"probe uninstall: cannot read the plan {plan_path}; nothing was removed by the finisher.",
             json_mode=json_mode)
        return 2
    folder = os.path.dirname(os.path.abspath(plan_path))
    tail = _read_json(os.path.join(folder, TAIL_NAME)) if json_mode else None
    _fd, busy = _lock(plan)
    if busy:
        message = ("another install of Probe holds the install lock; nothing was removed. "
                   f"Run this again in a minute: {resume_command(plan_path)}")
        _say(f"probe uninstall: {message}", json_mode=json_mode)
        if json_mode:
            _emit(_events(tail or {}, ok=False, message=message, exit_code=1, reason=_reason(tail or {}, "busy")))
        return 1
    removed, kept, left = 0, [], []
    for entry in ordered(finishing(plan["paths"])):
        outcome = remove(entry)
        if outcome == REMOVED:
            removed += 1
        elif outcome == CHANGED:
            kept.append(entry.get("path"))
        elif outcome == FAILED:
            left.append(entry.get("path"))
    if left:
        shown = ", ".join(str(p) for p in left[:5]) + (f" and {len(left) - 5} more" if len(left) > 5 else "")
        message = f"Probe is partly uninstalled. Still here: {shown}. Finish with: {resume_command(plan_path)}"
        _say(f"probe uninstall: {message}", json_mode=json_mode)
        if json_mode:
            _emit(_events(tail or {}, ok=False, message=message, exit_code=1,
                          reason=_reason(tail or {}, "partial", resume_command(plan_path))))
        return 1
    # Last: the uninstall's own folder (the barrier, this plan, this copy),
    # then the state folder when nothing else of Probe's is left in it.
    try:
        _rmtree(folder)
    except FileNotFoundError:
        pass
    except OSError as exc:
        message = f"Probe is uninstalled, but its folder {folder} could not be removed ({exc}): delete it by hand."
        _say(f"probe uninstall: {message}", json_mode=json_mode)
        if json_mode:
            _emit(_events(tail or {}, ok=False, message=message, exit_code=1,
                          reason=_reason(tail or {}, "partial", f"rm -rf {folder}")))
        return 1
    try:
        os.rmdir(os.path.dirname(folder))  # `~/.local/state/probe`, only when empty; never the folders above it
    except OSError:
        pass
    note = f" Kept {len(kept)} item(s) another install made since." if kept else ""
    message = f"Probe is uninstalled from this computer ({removed} item(s) removed by the finisher).{note}"
    _say(message, json_mode=json_mode)
    if json_mode:
        _emit(_events(tail or {}, ok=True, message=message, exit_code=0))
    return 0


def main(argv: list | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if "--version" in args:
        print(FINISHER_VERSION)
        return 0
    plan_path = _arg(args, "--plan")
    if not plan_path:
        _say("usage: finisher.py --plan <S>/uninstall/plan.json [--json]", json_mode=False)
        return 2
    return run(os.path.abspath(plan_path), json_mode="--json" in args)


if __name__ == "__main__":
    sys.exit(main())
