"""The lifeboat: an updater that lives outside every release (plan fool-proof-updates B1, B5).

Every update used to run the INSTALLED release's updater, so a release whose
updater was broken could never be replaced by a newer one. The lifeboat is a
copy of the frozen hand-off (`probe/_shared/handoff.py`: stdlib only, imports
nothing of `probe`) kept OUTSIDE the release folders, with a frozen `/bin/sh`
wrapper in front of it:

    ~/.local/state/probe/lifeboat/         L (`root`), 0700, never moved by XDG_STATE_HOME
        lifeboat.sh                        the wrapper (`probe/_shared/lifeboat.sh`, digest-pinned)
        current/handoff.py                 the copy a release may write
        current/.acted                     touched by the wrapper when this copy started a rescue
        known-good/handoff.py              the copy that last proved itself
        env.json                           what the hand-off needs of this install (`write_env`)
        state.json, acted.json             the hand-off's own clock, and what it did (it alone writes them)

The keeper unit (`keeper.py`) runs `/bin/sh L/lifeboat.sh keeper` every
minute; a session's start runs `... session` from the plugin's hook
dispatcher when no keeper unit runs it (a pod with no user scheduler).

Slot rules (R12: a bad release must never sink the lifeboat):
  * a release writes only `current/`: when its packaged HANDOFF_VERSION is
    higher than the installed copy's, or `current/` is missing or passes
    --selftest under none of the wrapper's pythons; never when the packaged
    copy itself passes under none (`install`);
  * `known-good/` is written once, from the same copy, when there is none (the
    first install), and otherwise only by promotion (`promote`): `current/`
    itself rescued this machine (its `.acted` is newer than it: a no-op run
    proves nothing; none of known-good's came after it) and an update cycle
    ended after that with the active CLI at the manifest's latest. Never from
    a test's HOME;
  * the wrapper runs `known-good/` instead of `current/` once current's own
    rescue has had two hours and the machine is still behind its release.

Installed (and env.json refreshed, with the login shell's index settings) by
release code with the keeper's own guards -- only the account's own home,
never with PROBE_SERVICE_KEEPER=0, never after an Uninstall -- at every
service start (`keeper.install`), and at the end of every update whose CLI
step ended ok, whatever ran it (`probe.cli.upgrading`), and every `probe
doctor` (`keeper.refresh_lifeboat`): a pod where no service runs
(no_new_privs) still gets one, which its sessions' starts run.
Uninstall removes it (`keeper.remove`); turning automatic updates off stops it
at its next run (`note_auto_update`). After each cycle and at its start the
service reports what the lifeboat did (`acted.json`, as `lifeboat.acted`
through `statepost`) and deletes the record.

Stdlib only, light at import: the service's start imports it.
"""

from __future__ import annotations

import contextlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
from collections.abc import Iterator, Mapping
from pathlib import Path

from . import paths

DIRNAME = "lifeboat"
WRAPPER_NAME = "lifeboat.sh"
HANDOFF_NAME = "handoff.py"
CURRENT = "current"
KNOWN_GOOD = "known-good"
#: Touched by the wrapper in a slot whose copy started a rescue in that run.
ACTED_STAMP = ".acted"
ENV_NAME = "env.json"
ENV_VERSION = 1
#: Written by the hand-off when it rescued this machine; reported and deleted here.
ACTED_NAME = "acted.json"
#: The wrapper's triggers (`/bin/sh L/lifeboat.sh <trigger>`).
TRIGGERS = ("keeper", "session", "cli")
#: The interpreter the wrapper tries third, after the recorded base python and uv's.
SYSTEM_PYTHON = "/usr/bin/python3"
SELFTEST_TIMEOUT_S = 30.0
UV_TIMEOUT_S = 20.0
#: An `acted.json` older than this is dropped unreported: the machine's
#: consent never allowed it, and a week-old rescue says nothing new.
ACTED_MAX_AGE_S = 7 * 24 * 3600
#: The login environment the hand-off's installs need (`env.json` `index_env`):
#: package indexes, proxies, CA bundles.
INDEX_ENV_NAMES = (
    "UV_INDEX_URL", "UV_EXTRA_INDEX_URL", "UV_DEFAULT_INDEX", "UV_INDEX", "UV_NATIVE_TLS",
    "PIP_INDEX_URL", "PIP_EXTRA_INDEX_URL",
    "HTTP_PROXY", "HTTPS_PROXY", "NO_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "no_proxy", "all_proxy",
    "SSL_CERT_FILE", "SSL_CERT_DIR", "REQUESTS_CA_BUNDLE",
)

_HANDOFF_VERSION = re.compile(rb"^HANDOFF_VERSION(?:\s*:\s*int)?\s*=\s*(\d+)\s*(?:#.*)?$", re.MULTILINE)
_SHARED = Path(__file__).resolve().parent.parent / "_shared"


def root() -> Path:
    """`~/.local/state/probe/lifeboat` (L)."""
    return paths.state_dir() / DIRNAME


def wrapper_path() -> Path:
    """What every keeper unit runs, by this fixed path."""
    return root() / WRAPPER_NAME


def supported() -> bool:
    """POSIX only: Windows has no `/bin/sh` and keeps its direct keeper task."""
    return os.name == "posix"


def packaged_wrapper() -> Path:
    return _SHARED / WRAPPER_NAME


def packaged_handoff() -> Path | None:
    """This release's `probe/_shared/handoff.py`, or None (a release without one)."""
    path = _SHARED / HANDOFF_NAME
    return path if path.is_file() else None


def handoff_version(path: Path) -> int | None:
    """`HANDOFF_VERSION = N` as the file spells it (read, never imported)."""
    try:
        found = _HANDOFF_VERSION.search(path.read_bytes())
    except OSError:
        return None
    return int(found.group(1)) if found else None


# -- env.json --------------------------------------------------------------------


def _executable(path: object) -> bool:
    return isinstance(path, str) and os.path.isabs(path) and os.path.isfile(path) and os.access(path, os.X_OK)


def _find_uv() -> str | None:
    """`uv` on PATH, else where its installers put it (the service's own PATH is clean)."""
    found = shutil.which("uv")
    if found:
        return found
    home = paths.home()
    for candidate in (home / ".local" / "bin" / "uv", home / ".cargo" / "bin" / "uv",
                      Path("/opt/homebrew/bin/uv"), Path("/usr/local/bin/uv")):
        if _executable(str(candidate)):
            return str(candidate)
    return None


def _uv_python(uv: object) -> str | None:
    """`uv python find`'s first line: the wrapper's second candidate."""
    if not _executable(uv):
        return None
    try:
        out = subprocess.run([str(uv), "python", "find"], capture_output=True, text=True,
                             stdin=subprocess.DEVNULL, timeout=UV_TIMEOUT_S, check=False)
    except (OSError, subprocess.SubprocessError):
        return None
    line = (out.stdout or "").strip().splitlines()
    return line[0].strip() if out.returncode == 0 and line else None


def _pyvenv(env: Path) -> dict:
    try:
        text = (env / "pyvenv.cfg").read_text(encoding="utf-8")
    except OSError:
        return {}
    fields = {}
    for line in text.splitlines():
        key, sep, value = line.partition("=")
        if sep:
            fields[key.strip()] = value.strip()
    return fields


def base_python(env: Path) -> str | None:
    """The interpreter the active env was made from (`pyvenv.cfg`'s `home`):
    `pythonX.Y` there, else `python3`."""
    fields = _pyvenv(env)
    home = fields.get("home")
    if not home:
        return None
    found = re.match(r"(\d+)\.(\d+)", fields.get("version_info") or fields.get("version") or "")
    names = ([f"python{found.group(1)}.{found.group(2)}"] if found else []) + ["python3"]
    for name in names:
        candidate = os.path.join(home, name)
        if _executable(candidate):
            return candidate
    return None


def _requirement(entry: dict) -> str | None:
    """One uv-receipt requirement as `--with` takes it (`probe.cli.updater`'s
    rule), or None when it has a shape that cannot be restated."""
    if set(entry) - {"name", "extras", "specifier", "url", "directory", "git"}:
        return None
    name = entry.get("name")
    if not isinstance(name, str) or not name:
        return None
    extras = [e for e in entry.get("extras") or [] if isinstance(e, str)]
    text = name + (f"[{','.join(extras)}]" if extras else "")
    sources = [k for k in ("url", "directory", "git") if entry.get(k)]
    if len(sources) > 1:
        return None
    if sources:
        where = str(entry[sources[0]])
        if sources[0] == "directory":
            where = Path(where).resolve().as_uri()
        elif sources[0] == "git" and not where.startswith("git+"):
            where = "git+" + where
        return f"{text} @ {where}"
    return text + str(entry.get("specifier") or "")


def receipt(env: Path) -> dict:
    """What the active env's `uv-receipt.toml` records: `extras` (probe-research's),
    `with` (everything else, restated), `python` (an exact `--python`, or None)."""
    from probe._compat import tomllib

    out: dict = {"extras": [], "with": [], "python": None}
    try:
        tool = tomllib.loads((env / "uv-receipt.toml").read_text(encoding="utf-8")).get("tool") or {}
    except (OSError, ValueError):
        return out
    for entry in tool.get("requirements") or []:
        if not isinstance(entry, dict):
            continue
        if entry.get("name") in ("probe-research", "probe-agent"):
            out["extras"] = sorted(e for e in entry.get("extras") or [] if isinstance(e, str))
            continue
        requirement = _requirement(entry)
        if requirement is not None:
            out["with"].append(requirement)
    python = tool.get("python")
    if isinstance(python, str) and python and not (os.path.isabs(python) and not os.path.exists(python)):
        out["python"] = python
    return out


def _userinfo(value: str) -> bool:
    """Does any URL in `value` carry a user (and a password)? Index variables
    hold lists (`UV_EXTRA_INDEX_URL="https://pypi.org/simple
    https://user:tok@priv/simple"`, comma-separated too): every entry is
    looked at, and one with credentials is enough."""
    return any("@" in entry.split("://", 1)[-1].split("/", 1)[0]
               for entry in re.split(r"[\s,]+", value) if entry)


def index_env(login: Mapping) -> dict:
    """The index, proxy and CA variables of the login environment, never one
    with credentials in any of its URLs: env.json is a file on disk
    (`loginenv`: such values are never stored). A machine that needs them gets
    its rescue from a session start, whose environment the hand-off inherits."""
    return {name: str(login[name]) for name in INDEX_ENV_NAMES
            if isinstance(login.get(name), str) and login[name] and not _userinfo(login[name])}


def _managed(tools: Path, prefix: Path) -> bool:
    """Is this interpreter's env the machine's managed CLI: the uv tool env at
    the tool path, or a version env beside it (side by side)?"""
    from probe._shared import installs

    try:
        here = prefix.resolve()
        if installs.tool_env(tools).resolve() == here:
            return True
        versions = installs.versions_root(tools).resolve()
        return here == versions or versions in here.parents
    except OSError:
        return False


def _read_env() -> dict:
    try:
        data = json.loads((root() / ENV_NAME).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def login_env() -> dict | None:
    """The login shell's variables (`loginenv.read`, on this thread: a
    blocking caller's), asked with the service's clean environment
    (`client._clean_env`), never the caller's: an agent's sandbox sets a
    localhost proxy only its own processes can use, and an update or `probe
    doctor` may run inside one. None when the shell gave no answer (then the
    last record's index settings are kept, never wiped)."""
    try:
        import asyncio

        from . import client, loginenv

        found = asyncio.run(loginenv.read(env=client._clean_env()))  # noqa: SLF001 -- the service's own env
    except Exception:  # noqa: BLE001 -- unread: keep what was recorded
        return None
    return dict(found[1]) if found is not None else None


def env_record(login: Mapping | None = None) -> dict:
    """env.json's content for this install (plan Build contract). `login`:
    the login shell's (or the caller's own) variables when the caller has
    them; else the ones the last record kept, else the shell is asked once."""
    from probe import version_policy
    from probe._shared import installs

    from . import client, watch

    tools = installs.tool_dir()
    env = installs.tool_env(tools)
    active = installs.env_python(env)
    active_python = str(active) if _executable(str(active)) else client.runtime_python()
    recorded = receipt(env)
    extras = {"all", *recorded["extras"]}
    if importlib.util.find_spec("pydantic_ai_harness") is not None:
        extras.add("daemon")  # as the CLI's own updater keeps the daemon's libraries (`_dist`)
    if login is None:
        previous = _read_env().get("index_env")
        kept = previous if isinstance(previous, dict) else None
        index = index_env(kept if kept is not None else (login_env() or {}))
    else:
        index = index_env(login)
    base = base_python(env)
    return {
        "v": ENV_VERSION,
        "tools": str(tools),
        "versions_root": str(installs.versions_root(tools)),
        "uv": _find_uv(),
        "base_python": base,
        "active_python": active_python,
        "extras": sorted(extras),
        "with": recorded["with"],
        "python_request": recorded["python"] or base,
        "index_env": index,
        "base_url": watch.config_base_url(),
        "auto_update": bool(version_policy.autoupdate_enabled()),
        "managed": _managed(tools, Path(sys.prefix)),
        # Where the hand-off asks `service.hello` (a keeper run: is the service down?).
        "socket": str(paths.socket_path()),
    }


def _write(path: Path, data: bytes, mode: int = 0o600) -> bool:
    """`data` at `path`, whole (a private temporary file renamed into place).
    True when it changed."""
    try:
        if path.read_bytes() == data:
            return False
    except OSError:
        pass
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | getattr(os, "O_NOFOLLOW", 0), mode)
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
        os.chmod(tmp, mode)
        os.replace(tmp, path)
    finally:
        with contextlib.suppress(OSError):
            tmp.unlink()
    return True


def write_env(login: Mapping | None = None) -> dict:
    """Write env.json: the one writer of it, in release code. Called by every
    `install` (the service's start, with the login shell's variables; the end
    of an update that succeeded and `probe doctor`, with their own) and after
    each update cycle (`after_cycle`): `auto_update`, `managed` and `socket`
    fresh each time. One key per line: the wrapper reads it with `sed`.
    Returns what it wrote. `tests/test_lifeboat.py` holds it to every key
    `handoff.py` reads."""
    data = env_record(login)
    paths.private_dir(root())
    _write(root() / ENV_NAME, _env_text(data))
    return data


def _env_text(data: Mapping) -> bytes:
    return (json.dumps(data, indent=1, ensure_ascii=False) + "\n").encode("utf-8")


def note_auto_update(enabled: bool) -> bool:
    """The automatic-update setting was saved (`autoupdate.save`): env.json says
    so at once, so a person who turns updates off is never rescued 12 h later
    by a lifeboat that read the setting at the last service start. Only an
    env.json that exists is touched (a lifeboat release code installed). True
    when it changed. Never raises."""
    try:
        data = _read_env()
        if not data or data.get("auto_update") is bool(enabled):
            return False
        data["auto_update"] = bool(enabled)
        return _write(root() / ENV_NAME, _env_text(data))
    except Exception:  # noqa: BLE001 -- the next service start writes it anyway
        return False


# -- the slots ----------------------------------------------------------------------


def candidates(env: Mapping) -> Iterator[str]:
    """The wrapper's pythons, in its order, each once, existing only; `uv
    python find` asked only when the ones before it did not do."""
    seen: set = set()

    def fresh(path: object) -> bool:
        if not _executable(path) or path in seen:
            return False
        seen.add(path)
        return True

    if fresh(env.get("base_python")):
        yield str(env["base_python"])
    uv = env.get("uv") if _executable(env.get("uv")) else shutil.which("uv")
    found = _uv_python(uv)
    if fresh(found):
        yield str(found)
    if fresh(SYSTEM_PYTHON):
        yield SYSTEM_PYTHON
    if fresh(env.get("active_python")):
        yield str(env["active_python"])


def selftest(script: Path, env: Mapping) -> str | None:
    """The first of the wrapper's pythons under which `script --selftest`
    exits 0 (the one the wrapper would run it with), or None."""
    for python in candidates(env):
        try:
            done = subprocess.run([python, "-I", "-S", str(script), "--selftest"], capture_output=True,
                                  stdin=subprocess.DEVNULL, timeout=SELFTEST_TIMEOUT_S, check=False)
        except (OSError, subprocess.SubprocessError):
            continue
        if done.returncode == 0:
            return python
    return None


def _slot(name: str) -> Path:
    return root() / name / HANDOFF_NAME


def _place(data: bytes, slot: str, env: Mapping) -> bool:
    """`data` as `slot`'s handoff.py, only if it passes --selftest first (as a
    private file beside it, renamed into place). True when it is there."""
    folder = paths.private_dir(root() / slot)
    target = folder / HANDOFF_NAME
    trial = folder / f".{HANDOFF_NAME}.{os.getpid()}.new"
    try:
        _write(trial, data)
        if selftest(trial, env) is None:
            return False
        # Proof is per copy: the rescue of the one replaced proves nothing of
        # this one (the wrapper stamps only the copy that ran, by its checksum).
        with contextlib.suppress(OSError):
            (folder / ACTED_STAMP).unlink()
        os.replace(trial, target)
        return True
    finally:
        with contextlib.suppress(OSError):
            trial.unlink()


def install(login: Mapping | None = None) -> str:
    """Install or refresh the lifeboat (the caller holds the keeper's guards
    and lock: `keeper.install`, `keeper.install_lifeboat`), env.json with the
    index settings of `login` (else the last record's). Returns what
    happened. Never raises."""
    if not supported():
        return "unsupported"
    try:
        paths.private_dir(root())
        env = write_env(login)
        done = []
        if _write(wrapper_path(), packaged_wrapper().read_bytes(), 0o700):
            done.append(WRAPPER_NAME)
        source = packaged_handoff()
        if source is None:
            return "no handoff in this release" + (f" ({', '.join(done)})" if done else "")
        packaged = source.read_bytes()
        current = _slot(CURRENT)
        mine, theirs = handoff_version(source), handoff_version(current)
        if not current.is_file() or theirs is None or (mine is not None and mine > theirs) \
                or selftest(current, env) is None:
            if not _place(packaged, CURRENT, env):
                return "failed: this release's handoff.py passes --selftest under no python here"
            done.append(CURRENT)
        if not _slot(KNOWN_GOOD).is_file():
            if _place(current.read_bytes(), KNOWN_GOOD, env):
                done.append(KNOWN_GOOD)
        return f"installed ({', '.join(done)})" if done else "current"
    except Exception as exc:  # noqa: BLE001 -- the keeper and the service go on without it
        return f"failed: {exc!r}"[:300]


def rescued_at(current: Path) -> float | None:
    """When `current/`'s copy, as it is now, started a rescue (its `.acted`,
    newer than the copy), or None: a run that did nothing proves nothing."""
    try:
        stamp = (current.parent / ACTED_STAMP).stat()
        if stamp.st_mtime_ns > current.stat().st_mtime_ns:
            return stamp.st_mtime
    except OSError:
        pass
    return None


def promote(*, ok: bool, active: str | None, latest: str | None, ended_at: float | None = None) -> bool:
    """After an update cycle: `current/` becomes `known-good/` when that copy
    rescued this machine (`rescued_at`) and a cycle that ended after it
    (`ended_at`, now when not said) ended `ok` with the active CLI (`active`)
    at the manifest's latest (`latest`): a copy is trusted for what it did,
    never for having run. Not when known-good's own rescue came after
    current's (current's failed: the latest is known-good's doing). The stamp
    is spent by a promotion. Never from a test's HOME, never with the keeper
    off. True when it was promoted. Never raises."""
    try:
        import time

        from . import keeper

        if not (supported() and keeper.wanted() and ok and active and latest and active == latest):
            return False
        current, known = _slot(CURRENT), _slot(KNOWN_GOOD)
        rescued = rescued_at(current) if current.is_file() else None
        if rescued is None or rescued > (time.time() if ended_at is None else ended_at):
            return False
        with contextlib.suppress(OSError):
            if (known.parent / ACTED_STAMP).stat().st_mtime > rescued:
                # The last rescue was known-good's (the wrapper ran it once
                # current's had failed): what reached the latest is not current.
                return False
        data = current.read_bytes()
        with contextlib.suppress(OSError):
            if known.read_bytes() == data:
                return False
        paths.private_dir(known.parent)
        _write(known, data)
        # Its proof is spent: the next promotion needs a rescue of its own.
        with contextlib.suppress(OSError):
            (current.parent / ACTED_STAMP).unlink()
        return True
    except Exception:  # noqa: BLE001 -- the slots stay as they are
        return False


def manifest_latest() -> str | None:
    """The manifest's `cli.latest`, from the CLI's cache (what the last update read)."""
    try:
        from probe import version_policy

        manifest, _fetched, _ok = version_policy.read_cache()
        latest = (manifest or {}).get("cli", {}).get("latest") if isinstance(manifest, dict) else None
    except Exception:  # noqa: BLE001
        return None
    return latest if isinstance(latest, str) and latest else None


def after_cycle(result: Mapping) -> bool:
    """An update cycle ended (`update.done`'s payload): promote `current/`
    when it proved itself (`promote`). Blocking: a thread."""
    steps = result.get("steps") if isinstance(result.get("steps"), Mapping) else {}
    self_step = steps.get("self") if isinstance(steps.get("self"), Mapping) else {}
    active = self_step.get("to_version")
    ok = result.get("ok") is True and not result.get("deferred")
    ended = result.get("at") if isinstance(result.get("at"), (int, float)) else None
    with contextlib.suppress(Exception):
        if supported() and root().is_dir():
            write_env()  # what the cycle may have changed: the setting, the active env
    return promote(ok=ok, active=active if isinstance(active, str) else None, latest=manifest_latest(),
                   ended_at=ended)


# -- what it did --------------------------------------------------------------------


def read_acted(now: float | None = None) -> dict | None:
    """`acted.json` as the hand-off wrote it, or None (none, unreadable: an
    unreadable or week-old one is deleted)."""
    import time

    path = root() / ACTED_NAME
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        data = json.loads(raw)
    except ValueError:
        data = None
    now = time.time() if now is None else now
    at = data.get("at") if isinstance(data, dict) else None
    stale = isinstance(at, (int, float)) and not isinstance(at, bool) and now - at > ACTED_MAX_AGE_S
    if not isinstance(data, dict) or stale:
        clear_acted()
        return None
    return data


def clear_acted() -> None:
    with contextlib.suppress(OSError):
        (root() / ACTED_NAME).unlink()


def remove() -> None:
    """Uninstall: the whole lifeboat goes (the caller checked it is this account's home)."""
    shutil.rmtree(root(), ignore_errors=True)


__all__ = [
    "TRIGGERS", "after_cycle", "candidates", "clear_acted", "env_record", "handoff_version", "install",
    "login_env", "note_auto_update", "promote", "read_acted", "remove", "rescued_at", "root", "selftest",
    "write_env", "wrapper_path",
]
