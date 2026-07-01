"""Pure shell-script helpers for the Plato Harbor environment.

This module deliberately has **no** Harbor or Plato-SDK imports so its logic can
be unit-tested without installing Harbor (which requires Python 3.12+).

All remote interaction with a Plato VM goes through the environment's
``execute`` channel, which returns stdout/stderr **and a real exit code** (a
``ExecuteCommandResult``). Unlike the desktop ``/bash`` endpoint there is no
need for an exit-code sentinel — the helpers here only assemble the command
strings (working-directory / env prefixes and base64 file-transfer scripts).
"""

from __future__ import annotations

import os
import shlex


def build_host_command(
    command: str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
) -> str:
    """Wrap *command* with optional ``cd`` and ``env`` prefixes.

    The command runs in a fresh ``bash -lc`` login subshell so ``PATH`` (and
    therefore ``docker``) resolves the same way an interactive root shell would,
    and so working-directory / shell-variable state never leaks between calls.
    """
    prefix = ""
    if cwd:
        prefix += f"cd {shlex.quote(cwd)} && "
    if env:
        assignments = " ".join(shlex.quote(f"{k}={v}") for k, v in env.items())
        prefix += f"env {assignments} "
    return f"{prefix}bash -lc {shlex.quote(command)}"


def build_upload_file_script(target_path: str, b64: str) -> str:
    """Decode *b64* into *target_path* on the VM (creating parent dirs)."""
    parent = os.path.dirname(target_path) or "/"
    return f"mkdir -p {shlex.quote(parent)} && printf %s {shlex.quote(b64)} | base64 -d > {shlex.quote(target_path)}"


def build_upload_dir_script(target_dir: str, b64: str) -> str:
    """Decode *b64* (a gzip tar) and extract it into *target_dir* on the VM."""
    return (
        f"mkdir -p {shlex.quote(target_dir)} && "
        f"printf %s {shlex.quote(b64)} | base64 -d | "
        f"tar xzf - -C {shlex.quote(target_dir)}"
    )


def build_download_file_script(source_path: str) -> str:
    """Emit *source_path* as a single base64 line on stdout."""
    return f"base64 -w0 {shlex.quote(source_path)}"


def build_download_dir_script(source_dir: str) -> str:
    """Emit a gzip tar of *source_dir*'s contents as a base64 line on stdout."""
    return f"tar czf - -C {shlex.quote(source_dir)} . | base64 -w0"
