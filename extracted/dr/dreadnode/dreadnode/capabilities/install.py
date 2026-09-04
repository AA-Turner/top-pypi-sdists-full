"""Install capability dependencies into the SDK runtime.

Runs only in sandbox runtimes, after the project capability sync completes
and before ``Capability.discover`` registers components — so any preflight
``checks:`` see installed binaries.

Pipeline (per-boot):

1. ``packages`` — apt-get per capability. Skipped when the install marker
   is already present in the capability's cache directory, and skipped again
   when dpkg already reports every declared package as installed — ``apt-get
   update`` reaches the archives unconditionally, so a pre-baked image must
   not enter this step at all.
2. ``python`` — combined ``uv pip install`` (or ``python -m pip install``)
   across every capability's pins, targeting the active virtualenv when there
   is one and the system interpreter (via sudo) when there is not. Runs every
   boot so the environment re-resolves when the binding set changes; pip is
   fast on already-satisfied specs.
3. ``scripts`` — bash scripts per capability, in declaration order. Skipped
   when the install marker is already present.

A successful packages+scripts pass writes ``.dreadnode-installed`` into the
capability's cache directory. ``CapabilitySyncClient`` atomically replaces
that directory whenever the capability's runtime_digest changes, so the
marker disappears with the directory and a fresh install runs automatically
on the next boot — no extra cache bookkeeping required.

See specs/capabilities/runtime.md (CAP-INST-*) and
packages/docs/src/content/docs/capabilities/dependencies-and-checks.mdx.
"""

import contextlib
import os
import shutil
import subprocess
import sys
import time
import typing as t
from dataclasses import dataclass, field
from pathlib import Path

from loguru import logger

from dreadnode.capabilities.types import DependencySpec

# Per-step subprocess timeout. Heavy installs (Caido, Burp, large pip
# resolutions) need a generous budget; ``checks:`` is the 5s fast surface.
_INSTALL_TIMEOUT_SECONDS = 600

# `dpkg-query` reads the local status database and never touches the network,
# so it needs a fraction of the install budget.
_DPKG_QUERY_TIMEOUT_SECONDS = 30

# Sealed installs get a much smaller budget than the 600s connected one.
# Nothing legitimately downloads in sealed mode, so a step that takes minutes
# is waiting on a network that will not answer. A deny-all policy that DROPs
# rather than REJECTs turns every such wait into the full timeout, which is
# how one unreachable host becomes ten minutes of boot; capping it keeps the
# outcome the same whether the network drops, refuses, or blackholes DNS.
_SEALED_TIMEOUT_SECONDS = 180

# Aggregate ceiling for one install pass. The per-step timeouts above bound a
# single command; nothing bounded the pass, so a capability set with several
# slow steps could run for tens of minutes while the platform's readiness budget
# expired and reclaimed the sandbox underneath it. Capping the pass instead
# means installs get cut short and report unmet prerequisites through
# ``checks:`` — a runtime that comes up degraded, rather than one that never
# comes up at all.
#
# Sized from the platform's own readiness budget when it tells us, so the two
# cannot drift: an operator who raises `readyTimeoutSeconds` for slow internal
# mirrors gets a proportionally longer install pass without a second knob.
_READY_BUDGET_ENV = "DREADNODE_RUNTIME_READY_BUDGET_SEC"

# Held back from the install pass for the rest of startup — scope validation
# with its retry backoff, capability sync, discovery, and the platform's own
# polling interval.
_STARTUP_RESERVE_SECONDS = 90

# Used off-platform (a laptop, CI, a customer's own process), where no readiness
# budget exists and nothing is going to reclaim anything.
_DEFAULT_TOTAL_BUDGET_SECONDS = 420

_pass_deadline: float | None = None

# Set by the platform when the deployment has no public egress. This is a
# directive about one behaviour, not a description of the deployment: the SDK
# runs in a sandbox, on a laptop, in CI and inside a customer's own process,
# and only the first of those is ever told this.
_INSTALL_MODE_ENV = "DREADNODE_CAPABILITY_INSTALL"

# Substrings that mark a failure as an outbound attempt rather than a local
# one. Advisory: the failure is recorded either way, and this only decides how
# it is labelled. Worth labelling, because "the capability could not install"
# and "the capability tried to reach the internet" are different findings to an
# operator running a disconnected deployment — the second one is a defect even
# when it is handled.
_EGRESS_FAILURE_MARKERS = (
    "could not resolve host",
    "temporary failure in name resolution",
    "name or service not known",
    "network is unreachable",
    "no route to host",
    "connection refused",
    "connection timed out",
    "operation timed out",
    "failed to fetch",
    "could not connect",
    "proxy connect",
    "tls handshake timeout",
)


def _sealed() -> bool:
    """Whether this runtime must complete installs without reaching a network."""
    return os.environ.get(_INSTALL_MODE_ENV, "").strip().lower() == "sealed"


def _total_budget() -> float:
    """Seconds the whole install pass may take."""
    raw = os.environ.get(_READY_BUDGET_ENV, "").strip()
    if raw:
        try:
            ready_budget = float(raw)
        except ValueError:
            logger.warning("Ignoring non-numeric {}={!r}", _READY_BUDGET_ENV, raw)
        else:
            return max(60.0, ready_budget - _STARTUP_RESERVE_SECONDS)
    return float(_DEFAULT_TOTAL_BUDGET_SECONDS)


@contextlib.contextmanager
def _install_budget() -> t.Iterator[None]:
    """Bound one install pass. Reentrant calls keep the outermost deadline."""
    global _pass_deadline  # noqa: PLW0603
    if _pass_deadline is not None:
        yield
        return
    _pass_deadline = time.monotonic() + _total_budget()
    try:
        yield
    finally:
        _pass_deadline = None


def _remaining_budget() -> float | None:
    """Seconds left in the pass, or None when no pass is in progress."""
    if _pass_deadline is None:
        return None
    return _pass_deadline - time.monotonic()


def _step_timeout() -> int:
    """Per-step budget, never exceeding what is left of the whole pass."""
    step = _SEALED_TIMEOUT_SECONDS if _sealed() else _INSTALL_TIMEOUT_SECONDS
    remaining = _remaining_budget()
    if remaining is None:
        return step
    return max(1, min(step, int(remaining)))


def _label_failure(err: str) -> str:
    """Prefix a failure that looks like an outbound attempt.

    Matching on message text is imprecise by nature, so this only ever adds a
    label — it never suppresses or rewrites the underlying error.
    """
    lowered = err.lower()
    if any(marker in lowered for marker in _EGRESS_FAILURE_MARKERS):
        return f"outbound attempt failed (no egress available): {err}"
    return err


# Marker written into each capability's cache directory after a successful
# packages+scripts pass. Wiped automatically when the sync replaces the
# directory on a runtime_digest change.
_INSTALLED_MARKER = ".dreadnode-installed"


@dataclass
class InstallReport:
    """Outcome of one install pass over a set of capabilities.

    Mutually exclusive: a capability appears in exactly one of ``installed``,
    ``cached``, or ``failed``.
    """

    installed: list[str] = field(default_factory=list)
    cached: list[str] = field(default_factory=list)
    failed: dict[str, str] = field(default_factory=dict)
    durations: dict[str, float] = field(default_factory=dict)
    """Wall-clock seconds per step: ``packages.<cap>``, ``python``, ``scripts.<cap>``."""

    def time_step(self, name: str) -> "t.ContextManager[None]":
        return _timed(self, name)


@contextlib.contextmanager
def _timed(report: InstallReport, name: str) -> t.Iterator[None]:
    started = time.perf_counter()
    try:
        yield
    finally:
        report.durations[name] = round(
            report.durations.get(name, 0.0) + time.perf_counter() - started, 3
        )


def install_dependencies(
    specs: list[tuple[str, Path, DependencySpec]],
) -> InstallReport:
    """Run the three-step install pipeline across the supplied capabilities.

    ``specs`` is the list returned by
    :func:`dreadnode.capabilities.loader.preload_dependency_specs` — tuples of
    ``(capability_name, capability_dir, DependencySpec)``.
    """
    report = InstallReport()
    if not specs:
        return report

    to_install: list[tuple[str, Path, DependencySpec]] = []
    for name, path, dep in specs:
        if (path / _INSTALLED_MARKER).exists():
            report.cached.append(name)
        else:
            to_install.append((name, path, dep))

    with _install_budget():
        _install_packages(to_install, report)
        _install_python_combined(specs, report)
        _install_scripts(to_install, report)

    for name, path, _dep in to_install:
        if name in report.failed:
            continue
        try:
            (path / _INSTALLED_MARKER).touch()
        except OSError:
            logger.warning(
                "Failed to write install marker for capability '{}' at {}",
                name,
                path,
            )
        report.installed.append(name)

    return report


def _installed_apt_packages(pkgs: list[str]) -> set[str]:
    """Return the subset of *pkgs* dpkg already reports as fully installed.

    Queried per package because ``dpkg-query`` exits non-zero as soon as one
    name is unknown, which would otherwise discard the status of every name
    that *was* known.

    When ``dpkg-query`` is missing the answer is "none of them": that is the
    conservative direction, since claiming a package is present when it is not
    turns a loud install failure into a capability that loads and then cannot
    run.
    """
    dpkg_query = shutil.which("dpkg-query")
    if dpkg_query is None:
        return set()

    installed: set[str] = set()
    for pkg in pkgs:
        try:
            result = subprocess.run(  # noqa: S603
                [dpkg_query, "-W", "-f=${db:Status-Status}", pkg],
                capture_output=True,
                timeout=_DPKG_QUERY_TIMEOUT_SECONDS,
                check=False,
            )
        except (subprocess.TimeoutExpired, OSError):
            continue
        if result.returncode == 0 and result.stdout.decode(errors="replace").strip() == "installed":
            installed.add(pkg)
    return installed


def _install_packages(
    specs: list[tuple[str, Path, DependencySpec]],
    report: InstallReport,
) -> None:
    """Run privileged apt installs per capability that declares packages."""
    apt = shutil.which("apt-get")
    sudo = shutil.which("sudo")
    for name, _path, dep in specs:
        pkgs = [pkg for pkg in dep.packages if isinstance(pkg, str)]
        if not pkgs:
            continue

        # Skip the whole step when the image already carries every package.
        # `apt-get update` refreshes the archives unconditionally, so without
        # this a pre-baked runtime still reaches the network on every boot
        # whose marker the sync invalidated (CAP-INST-012). uv and pip already
        # short-circuit satisfied requirements this way; apt has no equivalent,
        # so the check has to be ours.
        installed = _installed_apt_packages(pkgs)
        missing = [pkg for pkg in pkgs if pkg not in installed]
        if not missing:
            logger.debug(
                "apt packages for '{}' are already installed; skipping apt entirely: {}",
                name,
                pkgs,
            )
            continue

        # A sealed runtime does not enter apt at all when something is
        # missing. `apt-get update` contacts the configured archives before it
        # installs anything, and here we already know the answer: the package
        # is absent and there is no route to fetch it. Making the request
        # regardless would be an outbound attempt with no chance of success,
        # which is the thing this mode exists to avoid — so report the gap
        # instead of reaching for it.
        if _sealed():
            report.failed[name] = (
                "packages: "
                + ", ".join(missing)
                + " not present in the runtime image, and this deployment installs "
                "without network access. Pre-bake the package into the runtime "
                "image, or install this capability on a connected deployment."
            )
            continue

        if apt is None:
            logger.warning(
                "Capability '{}' declares packages but apt-get is unavailable; skipping",
                name,
            )
            continue
        command_prefix = _privileged_command_prefix(sudo)
        if command_prefix is None:
            report.failed[name] = (
                "packages: apt-get requires root privileges but sudo is unavailable"
            )
            continue
        logger.info("Installing apt packages for '{}': {}", name, missing)
        with report.time_step(f"packages.{name}"):
            err = _run([*command_prefix, apt, "update"])
            if err is None:
                err = _run([*command_prefix, apt, "install", "-y", *missing])
        if err:
            report.failed[name] = f"packages: {_label_failure(err)}"


def _privileged_command_prefix(sudo: str | None) -> list[str] | None:
    """Return the prefix needed to run a command with root privileges.

    ``-n`` keeps the runtime non-interactive: an image whose sudoers entry is
    not NOPASSWD fails immediately instead of blocking on the password prompt
    until the 600s subprocess timeout.
    """
    if os.geteuid() == 0:
        return []
    if sudo:
        return [sudo, "-n"]
    return None


def _install_python_combined(
    specs: list[tuple[str, Path, DependencySpec]],
    report: InstallReport,
) -> None:
    """Union pip specs across every capability and install in one call.

    A failure blames every capability that contributed pins; a marker-cached
    capability is moved out of ``cached`` into ``failed`` because the boot
    is broken even though its prior packages+scripts pass remains valid.
    """
    union = sorted({pkg for _name, _path, dep in specs for pkg in dep.python})
    if not union:
        return

    cmd = _python_install_cmd(union)
    if cmd is None:
        err: str | None = (
            "no virtualenv is active and installing into the system interpreter "
            "requires root privileges, but sudo is unavailable"
        )
    else:
        logger.info("Installing python deps (combined across {} caps): {}", len(specs), union)
        with report.time_step("python"):
            err = _run(cmd)
    if err is None:
        return

    for name, _path, dep in specs:
        if not dep.python:
            continue
        report.failed[name] = f"python: {_label_failure(err)}"
        if name in report.cached:
            report.cached.remove(name)


def _install_scripts(
    specs: list[tuple[str, Path, DependencySpec]],
    report: InstallReport,
) -> None:
    """Run each capability's install scripts sequentially with cwd = cap dir."""
    for name, path, dep in specs:
        if name in report.failed:
            continue
        for script in dep.scripts:
            script_path = path / script
            logger.info("Running install script for '{}': {}", name, script)
            with report.time_step(f"scripts.{name}"):
                err = _run(["bash", str(script_path)], cwd=path)
            if err:
                report.failed[name] = f"scripts/{script}: {_label_failure(err)}"
                break


def _python_install_cmd(packages: list[str]) -> list[str] | None:
    """Build the combined python install command for this host's environment.

    Two sandbox image shapes have to be satisfied. When a virtualenv is active
    the runtime user owns it, so uv's own environment discovery targets it and
    no escalation is needed. Without one the running interpreter is the image's
    root-owned system python: uv refuses to touch it without ``--system``, and
    the non-root runtime user cannot write to its site-packages without sudo —
    the same escalation ``packages:`` already performs for apt.

    Every variant pins the target to ``sys.executable`` so uv and pip install
    into the interpreter the runtime actually imports from, rather than
    whichever python each tool discovers on its own.

    Returns ``None`` when escalation is required but unavailable.
    """
    uv = shutil.which("uv")

    # A sealed runtime resolves from what is already here and never opens a
    # socket. uv's `--offline` still uses its local cache, and pip's
    # `--no-index` still satisfies requirements already installed, so a
    # pre-baked environment succeeds exactly as it does connected — it simply
    # cannot reach out to do it. An unsatisfied pin fails locally and
    # immediately, with the same message every time, rather than depending on
    # how the network happens to refuse.
    uv_offline = ["--offline"] if _sealed() else []
    pip_offline = ["--no-index"] if _sealed() else []

    if _in_virtualenv():
        if uv:
            return [uv, "pip", "install", *uv_offline, "--python", sys.executable, *packages]
        return [sys.executable, "-m", "pip", "install", *pip_offline, *packages]

    command_prefix = _privileged_command_prefix(shutil.which("sudo"))
    if command_prefix is None:
        return None
    # `--break-system-packages` is required on PEP 668 images (Debian bookworm,
    # Ubuntu 24.04), where both uv and pip refuse to touch the externally
    # managed system interpreter without it.
    if uv:
        return [
            *command_prefix,
            uv,
            "pip",
            "install",
            *uv_offline,
            "--python",
            sys.executable,
            "--system",
            "--break-system-packages",
            *packages,
        ]
    return [
        *command_prefix,
        sys.executable,
        "-m",
        "pip",
        "install",
        *pip_offline,
        "--break-system-packages",
        *packages,
    ]


def _in_virtualenv() -> bool:
    """Whether the running interpreter lives inside a virtualenv.

    ``VIRTUAL_ENV`` is only set by ``bin/activate``, so an image that execs the
    venv interpreter directly (``/opt/venv/bin/python -m dreadnode ...``) leaves
    it unset; ``sys.prefix``/``sys.base_prefix`` is the reliable signal.
    """
    return sys.prefix != sys.base_prefix or bool(os.environ.get("VIRTUAL_ENV", "").strip())


def _run(cmd: list[str], cwd: Path | None = None) -> str | None:
    """Run a subprocess, returning ``None`` on success or a short error tail.

    The returned string is the last few lines of stderr (or a generic
    "exit code N" / "timed out" message) — enough to land in logs without
    flooding them.
    """
    remaining = _remaining_budget()
    if remaining is not None and remaining <= 0:
        return (
            f"skipped: install budget of {_total_budget():.0f}s exhausted before this step started"
        )

    budget = _step_timeout()
    try:
        result = subprocess.run(  # noqa: S603
            cmd,
            cwd=cwd,
            capture_output=True,
            timeout=budget,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return f"timed out after {budget}s"
    except FileNotFoundError as exc:
        return f"command not found: {exc.filename or cmd[0]}"
    except Exception as exc:
        return str(exc)

    if result.returncode == 0:
        return None

    stderr = result.stderr.decode("utf-8", errors="replace").strip()
    if stderr:
        return "\n".join(stderr.splitlines()[-5:])
    return f"exit code {result.returncode}"


__all__ = ["InstallReport", "install_dependencies"]
