"""the installed package's directory and version, and `pi update` of our source."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from collections.abc import Mapping
from pathlib import Path

# One of the two non-stdlib imports here (`durable` below is the other), and free:
# claude_cli.py is itself stdlib-only (shutil/subprocess/dataclasses, see its
# own docstring), so importing it adds no dependency weight and, critically,
# no import cycle -- it does not import agent_rules, pi_config, or anything
# else in this package back. It is imported for `Result`, and for the bounded
# way to run a binary (`claude_cli.capture`, `pi_binary_available`'s sniff).
# setup.py's install_plugin/uninstall_plugin already return claude_cli.Result,
# and a later task wires pi's install/remove into the SAME call sites
# (apply_capture, apply_tracking) that already know how to read `.ok` and
# `.detail` off one. Inventing a second, differently-shaped result type here
# would make that wiring a translation layer instead of a drop-in.
from probe.shared.harness.harnesses.claude_code import binary as claude_cli
from probe.shared.harness.harnesses.pi.package_source import (
    MIRROR_GIT_SOURCE,
    PACKAGE_NAME,
    PackageRootError,
    _entry_source,
    _git_repo_identity,
    _our_entry_index,
    local_package_root,
)
from probe.shared.harness.harnesses.pi.settings import _SettingsRefusal, _load_settings, pi_agent_dir, settings_path

#: How long the wizard waits for `pi update` before saying what to run.
UPDATE_TIMEOUT_S = 30


def installed_package_dir(env: Mapping[str, str] | None = None) -> Path | None:
    """The package directory pi loads our entry from, or None: pi's clone of the
    mirror (`<agent dir>/git/<host>/<owner>/<repo>/plugins/probe-research-pi`)
    or the local path the entry names."""
    active = env if env is not None else os.environ
    agent_dir = pi_agent_dir(active)
    try:
        data = _load_settings(settings_path(active))
        root = local_package_root(active)
    except (_SettingsRefusal, PackageRootError):
        return None
    index = _our_entry_index(data, root=root, agent_dir=agent_dir)
    if index is None:
        return None
    source = _entry_source(data["packages"][index]) or ""
    identity = _git_repo_identity(source)
    if identity is not None:
        host, repo = identity
        return agent_dir / "git" / host / repo / "plugins" / PACKAGE_NAME
    candidate = Path(source)
    return candidate if candidate.is_absolute() else agent_dir / candidate


def installed_package_version(env: Mapping[str, str] | None = None) -> tuple[int, ...] | None:
    """The installed package's `version`, or None when it cannot be read."""
    directory = installed_package_dir(env)
    if directory is None:
        return None
    try:
        raw = json.loads((directory / "package.json").read_text(encoding="utf-8")).get("version")
        return tuple(int(part) for part in str(raw).split(".")[:3])
    except (OSError, ValueError, TypeError, AttributeError):
        return None


def update_package(env: Mapping[str, str] | None = None, *, cwd: Path | None = None) -> claude_cli.Result:
    """`pi update <our source>`: pi re-fetches an unpinned git package."""
    active = env if env is not None else os.environ
    binary = shutil.which("pi", path=active.get("PATH"))
    if not binary:
        return claude_cli.Result(ok=False, detail="pi is not on PATH", reachable=False)
    if cwd is not None:
        binary = str(Path(binary).resolve())
    try:
        data = _load_settings(settings_path(active))
        index = _our_entry_index(data, root=local_package_root(active), agent_dir=pi_agent_dir(active))
    except (_SettingsRefusal, PackageRootError) as exc:
        return claude_cli.Result(ok=False, detail=str(exc))
    if index is None:
        return claude_cli.Result(ok=False, detail="probe-research-pi is not installed")
    source = _entry_source(data["packages"][index]) or MIRROR_GIT_SOURCE
    command = ["pi", "update", source]
    try:
        # Through `claude_cli.capture`: inside an update's pi step its process
        # group is the step's to stop at its deadline (`upgrading`).
        completed = claude_cli.capture(
            [binary, "update", source], timeout=UPDATE_TIMEOUT_S, env=dict(active),
            cwd=str(cwd) if cwd is not None else None,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return claude_cli.Result(ok=False, detail=f"{' '.join(command)}: {exc}", command=" ".join(command))
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout or "").strip() or f"exit {completed.returncode}"
        return claude_cli.Result(ok=False, detail=detail, command=" ".join(command))
    return claude_cli.Result(ok=True, detail="updated", command=" ".join(command))
