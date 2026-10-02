"""Make sure the wizard leaves a real `probe` behind.

`npx probe-research` resolves the CLI through `uv tool run` / `pipx run`, both
of which are EPHEMERAL: they fetch, execute, and leave nothing installed. That
is the right way to *launch* a wizard and completely wrong as an end state,
because everything the wizard sets up depends on a persistent binary afterwards:

  * the wizard's own closing line tells you to run `probe doctor`
  * the tracking plugin's SessionStart hook resolves PROBE_BIN from PATH or
    ~/.local/bin to do its version check
  * the MCP config's headersHelper shells out to fetch the stored token, so
    with no binary the MCP has no credential

Without this the only path that worked end to end was the one where `probe` was
already installed — the re-run case, not onboarding. Exactly backwards.

So: if we are running ephemerally, install ourselves properly before doing
anything else, and say so.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

DIST = "probe-research"
#: What an install ASKS for (plan 2.11, D29): the package with the `all` extra,
#: which carries the CLI's and the MCP server's dependencies. They still sit in
#: core in this release; the next release removes them from core, and an
#: install recorded without `[all]` would then lose `probe` on its next upgrade.
INSTALL_SPEC = f"{DIST}[all]"
LEGACY_DIST = "probe-agent"
_INSTALL_TIMEOUT_S = 300.0


@dataclass(frozen=True)
class BootstrapResult:
    installed: bool
    """True only when THIS run performed a persistent install."""
    already_persistent: bool
    message: str


def _launcher_caches() -> tuple[str, ...]:
    """Where uv and pipx park a copy they are about to throw away.

    Read from the environment first, because both tools let the cache move and
    a hardcoded path would quietly stop matching for anyone who moved it --
    which is the same silent-wrong-answer this whole function exists to stop.
    """
    roots = [os.environ.get("UV_CACHE_DIR")]
    xdg = os.environ.get("XDG_CACHE_HOME")
    roots.append(os.path.join(xdg, "uv") if xdg else None)
    home = os.path.expanduser("~")
    roots += [
        f"{home}/.cache/uv",
        f"{home}/.cache/pipx",
        f"{home}/.local/pipx/.cache",
    ]
    pipx_home = os.environ.get("PIPX_HOME")
    if pipx_home:
        roots.append(os.path.join(pipx_home, ".cache"))
    return tuple(os.path.realpath(r) for r in roots if r)


def _is_throwaway(path: str) -> bool:
    """Whether this `probe` is a launcher's temporary copy rather than an install.

    THE BUG THIS EXISTS FOR: `npx probe-research` runs us through `uv tool run`,
    which unpacks the CLI into its cache and puts that cache's `bin` on our
    PATH. So `shutil.which("probe")` finds a `probe` on every from-zero run --
    THIS process -- and the caller concluded a real install was already present
    and skipped the one it exists to perform. Measured on a fresh machine:
    `which("probe")` returned `~/.cache/uv/archive-v0/<hash>/bin/probe`, the
    version matched, and the wizard reported success while leaving no `probe`
    behind at all. Every instruction that follows -- `probe doctor`, the
    plugin's SessionStart hook, the MCP headers helper -- then had no binary.

    Tested on the LOCATION, not on `realpath` and not on `sys.prefix`. Both of
    those look identical for a real install: `~/.local/bin/probe` is a symlink
    INTO `~/.local/share/uv/tools/probe-research`, which is also that process's
    own `sys.prefix`. Judging by either would call a healthy install throwaway
    and reinstall it on every single run.
    """
    real = os.path.realpath(path)
    return any(real.startswith(root + os.sep) for root in _launcher_caches())


def _installed_binary() -> str | None:
    """A `probe` a future shell (or a plugin hook) could actually find.

    PATH alone is not enough: Claude Code launched from the dock sources no
    profile, so ~/.local/bin may be missing from its environment even though the
    binary is there. The plugin hook checks those same fallbacks, so we must
    agree with it or we would reinstall on every run.

    PATH is also too MUCH, which is the other half: a launcher's own cache is on
    it while we run. A hit there is skipped and the durable candidates below are
    consulted instead -- so a from-zero run correctly finds nothing.
    """
    found = shutil.which("probe")
    if found and not _is_throwaway(found):
        return found
    home = os.path.expanduser("~")
    for candidate in (
        f"{home}/.local/bin/probe",
        f"{home}/.local/share/uv/tools/{DIST}/bin/probe",
    ):
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate
    return None


def _version_of(binary: str) -> str | None:
    try:
        completed = subprocess.run(  # noqa: S603 - resolved path, no shell
            [binary, "--version"], capture_output=True, text=True, timeout=20, check=False
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if completed.returncode != 0:
        return None
    import re

    match = re.search(r"(\d+\.\d+\.\d+(?:\.\d+)?)", completed.stdout)
    return match.group(1) if match else None


def _at_least(found: str, wanted: str) -> bool:
    fa = [int(x) for x in found.split(".") if x.isdigit()]
    wa = [int(x) for x in wanted.split(".") if x.isdigit()]
    for i in range(max(len(fa), len(wa))):
        a, b = (fa[i] if i < len(fa) else 0), (wa[i] if i < len(wa) else 0)
        if a != b:
            return a > b
    return True


def _resolves_on_path() -> bool:
    """Whether a GOOD ENOUGH `probe` is installed.

    Existence is not enough. A machine with an old `probe` -- every existing
    user -- would otherwise keep it forever: the wizard runs the new version
    ephemerally through uvx, decides nothing needs installing, and the user's
    shell stays on the old one indefinitely. Same trap the npx launcher fell
    into.
    """
    from probe import __version__

    binary = _installed_binary()
    if binary is None:
        return False
    if _is_this_install(binary):
        # The persistent `probe` IS this process (the common case: someone ran
        # `probe wizard`), so its version is ours. Asking it with a subprocess
        # cost ~0.9s on every wizard launch.
        return True
    found = _version_of(binary)
    return bool(found and _at_least(found, __version__))


def _is_this_install(binary: str) -> bool:
    """Whether `binary` is the entry point of THIS interpreter's environment
    (`<env>/bin/probe`, or `<env>\\Scripts\\probe.exe`), through any symlink
    (`~/.local/bin/probe` -> the uv or pipx tool env)."""
    import sys

    try:
        return Path(os.path.realpath(binary)).parent.parent == Path(os.path.realpath(sys.prefix))
    except OSError:
        return False


def installed_version() -> str | None:
    """The version of the persistent `probe`, or None when there is none."""
    binary = _installed_binary()
    return _version_of(binary) if binary else None


def ensure_persistent_install(*, dry_run: bool = False) -> BootstrapResult:
    """Install the CLI for real if this process is an ephemeral one.

    Prefers uv, falls back to pipx. Deliberately never falls back to a bare
    `pip install`: on a researcher's machine that usually means a conda or
    system environment, and silently mutating it is how you break a training
    run three days later.
    """
    if _resolves_on_path():
        return BootstrapResult(
            installed=False,
            already_persistent=True,
            message="",
        )

    if dry_run:
        return BootstrapResult(
            installed=False,
            already_persistent=False,
            message=f"would install {DIST} persistently",
        )
    return install_persistent()


def _persistent_tool_env(command: list[str], name: str) -> str | None:
    """The directory of the persistent install ``name`` under a tool manager,
    from the manager itself (`uv tool dir`, `pipx environment`), or None."""
    try:
        done = subprocess.run(  # noqa: S603 - fixed binary, no shell
            command, capture_output=True, text=True, check=False, timeout=30
        )
    except (OSError, subprocess.SubprocessError):
        return None
    root = (done.stdout or "").strip().splitlines()
    if done.returncode != 0 or not root:
        return None
    path = os.path.join(root[-1].strip(), name)
    return path if os.path.isdir(path) else None


def install_persistent(spec: str = INSTALL_SPEC) -> BootstrapResult:
    """Install `spec` as the persistent CLI, replacing whatever is there.

    `spec` is `probe-research[all]@latest` when an existing install is known to be
    behind: a launcher that served a stale cached copy would otherwise resolve
    the same stale version here too.
    """
    injected: list[str] = []
    dropped = ""
    if shutil.which("uv"):
        # The legacy distribution owns the same `probe` executable, so it has to
        # go FIRST or the old build keeps answering. Removing it afterwards
        # deletes the shared binary out from under the new install.
        subprocess.run(  # noqa: S603 - fixed binary, no shell
            ["uv", "tool", "uninstall", LEGACY_DIST],
            capture_output=True,
            check=False,
            timeout=_INSTALL_TIMEOUT_S,
        )
        # `--force` replaces the permanent install's receipt: restate what it
        # records -- extras, `--with` packages, its Python -- or an update run
        # from `npx`/`uvx` strips them (#2043 review: `--with six` gone, Python
        # 3.10 became 3.13). The same restatement `probe update` makes.
        from . import updater

        existing = _persistent_tool_env(["uv", "tool", "dir"], DIST)
        kept = updater.kept_from_uv_receipt(existing) if existing else updater.KeptInstall()
        if kept is None:
            # Unlike `probe update`, which leaves such a receipt alone, this is
            # a (re)install: it goes ahead -- but says what it could not carry.
            dropped = (
                " The previous install's uv receipt had entries this cannot restate (an "
                "editable or local `--with` package, constraints); they were NOT carried over. "
                "Re-add them with `uv tool install --force 'probe-research[all]' --with ...`."
            )
        version = "@latest" if spec.endswith("@latest") else ""
        command = updater.uv_tool_install_command(
            kept or updater.KeptInstall(), force=True, version=version
        )
    elif shutil.which("pipx"):
        # pipx has no `@latest`; a plain install already resolves the newest.
        # Its recorded extras stay in the spec; injected packages go back in
        # after (`install --force` drops them).
        from . import updater

        existing = _persistent_tool_env(["pipx", "environment", "--value", "PIPX_LOCAL_VENVS"], DIST)
        extras = updater.pipx_extras(existing) if existing else ()
        injected = updater.pipx_injected(existing) if existing else []
        command = ["pipx", "install", "--force", updater._dist(extras)]
    else:
        return BootstrapResult(
            installed=False,
            already_persistent=False,
            message=(
                "could not install `probe` persistently: neither uv nor pipx is "
                "available. The wizard will still finish, but `probe doctor` and "
                "the plugin's version check will not work until you install it."
            ),
        )

    try:
        completed = subprocess.run(  # noqa: S603 - fixed binary, no shell
            command,
            capture_output=True,
            text=True,
            check=False,
            timeout=_INSTALL_TIMEOUT_S,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return BootstrapResult(False, False, f"could not install `probe`: {exc}")

    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).strip().splitlines()
        return BootstrapResult(
            installed=False,
            already_persistent=False,
            message=f"could not install `probe`: {detail[-1] if detail else 'unknown error'}",
        )
    if command[0] == "pipx" and injected:
        subprocess.run(  # noqa: S603 - fixed binary, no shell
            ["pipx", "inject", DIST, *injected],
            capture_output=True,
            check=False,
            timeout=_INSTALL_TIMEOUT_S,
        )

    note = ""
    if not shutil.which("probe"):
        # Installed, but this shell will not see it. Saying so beats letting the
        # user discover it when `probe doctor` fails.
        note = " Add ~/.local/bin to your PATH to use it in this shell."
    return BootstrapResult(
        installed=True,
        already_persistent=False,
        message=f"Installed `probe` ({' '.join(command[:2])}).{note}{dropped}",
    )
