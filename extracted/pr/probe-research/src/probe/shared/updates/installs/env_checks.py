"""check a version env is a complete, working CLI (selftest, dist-info version)."""

from __future__ import annotations
import errno
import re
import signal
import subprocess
from pathlib import Path

from .. import handoff
#: A check killed by one of these could not finish (the OOM killer's SIGKILL, a
#: shutdown's SIGTERM): the machine's, UNKNOWN. Any other signal (SIGSEGV,
#: SIGBUS, SIGABRT, SIGILL) is the env's own crash: BROKEN.
UNKNOWN_SIGNALS = frozenset({int(getattr(signal, "SIGKILL", 9)), int(signal.SIGTERM)})
#: A check that could not be spawned for one of these is the machine's (no
#: process slot, no memory): UNKNOWN. Any other (ENOEXEC, EACCES on the env's
#: own interpreter) is the env's: BROKEN.
UNKNOWN_SPAWN_ERRNOS = frozenset({errno.EAGAIN, errno.ENOMEM})


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
from probe.shared.updates.installs.layout import DIST  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.updates.installs.link import env_python  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.updates.installs.shims import RECEIPT  # noqa: E402 -- pieces need each other; the front door loads this one first
