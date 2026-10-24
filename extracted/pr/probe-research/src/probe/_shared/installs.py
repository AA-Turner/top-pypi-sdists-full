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

Stdlib only: the Probe service imports this to switch back (plan S1).
"""

from __future__ import annotations

import contextlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

DIST = "probe-research"
VERSIONS_DIRNAME = "probe-versions"
ACTIVE_NAME = "active.json"
#: Versions kept beside the active one when pruning (the previous one always).
KEEP = 3
#: A version folder younger than this is never pruned (a run may have just started on it).
PRUNE_MIN_AGE_S = 24 * 3600
_VERSION = re.compile(r"^[0-9][0-9A-Za-z.+!_-]{0,63}$")
_UV_TIMEOUT_S = 15


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


def install_command(spec: str, *, with_packages: tuple = (), python: str | None = None) -> list[str]:
    command = ["uv", "tool", "install", "--refresh-package", DIST, spec]
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
) -> Path:
    """Install `spec` (`probe-research[...]==<version>`) as its own env,
    `probe-versions/<version>/probe-research`, beside the active one. A
    complete env of that version already there is reused. Returns the env;
    raises RuntimeError (with what uv said) when it does not end up holding
    `version`."""
    tools = tools or tool_dir()
    env = version_env(version, tools)
    if env_version(env) == version:
        return env
    holder = env.parent
    if holder.exists():
        shutil.rmtree(holder, ignore_errors=True)  # a half-finished earlier try
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
    got = env_version(env)
    if got is None and env_python(env).exists():
        got = env_version(env, timeout=120.0)  # a loaded machine, not a failed install
    if got != version:
        said = ((done.stderr or "") + (done.stdout or "")).strip()[-1500:]
        shutil.rmtree(holder, ignore_errors=True)
        raise RuntimeError(f"`uv tool install {spec}` exited {done.returncode} and left {got or 'nothing'}: {said}")
    return env


def selftest(env: Path, *, timeout: float = 60.0) -> str | None:
    """Does the env start? The service's start path (`-m probe.service
    --selftest`) and the CLI's import, each by the env's own interpreter.
    None when both work, else what failed (D5's check before a switch)."""
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
        except (OSError, subprocess.SubprocessError) as exc:
            return f"{name} would not start: {exc}"
        if done.returncode != 0:
            tail = (done.stderr or "").strip().splitlines()[-1:] or [f"exit {done.returncode}"]
            return f"{name} would not start: {tail[0][:300]}"
    return None


def discard(env: Path) -> None:
    """Delete a version env that will not be used (never the active one)."""
    holder = env.parent
    if active() is not None and active() == env.resolve():
        return
    shutil.rmtree(holder, ignore_errors=True)


def rejected(tools: Path | None = None) -> dict:
    """`{version: when}`: versions switched back from on this machine (D5),
    never installed again (a newer release is)."""
    value = record(tools).get("rejected")
    return value if isinstance(value, dict) else {}


def reject(version: str, reason: str, tools: Path | None = None) -> None:
    data = record(tools)
    marks = data.get("rejected") if isinstance(data.get("rejected"), dict) else {}
    marks[version] = {"at": time.time(), "reason": reason[:500]}
    data["rejected"] = marks
    _write_record(data, tools)


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
    if dest.exists():
        dest = versions_root(tools) / f"{version}-{int(time.time())}" / DIST
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
    after that puts it back, so the CLI is never left without a tool path."""
    tools = tools or tool_dir()
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
            "previous": str(previous) if previous is not None and Path(previous) != target else data.get("previous"),
            "switched_at": time.time(),
            # Where the tool path is, for a process running from a version env
            # that must not ask `uv tool dir` on every start.
            "tools": str(tools),
        }
    )
    _write_record(data, tools)
    return data


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
    head = name.split("-", 1)[0]
    parts = head.split(".")
    return tuple(int(p) for p in parts) if all(p.isdigit() for p in parts) else ()


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
    commands = _commands()
    mark_in_use(tools)
    # Newest first by version (a folder's own mtime moves with its marks), and
    # aged by when its env was made (`pyvenv.cfg`, written once at install).
    folders.sort(key=lambda f: (_version_key(f.name), _installed_at(f)), reverse=True)
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
