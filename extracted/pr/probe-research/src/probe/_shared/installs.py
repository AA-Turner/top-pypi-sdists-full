"""Side-by-side installs of the CLI's uv tool environment, and the switch between them (plan D6, D5).

An update used to rebuild the one environment every `probe` process runs
from, under them: a process that imported a module after `uv tool upgrade`
read the new files with the old code (2026-10-12: a daemon worker crashed on
its own deleted `lib/python3.13`), and an update that failed halfway left a
half-installed Probe. So each version gets an environment of its own, and the
update is one rename:

    ~/.local/share/uv/tools/probe-research                 a symlink, switched in one rename
        -> ~/.local/share/uv/probe-versions/<v>/probe-research   one complete uv tool env per version
    ~/.local/share/uv/probe-versions/active.json           {"active", "previous", "switched_at"}

The tool path stays valid for everything that names it (`~/.local/bin/probe`,
`runtime.json` fallbacks, older plugin copies, the desktop app): it is the
active version. A process started through it runs on, pinned to its version,
because uv writes each environment's scripts with that environment's own
interpreter path, so the shebang resolves to `probe-versions/<v>/...`: a long
training run or a daemon worker keeps the version it started with, and
nothing is replaced under it. The previous version stays, for the automatic
switch back (D5, `probe.service.guard`).

The first switch on a machine moves the environment uv made (a real folder at
the tool path) into `probe-versions/<its version>/` first: it is the version
to switch back to. Only that first switch is not one rename (two, a moment
apart).

Where the side-by-side layout cannot be used (no uv tool env, the versions
folder on another filesystem, a pipx or pip install), callers update in place
as before.

Generations (plan clean-uninstall-reinstall R-T3): a version whose folder is
in use (the active env, the one to switch back to, or one a process runs from)
is never rebuilt in place. A rebuild of it goes in a folder of its own,
`probe-versions/<version>+g<N>/probe-research` (N >= 2), and is switched to
like any other version. The version is read from the env's dist-info, never
from a folder's name: `+gN` is no release, so the hand-off's stage 1 (v1, v2)
falls back to dist-info for it too. A first switch whose version folder exists
already moves uv's folder to the next generation as well (older releases made
`<version>-<unix time>`: a migration leftover, `leftover`).

Every install and switch here holds the one install lock
(`probe._shared.handoff.install_lock`, `<versions root>/install.lock`), as the
hand-off and the in-place updater do: re-entrant, so the new release a
hand-off exec'd switches under the lock it was handed (plan I8). None of them
runs while an uninstall's barrier is LIVE (`probe._shared.uninstall_barrier`).

Stdlib only: the Probe service imports this to switch back (plan S1).
"""

from __future__ import annotations

import contextlib
import errno
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

from . import handoff, uninstall_barrier

DIST = "probe-research"
VERSIONS_DIRNAME = "probe-versions"
ACTIVE_NAME = "active.json"
#: Versions kept beside the active one when pruning (the previous one always).
KEEP = 3
#: A version folder younger than this is never pruned (a run may have just started on it).
PRUNE_MIN_AGE_S = 24 * 3600
_VERSION = re.compile(r"^[0-9][0-9A-Za-z.+!_-]{0,63}$")
_UV_TIMEOUT_S = 15
#: How long an install or a switch waits for another live update's install lock.
LOCK_WAIT_S = handoff.LOCK_WAIT_S
#: A check killed by one of these could not finish (the OOM killer's SIGKILL, a
#: shutdown's SIGTERM): the machine's, UNKNOWN. Any other signal (SIGSEGV,
#: SIGBUS, SIGABRT, SIGILL) is the env's own crash: BROKEN.
UNKNOWN_SIGNALS = frozenset({int(getattr(signal, "SIGKILL", 9)), int(signal.SIGTERM)})
#: A check that could not be spawned for one of these is the machine's (no
#: process slot, no memory): UNKNOWN. Any other (ENOEXEC, EACCES on the env's
#: own interpreter) is the env's: BROKEN.
UNKNOWN_SPAWN_ERRNOS = frozenset({errno.EAGAIN, errno.ENOMEM})


def tool_dir() -> Path:
    """uv's tool folder: `UV_TOOL_DIR`, else `uv tool dir`, else the default."""
    override = os.environ.get("UV_TOOL_DIR")
    if override:
        return Path(override)
    uv = shutil.which("uv")
    if uv:
        try:
            out = subprocess.run(
                [uv, "tool", "dir"], capture_output=True, text=True, timeout=_UV_TIMEOUT_S, check=False
            )
            line = (out.stdout or "").strip().splitlines()
            if out.returncode == 0 and line and os.path.isabs(line[-1]):
                return Path(line[-1])
        except (OSError, subprocess.SubprocessError):
            pass
    base = os.environ.get("XDG_DATA_HOME") or str(Path.home() / ".local" / "share")
    return Path(base) / "uv" / "tools"


def tool_env(tools: Path | None = None) -> Path:
    """The tool path: `<uv tool dir>/probe-research`."""
    return (tools or tool_dir()) / DIST


def versions_root(tools: Path | None = None) -> Path:
    """`<uv tool dir>/../probe-versions`: beside uv's tools, on the same filesystem."""
    return (tools or tool_dir()).parent / VERSIONS_DIRNAME


def version_env(version: str, tools: Path | None = None) -> Path:
    if not _VERSION.match(version):
        raise ValueError(f"not a version: {version!r}")
    return versions_root(tools) / version / DIST


#: `<version>+g<N>`: a rebuild of `<version>` beside the folder in use. `-<digits>`:
#: an older release's migration leftover (`<version>-<unix time>`).
_FOLDER = re.compile(r"^(?P<version>.+?)(?:\+g(?P<generation>[0-9]{1,6}))?(?:-(?P<stamp>[0-9]{6,}))?$")


def folder_parts(name: str) -> tuple[str, int, bool]:
    """`(version, generation, leftover)` of a version folder's name:
    `0.3.1` -> ("0.3.1", 1, False), `0.3.1+g2` -> ("0.3.1", 2, False),
    `0.3.1-1730000000` -> ("0.3.1", 1, True). Only a NAME: the version an env
    holds is its dist-info's (`env_version`)."""
    found = _FOLDER.match(name)
    if not found:
        return name, 1, False
    generation = int(found.group("generation") or 1)
    return found.group("version"), max(generation, 1), found.group("stamp") is not None


def generation_env(version: str, generation: int, tools: Path | None = None) -> Path:
    """`probe-versions/<version>/probe-research` for generation 1, else
    `probe-versions/<version>+g<N>/probe-research`."""
    if generation <= 1:
        return version_env(version, tools)
    return version_env(f"{version}+g{int(generation)}", tools)


def _folders(tools: Path | None = None) -> list[Path]:
    try:
        return [p for p in versions_root(tools).iterdir() if p.is_dir() and not p.name.startswith(".")]
    except OSError:
        return []


def next_generation(version: str, tools: Path | None = None) -> int:
    """The generation a rebuild of `version` gets: one past every folder of it."""
    highest = 1
    for folder in _folders(tools):
        name, generation, _leftover = folder_parts(folder.name)
        if name == version:
            highest = max(highest, generation)
    return highest + 1


def envs_of(version: str, tools: Path | None = None) -> list[Path]:
    """Every generation's env of `version` that has an interpreter, newest
    generation first (leftovers last). Their dist-info decides what they hold."""
    found = []
    for folder in _folders(tools):
        name, generation, leftover = folder_parts(folder.name)
        env = folder / DIST
        if name == version and env_python(env).exists():
            found.append((not leftover, generation, env))
    return [env for *_key, env in sorted(found, key=lambda item: (item[0], item[1]), reverse=True)]


def refuse_while_uninstalling() -> None:
    """Raise `uninstall_barrier.UninstallRunning` (a RuntimeError) while an
    uninstall's barrier is LIVE: no install or switch starts under it."""
    uninstall_barrier.check()


def is_link(path: Path) -> bool:
    """A symlink, or on Windows a junction (how the tool path is switched there:
    a directory symlink needs Developer Mode or an administrator)."""
    if path.is_symlink():
        return True
    if os.name == "nt":
        is_junction = getattr(path, "is_junction", None)  # Python 3.12
        if is_junction is not None:
            return is_junction()
        try:
            os.readlink(path)
            return True
        except (OSError, ValueError):
            return False
    return False


def _make_link(target: Path, link: Path) -> None:
    if os.name == "nt":
        import _winapi

        _winapi.CreateJunction(str(target), str(link))
    else:
        os.symlink(target, link, target_is_directory=True)


def _drop_link(link: Path) -> None:
    """Remove the link itself, never what it names (rmdir on a junction)."""
    if os.name == "nt" and not link.is_symlink():
        os.rmdir(link)
    else:
        link.unlink()


def _swap_link(link: Path, env: Path) -> None:
    """Put `link` at `env`: one rename on POSIX. Windows cannot rename onto a
    folder (a junction is one), so the old link moves aside first, for the
    moment between two renames."""
    if os.name != "nt" or not (env.exists() or is_link(env)):
        os.replace(link, env)
        return
    aside = env.with_name(f".{env.name}.old-{os.getpid()}")
    os.rename(env, aside)
    try:
        os.rename(link, env)
    except OSError:
        os.rename(aside, env)
        raise
    with contextlib.suppress(OSError):
        _drop_link(aside)


def env_python(env: Path) -> Path:
    if os.name == "nt":
        return env / "Scripts" / "python.exe"
    return env / "bin" / "python"


def env_version(env: Path, *, timeout: float = 30.0) -> str | None:
    """The probe-research version installed in `env`, read by its own interpreter."""
    python = env_python(env)
    if not python.exists():
        return None
    try:
        out = subprocess.run(  # noqa: S603 -- the env's own interpreter, no shell
            [str(python), "-I", "-c", f"from importlib.metadata import version; print(version({DIST!r}))"],
            capture_output=True,
            text=True,
            stdin=subprocess.DEVNULL,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    text = (out.stdout or "").strip()
    return text if out.returncode == 0 and text else None


def same_filesystem(tools: Path | None = None) -> bool:
    """Can the tool path be switched by rename onto the versions folder?"""
    tools = tools or tool_dir()
    try:
        root = versions_root(tools)
        root.mkdir(parents=True, exist_ok=True)
        return os.stat(root).st_dev == os.stat(tools).st_dev
    except OSError:
        return False


def usable(tools: Path | None = None) -> bool:
    """Is the side-by-side layout usable here: a uv tool env (a folder or our
    symlink) at the tool path, and the versions folder on its filesystem?"""
    if os.name == "nt":
        # Not yet: the first switch moves the folder the running CLI (and the
        # service) run from, which Windows refuses while they run. Windows
        # updates in place, through the CLI's own updater, as before.
        return False
    tools = tools or tool_dir()
    env = tool_env(tools)
    return (is_link(env) or env.is_dir()) and same_filesystem(tools)


# -- the record ------------------------------------------------------------------


def _record_path(tools: Path | None = None) -> Path:
    return versions_root(tools) / ACTIVE_NAME


def record(tools: Path | None = None) -> dict:
    try:
        data = json.loads(_record_path(tools).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def _write_record(data: dict, tools: Path | None = None) -> None:
    target = _record_path(tools)
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_name(f"{target.name}.{os.getpid()}.tmp")
    try:
        with open(tmp, "w", encoding="utf-8") as handle:
            json.dump(data, handle)
        os.replace(tmp, target)
    finally:
        with contextlib.suppress(OSError):
            os.unlink(tmp)


def active(tools: Path | None = None) -> Path | None:
    """The version env the tool path names now, resolved; None when it is a
    plain folder (no switch yet) or missing."""
    env = tool_env(tools)
    if not is_link(env):
        return None
    try:
        return env.resolve(strict=True)
    except OSError:
        return None


# -- installing ------------------------------------------------------------------


#: What uv reads as true in a boolean variable (any case).
_UV_TRUE = frozenset({"1", "true", "yes", "on", "t", "y"})


def uv_offline(env: dict | None = None) -> bool:
    """Does uv run offline (`UV_OFFLINE` set to any value uv reads as true)?
    uv refuses every refresh then."""
    value = (env if env is not None else os.environ).get("UV_OFFLINE", "")
    return value.strip().lower() in _UV_TRUE


def install_command(spec: str, *, with_packages: tuple = (), python: str | None = None) -> list[str]:
    # A fresh read of the index for probe-research (uv's cache can predate the
    # release) -- unless uv is offline, which refuses any refresh outright.
    refresh = [] if uv_offline() else ["--refresh-package", DIST]
    command = ["uv", "tool", "install", *refresh, spec]
    for requirement in with_packages:
        command += ["--with", requirement]
    if python:
        command += ["--python", python]
    return command


def install(
    version: str,
    spec: str,
    *,
    with_packages: tuple = (),
    python: str | None = None,
    tools: Path | None = None,
    timeout: float = 300.0,
    run=subprocess.run,
    rebuild: bool = False,
) -> Path:
    """Install `spec` (`probe-research[...]==<version>`) as its own env,
    `probe-versions/<version>/probe-research`, beside the active one. A
    complete env of that version already there is reused, unless `rebuild`
    (it is broken: `health`). A folder in use (`protected`) is never removed
    for it: the install goes in the next generation's folder
    (`<version>+g<N>`). Returns the env; raises RuntimeError (with what uv
    said) when it does not end up holding `version`. Under the install lock
    (raises `handoff.LockBusy`, a RuntimeError, when another live update keeps
    it); never while an uninstall runs (`refuse_while_uninstalling`)."""
    tools = tools or tool_dir()
    refuse_while_uninstalling()
    with handoff.install_lock(versions_root(tools), wait_s=LOCK_WAIT_S):
        refuse_while_uninstalling()  # written while this waited for the lock
        return _install(version, spec, with_packages=with_packages, python=python, tools=tools,
                        timeout=timeout, run=run, rebuild=rebuild)


def protected(folder: Path, tools: Path | None = None, *, commands: list[str] | None = None) -> bool:
    """Must `folder` (a version folder) stay as it is: the active env's, the
    one to switch back to, the record's interrupted migration, or one a
    process runs from? Unknown reads as yes."""
    try:
        resolved = folder.resolve()
    except OSError:
        return True
    keep = set()
    for env in (active(tools), previous(tools)):
        if env is not None:
            with contextlib.suppress(OSError):
                keep.add(env.parent.resolve())
    moving = record(tools).get("migrating")
    if isinstance(moving, dict) and isinstance(moving.get("to"), str):
        with contextlib.suppress(OSError):
            keep.add(Path(moving["to"]).parent.resolve())
    return resolved in keep or _in_use(folder, commands)


def _target(version: str, tools: Path, rebuild: bool) -> Path:
    """Where `install` puts `version`: its own folder, unless that is in use
    and incomplete (or to be rebuilt): then the next generation's."""
    env = version_env(version, tools)
    if not env.parent.exists():
        return env
    if not rebuild and handoff.complete(env, version):
        return env
    if protected(env.parent, tools):
        return generation_env(version, next_generation(version, tools), tools)
    return env


def _install(version: str, spec: str, *, with_packages: tuple, python: str | None, tools: Path,
             timeout: float, run, rebuild: bool = False) -> Path:
    env = _target(version, tools, rebuild)
    if not rebuild and handoff.complete(env, version):
        return env
    holder = env.parent
    if holder.exists():
        shutil.rmtree(holder, ignore_errors=True)  # a half-finished earlier try, or a broken one not in use
    holder.mkdir(parents=True, exist_ok=True)
    child_env = {
        **os.environ,
        "UV_TOOL_DIR": str(holder),
        # Its scripts go nowhere anyone runs them from: `~/.local/bin/probe`
        # keeps naming the tool path, which the switch points here.
        "UV_TOOL_BIN_DIR": str(holder / ".bin"),
    }
    done = run(
        install_command(spec, with_packages=with_packages, python=python),
        env=child_env,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    # Only an install uv says worked (exit 0) and finished (`handoff.complete`:
    # its receipt, written last, is there) counts, as for the hand-off's own.
    if done.returncode == 0 and handoff.complete(env, version):
        return env
    got = env_version(env)
    if got is None and env_python(env).exists():
        got = env_version(env, timeout=120.0)  # a loaded machine, not a failed install
    if done.returncode == 0 and got == version and (env / RECEIPT).is_file():
        return env
    said = ((done.stderr or "") + (done.stdout or "")).strip()[-1500:]
    unfinished = "" if got is None or (env / RECEIPT).is_file() else " (no uv receipt: unfinished)"
    shutil.rmtree(holder, ignore_errors=True)
    raise RuntimeError(
        f"`uv tool install {spec}` exited {done.returncode} and left {got or 'nothing'}{unfinished}: {said}")


def selftest(env: Path, *, timeout: float = 60.0) -> str | None:
    """Does the env start? The service's start path (`-m probe.service
    --selftest`) and the CLI's import, each by the env's own interpreter.
    None when both work, else what failed (D5's check before a switch)."""
    return selftest_checked(env, timeout=timeout)[0]


def selftest_checked(env: Path, *, timeout: float = 60.0) -> tuple[str | None, bool]:
    """`selftest`, as `(what failed, broken)`. `broken` is False only when a
    check could not finish for the machine's sake: a timeout on a loaded
    machine, a kill by SIGKILL or SIGTERM (the OOM killer, a shutdown), a
    spawn refused with EAGAIN or ENOMEM. Anything else is the env's: an exit
    status > 0, a crash (SIGSEGV, SIGBUS, SIGABRT, SIGILL), an interpreter
    that cannot be executed (ENOEXEC, EACCES)."""
    python = str(env_python(env))
    checks = (
        ("the Probe service", [python, "-I", "-m", "probe.service", "--selftest"]),
        ("the probe CLI", [python, "-I", "-c", "import probe.cli.main"]),
    )
    for name, argv in checks:
        try:
            done = subprocess.run(  # noqa: S603 -- the env's own interpreter
                argv, capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=timeout, check=False
            )
        except subprocess.TimeoutExpired:
            return f"{name} did not answer within {timeout:g} s", False
        except OSError as exc:
            return f"{name} could not be checked: {exc}", exc.errno not in UNKNOWN_SPAWN_ERRNOS
        except subprocess.SubprocessError as exc:
            return f"{name} could not be checked: {exc}", True
        if done.returncode < 0:
            return f"{name} was killed by signal {-done.returncode}", -done.returncode not in UNKNOWN_SIGNALS
        if done.returncode != 0:
            tail = (done.stderr or "").strip().splitlines()[-1:] or [f"exit {done.returncode}"]
            return f"{name} would not start: {tail[0][:300]}", True
    return None, False


def health(env: Path, version: str | None = None, *, timeout: float = 60.0) -> str | None:
    """`check`'s finding alone: None when `env` works, else what is wrong (or
    what could not be checked), in one line."""
    return check(env, version, timeout=timeout)[0]


def check(env: Path, version: str | None = None, *, timeout: float = 60.0) -> tuple[str | None, bool]:
    """Is `env` a working CLI (plan R-T3)? A finished uv install (interpreter,
    receipt, the dist-info of `version` when given), whose update path imports
    (`probe.core.run`, `probe.core.adopt`: `handoff.starts`) and which starts
    (`selftest_checked`: the service's start path, the CLI's import).
    `(None, False)` when it is; else `(what is wrong, broken)`. `broken` for
    a definite failure; a check that could not finish for the machine's sake
    (a timeout, a kill by SIGKILL or SIGTERM, a spawn refused with EAGAIN or
    ENOMEM: `_machines`) is UNKNOWN: the env is kept, never rebuilt for it,
    as the hand-off keeps an env whose check could not run. A crash by any
    other signal, or an interpreter that cannot be executed, is BROKEN."""
    if not env_python(env).exists():
        return f"{env} has no interpreter", True
    if not (env / RECEIPT).is_file():
        return f"{env} is an unfinished install (no uv receipt)", True
    found = _dist_info_version(env)
    if found is None:
        return f"{env} holds no probe-research dist-info", True
    if version is not None and found != version:
        return f"{env} holds probe-research {found}, not {version}", True
    problem, broken = handoff.starts(env)
    if problem:
        # The frozen hand-off calls every check that could not finish UNKNOWN;
        # only the machine's reasons are (its own words, read back here).
        return f"its update path does not import: {problem}", broken or not _machines(problem)
    return selftest_checked(env, timeout=timeout)


def _machines(said: str) -> bool:
    """Was `handoff.starts`'s UNKNOWN the machine's: a timeout, a kill by
    SIGKILL or SIGTERM, a spawn refused with EAGAIN or ENOMEM? Its words are
    frozen with it (`tests/test_handoff_frozen.py`): "timed out after N s",
    "killed by signal N", "<OSError's type>: [Errno N] ..."."""
    if said.startswith("timed out after "):
        return True
    killed = re.fullmatch(r"killed by signal (\d+)", said)
    if killed:
        return int(killed.group(1)) in UNKNOWN_SIGNALS
    spawn = re.match(r"\w+: \[Errno (\d+)\]", said)
    return bool(spawn) and int(spawn.group(1)) in UNKNOWN_SPAWN_ERRNOS


def _dist_info_version(env: Path) -> str | None:
    """The probe-research version `env`'s dist-info folder names (no
    interpreter started), else its interpreter's answer."""
    found = []
    for site in [*env.glob("lib/python3*/site-packages"), *env.glob("Lib/site-packages")]:
        for info in site.glob("probe_research-*.dist-info"):
            found.append(info.name[len("probe_research-"): -len(".dist-info")])
    if found:
        return max(found, key=lambda v: handoff.release(v) or ())
    return env_version(env)


def discard(env: Path, tools: Path | None = None) -> None:
    """Delete a version env that will not be used: never the active one, the
    one to switch back to, nor one a process runs from (`protected`)."""
    holder = env.parent
    if active(tools) is not None and active(tools) == env.resolve():
        return
    if versions_root(tools) in holder.parents and protected(holder, tools):
        return
    shutil.rmtree(holder, ignore_errors=True)


#: A rejected version is skipped this long, then tried again (plan I1, A5).
REJECT_TTL_S = handoff.REJECT_TTL_S


def _mark(value: object) -> dict | None:
    """One `rejected` entry as `{"at", "reason"}`: today's shape, or an older
    bare timestamp. None for anything else."""
    if isinstance(value, dict):
        at = value.get("at")
        reason = value.get("reason")
    else:
        at, reason = value, ""
    if isinstance(at, bool) or not isinstance(at, (int, float)):
        return None
    return {"at": float(at), "reason": reason if isinstance(reason, str) else ""}


def rejected(tools: Path | None = None, *, now: float | None = None) -> dict:
    """`{version: {"at", "reason"}}`: versions switched back from on this
    machine (D5) less than REJECT_TTL_S ago. Skipped while they are; a newer
    release than a rejected one is never held off by it (only the newest
    release is ever the target)."""
    value = record(tools).get("rejected")
    if not isinstance(value, dict):
        return {}
    now = time.time() if now is None else now
    out = {}
    for version, raw in value.items():
        mark = _mark(raw)
        if mark is not None and now - mark["at"] < REJECT_TTL_S:
            out[version] = mark
    return out


def reject(version: str, reason: str, tools: Path | None = None) -> None:
    """Mark `version` rejected now; the entries past REJECT_TTL_S go."""
    data = record(tools)
    marks = rejected(tools)
    marks[version] = {"at": time.time(), "reason": reason[:500]}
    data["rejected"] = marks
    _write_record(data, tools)


def set_fields(tools: Path | None = None, **fields: object) -> None:
    """Set fields of the record (`active.json`); None takes one out."""
    data = record(tools)
    for name, value in fields.items():
        if value is None:
            data.pop(name, None)
        else:
            data[name] = value
    _write_record(data, tools)


def record_dropped_with(packages: list, tools: Path | None = None, *, python: str | None = None) -> None:
    """What the active env lacks of the install before it: the `--with`
    packages that would not install beside it (`dropped_with`) and the exact
    Python it ran on (`dropped_python`), for `probe doctor`'s re-add line and
    for the next install to try again first. Empty clears each."""
    set_fields(tools, dropped_with=[str(p) for p in packages][:20] or None, dropped_python=python or None)


def dropped_with(tools: Path | None = None) -> list[str]:
    value = record(tools).get("dropped_with")
    return [str(p) for p in value] if isinstance(value, list) else []


def dropped_python(tools: Path | None = None) -> str | None:
    value = record(tools).get("dropped_python")
    return value if isinstance(value, str) and value else None


# -- switching -------------------------------------------------------------------


def needs_migration(tools: Path | None = None) -> bool:
    """Is the tool path still the folder uv made (no switch has happened)?
    The first switch moves it, and every process started from it reads its
    files through that path, so it is made only on a quiet machine (the
    in-place update's own checks); every later switch is a link."""
    env = tool_env(tools)
    return env.is_dir() and not is_link(env)


def _migrate(tools: Path) -> Path | None:
    """The first switch: move the folder uv made at the tool path into
    `probe-versions/<its version>/` so it is a version to switch back to.
    Returns where it went, or None when there was nothing to move. Recorded
    first (`migrating`), so a switch cut short is put back (`recover`)."""
    env = tool_env(tools)
    if is_link(env) or not env.is_dir():
        return None
    version = env_version(env) or f"unknown-{int(time.time())}"
    dest = version_env(version, tools) if _VERSION.match(version) else versions_root(tools) / version / DIST
    if dest.exists() or dest.parent.exists():
        # That version's folder is there already (a `uv tool install` over the
        # link, or after `uv tool uninstall`, made uv's folder again): the next
        # generation's, never a name that reads as another version.
        dest = (generation_env(version, next_generation(version, tools), tools) if _VERSION.match(version)
                else versions_root(tools) / f"{version}-{int(time.time())}" / DIST)
    dest.parent.mkdir(parents=True, exist_ok=True)
    data = record(tools)
    data["migrating"] = {"from": str(env), "to": str(dest), "at": time.time()}
    _write_record(data, tools)
    os.rename(env, dest)
    return dest


RECEIPT = "uv-receipt.toml"
_INSTALL_PATH = re.compile(r'install-path\s*=\s*"([^"]+)"')


def _receipt_bins(env: Path) -> list[Path]:
    try:
        text = (env / RECEIPT).read_text(encoding="utf-8")
    except OSError:
        return []
    return [Path(m.group(1)).parent for m in _INSTALL_PATH.finditer(text)]


def bin_dir(tools: Path | None = None) -> Path:
    """Where `probe` is on PATH (`~/.local/bin`, as uv chose it for this
    machine): the record's, else the tool path's own receipt (the folder uv
    made), else uv's rule."""
    tools = tools or tool_dir()
    saved = record(tools).get("bin")
    if isinstance(saved, str) and saved:
        return Path(saved)
    versions = versions_root(tools)
    for found in _receipt_bins(tool_env(tools)):
        if versions not in found.parents:
            return found
    for name in ("UV_TOOL_BIN_DIR", "XDG_BIN_HOME"):
        if os.environ.get(name):
            return Path(os.environ[name])
    if os.environ.get("XDG_DATA_HOME"):
        return Path(os.environ["XDG_DATA_HOME"]).parent / "bin"
    return Path.home() / ".local" / "bin"


def fix_receipt(env: Path, bins: Path) -> bool:
    """A version env's uv receipt names its scripts where uv put them
    (`probe-versions/<v>/.bin`, which nothing runs). uv reads the receipt of
    whatever the tool path names, and a plain `uv tool install` (what
    `npx probe-research` runs on a stale CLI) then finds `~/.local/bin/probe`
    "not its own", deletes the tool path and fails. Point the receipt at the
    real scripts folder instead. True when it changed. Never raises."""
    path = env / RECEIPT
    try:
        text = path.read_text(encoding="utf-8")
        old = f'"{env.parent / ".bin"}/'
        if old not in text:
            return False
        tmp = path.with_name(f"{RECEIPT}.{os.getpid()}.tmp")
        tmp.write_text(text.replace(old, f'"{bins}/'), encoding="utf-8")
        os.replace(tmp, path)
        return True
    except OSError:
        return False


def recover(tools: Path | None = None) -> bool:
    """A first switch cut short between moving the folder and linking the
    tool path (a crash, a full disk): move the folder back. True when it did.
    Never raises."""
    tools = tools or tool_dir()
    try:
        data = record(tools)
        moving = data.get("migrating")
        if not isinstance(moving, dict):
            return False
        env, dest = Path(str(moving.get("from"))), Path(str(moving.get("to")))
        done = False
        if not env.exists() and not is_link(env) and dest.is_dir():
            os.rename(dest, env)
            done = True
        data.pop("migrating", None)
        _write_record(data, tools)
        return done
    except OSError:
        return False


def activate(target: Path, *, tools: Path | None = None) -> dict:
    """Point the tool path at `target` (a version env) in one rename. Returns
    the record: `{"active", "previous", "switched_at"}` (paths as strings).
    The first switch also moves the folder uv made (`_migrate`); a failure
    after that puts it back, so the CLI is never left without a tool path.
    Under the install lock (re-entrant: a hand-off's exec'd release holds it
    already); `handoff.LockBusy` (a RuntimeError) when another update keeps it;
    `uninstall_barrier.UninstallRunning` (a RuntimeError) while an uninstall
    runs: no switch, not even back (the guard's), starts under it."""
    tools = tools or tool_dir()
    refuse_while_uninstalling()
    with handoff.install_lock(versions_root(tools), wait_s=LOCK_WAIT_S):
        refuse_while_uninstalling()  # written while this waited for the lock
        return _activate(target, tools)


def _activate(target: Path, tools: Path) -> dict:
    env = tool_env(tools)
    if not env_python(target).exists():
        raise RuntimeError(f"{target} is not a complete environment")
    recover(tools)
    bins = bin_dir(tools)
    fix_receipt(target, bins)
    before = active(tools)
    # The link first: nothing has moved if it cannot be made.
    link = tools / f".{DIST}.switch-{os.getpid()}"
    with contextlib.suppress(FileNotFoundError, OSError):
        _drop_link(link)
    _make_link(target, link)
    try:
        migrated = _migrate(tools)
    except OSError:
        with contextlib.suppress(OSError):
            _drop_link(link)
        recover(tools)
        raise
    previous = before or migrated
    try:
        _swap_link(link, env)
    except OSError:
        with contextlib.suppress(OSError):
            _drop_link(link)
        recover(tools)
        raise
    data = record(tools)
    data.pop("migrating", None)
    data["bin"] = str(bins)
    data.update(
        {
            "active": str(target),
            "previous": str(previous) if previous is not None and not _same(Path(previous), target)
            else data.get("previous"),
            "switched_at": time.time(),
            # Where the tool path is, for a process running from a version env
            # that must not ask `uv tool dir` on every start.
            "tools": str(tools),
        }
    )
    _write_record(data, tools)
    return data


def _same(a: Path, b: Path) -> bool:
    try:
        return a.resolve() == b.resolve()
    except OSError:
        return a == b


def previous(tools: Path | None = None) -> Path | None:
    """The version to switch back to, if it is still complete."""
    prior = record(tools).get("previous")
    if not isinstance(prior, str):
        return None
    path = Path(prior)
    return path if env_python(path).exists() else None


def switch_back(tools: Path | None = None) -> dict | None:
    """Back to the previous version (D5). None when there is none to go to."""
    prior = previous(tools)
    if prior is None:
        return None
    return activate(prior, tools=tools)


# -- repairing the layout (plan clean-uninstall-reinstall R-T1, R-T2) -------------


class ToolPath:
    """What is at the tool path (`<uv tool dir>/probe-research`)."""

    #: Nothing: a fresh machine, or `uv tool uninstall` took the link away
    #: (it removes the link and the shims; the versions stay).
    MISSING = "missing"
    #: uv's own folder: no switch yet, or `uv tool install --force` (or a
    #: reinstall after `uv tool uninstall`) made it again over the layout.
    PLAIN = "plain"
    #: Our link, to an env with an interpreter.
    LINKED = "linked"
    #: Our link, to nothing usable (its env deleted).
    DANGLING = "dangling"
    #: A file, or something else that is not a folder.
    OTHER = "other"


def adopt_plain(tools: Path | None = None) -> Path | None:
    """The first switch to the env uv made itself (a reinstall by hand over the
    layout, or a machine that never switched): move it into the versions
    folder (`_migrate`: the next generation when its version's folder is
    taken) and link the tool path to it. The moved env, or None when the tool
    path is no plain folder. Under the install lock; a failure puts it back."""
    tools = tools or tool_dir()
    refuse_while_uninstalling()
    with handoff.install_lock(versions_root(tools), wait_s=LOCK_WAIT_S):
        if tool_state(tools) != ToolPath.PLAIN:
            return None
        env = tool_env(tools)
        moved = _migrate(tools)
        if moved is None:
            return None
        try:
            _make_link(moved, env)
        except OSError:
            recover(tools)
            raise
        bins = bin_dir(tools)
        fix_receipt(moved, bins)
        data = record(tools)
        data.pop("migrating", None)
        data.update({"active": str(moved), "switched_at": time.time(), "tools": str(tools), "bin": str(bins)})
        if isinstance(data.get("previous"), str) and _same(Path(data["previous"]), moved):
            data.pop("previous", None)
        _write_record(data, tools)
        return moved


def tool_state(tools: Path | None = None) -> str:
    env = tool_env(tools)
    if is_link(env):
        try:
            target = env.resolve(strict=True)
        except OSError:
            return ToolPath.DANGLING
        return ToolPath.LINKED if env_python(target).exists() else ToolPath.DANGLING
    if env.is_dir():
        return ToolPath.PLAIN
    if env.exists():
        return ToolPath.OTHER
    return ToolPath.MISSING


def fix_record(tools: Path | None = None) -> list[str]:
    """Make `active.json` say what is (R-T2): `active` the env the tool path
    names now (none while it names none), `previous` only an env with an
    interpreter that is not the active one, `tools` this folder. Returns what
    it changed, one line each. Never raises."""
    tools = tools or tool_dir()
    try:
        data = record(tools)
        if not data:
            return []
        said = []
        now = active(tools)
        recorded = data.get("active")
        if now is not None and (not isinstance(recorded, str) or not _same(Path(recorded), now)):
            said.append(f"active.json named {recorded or 'nothing'} as the active version; the tool path names {now}")
            data["active"] = str(now)
        elif now is None and recorded is not None:
            said.append(f"active.json named {recorded} as the active version; the tool path names no version env")
            data.pop("active", None)
        prior = data.get("previous")
        if isinstance(prior, str) and (not env_python(Path(prior)).exists()
                                       or (now is not None and _same(Path(prior), now))):
            said.append(f"active.json named {prior} to switch back to; it is gone or the active one")
            data.pop("previous", None)
        if data.get("tools") != str(tools) and now is not None:
            data["tools"] = str(tools)
            said.append(f"active.json's tool folder is {tools} now")
        if said:
            _write_record(data, tools)
        return said
    except OSError:
        return []


def clear_rejected(version: str, tools: Path | None = None) -> bool:
    """A person asked for `version` itself (an install, `probe repair`):
    its rejection on this machine goes (R-T2). True when there was one."""
    data = record(tools)
    marks = data.get("rejected")
    if not isinstance(marks, dict) or version not in marks:
        return False
    marks.pop(version, None)
    data["rejected"] = marks
    _write_record(data, tools)
    return True


def entrypoints(env: Path) -> list[str]:
    """The scripts uv put on PATH for `env` (its receipt's `install-path`s),
    by name; `probe` when the receipt says none."""
    names = []
    try:
        text = (env / RECEIPT).read_text(encoding="utf-8")
    except OSError:
        text = ""
    for found in _INSTALL_PATH.finditer(text):
        name = Path(found.group(1)).name
        if name and name not in names:
            names.append(name)
    return names or ["probe"]


def _ours(link_text: str, tools: Path) -> bool:
    """Is a shim's link one of Probe's to put right: into the tool path or the
    versions folder, or to nothing at all?"""
    target = Path(link_text)
    if not target.is_absolute():
        return False
    for root in (tool_env(tools), versions_root(tools)):
        if target == root or root in target.parents:
            return True
    return not target.exists()


def ensure_shims(tools: Path | None = None) -> tuple[list[str], list[str]]:
    """The public scripts (`~/.local/bin/probe*`, `bin_dir`) for every
    entrypoint the tool path's receipt names, each a link through the tool
    path (so it follows every switch), as uv makes them (R-T1): an install
    into a version folder fills only that folder's `.bin`. A missing one is
    made; one of ours that names a version env or nothing is put right; a
    file or a link that is someone else's is left, and named. Returns
    `(what it did, what is in the way)`. Never raises."""
    tools = tools or tool_dir()
    made: list[str] = []
    blocked: list[str] = []
    env = tool_env(tools)
    try:
        bins = bin_dir(tools)
        names = entrypoints(env)
    except OSError as exc:
        return [], [f"the scripts folder could not be read: {exc}"]
    for name in names:
        want = env / "bin" / name
        if not (want.exists() or want.is_symlink()):
            continue
        shim = bins / name
        try:
            if shim.is_symlink():
                current = os.readlink(shim)
                if Path(current) == want:
                    continue
                if not _ours(current, tools):
                    blocked.append(f"{shim} names {current}, not Probe's {want}")
                    continue
            elif shim.exists():
                blocked.append(f"{shim} is a file Probe did not make")
                continue
            bins.mkdir(parents=True, exist_ok=True)
            tmp = bins / f".{name}.probe-{os.getpid()}"
            with contextlib.suppress(FileNotFoundError):
                tmp.unlink()
            os.symlink(want, tmp)
            os.replace(tmp, shim)
            made.append(f"{shim} -> {want}")
        except OSError as exc:
            blocked.append(f"{shim}: {exc}")
    return made, blocked


def cleanup(tools: Path | None = None, *, now: float | None = None) -> list[Path]:
    """After a switch (R-T2): delete what a crash or an older release left in
    the versions folder that nothing uses -- migration leftovers
    (`<version>-<unix time>`) and unfinished installs (no interpreter or no
    uv receipt) -- never the active, the previous, an interrupted
    migration's or one a process here or on another machine runs from
    (`protected`, the marks of `prune`); then `prune`. Under the install lock
    (an unfinished install is no other installer's then). Returns what was
    deleted. Never raises."""
    tools = tools or tool_dir()
    now = time.time() if now is None else now
    removed: list[Path] = []
    try:
        with handoff.install_lock(versions_root(tools), wait_s=LOCK_WAIT_S):
            commands = _commands()
            for folder in _folders(tools):
                _version, _generation, leftover = folder_parts(folder.name)
                env = folder / DIST
                unfinished = not env_python(env).exists() or not (env / RECEIPT).is_file()
                if not (leftover or unfinished):
                    continue
                if protected(folder, tools, commands=commands) or _used_elsewhere(folder, now):
                    continue
                shutil.rmtree(folder, ignore_errors=True)
                if not folder.exists():
                    removed.append(folder)
            removed += prune(tools, now=now)
    except (OSError, RuntimeError):
        pass
    return removed


# -- pruning ---------------------------------------------------------------------


#: Each machine marks the versions its processes run from (`.used-<machine key>`):
#: a home shared by several machines (NFS) has one versions folder, and a
#: machine sees only its own processes. A mark this fresh keeps a version.
USED_PREFIX = ".used-"
USED_FRESH_S = 3 * 24 * 3600


def _commands() -> list[str] | None:
    """Every running process's command line and executable, once; None when
    they cannot be read (unknown: everything reads as in use)."""
    proc = Path("/proc")
    if proc.is_dir():
        found = []
        try:
            for entry in proc.iterdir():
                if not entry.name.isdigit():
                    continue
                with contextlib.suppress(OSError):
                    found.append((entry / "cmdline").read_bytes().decode("utf-8", "replace"))
                with contextlib.suppress(OSError):
                    found.append(os.readlink(entry / "exe"))
        except OSError:
            return None
        return found
    try:
        out = subprocess.run(["ps", "-axww", "-o", "command="], capture_output=True, text=True, timeout=10, check=False)
    except (OSError, subprocess.SubprocessError):
        return None
    return None if out.returncode != 0 else (out.stdout or "").splitlines()


def _in_use(folder: Path, commands: list[str] | None = None) -> bool:
    """Does any running process run from `folder`? (Its command line names it,
    either spelling of the path.) Unknown reads as yes."""
    commands = _commands() if commands is None else commands
    if commands is None:
        return True
    needles = {str(folder)}
    with contextlib.suppress(OSError):
        needles.add(str(folder.resolve()))
    return any(n in c for c in commands for n in needles)


def _machine() -> str:
    try:
        from probe.service import paths

        return paths.machine_key()
    except Exception:  # noqa: BLE001
        return "unknown"


def _mtime(path: Path) -> float:
    try:
        return path.stat().st_mtime
    except OSError:
        return 0.0


def mark_in_use(tools: Path | None = None) -> list[Path]:
    """Mark (`.used-<this machine>`) every version folder a process here runs
    from, and clear this machine's mark on the others. Returns the marked.
    Never raises."""
    try:
        tools = tools or tool_dir()
        folders = [p for p in versions_root(tools).iterdir() if p.is_dir()]
    except OSError:
        return []
    commands = _commands()
    mine = USED_PREFIX + _machine()
    marked = []
    for folder in folders:
        mark = folder / mine
        with contextlib.suppress(OSError):
            if commands is not None and not _in_use(folder, commands):
                mark.unlink(missing_ok=True)
                continue
            mark.touch()
            marked.append(folder)
    return marked


def _version_key(name: str) -> tuple:
    """A version folder's place in line by its NAME alone: `(release, generation)`;
    a name that is no release sorts first. `_place` reads the env's dist-info first."""
    version, generation, _leftover = folder_parts(name)
    return handoff.release(version) or (), generation


def _place(folder: Path) -> tuple:
    """A version folder's place in prune's line: the version its env HOLDS (its
    dist-info, no interpreter started where it has one), else its name's; then
    its generation, so a rebuilt `<v>+g<N>` counts as `<v>` (newer than the
    `<v>` it replaced), never as junk; then when it was installed. A folder
    with no env in it (junk, whatever its name) sorts first, and goes first."""
    env = folder / DIST
    named, generation = _version_key(folder.name)
    if not env_python(env).exists():
        return (), 0, _installed_at(folder)
    return handoff.release(handoff.env_version(env, timeout=10.0)) or named, generation, _installed_at(folder)


def _installed_at(folder: Path) -> float:
    for marker in (folder / DIST / "pyvenv.cfg", folder / DIST / "bin" / "python"):
        try:
            return marker.lstat().st_mtime
        except OSError:
            continue
    return _mtime(folder)


def _used_elsewhere(folder: Path, now: float) -> bool:
    mine = USED_PREFIX + _machine()
    try:
        marks = [m for m in folder.iterdir() if m.name.startswith(USED_PREFIX) and m.name != mine]
    except OSError:
        return True
    return any(now - _mtime(m) < USED_FRESH_S for m in marks)


def prune(tools: Path | None = None, *, keep: int = KEEP, now: float | None = None) -> list[Path]:
    """Delete version folders beyond the newest `keep`, never the active or the
    previous one, never one younger than PRUNE_MIN_AGE_S, never one a running
    process uses -- here, or on another machine sharing this home (its mark,
    `mark_in_use`, younger than USED_FRESH_S). Returns what was deleted. Never raises."""
    tools = tools or tool_dir()
    root = versions_root(tools)
    now = time.time() if now is None else now
    try:
        folders = [p for p in root.iterdir() if p.is_dir()]
    except OSError:
        return []
    protected = set()
    for env in (active(tools), previous(tools)):
        if env is not None:
            with contextlib.suppress(OSError):
                protected.add(env.parent.resolve())
    moving = record(tools).get("migrating")
    if isinstance(moving, dict) and isinstance(moving.get("to"), str):
        with contextlib.suppress(OSError):
            protected.add(Path(moving["to"]).parent.resolve())  # what `recover` puts back
    commands = _commands()
    mark_in_use(tools)
    # Newest first by the version each env holds, then its generation (a
    # folder's own mtime moves with its marks), aged by when its env was made
    # (`pyvenv.cfg`, written once at install).
    folders.sort(key=_place, reverse=True)
    removed: list[Path] = []
    for folder in folders[keep:]:
        try:
            if (folder.resolve() in protected or now - _installed_at(folder) < PRUNE_MIN_AGE_S
                    or _in_use(folder, commands) or _used_elsewhere(folder, now)):
                continue
            shutil.rmtree(folder)
            removed.append(folder)
        except OSError:
            continue
    return removed


def running_from_versions(prefix: str | None = None) -> bool:
    """Does this interpreter run from a version env (`probe-versions/<v>/...`)?"""
    text = (prefix if prefix is not None else sys.prefix).replace(os.sep, "/")
    return f"/{VERSIONS_DIRNAME}/" in text


def versions_root_of(prefix: str | None = None) -> Path | None:
    """The versions folder this interpreter runs from (`probe-versions/<v>/probe-research`'s
    grandparent), or None when it does not run from a version env. No `uv` asked."""
    path = Path(prefix if prefix is not None else sys.prefix)
    if not running_from_versions(str(path)):
        return None
    for parent in path.parents:
        if parent.name == VERSIONS_DIRNAME:
            return parent
    return None
