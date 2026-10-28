"""The hand-off: download the newest Probe CLI, then run the rest of the update in ITS code.

FROZEN. This file is digest-pinned by `agent/tests/test_handoff_frozen.py`:
it is the one piece of updater code a newer release cannot replace on a
machine that is already stuck, so a change to it is deliberate. To change it,
raise HANDOFF_VERSION and re-pin the digest (the test says how).

Why it exists (plan "Fool-proof automatic updates", A1/B1). An update used to
run every step in the INSTALLED release's code, so a bug in that release's
updater (a plugin step that raised, a hang, an install it could not do) could
only be fixed by a person. Now the old code does exactly two things -- find the
newest release and download it beside the running one -- and then replaces
itself (`os.execve`, the same pid) with the NEW release's
`python -I -m probe.core.run update`, which switches the CLI and updates
everything else (`probe.core.adopt`). A bug in today's updater is fixed by
shipping a newer release.

The same file runs in two places:

    stage 1   inside a release: every update entry calls `stage1(trigger)`
              first (`probe.core.adopt.begin`), before any other updater code.
              "current" (or any answer that is not a hand-off) returns to the
              caller, which goes on in-process as before.
    lifeboat  outside every release: copies under
              ~/.local/state/probe/lifeboat/{current,known-good}/handoff.py,
              run by `lifeboat.sh` with whatever Python works. It installs
              the newest release on a machine that has been behind for 12 h by
              its own clock (5 min, when its service has not answered either).
              It never switches back: that is the guard's, in release code.

Modes:

    python -I -S handoff.py --selftest              exit 0: it parses and its imports load
    python -I handoff.py --stage1 --trigger T [--reason R]
    python -I handoff.py --lifeboat --trigger keeper|session|cli

    exit 0 normal (nothing to do, or done), 1 a hand-off that failed (logged),
    3 an internal error of its own (the wrapper then tries known-good).

Files (all under L = ~/.local/state/probe/lifeboat, never moved by XDG_STATE_HOME):

    L/env.json     written by RELEASE code; read here (`read_env`)
    L/state.json   written ONLY here, lifeboat mode: its own clocks
    L/acted.json   written here when a lifeboat run rescued; the next release reports it
    <versions_root>/install.lock       the one install lock (`fcntl.flock`)
    <versions_root>/install.lock.json  its holder: {"pid", "start", "cmd", "at", "mono"}
    <versions_root>/active.json        read: the active, rejected and `dropped_with`

The install lock (I8): every install and switch, from any path, holds it.
A waiter waits for a live holder; one that has held it STALE_HOLDER_S (45
min: the service's 30 min update limit + 15) by the wall clock AND awake
(`mono`: a sleeping laptop does not age it), and whose argv is one of our
updates (`holder_kind`: the update child, this file, the CLI's own update),
is stopped: SIGTERM, KILL_GRACE_S, SIGKILL -- to its process group only when
it leads one of its own, else to it alone. The lock fd is handed across the
exec (PROBE_INSTALL_LOCK_FD), so the new release switches under the same
lock without taking it again (`install_lock` is re-entrant).

An install counts only when uv exits 0 and leaves a complete env (its
receipt included), and the new env is exec'd only once its update path
imports (`starts`). A failed install, or an env whose import fails, is
deleted (never the active env) and installed afresh next time; one whose
check could not run (a timeout) is kept for the next try. `--with`
packages are left out only as the last try (`attempts`).

Versions: releases are plain X.Y.Z[.N]; anything else is never newer.

Stdlib only, and nothing from `probe`: the lifeboat runs it outside every
release, with `-I -S`.

Test-only environment (nothing else reads these):
    PROBE_HANDOFF_NOW       a unix time: the clock rejected-expiry and the
                            lifeboat's clocks read (default: the real time)
    PROBE_HANDOFF_PYPI_URL  the PyPI JSON URL (default: pypi.org's)
"""

from __future__ import annotations

import contextlib
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

try:
    import fcntl
except ImportError:  # Windows: no side-by-side installs there (`installs.usable`)
    fcntl = None  # type: ignore[assignment]

HANDOFF_VERSION = 1

DIST = "probe-research"
VERSIONS_DIRNAME = "probe-versions"
ACTIVE_NAME = "active.json"
LOCK_NAME = "install.lock"
LOCK_RECORD_NAME = "install.lock.json"
DEFAULT_BASE_URL = "https://api.research.prbe.ai"
MANIFEST_PATH = "/v1/client-version"
PYPI_URL = "https://pypi.org/pypi/probe-research/json"

#: Every network read: the manifest, PyPI.
HTTP_TIMEOUT_S = 5.0
#: At most this much of an answer is read (PyPI's JSON for probe-research was
#: 855,606 bytes on 2026-10-26, and grows with every release).
MAX_ANSWER_BYTES = 32 * 1024 * 1024
#: uv writes it last: an env without it is a half-finished install.
RECEIPT_NAME = "uv-receipt.toml"
#: The new env's import check before the exec (`starts`).
IMPORT_TIMEOUT_S = 30.0
#: One `uv tool install` (four at most: as recorded, without the Python pin,
#: without the `--with` packages an earlier install left out, without any)...
UV_TIMEOUT_S = 300.0
#: ...and all of them together, at most: the service gives its update child
#: 30 min, and the plugins' and pi's steps come after this one. A uv that
#: TIMES OUT ends the install there (the machine or the network, not the
#: package set): the next update tries again.
INSTALL_BUDGET_S = 600.0
#: How long a waiter waits for a live holder before it answers busy.
LOCK_WAIT_S = 120.0
LOCK_POLL_S = 0.5
#: A holder this old, running our update, is stopped (UPDATE_TIMEOUT_S 30 min + 15).
STALE_HOLDER_S = 45 * 60
KILL_GRACE_S = 10.0
#: A rejected version is skipped this long (I1).
REJECT_TTL_S = 24 * 3600
#: The lifeboat acts once the machine has been behind this long, by its own clock.
BEHIND_ACT_S = 12 * 3600
#: ... or once the service has not answered `service.hello` this long (keeper runs).
SERVICE_DOWN_ACT_S = 5 * 60
#: ... and asks the service for a check this often with no session (keeper runs).
KEEPER_CHECK_S = 6 * 3600
#: The manifest is read at most this often in lifeboat mode.
MANIFEST_EVERY_S = 3600
#: A rescue is not started again within this long of the last one.
ACT_RETRY_S = 3600
#: A log file past this is started again.
MAX_LOG_BYTES = 1024 * 1024

#: Set on the new release's process: the env it is to switch to (`probe.core.adopt`).
ADOPT_ENV = "PROBE_UPDATE_ADOPT"
#: The install lock's fd, inherited across the exec.
LOCK_FD_ENV = "PROBE_INSTALL_LOCK_FD"
#: What asked for this update: the report's trigger (`lifeboat` from here).
TRIGGER_ENV = "PROBE_HANDOFF_TRIGGER"
#: The version the machine ran before: the report's `cli.before`.
FROM_ENV = "PROBE_HANDOFF_FROM"
#: A JSON list of the `--with` packages the install had to leave out.
DROPPED_WITH_ENV = "PROBE_HANDOFF_DROPPED_WITH"
NOW_ENV = "PROBE_HANDOFF_NOW"
PYPI_URL_ENV = "PROBE_HANDOFF_PYPI_URL"

EXIT_OK = 0
EXIT_FAILED = 1
EXIT_USAGE = 2
EXIT_INTERNAL = 3


class Result:
    """What `stage1` answered (its "result"), when it did not exec."""

    ADOPT = "adopt"  # PROBE_UPDATE_ADOPT is set: the release adopts, nothing is installed
    NOT_MANAGED = "not_managed"  # no uv tool install of the CLI to update side by side
    BUSY = "busy"  # another live updater holds the install lock
    NO_TARGET = "no_target"  # neither the manifest nor PyPI answered
    UNKNOWN_ACTIVE = "unknown_active"  # the active version could not be read
    CURRENT = "current"  # the newest release is not newer than the active one
    REJECTED = "rejected"  # the newest release was switched back from < 24 h ago
    INSTALL_FAILED = "install_failed"
    #: Installed, but its import check could not run (a timeout, a kill): kept, tried next time.
    UNCHECKED = "unchecked"
    EXEC_FAILED = "exec_failed"


class Trigger:
    KEEPER = "keeper"
    SESSION = "session"
    CLI = "cli"
    #: What a lifeboat rescue reports (`probe.core.adopt`).
    LIFEBOAT = "lifeboat"


LIFEBOAT_TRIGGERS = (Trigger.KEEPER, Trigger.SESSION, Trigger.CLI)
_RELEASE = re.compile(r"^(\d+)\.(\d+)\.(\d+)(?:\.(\d+))?$")
_EXTRA = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$")
_LOOPBACK = ("localhost", "127.0.0.1", "::1")
#: CA bundles tried when the interpreter's own store cannot verify (a python.org
#: build on macOS has none until its `Install Certificates` ran).
_CA_BUNDLES = (
    "/etc/ssl/cert.pem",
    "/etc/ssl/certs/ca-certificates.crt",
    "/etc/pki/tls/certs/ca-bundle.crt",
    "/etc/ssl/ca-bundle.pem",
    "/opt/homebrew/etc/ca-certificates/cert.pem",
    "/usr/local/etc/ca-certificates/cert.pem",
)
_UV_CANDIDATES = (
    ".local/bin/uv",
    ".cargo/bin/uv",
    "/opt/homebrew/bin/uv",
    "/usr/local/bin/uv",
    "/usr/bin/uv",
)


def _log(message: str) -> None:
    with contextlib.suppress(Exception):
        print(f"probe handoff: {message}", file=sys.stderr, flush=True)


def now() -> float:
    """The clock: PROBE_HANDOFF_NOW when a test sets it, else the real time."""
    raw = os.environ.get(NOW_ENV)
    if raw:
        with contextlib.suppress(ValueError):
            return float(raw)
    return time.time()


# -- versions ----------------------------------------------------------------------


def release(version: object) -> tuple | None:
    """`X.Y.Z[.N]` as a 4-tuple, else None (a pre-release, a local tag, garbage)."""
    if not isinstance(version, str):
        return None
    found = _RELEASE.match(version.strip())
    return tuple(int(part or 0) for part in found.groups()) if found else None


def newer(candidate: object, base: object) -> bool:
    """Is `candidate` a release strictly newer than `base`? Either one not a plain release: no."""
    a, b = release(candidate), release(base)
    return bool(a and b and a > b)


# -- paths and files ---------------------------------------------------------------


def lifeboat_dir() -> Path:
    """`~/.local/state/probe/lifeboat` (`probe.service.paths.state_dir()`'s rule)."""
    return Path.home() / ".local" / "state" / "probe" / "lifeboat"


def env_path() -> Path:
    return lifeboat_dir() / "env.json"


def state_path() -> Path:
    return lifeboat_dir() / "state.json"


def acted_path() -> Path:
    return lifeboat_dir() / "acted.json"


def _read_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def _write_json(path: Path, data: dict) -> None:
    """Atomically, mode 0600; the lifeboat's own folder made 0700."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.parent == lifeboat_dir():
        with contextlib.suppress(OSError):
            os.chmod(path.parent, 0o700)
    tmp = path.with_name(f"{path.name}.{os.getpid()}.tmp")
    try:
        with open(os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600), "w", encoding="utf-8") as handle:
            json.dump(data, handle)
        os.replace(tmp, path)
    finally:
        with contextlib.suppress(OSError):
            os.unlink(tmp)


def read_env() -> dict:
    """`L/env.json` (release code writes it), or {}."""
    data = _read_json(env_path())
    return data if data.get("v") == 1 else {}


def read_state() -> dict:
    data = _read_json(state_path())
    if data.get("v") != 1:
        data = {"v": 1}
    for key in ("first_seen_behind", "behind_version", "service_down_since", "last_keeper_check",
                "last_manifest", "last_act"):
        data.setdefault(key, None)
    return data


def write_state(state: dict) -> None:
    _write_json(state_path(), {**state, "v": 1})


def env_python(env: Path) -> Path:
    return env / "bin" / "python"


def _tool_dir(env: dict) -> Path:
    """uv's tool folder: UV_TOOL_DIR, else `uv tool dir`, else uv's default."""
    if env.get("UV_TOOL_DIR"):
        return Path(env["UV_TOOL_DIR"])
    uv = find_uv(None, env)
    if uv:
        with contextlib.suppress(OSError, subprocess.SubprocessError):
            out = subprocess.run([uv, "tool", "dir"], capture_output=True, text=True, timeout=15,
                                 stdin=subprocess.DEVNULL, env=env, check=False)
            lines = (out.stdout or "").strip().splitlines()
            if out.returncode == 0 and lines and os.path.isabs(lines[-1]):
                return Path(lines[-1])
    base = env.get("XDG_DATA_HOME") or str(Path.home() / ".local" / "share")
    return Path(base) / "uv" / "tools"


def find_uv(recorded: object, env: dict) -> str | None:
    """The `uv` binary: the recorded path, else PATH, else where its installers put it."""
    candidates = [recorded] if isinstance(recorded, str) and recorded else []
    found = shutil.which("uv", path=env.get("PATH") or os.defpath)
    if found:
        candidates.append(found)
    for rel in _UV_CANDIDATES:
        candidates.append(rel if rel.startswith("/") else str(Path.home() / rel))
    for candidate in candidates:
        if os.path.isabs(candidate) and os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate
    return None


def env_version(env: Path, *, timeout: float = 30.0) -> str | None:
    """The probe-research version installed in `env`: its dist-info folder's
    name (no interpreter started), else its own interpreter's answer."""
    found = []
    for site in [*env.glob("lib/python3*/site-packages"), *env.glob("Lib/site-packages")]:
        for info in site.glob("probe_research-*.dist-info"):
            version = info.name[len("probe_research-"): -len(".dist-info")]
            if release(version):
                found.append(version)
    if found:
        return max(found, key=release)
    python = env_python(env)
    if not python.exists():
        return None
    try:
        out = subprocess.run(
            [str(python), "-I", "-c", f"from importlib.metadata import version; print(version({DIST!r}))"],
            capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=timeout, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    text = (out.stdout or "").strip()
    return text if out.returncode == 0 and text else None


def complete(env: Path, version: str) -> bool:
    """Is `env` an environment uv finished, of exactly `version`: its
    interpreter, its dist-info and the receipt uv writes last?"""
    return (
        env_python(env).exists()
        and (env / RECEIPT_NAME).is_file()
        and release(env_version(env)) == release(version) is not None
    )


def starts(env: Path) -> tuple[str | None, bool]:
    """Does the new env's own update path import (`probe.core.run`,
    `probe.core.adopt`)? `(None, False)` when it does; else `(what it said,
    broken)`: `broken` when the import itself failed (the release is), not
    when the check could not finish (a timeout on a loaded machine, an
    OSError, a kill by a signal -- the OOM killer: the machine's, so the env
    is kept for the next try). An env that fails is never exec'd: it would
    die before it could reject itself."""
    try:
        done = subprocess.run(
            [str(env_python(env)), "-I", "-c", "import probe.core.run, probe.core.adopt"],
            capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=IMPORT_TIMEOUT_S,
            cwd=str(Path.home()), check=False,
        )
    except subprocess.TimeoutExpired:
        return f"timed out after {IMPORT_TIMEOUT_S:g} s", False
    except (OSError, subprocess.SubprocessError) as exc:
        return f"{type(exc).__name__}: {exc}", False
    if done.returncode == 0:
        return None, False
    if done.returncode < 0:
        return f"killed by signal {-done.returncode}", False
    tail = (done.stderr or "").strip().splitlines()[-1:] or [f"exit {done.returncode}"]
    return tail[0][:300], True


class Layout:
    """Where the CLI's uv tool install lives: the tool path and the versions folder."""

    def __init__(self, tools: Path) -> None:
        self.tools = tools
        self.tool_env = tools / DIST
        self.root = tools.parent / VERSIONS_DIRNAME

    def usable(self) -> bool:
        """A uv tool env (a folder or our link) at the tool path, the versions
        folder on its filesystem (a switch is one rename), POSIX."""
        if os.name == "nt" or fcntl is None:
            return False
        if not (self.tool_env.is_symlink() or self.tool_env.is_dir()):
            return False
        try:
            self.root.mkdir(parents=True, exist_ok=True)
            return os.stat(self.root).st_dev == os.stat(self.tools).st_dev
        except OSError:
            return False

    def record(self) -> dict:
        return _read_json(self.root / ACTIVE_NAME)

    def active_version(self) -> str | None:
        """The version the tool path runs now: the dist-info of the env it
        resolves to (a `uv tool upgrade` through the link moves it, not the
        folder's name), else its version folder's name."""
        if self.tool_env.exists():
            found = env_version(self.tool_env)
            if found:
                return found
        if self.tool_env.is_symlink():
            with contextlib.suppress(OSError):
                target = Path(os.readlink(self.tool_env))
                if not target.is_absolute():
                    target = self.tool_env.parent / target
                if release(target.parent.name):
                    return target.parent.name
        return None

    def dropped_with(self) -> list:
        """The `--with` packages an earlier install had to leave out
        (`active.json` `dropped_with`): tried again first, every install."""
        value = self.record().get("dropped_with")
        return [str(item) for item in value if isinstance(item, str) and item.strip()] \
            if isinstance(value, list) else []


def rejected_at(record: dict, version: str) -> float | None:
    """When `version` was switched back from (`active.json` `rejected`: today's
    `{"at", "reason"}`, or an older bare timestamp), else None."""
    marks = record.get("rejected")
    if not isinstance(marks, dict):
        return None
    mark = marks.get(version)
    if isinstance(mark, dict):
        mark = mark.get("at")
    return float(mark) if isinstance(mark, (int, float)) and not isinstance(mark, bool) else None


def rejected_recently(record: dict, version: str, at: float | None = None) -> bool:
    """Was `version` rejected less than REJECT_TTL_S ago? A rejected version
    never blocks a newer one: only the newest release is ever the target."""
    when = rejected_at(record, version)
    return when is not None and (now() if at is None else at) - when < REJECT_TTL_S


# -- the network -------------------------------------------------------------------


def _proxies(env: dict, host: str) -> dict:
    if host in _LOOPBACK:
        return {}
    skip = env.get("no_proxy") or env.get("NO_PROXY") or ""
    for entry in (part.strip().lstrip(".") for part in skip.split(",")):
        if entry == "*" or (entry and (host == entry or host.endswith("." + entry))):
            return {}
    found = {}
    for scheme in ("http", "https"):
        value = env.get(f"{scheme}_proxy") or env.get(f"{scheme.upper()}_PROXY") \
            or env.get("all_proxy") or env.get("ALL_PROXY")
        if value:
            found[scheme] = value
    return found


def _contexts(env: dict):
    """TLS contexts to try in turn (made as they are asked for): the configured
    bundle, the interpreter's own store, the system bundles, certifi."""
    import ssl

    cafile = env.get("SSL_CERT_FILE") or env.get("REQUESTS_CA_BUNDLE")
    if cafile and os.path.isfile(cafile):
        with contextlib.suppress(ssl.SSLError, OSError):
            yield ssl.create_default_context(cafile=cafile)
    yield ssl.create_default_context()
    bundles = [path for path in _CA_BUNDLES if os.path.isfile(path)]
    with contextlib.suppress(Exception):
        import certifi  # type: ignore[import-not-found]

        bundles.append(certifi.where())
    for bundle in bundles:
        with contextlib.suppress(ssl.SSLError, OSError):
            yield ssl.create_default_context(cafile=bundle)


def fetch_json(url: str, env: dict, *, timeout: float = HTTP_TIMEOUT_S) -> dict | None:
    """GET `url` as a JSON object (through the proxy `env` names), or None."""
    import ssl
    import urllib.error
    import urllib.parse
    import urllib.request

    try:
        host = urllib.parse.urlsplit(url).hostname or ""
        contexts = _contexts(env) if url.startswith("https:") else [None]
        for context in contexts:
            handlers = [urllib.request.ProxyHandler(_proxies(env, host))]
            if context is not None:
                handlers.append(urllib.request.HTTPSHandler(context=context))
            opener = urllib.request.build_opener(*handlers)
            request = urllib.request.Request(url, headers={
                "Accept": "application/json", "User-Agent": f"probe-handoff/{HANDOFF_VERSION}"})
            try:
                with opener.open(request, timeout=timeout) as answer:
                    data = json.loads(answer.read(MAX_ANSWER_BYTES).decode("utf-8"))
                return data if isinstance(data, dict) else None
            except urllib.error.URLError as exc:
                if isinstance(getattr(exc, "reason", None), ssl.SSLCertVerificationError):
                    continue  # the next store may verify it
                return None
            except ssl.SSLCertVerificationError:
                continue
    except Exception:  # noqa: BLE001 -- http.client's own errors, a bad proxy URL, garbage: no answer
        return None
    return None


def latest_release(base_url: str | None, env: dict) -> tuple[str | None, str]:
    """`(newest CLI release, where it was read)`: the manifest's `cli.latest`,
    else PyPI's `info.version`; `(None, "")` when neither answered with a release."""
    base = (base_url or DEFAULT_BASE_URL).rstrip("/")
    manifest = fetch_json(base + MANIFEST_PATH, env)
    cli = manifest.get("cli") if isinstance(manifest, dict) else None
    latest = cli.get("latest") if isinstance(cli, dict) else None
    if release(latest):
        return latest, "manifest"
    pypi = fetch_json(os.environ.get(PYPI_URL_ENV) or PYPI_URL, env)
    info = pypi.get("info") if isinstance(pypi, dict) else None
    latest = info.get("version") if isinstance(info, dict) else None
    if release(latest):
        return latest, "pypi"
    return None, ""


# -- processes ----------------------------------------------------------------------


def proc_start(pid: int) -> str | None:
    """`pid`'s kernel start time (`probe.service.procid`'s rule), or None when
    it is gone (a zombie included: it has exited, only not been reaped)."""
    if pid <= 0:
        return None
    if Path("/proc/self/stat").exists():
        try:
            raw = Path(f"/proc/{pid}/stat").read_text(encoding="utf-8", errors="replace")
        except OSError:
            return None
        close = raw.rfind(")")
        fields = raw[close + 2:].split()
        if close < 0 or len(fields) < 20 or fields[0] in ("Z", "X"):
            return None
        return fields[19]
    try:
        out = subprocess.run(["ps", "-ww", "-o", "stat=,lstart=", "-p", str(pid)], capture_output=True,
                             text=True, timeout=5, check=False,
                             env={**os.environ, "LC_ALL": "C", "TZ": "UTC0"}).stdout
    except (OSError, subprocess.SubprocessError):
        return None
    tokens = out.split()
    if len(tokens) < 6 or tokens[0].startswith("Z"):
        return None
    return " ".join(tokens[1:6])


def proc_argv(pid: int) -> list | None:
    """`pid`'s argv: /proc's, else `ps`'s command split on spaces. None when unreadable."""
    try:
        raw = Path(f"/proc/{pid}/cmdline").read_bytes()
        return [part.decode("utf-8", "replace") for part in raw.split(b"\0") if part] or None
    except OSError:
        pass
    try:
        out = subprocess.run(["ps", "-ww", "-o", "command=", "-p", str(pid)], capture_output=True, text=True,
                             timeout=5, check=False).stdout
    except (OSError, subprocess.SubprocessError):
        return None
    return out.split() or None


def _own_cmdline() -> str:
    return " ".join(proc_argv(os.getpid()) or getattr(sys, "orig_argv", sys.argv))


#: What holds the install lock, by its argv (`holder_kind`).
UPDATE_CHILD = "update_child"  # `<python> -I -m probe.core.run update`
HANDOFF_RUN = "handoff"  # this file, run as a script
CLI_UPDATE = "cli_update"  # `probe update`, `probe wizard ... --action update`, `version_refresh --apply`
#: The CLI's root options that take a value (skipped to find its command).
_ROOT_VALUE_OPTIONS = ("--base-url", "--spool-dir")


def _cli_update(rest: list) -> bool:
    """`rest` (argv after `probe` / `-m probe.cli`) is an update: `update`, or
    `wizard` with `--action update`."""
    words: list = []
    skip = False
    for token in rest:
        if skip:
            skip = False
            continue
        if token in _ROOT_VALUE_OPTIONS:
            skip = True
            continue
        if not token.startswith("-"):
            words.append(token)
    if not words:
        return False
    if words[0] == "update":
        return True
    if words[0] != "wizard":
        return False
    for index, token in enumerate(rest):
        if token == "--action=update" or (token == "--action" and rest[index + 1: index + 2] == ["update"]):
            return True
    return False


def holder_kind(argv: list | None) -> str | None:
    """Is `argv` one of our updates, and which (matched token by token, never
    as a substring of something else's command line)? None: not ours."""
    if not argv:
        return None
    for index, token in enumerate(argv):
        if token == "-m" and argv[index + 1: index + 3] == ["probe.core.run", "update"]:
            return UPDATE_CHILD
        if os.path.basename(token) == "handoff.py":
            return HANDOFF_RUN
        if token == "-m" and argv[index + 1: index + 2] == ["probe.cli.version_refresh"] \
                and ({"--apply", "--apply-if-newer"} & set(argv[index + 2:])):
            return CLI_UPDATE
        if token == "-m" and argv[index + 1: index + 2] == ["probe.cli"] and _cli_update(argv[index + 2:]):
            return CLI_UPDATE
        if os.path.basename(token) == "probe" and _cli_update(argv[index + 1:]):
            return CLI_UPDATE
    return None


# -- the install lock ----------------------------------------------------------------


#: {lock path: fd} this process holds (re-entrant), the inherited one included.
_held: dict = {}


def lock_path(root: Path) -> Path:
    return Path(root) / LOCK_NAME


def _same_file(fd: int, path: Path) -> bool:
    try:
        a, b = os.fstat(fd), os.stat(path)
    except OSError:
        return False
    return (a.st_dev, a.st_ino) == (b.st_dev, b.st_ino)


def _inherited(path: Path) -> int | None:
    """The lock fd an earlier stage handed across the exec, when it is this lock's."""
    raw = os.environ.get(LOCK_FD_ENV, "")
    if not raw.isdigit():
        return None
    fd = int(raw)
    return fd if _same_file(fd, path) else None


def holds(root: Path) -> bool:
    """Does this process hold the install lock (taken here, or inherited)?"""
    path = lock_path(root)
    fd = _held.get(str(path))
    if fd is not None and _same_file(fd, path):
        return True
    return _inherited(path) is not None


def _write_holder(root: Path) -> None:
    """The holder record: who, since when by the wall clock (`at`) and by the
    awake clock (`mono`: time.monotonic(), system-wide since boot on Linux and
    macOS, stopped while the machine sleeps)."""
    with contextlib.suppress(OSError):
        _write_json(Path(root) / LOCK_RECORD_NAME, {
            "pid": os.getpid(), "start": proc_start(os.getpid()), "cmd": _own_cmdline()[:2000],
            "at": time.time(), "mono": time.monotonic()})


def _held_long(record: dict) -> bool:
    """Has the holder held the lock STALE_HOLDER_S both by the wall clock and
    awake (a laptop asleep over a running update does not age it)? A record
    without `mono` is aged by the wall clock alone."""
    try:
        at = float(record.get("at"))
    except (TypeError, ValueError):
        return False
    if time.time() - at < STALE_HOLDER_S:
        return False
    mono = record.get("mono")
    if isinstance(mono, (int, float)) and not isinstance(mono, bool):
        return time.monotonic() - mono >= STALE_HOLDER_S  # negative after a reboot: not stale
    return True


def _stop_stale_holder(root: Path) -> bool:
    """Stop the holder named in the lock record when it is one of our updates
    and has held the lock STALE_HOLDER_S (`_held_long`): SIGTERM, then SIGKILL
    past KILL_GRACE_S -- to its process group only when it leads one of its
    own (the service starts its update child that way), else to it alone (a
    child in the service's group must never take the service with it; the
    CLI's own update, a person's terminal, always alone). True when it did."""
    record = _read_json(Path(root) / LOCK_RECORD_NAME)
    try:
        pid = int(record.get("pid"))
    except (TypeError, ValueError):
        return False
    if pid <= 1 or pid == os.getpid() or not _held_long(record):
        return False
    start = proc_start(pid)
    if start is None or (record.get("start") and record.get("start") != start):
        return False  # gone, or the pid is another process now
    kind = holder_kind(proc_argv(pid))
    if kind is None:
        return False
    _log(f"the install lock's holder {pid} ({kind}) has held it {(time.time() - float(record['at'])) / 60:.0f} min:"
         " stopping it")
    leads = False
    if kind != CLI_UPDATE:
        with contextlib.suppress(OSError):
            leads = os.getpgid(pid) == pid and pid != os.getpgrp()

    def signal_it(sig: int) -> None:
        with contextlib.suppress(ProcessLookupError, PermissionError, OSError):
            if leads:
                os.killpg(pid, sig)
            else:
                os.kill(pid, sig)

    signal_it(signal.SIGTERM)
    deadline = time.monotonic() + KILL_GRACE_S
    while time.monotonic() < deadline and proc_start(pid) == start:
        time.sleep(0.2)
    if proc_start(pid) == start:
        signal_it(signal.SIGKILL)
    return True


def take_lock(root: Path, *, wait_s: float = LOCK_WAIT_S) -> int | None:
    """Take the install lock: its fd, or None when a live holder kept it for
    `wait_s` (a stale one of ours is stopped meanwhile). Not re-entrant: see
    `install_lock`."""
    if fcntl is None:
        return None
    path = lock_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_RDWR | os.O_CREAT, 0o600)
    deadline = time.monotonic() + max(0.0, wait_s)
    looked = 0.0
    while True:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            break
        except BlockingIOError:
            pass
        except OSError as exc:
            # A filesystem without locks (some NFS homes): unlocked, as every
            # install was before this lock existed, rather than never again.
            _log(f"the install lock cannot be taken here ({exc}); going on without it")
            break
        if time.monotonic() - looked >= 5.0:
            looked = time.monotonic()
            if _stop_stale_holder(root):
                continue
        if time.monotonic() >= deadline:
            os.close(fd)
            return None
        time.sleep(LOCK_POLL_S)
    _held[str(path)] = fd
    _write_holder(root)
    return fd


def release_lock(fd: int | None) -> None:
    if fd is None:
        return
    for key, held in list(_held.items()):
        if held == fd:
            del _held[key]
    with contextlib.suppress(OSError):
        os.close(fd)  # the flock goes with its last fd


def release_inherited(root: Path) -> None:
    """Close the lock fd an exec handed over (the switch is done) and forget
    it -- only when it IS `root`'s install lock (an fd number from the
    environment could name anything this process opened since)."""
    raw = os.environ.pop(LOCK_FD_ENV, "")
    if not raw.isdigit():
        return
    fd = int(raw)
    if not _same_file(fd, lock_path(root)):
        return
    for key, held in list(_held.items()):
        if held == fd:
            del _held[key]
    with contextlib.suppress(OSError):
        os.close(fd)


class LockBusy(RuntimeError):
    """Another live updater holds the install lock."""


@contextlib.contextmanager
def install_lock(root: Path, *, wait_s: float = LOCK_WAIT_S):
    """Hold the install lock for the block. Re-entrant: a process that holds it
    (taken here, or inherited across the hand-off's exec) takes nothing more.
    Raises LockBusy when a live holder kept it for `wait_s`. Without `fcntl`
    (Windows) it holds nothing."""
    if fcntl is None or holds(root):
        yield
        return
    fd = take_lock(root, wait_s=wait_s)
    if fd is None:
        raise LockBusy(f"another update holds {lock_path(root)}")
    try:
        yield
    finally:
        release_lock(fd)


# -- stage 1 -----------------------------------------------------------------------


def _child_env(cfg: dict) -> dict:
    """This process's environment, with what env.json recorded from the login
    shell (index, proxy, CA) for anything it does not set itself."""
    env = dict(os.environ)
    for name, value in (cfg.get("index_env") or {}).items():
        if isinstance(name, str) and isinstance(value, str) and name not in env:
            env[name] = value
    return env


def _install_inputs(cfg: dict, given: dict | None) -> dict:
    """extras, `--with` packages, the Python request and uv: the caller's, else env.json's."""
    source = given if isinstance(given, dict) else cfg
    extras = [e for e in source.get("extras") or [] if isinstance(e, str) and _EXTRA.match(e)]
    with_ = [w for w in source.get("with") or [] if isinstance(w, str) and w.strip()]
    python = source.get("python_request")
    return {
        "extras": sorted(set(extras) | {"all"}),
        "with": with_,
        "python_request": python if isinstance(python, str) and python else None,
        "uv": source.get("uv") or cfg.get("uv"),
    }


def install_command(uv: str, version: str, extras: list, with_: list, python: str | None) -> list[str]:
    command = [uv, "tool", "install", "--refresh-package", DIST, f"{DIST}[{','.join(extras)}]=={version}"]
    for requirement in with_:
        command += ["--with", requirement]
    if python:
        command += ["--python", python]
    return command


def requirement_name(requirement: str) -> str:
    """A requirement's distribution name, normalized (`Foo_Bar>=1` -> `foo-bar`)."""
    found = re.match(r"\s*([A-Za-z0-9][A-Za-z0-9._-]*)", requirement or "")
    return re.sub(r"[-_.]+", "-", found.group(1)).lower() if found else (requirement or "").strip().lower()


def attempts(with_: list, retried: list, pinned: str | None) -> list:
    """The installs to try, in order, each `(--with packages, --python)`: as
    recorded (the packages an earlier install left out, `retried`, again
    first), then without the Python pin, then without `retried`, then without
    any `--with` -- the last resort on ANY failure (a deleted local path, a
    repository gone, a build that fails, a conflict: the CLI must not stay
    behind for a package of the person's; a wrong drop heals, as it is tried
    again first next time). The same one twice is tried once."""
    names = {requirement_name(item) for item in with_}
    every = [*with_, *(item for item in retried if requirement_name(item) not in names)]
    found: list = []
    for packages, python in ((every, pinned), (every, None), (list(with_), None), ([], None)):
        if (packages, python) not in found:
            found.append((packages, python))
    return found


def _is_active(layout: Layout, env: Path) -> bool:
    try:
        return env.resolve() == layout.tool_env.resolve()
    except OSError:
        return True  # unknown: treated as the active one, never deleted


def discard(layout: Layout, version: str) -> None:
    """Delete `probe-versions/<version>` (a failed or broken install), never the active env."""
    holder = layout.root / version
    if not _is_active(layout, holder / DIST):
        shutil.rmtree(holder, ignore_errors=True)


def install(layout: Layout, version: str, inputs: dict, env: dict) -> tuple[Path | None, str, list]:
    """`probe-versions/<version>/probe-research`, installed by uv, a success
    only when uv exits 0 AND leaves a complete env (`complete`), tried in the
    order `attempts` gives (the `--with` packages an earlier install left out,
    `dropped_with`, again first; without any `--with` last), within
    INSTALL_BUDGET_S; a uv that times out ends it. Returns `(env, "", --with
    left out)` or `(None, what uv said, [])`, the folder deleted."""
    holder = layout.root / version
    target = holder / DIST
    if _is_active(layout, target):
        return None, f"{target} is the active environment and not a complete {version}", []
    uv = find_uv(inputs.get("uv"), env)
    if uv is None:
        return None, "uv was not found", []
    tries = attempts(list(inputs["with"]), layout.dropped_with(), inputs["python_request"])
    every = tries[0][0]
    said = ""
    budget_ends = time.monotonic() + INSTALL_BUDGET_S
    for packages, pinned in tries:
        left = min(UV_TIMEOUT_S, budget_ends - time.monotonic())
        if left <= 0:
            said = f"the install ran out of its {INSTALL_BUDGET_S:g} s ({said})"
            break
        shutil.rmtree(holder, ignore_errors=True)  # a half-finished earlier try
        holder.mkdir(parents=True, exist_ok=True)
        command = install_command(uv, version, inputs["extras"], packages, pinned)
        child = {**env, "UV_TOOL_DIR": str(holder), "UV_TOOL_BIN_DIR": str(holder / ".bin")}
        _log("running " + " ".join(command[1:]))
        exit_code = None
        try:
            done = subprocess.run(command, env=child, stdin=subprocess.DEVNULL, capture_output=True, text=True,
                                  timeout=left, check=False)
            exit_code = done.returncode
            said = ((done.stderr or "") + (done.stdout or "")).strip()[-1500:] or f"exit {done.returncode}"
        except subprocess.TimeoutExpired:
            said = f"`uv tool install` timed out after {left:.0f} s; the next update tries again"
            _log(said)
            break  # the machine or the network, not the package set: no other try helps now
        except (OSError, subprocess.SubprocessError) as exc:
            said = f"{type(exc).__name__}: {exc}"
        if exit_code == 0 and complete(target, version):
            return target, "", [item for item in every if item not in packages]
        if exit_code == 0:
            said = f"`uv tool install` exited 0 but left no complete {version} env: {said}"
        _log(f"`uv tool install` did not leave {version}: {said}")
    discard(layout, version)
    return None, said, []


def _exec(python: Path, argv: list, env: dict, fd: int, before_exec) -> None:
    """Become `python -I <argv>` (same pid, same stdio), the lock fd inherited."""
    os.set_inheritable(fd, True)
    try:
        if before_exec is not None:
            before_exec()
        with contextlib.suppress(Exception):
            sys.stdout.flush()
        with contextlib.suppress(Exception):
            sys.stderr.flush()
        os.execve(str(python), [str(python), "-I", *argv], env)
    except BaseException:
        with contextlib.suppress(OSError):
            os.set_inheritable(fd, False)
        raise


UPDATE_ARGV = ("-m", "probe.core.run", "update")


def stage1(
    trigger: str,
    *,
    argv: list | tuple | None = None,
    before_exec=None,
    tools: str | os.PathLike | None = None,
    base_url: str | None = None,
    install_inputs: dict | None = None,
    current: str | None = None,
    wait_s: float = LOCK_WAIT_S,
    acted: dict | None = None,
) -> dict:
    """Stage 1 of every update: when a release newer than the active one
    exists (and is not rejected < 24 h ago), install it beside the active one
    and exec its `python -I <argv>` (default `-m probe.core.run update`) with
    PROBE_UPDATE_ADOPT, under the install lock, handed over. That never
    returns. Anything else returns `{"result": Result.*, ...}` and the caller
    goes on in-process, as before.

    `tools`, `base_url`, `install_inputs` (extras, with, python_request, uv)
    and `current` (the caller's own version, when the active one cannot be
    read) override env.json; `before_exec` runs just before the exec (release
    a lock of the caller's, leave a terminal screen); `acted` is written to
    `L/acted.json` just before it (a lifeboat rescue)."""
    if os.environ.get(ADOPT_ENV):
        return {"result": Result.ADOPT}
    cfg = read_env()
    env = _child_env(cfg)
    folder = Path(tools) if tools else Path(cfg["tools"]) if isinstance(cfg.get("tools"), str) else _tool_dir(env)
    layout = Layout(folder)
    if not layout.usable():
        return {"result": Result.NOT_MANAGED}
    fd = take_lock(layout.root, wait_s=wait_s)
    if fd is None:
        return {"result": Result.BUSY, "detail": f"another update holds {lock_path(layout.root)}"}
    try:
        active = layout.active_version() or current
        latest, source = latest_release(base_url or cfg.get("base_url"), env)
        answer = {"latest": latest, "active": active, "source": source}
        if latest is None:
            return {"result": Result.NO_TARGET, **answer}
        if not release(active):
            return {"result": Result.UNKNOWN_ACTIVE, **answer}
        if not newer(latest, active):
            return {"result": Result.CURRENT, **answer}
        if rejected_recently(layout.record(), latest):
            return {"result": Result.REJECTED, **answer}
        target = layout.root / latest / DIST
        dropped: list = []
        if not complete(target, latest):
            installed, said, dropped = install(layout, latest, _install_inputs(cfg, install_inputs), env)
            if installed is None:
                return {"result": Result.INSTALL_FAILED, "detail": said, **answer}
        problem, broken = starts(target)
        if problem and broken:
            # It would die before it could reject itself: never exec'd, and
            # deleted, so the next update installs it afresh.
            discard(layout, latest)
            return {"result": Result.INSTALL_FAILED, "detail": f"CLI {latest} does not start: {problem}", **answer}
        if problem:
            # The check could not finish (a loaded machine): kept, tried next time.
            return {"result": Result.UNCHECKED,
                    "detail": f"CLI {latest} could not be checked ({problem}); the next update tries again", **answer}
        exec_env = {**env, ADOPT_ENV: str(target), LOCK_FD_ENV: str(fd), TRIGGER_ENV: trigger, FROM_ENV: active}
        exec_env.pop(DROPPED_WITH_ENV, None)
        if dropped:
            exec_env[DROPPED_WITH_ENV] = json.dumps(dropped)

        def before() -> None:
            if acted is not None:
                _write_json(acted_path(), {**acted, "from": active, "to": latest})
            if before_exec is not None:
                before_exec()

        _log(f"CLI {active} -> {latest} ({source}): handing the update to {latest}")
        try:
            _exec(env_python(target), list(argv or UPDATE_ARGV), exec_env, fd, before)
        except OSError as exc:
            return {"result": Result.EXEC_FAILED, "detail": f"{type(exc).__name__}: {exc}", **answer}
        raise AssertionError("unreachable: execve returned")  # pragma: no cover
    finally:
        release_lock(fd)


# -- the lifeboat ------------------------------------------------------------------


def _log_fd() -> int:
    path = lifeboat_dir() / "handoff.log"
    path.parent.mkdir(parents=True, exist_ok=True)
    with contextlib.suppress(OSError):
        if path.stat().st_size > MAX_LOG_BYTES:
            path.unlink()
    return os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)


def _detach(argv: list, env: dict | None = None) -> bool:
    """Start `argv` in a session of its own, its output to the lifeboat's log."""
    try:
        fd = _log_fd()
    except OSError:
        fd = subprocess.DEVNULL
    try:
        subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=fd, stderr=fd, cwd=str(Path.home()),
                         env=env, close_fds=True, start_new_session=True)
        return True
    except (OSError, ValueError) as exc:
        _log(f"could not start {argv[:3]}: {exc}")
        return False
    finally:
        if isinstance(fd, int) and fd >= 0:
            with contextlib.suppress(OSError):
                os.close(fd)


def service_answers(socket_path: object, *, timeout: float = 5.0) -> bool | None:
    """Did the service at `socket_path` answer `service.hello`? None: no path known."""
    import socket

    if not isinstance(socket_path, str) or not socket_path or not hasattr(socket, "AF_UNIX"):
        return None
    hello = {"jsonrpc": "2.0", "id": 1, "method": "service.hello",
             "params": {"client": "cli", "client_version": f"handoff-{HANDOFF_VERSION}", "api": 1}}
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as conn:
            conn.settimeout(timeout)
            conn.connect(socket_path)
            conn.sendall((json.dumps(hello) + "\n").encode("utf-8"))
            buffer = b""
            while b"\n" not in buffer and len(buffer) < 1024 * 1024:
                chunk = conn.recv(65536)
                if not chunk:
                    return False
                buffer += chunk
        message = json.loads(buffer.split(b"\n", 1)[0].decode("utf-8"))
        return isinstance(message, dict) and message.get("id") == 1
    except (OSError, ValueError):
        return False


def _this_file() -> str:
    return os.path.abspath(__file__)


def lifeboat(trigger: str) -> int:
    """One lifeboat run (`lifeboat.sh <trigger>`; the keeper's every minute).

    Cheap first: env.json, state.json and the tool link. It acts only for a
    managed CLI with automatic updates on:
      (a) behind (newest > active, not rejected) for BEHIND_ACT_S by its own
          clock -> stage 1, detached, trigger `lifeboat`;
      (b) keeper runs, behind: the service has not answered `service.hello`
          for SERVICE_DOWN_ACT_S -> (a) now. It only brings the newest
          release's rescue forward, never anything else: the service exits
          when no session needs it, so a silent socket is most often an idle
          machine, and the cost of reading it as down is an earlier update.
          (Switching back after a bad switch is the guard's, in release code.)
      (c) keeper runs: no check of its own for KEEPER_CHECK_S -> ask the
          service for one (`probe.service.client check-now --trigger keeper`).
    The clocks are its own (`L/state.json`), never the service's records."""
    cfg = read_env()
    if not cfg or cfg.get("auto_update") is not True or cfg.get("managed") is not True:
        return EXIT_OK
    at = now()
    state = read_state()
    env = _child_env(cfg)
    layout = Layout(Path(cfg["tools"]) if isinstance(cfg.get("tools"), str) else _tool_dir(env))
    active = layout.active_version()
    last = state.get("last_manifest") if isinstance(state.get("last_manifest"), dict) else None
    latest = last.get("latest") if last else None
    if not last or not isinstance(last.get("at"), (int, float)) or at - last["at"] >= MANIFEST_EVERY_S \
            or at < last["at"]:
        # Tried at most hourly, answered or not: an offline machine must not
        # spend two network timeouts every keeper minute.
        fetched, _source = latest_release(cfg.get("base_url"), env)
        latest = fetched or latest
        state["last_manifest"] = {"latest": latest, "at": at}
    known = release(latest) is not None and release(active) is not None
    behind = known and newer(latest, active) and not rejected_recently(layout.record(), latest, at)
    if behind:
        if not isinstance(state.get("first_seen_behind"), (int, float)) or state["first_seen_behind"] > at:
            state["first_seen_behind"] = at
        state["behind_version"] = latest
    elif known:
        state["first_seen_behind"] = None
        state["behind_version"] = None
    last_act = state.get("last_act") if isinstance(state.get("last_act"), dict) else {}
    # The hour between rescues is for trying the SAME release again: a newer
    # one than the last rescue went for (newest wins) is tried at once.
    acted_lately = isinstance(last_act.get("at"), (int, float)) and 0 <= at - last_act["at"] < ACT_RETRY_S \
        and not newer(latest, last_act.get("to"))
    act: str | None = None
    if behind and not acted_lately and at - state["first_seen_behind"] >= BEHIND_ACT_S:
        act = "behind"
    check = False
    if trigger == Trigger.KEEPER:
        answered = service_answers(cfg.get("socket"))
        if answered is True:
            state["service_down_since"] = None
        elif answered is False:
            since = state.get("service_down_since")
            if not isinstance(since, (int, float)) or since > at:
                state["service_down_since"] = at
            if act is None and behind and not acted_lately \
                    and at - state["service_down_since"] >= SERVICE_DOWN_ACT_S:
                act = "service_down"
        last_check = state.get("last_keeper_check")
        if act is None and (not isinstance(last_check, (int, float)) or at - last_check >= KEEPER_CHECK_S
                            or at < last_check):
            check = True
            state["last_keeper_check"] = at
    if act is not None:
        state["last_act"] = {"at": at, "reason": act, "from": active, "to": latest}
    write_state(state)
    if act is not None:
        _detach([sys.executable or "python3", "-I", _this_file(), "--stage1", "--trigger", Trigger.LIFEBOAT,
                 "--reason", act])
    elif check:
        active_python = cfg.get("active_python")
        if isinstance(active_python, str) and os.path.isfile(active_python):
            _detach([active_python, "-I", "-m", "probe.service.client", "check-now", "--trigger", Trigger.KEEPER],
                    env)
    return EXIT_OK


# -- the command line ----------------------------------------------------------------


def selftest() -> int:
    """It parses, its constants are what they say, and what its modes import loads."""
    import socket  # noqa: F401
    import ssl  # noqa: F401
    import urllib.request  # noqa: F401

    assert isinstance(HANDOFF_VERSION, int) and HANDOFF_VERSION >= 1
    assert newer("1.0.10", "1.0.9") and not newer("1.0.0rc1", "0.9.0")
    if os.name != "nt" and fcntl is None:
        return EXIT_FAILED
    return EXIT_OK


def _arg(args: list, name: str) -> str | None:
    if name in args:
        index = args.index(name)
        if index + 1 < len(args):
            return args[index + 1]
    return None


def main(argv: list | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    try:
        if "--selftest" in args:
            return selftest()
        trigger = _arg(args, "--trigger") or Trigger.CLI
        if "--lifeboat" in args:
            if trigger not in LIFEBOAT_TRIGGERS:
                _log(f"unknown trigger {trigger!r}")
                return EXIT_USAGE
            return lifeboat(trigger)
        if "--stage1" in args:
            reason = _arg(args, "--reason")
            acted = {"at": now(), "reason": reason, "trigger": trigger} if reason else None
            answer = stage1(trigger, acted=acted)
            _log(f"stage 1: {answer}")
            failed = answer.get("result") in (Result.INSTALL_FAILED, Result.EXEC_FAILED)
            return EXIT_FAILED if failed else EXIT_OK
        _log("usage: handoff.py --selftest | --stage1 --trigger T [--reason R] | --lifeboat --trigger T")
        return EXIT_USAGE
    except Exception as exc:  # noqa: BLE001 -- its own bug: the wrapper tries known-good
        _log(f"internal error: {type(exc).__name__}: {exc}")
        return EXIT_INTERNAL


if __name__ == "__main__":
    raise SystemExit(main())
