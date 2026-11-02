"""Doctor repair actions for certs/npmrc and managed CLIs.

Provides:
- ``repair_certs``: Repair a missing/stale CA bundle with npm-conditionality.
- ``repair_managed_cli``: Install a missing managed CLI (``gh`` or ``copilot``).
- ``_upsert_npmrc_cafile``: Idempotent, atomic upsert of ``cafile=`` in ``~/.agdt/npmrc``.
- Factory functions and registration into the default ``RepairRegistry``.
"""

from __future__ import annotations

import os
import tempfile
import time
from pathlib import Path

from .dependency_checker import DependencyStatus
from .doctor import RepairFn

# ── Constants ─────────────────────────────────────────────────────────────────

_CERT_TIMEOUT_SECONDS: int = 60
_MANAGED_CLI_NAMES: frozenset[str] = frozenset({"gh", "copilot"})


# ── npmrc upsert ──────────────────────────────────────────────────────────────


def _upsert_npmrc_cafile(ca_path: str | Path) -> Path:
    """Idempotent, atomic upsert of ``cafile=`` in ``~/.agdt/npmrc``.

    Reads the existing ``~/.agdt/npmrc`` (if present), replaces any existing
    ``cafile=`` line with ``cafile=<ca_path>``, or appends it if absent.
    All other lines are preserved verbatim.

    The write uses a temporary file in the same directory followed by
    ``os.replace()`` for atomicity.  The temp file is cleaned up on failure.

    Args:
        ca_path: Absolute path to the CA bundle file.

    Returns:
        Path to the written ``~/.agdt/npmrc`` file.

    Raises:
        OSError: If the directory cannot be created or the file cannot be
            written/renamed.
    """
    npmrc_path = Path.home() / ".agdt" / "npmrc"
    ca_path_str = str(ca_path)
    new_line = f"cafile={ca_path_str}\n"

    # Read existing content (if any).
    existing_lines: list[str] = []
    if npmrc_path.is_file():
        existing_lines = npmrc_path.read_bytes().decode("utf-8", errors="surrogateescape").splitlines(keepends=True)

    # Replace or append.
    # Only the first cafile= line is replaced; any further duplicates are
    # dropped so the result always contains exactly one cafile= entry.
    replaced = False
    output_lines: list[str] = []
    for line in existing_lines:
        if line.rstrip("\n").rstrip("\r").startswith("cafile="):
            if not replaced:
                output_lines.append(new_line)
                replaced = True
            # else: drop duplicate cafile= line
        else:
            output_lines.append(line)

    if not replaced:
        # Ensure the preceding content (if any) is separated by a newline so
        # the new cafile= entry starts on its own line even when the last
        # existing line has no trailing newline.
        if output_lines and not output_lines[-1].endswith("\n"):
            output_lines.append("\n")
        output_lines.append(new_line)

    # Atomic write: temp file → os.replace.
    npmrc_path.parent.mkdir(parents=True, exist_ok=True)
    fd = None
    tmp_path: str | None = None
    try:
        fd, tmp_path = tempfile.mkstemp(
            dir=str(npmrc_path.parent),
            prefix=".npmrc_",
            suffix=".tmp",
        )
        # os.write() may write fewer bytes than requested (POSIX), so loop
        # until the entire buffer has been flushed to the file descriptor.
        # Guard against a 0-byte write (e.g. disk full) to prevent an
        # infinite loop.
        data = "".join(output_lines).encode("utf-8", errors="surrogateescape")
        written = 0
        while written < len(data):
            n = os.write(fd, data[written:])
            if n == 0:
                raise OSError("os.write returned 0 — possible disk full or bad file descriptor")
            written += n
        # Flush OS buffers to disk before rename so a crash/power-loss after
        # os.replace() does not leave ~/.agdt/npmrc empty or truncated.
        os.fsync(fd)
        os.close(fd)
        fd = None
        os.replace(tmp_path, str(npmrc_path))
        tmp_path = None  # successfully renamed — no cleanup needed
    finally:
        if fd is not None:
            os.close(fd)
        if tmp_path is not None:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

    return npmrc_path


# ── Certificate repair ────────────────────────────────────────────────────────


def repair_certs(dep: DependencyStatus, *, repo_root: Path) -> None:
    """Repair a missing or stale CA bundle.

    Resolves ``npm_enabled`` via :func:`detect_npm_footprint` on *repo_root*.
    Iterates over the setup hosts calling :func:`ensure_ca_bundle` to fetch
    each host's certificate chain, then calls
    :func:`_build_unified_ca_bundle` to produce a combined PEM file.
    When npm is enabled, calls :func:`_upsert_npmrc_cafile` to update
    ``~/.agdt/npmrc`` atomically.

    Enforces a total timeout of 60 seconds across the entire cert-fetch
    operation.

    Args:
        dep: The ``DependencyStatus`` for the ``ca-bundle`` check.
        repo_root: Repository root used for npm footprint detection.

    Raises:
        RuntimeError: If the cert fetch fails or times out.
    """
    from agentic_devtools.cli.cert_utils import ensure_ca_bundle as _ensure_ca_bundle

    from .commands import _SETUP_HOSTS, _build_unified_ca_bundle
    from .npm_footprint import detect_npm_footprint

    npm_enabled = detect_npm_footprint(repo_root)

    start = time.monotonic()
    all_pem_paths: list[str] = []
    hosts_completed = 0

    # Fetch certs for setup hosts.
    for hostname in _SETUP_HOSTS:
        if time.monotonic() - start > _CERT_TIMEOUT_SECONDS:
            raise RuntimeError(
                f"Certificate repair timed out after {_CERT_TIMEOUT_SECONDS}s "
                f"(completed {hosts_completed}/{len(_SETUP_HOSTS)} hosts)"
            )
        pem = _ensure_ca_bundle(hostname)
        if pem:
            all_pem_paths.append(pem)
        hosts_completed += 1

    # Fetch npm registry cert when npm is enabled.
    if npm_enabled:
        if time.monotonic() - start <= _CERT_TIMEOUT_SECONDS:
            pem = _ensure_ca_bundle("registry.npmjs.org")
            if pem:
                all_pem_paths.append(pem)

    # Build unified bundle.
    unified_path = _build_unified_ca_bundle(all_pem_paths)
    if unified_path is None:
        raise RuntimeError("Failed to build unified CA bundle (certifi unavailable or write failed)")

    # Update npmrc only when npm is enabled.
    if npm_enabled:
        try:
            _upsert_npmrc_cafile(unified_path)
        except OSError as exc:
            raise RuntimeError(f"Failed to update ~/.agdt/npmrc with cafile={unified_path}: {exc}") from exc

    dep.found = True
    dep.path = str(unified_path)


# ── Managed CLI repair ────────────────────────────────────────────────────────


def repair_managed_cli(dep: DependencyStatus) -> None:
    """Install a missing managed CLI (``gh`` or ``copilot``).

    Args:
        dep: The ``DependencyStatus`` for the managed CLI.

    Raises:
        ValueError: If ``dep.name`` is not a known managed CLI.
        RuntimeError: If the installation fails or returns ``False``.
    """
    if dep.name not in _MANAGED_CLI_NAMES:
        raise ValueError(f"Unknown managed CLI: {dep.name!r} (expected one of {sorted(_MANAGED_CLI_NAMES)})")

    if dep.name == "gh":
        from .gh_cli_installer import get_gh_cli_binary, install_gh_cli

        try:
            success = install_gh_cli(force=False, dry_run=False)
        except Exception as exc:
            raise RuntimeError(f"Failed to install gh CLI: {exc}") from exc
        if not success:
            raise RuntimeError("gh CLI installation returned failure (install_gh_cli returned False)")
        resolved_path = get_gh_cli_binary()
        if not resolved_path:
            raise RuntimeError("gh CLI installation succeeded but binary was not found afterwards")
    else:
        # dep.name == "copilot"
        from .copilot_cli_installer import get_copilot_cli_binary, install_copilot_cli

        try:
            success = install_copilot_cli(force=False, dry_run=False)
        except Exception as exc:
            raise RuntimeError(f"Failed to install copilot CLI: {exc}") from exc
        if not success:
            raise RuntimeError("copilot CLI installation returned failure (install_copilot_cli returned False)")
        resolved_path = get_copilot_cli_binary()
        if not resolved_path:
            raise RuntimeError("copilot CLI installation succeeded but binary was not found afterwards")

    dep.found = True
    dep.path = resolved_path


# ── Factories ─────────────────────────────────────────────────────────────────


def _cert_repair_factory() -> RepairFn:
    """Return a closure that repairs certs with the repo root captured at dispatch time."""
    from agentic_devtools.state import _get_git_repo_root

    git_root = _get_git_repo_root()
    repo_root = Path(git_root) if git_root else Path.cwd()

    def _repair(dep: DependencyStatus) -> None:
        repair_certs(dep, repo_root=repo_root)

    return _repair


def _cli_repair_factory() -> RepairFn:
    """Return the managed CLI repair function."""
    return repair_managed_cli
