"""
CLI commands for the agdt-setup family of commands.

Entry points:
- ``agdt-setup``            — full setup (install copilot CLI + gh CLI, check all deps)
- ``agdt-setup-copilot-cli`` — install only the Copilot CLI standalone binary
- ``agdt-setup-gh-cli``     — install only the GitHub CLI
- ``agdt-setup-check``      — verify all dependencies without installing anything
- ``agdt-setup-certs``      — prefetch/refresh CA certificate bundles

All install commands accept ``--system-only`` to skip managed installs and rely
on whatever is available on the system ``PATH``.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast
from urllib.parse import urlparse

from agentic_devtools.cli.cert_utils import count_certificates_in_pem as _count_certificates_in_pem
from agentic_devtools.cli.cert_utils import ensure_ca_bundle as _ensure_ca_bundle
from agentic_devtools.cli.cert_utils import normalize_pem_block as _normalize_pem_block

from .copilot_cli_installer import install_copilot_cli
from .copilot_settings import ensure_copilot_settings
from .dependency_checker import DependencyStatus, check_all_dependencies, print_dependency_report
from .gh_cli_installer import install_gh_cli
from .script_generators.atomic_write import atomic_write
from .shell_profile import detect_shell_profile, detect_shell_type, persist_env_var, persist_path_entry

try:
    from agentic_devtools.config import VALID_ISSUE_ADAPTERS as _VALID_ISSUE_ADAPTERS
except ImportError:
    _VALID_ISSUE_ADAPTERS = frozenset({"jira", "github", "markdown"})

if TYPE_CHECKING:  # pragma: no cover - typing-only import
    from agentic_devtools.cli.setup.expectations_specializer import (
        _StartupFingerprintError,
        _StartupFingerprintState,
    )
    from agentic_devtools.cli.setup.refresh_outcome import RefreshOutcome
    from agentic_devtools.skill_injector import InjectionSummary

_MANAGED_BIN_DIR = Path.home() / ".agdt" / "bin"

_BANNER = """\
╔══════════════════════════════════════════════════════════════╗
║                    agentic-devtools Setup                    ║
╚══════════════════════════════════════════════════════════════╝"""

_PATH_INSTRUCTIONS = (
    "\n"
    "PATH Setup:\n"
    "  Add ~/.agdt/bin to your PATH:\n"
    "    # bash/zsh:\n"
    '    export PATH="$HOME/.agdt/bin:$PATH"\n'
    "    # PowerShell:\n"
    '    $env:PATH = "$env:USERPROFILE\\.agdt\\bin;$env:PATH"'
)


_SETUP_HOSTS = (
    "api.github.com",
    "github.com",
    "dev.azure.com",
    "release-assets.githubusercontent.com",
)

_ISSUE_ADAPTER_RESOLVED_KEY = "issue_adapter_resolved"
_GENERIC_HTTPS_REMOTE_RE = re.compile(
    r"^[A-Za-z][A-Za-z0-9+.-]*://(?:[^@/]+@)?[^/]+/(?:.+/)?([^/]+)/([^/]+?)(?:\.git)?/?$"
)
_GENERIC_SCP_REMOTE_RE = re.compile(
    r"^(?![A-Za-z][A-Za-z0-9+.-]*://)(?:[^@/\s]+@)?[^:/\s]+:(?:.+/)?([^/]+)/([^/]+?)(?:\.git)?$"
)


def _build_unified_ca_bundle(per_host_pem_paths: list[str]) -> Path | None:
    """Build a unified CA bundle combining certifi's system CAs and fetched corporate CAs.

    Reads the system certifi CA bundle, appends all non-leaf certificates
    (index > 0 in each chain, i.e. intermediates and roots) from the
    per-host PEM files, de-duplicates, and atomically writes the result to
    ``~/.agdt/certs/unified-ca-bundle.pem``.

    The bundle is always written even when no extra corporate CA certificates
    are found — in that case the result is a copy of the certifi bundle.
    This ensures ``REQUESTS_CA_BUNDLE`` can always be pointed at the unified
    bundle, giving subsequent requests a known-good CA store to fall back to.

    Args:
        per_host_pem_paths: List of paths to per-host PEM files.

    Returns:
        Path to the unified bundle file, or ``None`` if certifi is unavailable
        or if the certifi bundle cannot be read / the unified file cannot be
        written.
    """
    try:
        import certifi
    except ImportError:
        return None

    cert_pattern = r"-----BEGIN CERTIFICATE-----.*?-----END CERTIFICATE-----"

    # Start with certifi system CAs
    certifi_path = Path(certifi.where())
    try:
        system_pem = certifi_path.read_text(encoding="utf-8", errors="ignore")
    except OSError as exc:
        print(f"  ⚠ Could not read certifi CA bundle {certifi_path}: {exc}", file=sys.stderr)
        return None
    system_certs = set(re.findall(cert_pattern, system_pem, re.DOTALL))

    extra_certs: list[str] = []
    for pem_path in per_host_pem_paths:
        try:
            content = Path(pem_path).read_text(encoding="utf-8", errors="ignore")
        except OSError as exc:
            print(f"  ⚠ Could not read CA bundle {pem_path}: {exc}", file=sys.stderr)
            continue
        chain = re.findall(cert_pattern, content, re.DOTALL)
        # Skip index 0 (leaf/server cert); only add intermediates and roots
        for cert in chain[1:]:
            cert = _normalize_pem_block(cert)
            if cert not in system_certs:
                system_certs.add(cert)
                extra_certs.append(cert)

    # Always write a unified bundle: if no additional corporate CAs are found
    # this is effectively a certifi-only bundle, ensuring REQUESTS_CA_BUNDLE
    # always points at a known-good CA store instead of per-host leaf-only PEMs.
    unified_content = system_pem.rstrip("\n") + "\n" + "\n".join(extra_certs) + "\n"
    unified_path = Path.home() / ".agdt" / "certs" / "unified-ca-bundle.pem"
    try:
        atomic_write(unified_path, unified_content)
    except OSError as exc:
        print(f"  ⚠ Could not write unified CA bundle {unified_path}: {exc}", file=sys.stderr)
        return None
    return unified_path


def _prefetch_certs(
    *,
    npm_enabled: bool,
    dry_run: bool = False,
    selected_hosts_out: list[str] | None = None,
) -> tuple[Path | None, Path | None]:
    """Pre-fetch and cache corporate CA certificates for common setup hosts.

    Fetches the certificate chain for external hosts used during setup and
    stores the PEM bundles in ``~/.agdt/certs/``.  When *npm_enabled* is
    ``True``, also fetches the ``registry.npmjs.org`` cert and writes an
    ``~/.agdt/npmrc`` file that configures npm to use the cached CA bundle.

    After fetching all per-host bundles a unified CA bundle is built at
    ``~/.agdt/certs/unified-ca-bundle.pem`` by combining the system certifi
    CA store with any extra intermediate/root CAs found in the per-host chains.
    When the unified bundle is built and ``REQUESTS_CA_BUNDLE`` is not already
    set by the user, it is set in ``os.environ`` so that all subsequent HTTPS
    calls within the same process use it automatically.

    When *npm_enabled* is ``False``, the npm registry cert fetch, ``~/.agdt/npmrc``
    write, and ``NODE_EXTRA_CA_CERTS``/``NPM_CONFIG_USERCONFIG`` env vars are all
    skipped.  Any pre-existing npm artifacts are left intact (append-only
    coexistence invariant).

    When *dry_run* is ``True``, prints "would …" messages and returns the
    deterministic planned output paths immediately without making any network
    requests, writing any files, or mutating ``os.environ``.

    The cert cache only needs to be refreshed infrequently (e.g. yearly).
    To force a refresh, delete ``~/.agdt/certs/``.

    Args:
        npm_enabled: Whether to perform npm-specific certificate and
            configuration work.
        dry_run: When ``True``, skip all I/O and print preview messages.
        selected_hosts_out: Optional mutable list populated with the host set
            selected for this invocation's certificate-prefetch phase.

    Returns:
        A tuple of ``(unified_path, npmrc_path)`` where *unified_path* is
        the path to the unified CA bundle file (or ``None`` if it could not
        be built), and *npmrc_path* is the path to ``~/.agdt/npmrc`` (or
        ``None`` when npm work was skipped or npmrc was not written).
    """
    if dry_run:
        print("  ○ would prefetch certificates for setup hosts")
        planned_unified_path = Path.home() / ".agdt" / "certs" / "unified-ca-bundle.pem"
        planned_npmrc_path = Path.home() / ".agdt" / "npmrc" if npm_enabled else None
        if selected_hosts_out is not None:
            selected_hosts_out[:] = [*_SETUP_HOSTS, *(["registry.npmjs.org"] if npm_enabled else [])]
        return planned_unified_path, planned_npmrc_path
    print("Fetching CA certificates for external hosts...")

    # Determine Jira hostname dynamically
    extra_hosts: list[str] = []
    try:
        from ..jira.config import get_jira_base_url

        jira_url = get_jira_base_url()
        # Use urlparse to correctly strip port numbers (e.g. jira.example.com:8443).
        # Scheme-less URLs like "jira.example.com" need a "//" prefix so urlparse
        # treats the first component as a network location rather than a path.
        parsed = urlparse(jira_url)
        jira_hostname = parsed.hostname
        if not jira_hostname:
            jira_hostname = urlparse("//" + jira_url).hostname
        if jira_hostname:
            extra_hosts.append(jira_hostname)
    except Exception as exc:  # noqa: BLE001
        print(f"  ⚠ Could not determine Jira hostname (skipping Jira cert): {exc}", file=sys.stderr)

    selected_hosts = [*_SETUP_HOSTS, *extra_hosts]
    if npm_enabled:
        selected_hosts.append("registry.npmjs.org")
    if selected_hosts_out is not None:
        selected_hosts_out[:] = selected_hosts

    all_pem_paths: list[str] = []

    # Fetch certs for fixed setup hosts
    for hostname in _SETUP_HOSTS:
        pem = _ensure_ca_bundle(hostname)
        if pem:
            all_pem_paths.append(pem)
            print(f"  ✓ CA bundle cached for {hostname}")
        else:
            print(f"  ⚠ Could not cache CA bundle for {hostname}; will try system CA")

    # Fetch certs for dynamically determined hosts (e.g. Jira)
    for hostname in extra_hosts:
        pem = _ensure_ca_bundle(hostname)
        if pem:
            all_pem_paths.append(pem)
            print(f"  ✓ CA bundle cached for {hostname}")
        else:
            print(f"  ⚠ Could not cache CA bundle for {hostname}; will try system CA")

    # npm registry — conditionally gated by npm_enabled
    npmrc_result_path: Path | None = None
    if npm_enabled:
        npm_pem = _ensure_ca_bundle("registry.npmjs.org")
        if npm_pem:
            all_pem_paths.append(npm_pem)
            print("  ✓ CA bundle cached for registry.npmjs.org")
        else:
            print("  ⚠ Could not cache CA bundle for registry.npmjs.org; will try system CA")

        # Build unified CA bundle first so npmrc can reference it
        unified_path = _build_unified_ca_bundle(all_pem_paths)

        # Write ~/.agdt/npmrc pointing to the unified CA bundle (or the npm-specific
        # pem if unified bundle failed). npmrc is written even when npm cert fetch
        # fails — the unified bundle still contains system CAs that npm can use.
        ca_path_for_npmrc = str(unified_path) if unified_path else (npm_pem if npm_pem else None)
        if ca_path_for_npmrc:
            npmrc_path = Path.home() / ".agdt" / "npmrc"
            try:
                npmrc_path.parent.mkdir(parents=True, exist_ok=True)
                npmrc_path.write_text(f"cafile={ca_path_for_npmrc}\n", encoding="utf-8")
            except OSError as exc:
                print(f"  ⚠ Could not write npm CA config {npmrc_path}: {exc}", file=sys.stderr)
            else:
                print("  ✓ npm CA config written to ~/.agdt/npmrc")
                npmrc_result_path = npmrc_path
                # Set NPM_CONFIG_USERCONFIG for the current process
                npmrc_str = str(npmrc_path)
                if not os.environ.get("NPM_CONFIG_USERCONFIG"):
                    os.environ["NPM_CONFIG_USERCONFIG"] = npmrc_str
                    print(f"  ✓ NPM_CONFIG_USERCONFIG set for this session: {npmrc_str}")
    else:
        print("  ⚠ npm certificate work skipped (no npm footprint detected or --no-npm specified)")
        # Build unified CA bundle without npm cert
        unified_path = _build_unified_ca_bundle(all_pem_paths)

    # Wire the unified bundle into the running process so that all
    # subsequent HTTPS calls (e.g. install_copilot_cli, install_gh_cli)
    # use corporate CAs automatically.
    if unified_path:
        if not os.environ.get("REQUESTS_CA_BUNDLE"):
            os.environ["REQUESTS_CA_BUNDLE"] = str(unified_path)
            print(f"  ✓ REQUESTS_CA_BUNDLE set for this session: {unified_path}")
        if npm_enabled and not os.environ.get("NODE_EXTRA_CA_CERTS"):
            os.environ["NODE_EXTRA_CA_CERTS"] = str(unified_path)
            print(f"  ✓ NODE_EXTRA_CA_CERTS set for this session: {unified_path}")
        print("  ✓ Unified CA bundle written to ~/.agdt/certs/unified-ca-bundle.pem")

    return unified_path, npmrc_result_path


def _resolve_npm_enabled(args: argparse.Namespace, directory: Path) -> bool:
    """Resolve whether npm-specific setup work should be performed.

    Resolution priority:
    1. ``--npm`` flag → ``True``
    2. ``--no-npm`` flag → ``False``
    3. Neither → auto-detect via :func:`detect_npm_footprint`

    Args:
        args: Parsed CLI arguments (expects ``npm`` and ``no_npm`` attributes).
        directory: Directory to check for npm footprint (typically repo root).

    Returns:
        Whether npm certificate and configuration work should be performed.
    """
    from .npm_footprint import detect_npm_footprint

    if getattr(args, "npm", False):
        return True
    if getattr(args, "no_npm", False):
        return False
    return detect_npm_footprint(directory)


def _register_setup_artifacts(
    repo_root: Path,
    unified_path: Path | None,
    npmrc_path: Path | None,
    *,
    dry_run: bool = False,
) -> None:
    """Record this repository's cert/npm artifacts in ``~/.agdt/registry.json``.

    Maintains the append-only, content-addressed *reference index* backing
    FR-002 multi-repo coexistence (partial): each repository context references
    the shared artifacts it installed so that registering one repository's
    artifacts never removes another repository's reference.

    Scope note: this records references only and runs *after* the shared
    artifact files have already been written to their singleton paths by
    :func:`_prefetch_certs`.  It therefore tracks — but does not physically
    prevent — an in-place overwrite of a singleton artifact whose rebuilt
    content differs; hash-derived artifact storage remains follow-up work.

    Content hashes are computed *inside* the registry lock (inside
    :func:`~agentic_devtools.cli.setup.registry.register_context`) so the
    recorded hash matches the file's bytes at the moment of registration,
    avoiding a TOCTOU race between hashing and persisting.

    Under *dry_run* this prints a deterministic "would …" message and writes
    nothing.  Any registry failure is caught and reported without aborting
    setup — registration is best-effort bookkeeping, not a setup gate.

    Args:
        repo_root: The repository root defining the ``repository_context_id``.
        unified_path: Path to the unified CA bundle, or ``None``.
        npmrc_path: Path to the managed ``npmrc`` file, or ``None``.
        dry_run: When ``True``, only preview; never touch the filesystem.
    """
    if dry_run:
        planned = sum(1 for candidate in (unified_path, npmrc_path) if candidate is not None)
        print(f"  ○ would register {planned} artifact(s) for this repository context in ~/.agdt/registry.json")
        return
    try:
        from .registry import register_context

        artifact_paths: list[tuple[str, Path]] = []
        for artifact_type, artifact_path in (("cert_bundle", unified_path), ("npmrc", npmrc_path)):
            if artifact_path is not None and Path(artifact_path).is_file():
                artifact_paths.append((artifact_type, Path(artifact_path)))
        if artifact_paths:
            register_context(repo_root, artifact_paths)
            print(
                f"  \u2713 Registered {len(artifact_paths)} artifact(s) for this repository context"
                " in ~/.agdt/registry.json"
            )
    except Exception as exc:  # noqa: BLE001 - registration is best-effort bookkeeping
        print(f"  \u26a0 Could not update ~/.agdt/registry.json: {exc}", file=sys.stderr)


def _is_managed_bin_on_path() -> bool:
    """Check if ``~/.agdt/bin`` is already on the ``PATH``."""
    managed_bin = str(_MANAGED_BIN_DIR).rstrip(os.sep)
    path_entries = [entry.rstrip(os.sep) for entry in os.environ.get("PATH", "").split(os.pathsep) if entry]
    home = str(Path.home())
    normalised = [p.replace("~", home) for p in path_entries]
    return managed_bin in normalised


def _print_path_instructions_if_needed(*, persist_env: bool = False, overwrite_env: bool = False) -> None:
    """Print PATH setup instructions when ``~/.agdt/bin`` is not on the PATH.

    When *persist_env* is ``True``, attempts to persist the PATH entry to the
    shell profile instead of just printing instructions.
    """
    if not _is_managed_bin_on_path():
        if persist_env:
            _persist_env_vars_to_profile(
                npmrc_path=None,
                unified_path=None,
                persist_env=True,
                overwrite_env=overwrite_env,
                path_only=True,
            )
        else:
            print(_PATH_INSTRUCTIONS)


def _persist_env_vars_to_profile(
    *,
    npmrc_path: Path | None,
    unified_path: Path | None,
    persist_env: bool,
    overwrite_env: bool,
    path_only: bool = False,
    npm_enabled: bool = True,
    dry_run: bool = False,
) -> None:
    """Orchestrate persisting env vars to the user's shell profile.

    When *persist_env* is ``False``, prints manual instructions instead.
    When *path_only* is ``True``, only handles the ``PATH`` entry.

    When *npm_enabled* is ``False``, the npm-specific environment variables
    (``NPM_CONFIG_USERCONFIG`` and ``NODE_EXTRA_CA_CERTS``) are skipped
    entirely — any pre-existing lines in the shell profile are left intact
    (append/refresh-only coexistence invariant).

    When *dry_run* is ``True``, prints "would …" messages and returns
    without writing to any shell profile file.

    Args:
        npmrc_path: Path to the ``~/.agdt/npmrc`` file (or ``None``).
        unified_path: Path to the unified CA bundle (or ``None``).
        persist_env: Whether to persist to the shell profile.
        overwrite_env: Whether to replace existing lines.
        path_only: Only persist/print ``PATH`` instructions.
        npm_enabled: Whether npm-specific env vars should be persisted.
        dry_run: When ``True``, skip all writes and print preview messages.
    """
    managed_bin_str = str(_MANAGED_BIN_DIR)

    # Check if PATH already contains the managed bin dir
    managed_on_path = _is_managed_bin_on_path()

    # Best-effort shell detection for manual instructions; ignore failures.
    try:
        shell_type_hint = detect_shell_type()
    except Exception:  # noqa: BLE001
        shell_type_hint = None

    if not persist_env:
        if path_only:
            if not managed_on_path:
                print(_PATH_INSTRUCTIONS)
        else:
            _print_manual_instructions(
                npmrc_path,
                unified_path,
                managed_on_path,
                shell_type_hint,
                npm_enabled=npm_enabled,
            )
        return

    if dry_run:
        print("  ○ would persist environment variables to shell profile")
        return

    try:
        profile_path = detect_shell_profile()
        shell_type = detect_shell_type()
    except Exception as exc:  # noqa: BLE001
        print(f"  ⚠ Could not detect shell profile: {exc}", file=sys.stderr)
        # Fall back to manual instructions
        _persist_env_vars_to_profile(
            npmrc_path=npmrc_path,
            unified_path=unified_path,
            persist_env=False,
            overwrite_env=overwrite_env,
            path_only=path_only,
            npm_enabled=npm_enabled,
        )
        return

    if profile_path is None:
        # Unknown shell — print manual instructions
        if path_only:
            if not managed_on_path:
                print(_PATH_INSTRUCTIONS)
        else:
            _print_manual_instructions(
                npmrc_path,
                unified_path,
                managed_on_path,
                shell_type_hint,
                npm_enabled=npm_enabled,
            )
        return

    if not path_only:
        if npmrc_path and npm_enabled:
            _persist_single_var(profile_path, "NPM_CONFIG_USERCONFIG", str(npmrc_path), shell_type, overwrite_env)
        if unified_path:
            _persist_single_var(profile_path, "REQUESTS_CA_BUNDLE", str(unified_path), shell_type, overwrite_env)
            if npm_enabled:
                _persist_single_var(profile_path, "NODE_EXTRA_CA_CERTS", str(unified_path), shell_type, overwrite_env)

    # PATH entry
    if not managed_on_path:
        result = persist_path_entry(profile_path, managed_bin_str, shell_type, overwrite=overwrite_env)
        if result:
            print(f"  ✓ PATH entry persisted to {profile_path}")
        else:
            # Check if it was skipped (already exists) vs. failed
            try:
                if profile_path.exists() and managed_bin_str in profile_path.read_text(
                    encoding="utf-8", errors="replace"
                ):
                    print(f"  ℹ PATH entry already set in {profile_path} (use --overwrite-env to replace)")
            except OSError:
                pass  # persist_path_entry already printed a warning


def _print_manual_instructions(
    npmrc_path: Path | None,
    unified_path: Path | None,
    managed_on_path: bool,
    shell_type: str | None,
    npm_enabled: bool = True,
) -> None:
    """Print shell-specific manual instructions for env var persistence."""
    if not npm_enabled:
        npmrc_path = None

    has_vars = bool(npmrc_path or unified_path or not managed_on_path)
    if not has_vars:
        return

    if shell_type in ("bash", "zsh"):
        instructions = ["\n  ℹ Add the following to your ~/.bashrc or ~/.zshrc:"]
        if npmrc_path:
            instructions.append(f'    export NPM_CONFIG_USERCONFIG="{npmrc_path}"')
        if unified_path:
            instructions.append(f'    export REQUESTS_CA_BUNDLE="{unified_path}"')
            if npm_enabled:
                instructions.append(f'    export NODE_EXTRA_CA_CERTS="{unified_path}"')
        if not managed_on_path:
            instructions.append('    export PATH="$HOME/.agdt/bin:$PATH"')
        print("\n".join(instructions))
    elif shell_type == "powershell":
        instructions = ["\n  ℹ Add the following to your PowerShell $PROFILE:"]
        if npmrc_path:
            instructions.append(f'    $env:NPM_CONFIG_USERCONFIG = "{npmrc_path}"')
        if unified_path:
            instructions.append(f'    $env:REQUESTS_CA_BUNDLE = "{unified_path}"')
            if npm_enabled:
                instructions.append(f'    $env:NODE_EXTRA_CA_CERTS = "{unified_path}"')
        if not managed_on_path:
            instructions.append('    $env:PATH = "$env:USERPROFILE\\.agdt\\bin;$env:PATH"')
        print("\n".join(instructions))
    else:
        # Unknown shell: show both bash/zsh and PowerShell examples
        instructions = [
            "\n  ℹ Add the following to your shell profile.",
            "  Examples for bash/zsh and PowerShell:",
        ]
        if npmrc_path or unified_path or not managed_on_path:  # pragma: no branch
            instructions.append("    # bash / zsh:")
        if npmrc_path:
            instructions.append(f'    export NPM_CONFIG_USERCONFIG="{npmrc_path}"')
        if unified_path:
            instructions.append(f'    export REQUESTS_CA_BUNDLE="{unified_path}"')
            if npm_enabled:
                instructions.append(f'    export NODE_EXTRA_CA_CERTS="{unified_path}"')
        if not managed_on_path:
            instructions.append('    export PATH="$HOME/.agdt/bin:$PATH"')
        if npmrc_path or unified_path or not managed_on_path:  # pragma: no branch
            instructions.append("    # PowerShell:")
        if npmrc_path:
            instructions.append(f'    $env:NPM_CONFIG_USERCONFIG = "{npmrc_path}"')
        if unified_path:
            instructions.append(f'    $env:REQUESTS_CA_BUNDLE = "{unified_path}"')
            if npm_enabled:
                instructions.append(f'    $env:NODE_EXTRA_CA_CERTS = "{unified_path}"')
        if not managed_on_path:
            instructions.append('    $env:PATH = "$env:USERPROFILE\\.agdt\\bin;$env:PATH"')
        print("\n".join(instructions))


def _persist_single_var(profile_path: Path, var_name: str, var_value: str, shell_type: str, overwrite: bool) -> None:
    """Persist a single env var and print the appropriate message."""
    result = persist_env_var(profile_path, var_name, var_value, shell_type, overwrite=overwrite)
    if result:
        print(f"  ✓ {var_name} persisted to {profile_path}")
    else:
        # Check if it was skipped (already exists) vs. failed
        try:
            if profile_path.exists() and var_name in profile_path.read_text(encoding="utf-8", errors="replace"):
                print(f"  ℹ {var_name} already set in {profile_path} (use --overwrite-env to replace)")
        except OSError:
            pass  # persist_env_var already printed a warning


def _prompt_project_config(*, force_prompt: bool = False) -> None:
    """Prompt the user for project-specific configuration values.

    Reads existing values from ``.agdt/config/project.json`` as defaults.
    Saves responses back to the same file.

    When *force_prompt* is ``False`` (the default), prompts are **skipped**
    for any key that is already present in the config (even if the value is
    ``""``).  Pass ``force_prompt=True`` (via ``--reconfigure``) to
    re-prompt for every field.
    """
    from agentic_devtools.cli.config.project_config import (
        load_project_config,
        save_project_config,
    )

    existing = load_project_config()

    print()
    print("─── Project Configuration ───────────────────────────────────")
    print("  Configure project-specific settings.")
    print("  Press Enter to keep current value; for optional fields, type '-' or 'clear' to clear.")
    print()

    def _ask(prompt: str, key: str, allow_clear: bool = False) -> str:
        # Skip prompt entirely when the key is already present and re-prompting
        # was not requested (key presence = "already answered").
        if not force_prompt and key in existing:
            # Normalise to str: config is dict[str, Any] so values may be
            # None or non-string after manual JSON edits.
            value = existing[key]
            return "" if value is None else str(value)
        raw_current = existing.get(key, "")
        current = "" if raw_current is None else str(raw_current)
        suffix = f" [{current}]" if current else ""
        answer = input(f"  {prompt}{suffix}: ").strip()
        if allow_clear and answer.lower() in {"-", "clear"}:
            return ""
        # Reject clear sentinels for required fields — treat as "keep current"
        if not allow_clear and answer.lower() in {"-", "clear"}:
            return current
        if answer:
            return answer
        return current

    jira_keys = _ask("Jira project key(s), comma-separated (e.g. ACME,PROJ)", "jira_project_keys")
    jira_base_url = _ask("Jira base URL (e.g. https://jira.example.com)", "jira_base_url")
    corp_host = _ask(
        "Corporate network test host (type '-' or 'clear' to clear)", "corporate_network_test_host", allow_clear=True
    )
    vpn_url = _ask("VPN portal URL (type '-' or 'clear' to clear)", "vpn_url", allow_clear=True)
    vpn_hostnames = _ask(
        "VPN hostnames for smart detection, comma-separated (type '-' or 'clear' to clear)",
        "vpn_hostnames",
        allow_clear=True,
    )

    config = dict(existing)  # preserve any extra keys
    for key, value in [
        ("jira_project_keys", jira_keys),
        ("jira_base_url", jira_base_url),
        ("corporate_network_test_host", corp_host),
        ("vpn_url", vpn_url),
        ("vpn_hostnames", vpn_hostnames),
    ]:
        config[key] = value

    # Per-field idempotency: write commit type defaults only when both
    # camelCase canonical and snake_case alias are absent (FR-007).
    from agentic_devtools.cli.config.commit_type_resolution import STANDARD_COMMIT_TYPES

    if "defaultCommitIssueType" not in config and "default_commit_issue_type" not in config:
        config["defaultCommitIssueType"] = "feat"
    if "availableCommitIssueTypes" not in config and "available_commit_issue_types" not in config:
        config["availableCommitIssueTypes"] = list(STANDARD_COMMIT_TYPES)

    path = save_project_config(config)
    print(f"\n  ✓ Project configuration saved to {path}")


def _query_copilot_model_records(*, refresh: bool = True, allow_stale: bool = False) -> list[Any]:
    """Return complete Copilot ACP records, including raw metadata and source."""
    from agentic_devtools.ai_providers.copilot_discovery import discover_copilot_models  # noqa: PLC0415

    return discover_copilot_models(refresh=refresh, allow_stale=allow_stale)


def _query_copilot_models(*, refresh: bool = True, allow_stale: bool = False) -> list[str]:
    """Return the available Copilot model ids discovered over ACP.

    Delegates to
    :func:`agentic_devtools.ai_providers.copilot_discovery.discover_copilot_models`,
    which performs the ``initialize`` → ``session/new`` ACP handshake and reads
    the authoritative ``result.models.availableModels`` list.

    *refresh* controls whether a live ACP query is attempted.  Pass
    ``refresh=False`` (``--no-refresh-models``) to skip the live query and
    read the cache only.

    *allow_stale* is an independent policy gate.  When ``True``, an expired
    cache entry may be returned as a last resort if neither the live query nor
    a fresh cache entry succeeded.  It should be ``True`` only when the caller
    is honouring the user's ``--no-refresh-models`` choice; internal calls that
    merely skip a redundant ACP handshake should leave it at its default
    ``False`` so that a stale cache is never promoted during an ordinary
    refresh run.  Never raises.
    """
    return [record.model_id for record in _query_copilot_model_records(refresh=refresh, allow_stale=allow_stale)]


def _populate_available_models(*, refresh_models: bool = True) -> None:
    """Populate or refresh the top-level ``availableModels`` inventory in project.json.

    Discovers the live inventory via :func:`_query_copilot_model_records` (the ACP
    ``initialize`` → ``session/new`` handshake) and caches the result under both the
    top-level ``"availableModels"`` key and the normalized ``"models"`` tree in
    ``.agdt/config/project.json``.  The cached inventory is read (never re-queried)
    during PR reviews.

    Discovery runs on every ``agdt-setup`` run by default.  Pass
    ``refresh_models=False`` (``--no-refresh-models``) to skip the live query;
    in that case an already-valid inventory is kept as-is and only a missing or
    invalid inventory is filled in from the discovery cache.

    When the inventory cannot be discovered the previously cached value is kept
    and a warning is printed — setup is never failed because Copilot is
    unreachable.  ``--reconfigure`` still re-prompts the default-model
    selection without changing this refresh policy.
    """
    from agentic_devtools.cli.config.project_config import (
        load_project_config,
        save_project_config,
    )

    existing = load_project_config()

    print()
    print("─── Available Models Inventory ──────────────────────────────")
    cached = existing.get("availableModels")
    has_valid_cache = (
        isinstance(cached, list) and bool(cached) and all(isinstance(m, str) and m.strip() for m in cached)
    )
    if not refresh_models and has_valid_cache:
        print("  ℹ Available models inventory kept (--no-refresh-models)")
        return

    cached_records_by_model_id: dict[str, Any] = {}
    if refresh_models:
        from agentic_devtools.ai_providers.copilot_discovery import read_model_cache

        cached_records = read_model_cache(allow_stale=False)
        if cached_records:
            for cached_record in cached_records:
                cached_model_id = getattr(cached_record, "model_id", None)
                if isinstance(cached_model_id, str) and cached_model_id.strip():
                    normalized_cached_model_id = cached_model_id.strip()
                    cached_records_by_model_id.setdefault(normalized_cached_model_id, cached_record)

    records = _query_copilot_model_records(refresh=refresh_models, allow_stale=not refresh_models)
    if not records:
        if has_valid_cache:
            print("  ⚠ Model discovery returned nothing — keeping the cached availableModels inventory")
        else:
            print("  ⚠ Model discovery returned nothing — availableModels remains empty")
        return

    from agentic_devtools.cli.config.project_config import _build_model_metadata_entry

    config = dict(existing)
    existing_models = existing.get("models")
    existing_models = existing_models if isinstance(existing_models, dict) else {}
    normalized_records = []
    seen: set[str] = set()
    for record in records:
        model_id = getattr(record, "model_id", None)
        if not isinstance(model_id, str) or not model_id.strip():
            continue
        model_id = model_id.strip()
        if model_id in seen:
            continue
        seen.add(model_id)
        normalized_records.append(record)
    config["availableModels"] = [record.model_id.strip() for record in normalized_records]
    normalized_models = dict(existing_models)
    for record in normalized_records:
        normalized_models[record.model_id.strip()] = _build_model_metadata_entry(
            record.model_id,
            existing_entry=(
                existing_models.get(record.model_id.strip()) if isinstance(existing_models, dict) else None
            ),
            acp_record=record,
            acp_cache_record=cached_records_by_model_id.get(record.model_id.strip()),
            emit_warnings=False,
        )
    if normalized_models:
        config["models"] = normalized_models
    save_project_config(config)
    print(f"  ✓ Cached {len(normalized_records)} available model(s) to availableModels")


def _prompt_copilot_model(*, force_prompt: bool = False, refresh_models: bool = False) -> None:
    """Prompt the user to select the default Copilot model for workflow sessions.

    Reads the inventory from the ``availableModels`` key already written to
    project config by :func:`_populate_available_models`.  Falls back to
    :func:`_query_copilot_models` only when that key is absent.  When no
    inventory is available (Copilot unreachable and no cache) a free-form model
    name can still be entered.  Persists the selection to
    ``.agdt/config/project.json`` under ``"default_copilot_model"``.

    When *force_prompt* is ``False`` (the default), the prompt is **skipped**
    if ``"default_copilot_model"`` already exists in the config (even if
    ``""``).  Pass ``force_prompt=True`` (via ``--reconfigure``) to force
    re-selection.
    """
    from agentic_devtools.cli.config.project_config import (
        load_project_config,
        save_project_config,
    )

    existing = load_project_config()
    raw_model = existing.get("default_copilot_model", "")
    current_model = raw_model.strip() if isinstance(raw_model, str) else ""

    if not force_prompt and "default_copilot_model" in existing:
        current_value = existing["default_copilot_model"]
        print()
        print("─── Copilot Model Configuration ─────────────────────────────")
        print(f"  ℹ Default Copilot model already set: {current_value}")
        return

    print()
    print("─── Copilot Model Configuration ─────────────────────────────")
    print("  Select the default Copilot model for workflow sessions.")
    print()

    # Prefer the availableModels already written to project config by
    # _populate_available_models; fall back to _query_copilot_models only when
    # the project inventory is absent (e.g. first run before any discovery).
    project_inventory = existing.get("availableModels")
    if isinstance(project_inventory, list):
        models = []
        for model in project_inventory:
            if isinstance(model, str):
                normalized = model.strip()
                if normalized:
                    models.append(normalized)
    else:
        models = _query_copilot_models(refresh=False, allow_stale=False)

    if models:
        print("  Available models:")
        for i, m in enumerate(models, start=1):
            print(f"    {i}. {m}")
    else:
        print("  ⚠ No Copilot model inventory available — type a model name manually.")
    print()
    if current_model in models:
        default_selection = current_model
    elif models:
        default_selection = models[0]
    else:
        default_selection = current_model

    try:
        answer = input(f"  Default Copilot model [{default_selection}]: ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return

    if not answer:
        chosen = default_selection
    elif answer.isdigit():
        idx = int(answer) - 1
        if 0 <= idx < len(models):
            chosen = models[idx]
        else:
            print(f"  ⚠ Invalid selection — keeping current default ({default_selection})")
            chosen = default_selection
    else:
        # Accept a free-form model name typed directly
        chosen = answer

    if not chosen:
        print("  ⚠ No model selected — leaving default_copilot_model unset")
        return

    config = dict(existing)
    config["default_copilot_model"] = chosen
    save_project_config(config)
    print(f"  ✓ Default Copilot model set to: {chosen}")


def _generate_setup_scripts(git_root: Path) -> None:
    """Generate the modular setup scripts in ``.agdt/`` and repo root.

    This is the new final phase of ``agdt-setup``.  It always overwrites
    managed scripts and only creates ``setup-repo-specific-dev-tools.py``
    when it does not already exist.
    """
    from .script_generators.atomic_write import atomic_write
    from .script_generators.complete_setup import generate_complete_setup_script
    from .script_generators.configured_setup import generate_configured_setup_script
    from .script_generators.constants import (
        COMPLETE_SETUP_FILENAME,
        CONFIGURED_SETUP_FILENAME,
        REPO_SPECIFIC_FILENAME,
        REQUIRED_SETUP_FILENAME,
        ROOT_ENTRY_POINT_FILENAME,
    )
    from .script_generators.gitignore_updater import update_gitignore
    from .script_generators.legacy_migration import detect_legacy_script, migrate_legacy_content
    from .script_generators.repo_specific import generate_repo_specific_stub
    from .script_generators.required_setup import generate_required_setup_script
    from .script_generators.root_entry_point import generate_root_entry_point

    agdt_dir = git_root / ".agdt"
    agdt_dir.mkdir(parents=True, exist_ok=True)

    # 1) Always overwrite managed scripts
    atomic_write(agdt_dir / REQUIRED_SETUP_FILENAME, generate_required_setup_script())
    print(f"  ✓ Generated .agdt/{REQUIRED_SETUP_FILENAME}")

    # For now, no tool selections are wired — generate with empty tools.
    # Future: pass selected tools from agdt-setup prompts.
    atomic_write(agdt_dir / CONFIGURED_SETUP_FILENAME, generate_configured_setup_script())
    print(f"  ✓ Generated .agdt/{CONFIGURED_SETUP_FILENAME}")

    atomic_write(agdt_dir / COMPLETE_SETUP_FILENAME, generate_complete_setup_script())
    print(f"  ✓ Generated .agdt/{COMPLETE_SETUP_FILENAME}")

    # 2) Legacy migration — check before overwriting the root entry point
    root_entry = git_root / ROOT_ENTRY_POINT_FILENAME
    migration_failed = False
    if detect_legacy_script(root_entry):
        repo_specific = git_root / REPO_SPECIFIC_FILENAME
        success, msg = migrate_legacy_content(root_entry, repo_specific)
        print(msg)
        if not success:
            migration_failed = True

    # 3) Overwrite root entry point only if migration succeeded (or was not needed)
    if migration_failed:
        print(f"  ⚠ Skipping {ROOT_ENTRY_POINT_FILENAME} overwrite due to migration failure")
    else:
        atomic_write(root_entry, generate_root_entry_point())
        print(f"  ✓ Generated {ROOT_ENTRY_POINT_FILENAME}")

    # 4) Create repo-specific stub only if it doesn't exist
    repo_specific = git_root / REPO_SPECIFIC_FILENAME
    if not repo_specific.exists():
        atomic_write(repo_specific, generate_repo_specific_stub())
        print(f"  ✓ Created {REPO_SPECIFIC_FILENAME} (customize as needed)")
    else:
        print(f"  ℹ {REPO_SPECIFIC_FILENAME} already exists — not overwriting")

    # 5) Update .gitignore
    msg = update_gitignore(git_root)
    print(msg)


def _resolve_injection_axes(
    explicit_issue_adapter: str | None,
    explicit_code_hosting: str | None,
    *,
    skip_platform_detection: bool,
    detection_failed: bool,
    is_interactive: bool,
) -> tuple[str | None, str | None]:
    """Resolve filter-capable skill-injection axes from explicitly-tracked values.

    Returns ``(None, None)`` — legacy inject-all — when *any* of the following
    hold (FR-003):

    - ``skip_platform_detection`` is ``True``
    - ``detection_failed`` is ``True``
    - ``is_interactive`` is ``False`` (no TTY)

    Otherwise, maps *explicit_issue_adapter* and *explicit_code_hosting* to a
    filter-capable ``(issue_adapter, code_hosting)`` pair via
    :func:`resolve_platform_context`.  Values that are not filter-capable
    (``"markdown"`` for the adapter axis, ``"other"`` for the hosting axis) are
    normalised to ``None`` so that the corresponding axis stays unrestricted.

    **Callers must pass only genuinely resolved values** — values from a
    positive platform detection, an explicit ``--issue-adapter`` CLI override,
    or an authoritative persisted platform value.  Callers must not pass
    synthesized/persisted fallback defaults (for example
    ``DEFAULT_ISSUE_ADAPTER`` or ``DEFAULT_CODE_HOSTING``): those are not
    evidence of a real detection and would cause spurious skill pruning when
    no platform was actually found.

    A returned ``None`` axis means "inject-all for that axis"; when both axes are
    ``None`` injection is byte-identical to the legacy inject-all behavior.
    """
    if skip_platform_detection or detection_failed or not is_interactive:
        return None, None

    from agentic_devtools.skill_classification import resolve_platform_context  # noqa: PLC0415

    return resolve_platform_context({"issue_adapter": explicit_issue_adapter, "code_hosting": explicit_code_hosting})


def _resolve_saved_injection_axes(git_root: Path) -> tuple[str | None, str | None]:
    """Resolve injection axes from saved platform config using live marker semantics.

    Uses the same ``issue_adapter_resolved`` interpretation as live setup for
    persisted config: a boolean ``True`` marker is authoritative, a non-boolean
    marker is ignored as malformed, and legacy markerless configs are
    authoritative only when ``issue_adapter`` is a non-default adapter.
    """
    from agentic_devtools.config import DEFAULT_ISSUE_ADAPTER, load_repo_config  # noqa: PLC0415
    from agentic_devtools.skill_classification import resolve_platform_context  # noqa: PLC0415

    repo_cfg = load_repo_config(str(git_root))
    raw_platform = repo_cfg.get("platform")
    if not isinstance(raw_platform, dict):
        return None, None

    issue_adapter, code_hosting = resolve_platform_context(raw_platform)
    resolved_marker = raw_platform.get(_ISSUE_ADAPTER_RESOLVED_KEY)
    if isinstance(resolved_marker, bool):
        issue_adapter_resolved = resolved_marker
    elif _ISSUE_ADAPTER_RESOLVED_KEY in raw_platform:
        issue_adapter_resolved = False
    else:
        issue_adapter_resolved = raw_platform.get("issue_adapter") not in (None, DEFAULT_ISSUE_ADAPTER)

    return (issue_adapter if issue_adapter_resolved else None), code_hosting


def _format_injection_summary(
    summary: InjectionSummary,
    issue_adapter: str | None,
    code_hosting: str | None,
) -> str:
    """Build the success line printed after a skill-injection pass.

    When both axes are ``None`` (legacy inject-all), no filter was applied and
    the pruned count is always zero, so the line omits the prune/platform
    detail.  When at least one axis is resolved, the line reports how many files
    were pruned and which axes constrained injection (an unresolved axis renders
    as ``unrestricted``).
    """
    if issue_adapter is None and code_hosting is None:
        return f"  ✓ Injected {summary.injected} agent/prompt/skill items (no platform filter applied)"

    adapter_label = issue_adapter if issue_adapter is not None else "unrestricted"
    hosting_label = code_hosting if code_hosting is not None else "unrestricted"
    return (
        f"  ✓ Injected {summary.injected} agent/prompt/skill items, pruned {summary.pruned} "
        f"(issue_adapter={adapter_label}, code_hosting={hosting_label})"
    )


def _preview_skill_injection(git_root: Path) -> None:
    """Print the skill-injection manifest diff for a ``--dry-run`` invocation.

    Runs the injector in its dry-run mode, which prints the per-kind adds /
    overwrites / deletes lists and writes, copies and unlinks nothing.  The
    import is guarded exactly like the real injection call site so a missing or
    unimportable injector degrades to a warning instead of failing the dry run.

    Platform detection still does not run under ``--dry-run``.  To keep the
    preview closer to what a subsequent live run executes, the injector uses the
    persisted platform axes resolved with the same marker semantics as live
    setup; when no authoritative saved axis exists, that axis remains
    unrestricted (``None``).
    """
    print("  ○ would inject agent/prompt/skill files")
    try:
        from agentic_devtools.skill_injector import (  # noqa: PLC0415
            inject_skills_with_summary as _inject_with_summary,
        )
    except (SyntaxError, ImportError) as exc:
        print(
            f"  ⚠ Failed to import skill injector ({exc!r}) — manifest diff unavailable",
            file=sys.stderr,
        )
        return

    issue_adapter, code_hosting = _resolve_saved_injection_axes(git_root)
    adapter_label = issue_adapter if issue_adapter is not None else "unrestricted"
    hosting_label = code_hosting if code_hosting is not None else "unrestricted"
    print(
        "    (diff computed using saved platform axes"
        f" issue_adapter={adapter_label}, code_hosting={hosting_label};"
        " platform detection does not run under --dry-run)"
    )

    success, _summary = _inject_with_summary(
        git_root,
        issue_adapter=issue_adapter,
        code_hosting=code_hosting,
        dry_run=True,
    )
    if not success:
        print(
            "  ⚠ Skill injector reported a failure — manifest diff may be incomplete",
            file=sys.stderr,
        )


def _specialization_repo_identifier(remote_url: str | None) -> str:
    """Return the supported origin identifier used in specialization metadata."""
    if not remote_url:
        return ""

    from .platform_detection import _ADO_HTTPS_RE, _ADO_LEGACY_RE, _ADO_SSH_RE

    for pattern in (_ADO_HTTPS_RE, _ADO_SSH_RE, _ADO_LEGACY_RE):
        match = pattern.search(remote_url)
        if match:
            return f"{match.group(1)}/{match.group(2)}"

    match = _GENERIC_HTTPS_REMOTE_RE.search(remote_url)
    if match:
        return f"{match.group(1)}/{match.group(2)}"

    match = _GENERIC_SCP_REMOTE_RE.search(remote_url)
    if match:
        return f"{match.group(1)}/{match.group(2)}"

    return ""


def _cleanup_stale_specialization_artifact(
    reason: str,
    *,
    startup_fingerprint: tuple[int, int, int] | None | object,
) -> None:
    """Remove stale setup-expectations-specialized.md on an early exit path.

    Called on every exit path that does not produce a current specialization so
    a previous run's artifact is not presented as current metadata.  Failures
    are non-fatal — a warning is emitted on stderr but the caller's exit path
    proceeds normally.

    Args:
        startup_fingerprint: Pre-captured fingerprint from
            ``capture_startup_fingerprint()`` taken at setup startup.  Passed
            through to ``cleanup_specialized_output()`` so that a stale run
            cannot remove an artifact published by a concurrent newer run after
            startup.
    """
    try:
        from agentic_devtools.state import get_state_dir

        from .expectations_specializer import _StartupFingerprintState, cleanup_specialized_output

        state_dir = (
            startup_fingerprint.state_dir
            if isinstance(startup_fingerprint, _StartupFingerprintState)
            else get_state_dir()
        )
        result = cleanup_specialized_output(
            state_dir,
            status="skipped",
            reason=reason,
            startup_fingerprint=startup_fingerprint,
        )
        if result.status == "error":
            print(
                f"  ⚠ Failed to clean up stale setup-expectations-specialized.md: {result.reason}",
                file=sys.stderr,
            )
    except Exception as exc:  # noqa: BLE001
        print(
            f"  ⚠ Failed to clean up stale setup-expectations-specialized.md: {exc}",
            file=sys.stderr,
        )


def _capture_specialization_startup_fingerprint(
    *, dry_run: bool
) -> tuple[int, int, int] | _StartupFingerprintState | None | _StartupFingerprintError | object:
    """Capture the specialization output fingerprint unless dry-run suppresses it.

    ``agdt-setup --dry-run`` is preview-only, so it must not resolve/create the
    state directory just to inspect or clean up the specialized expectations
    artifact. Live runs still capture the fingerprint at startup so later
    cleanup and publish decisions can distinguish stale output from a newer
    concurrent run's artifact.
    """
    if dry_run:
        return None

    from .expectations_specializer import _StartupFingerprintError
    from .expectations_specializer import capture_startup_state as _cap_state

    try:
        from agentic_devtools.state import get_state_dir as _get_state_dir_for_fp

        state_dir = _get_state_dir_for_fp(create=False)
        return _cap_state(state_dir)
    except Exception as exc:  # noqa: BLE001
        return _StartupFingerprintError(error=exc if isinstance(exc, OSError) else OSError(str(exc)))


def _specialize_setup_expectations(
    git_root: Path | None,
    args: argparse.Namespace,
    *,
    npm_enabled: bool,
    skip_repo_steps: bool,
    resolved_platform: Mapping[str, Any] | None = None,
    version_pin: str | None = None,
    ssl_hosts: tuple[str, ...] = (),
    startup_fingerprint: tuple[int, int, int] | None | object,
) -> None:
    """Write the repository-specialized setup expectations document.

    Args:
        resolved_platform: This run's resolved platform configuration
            (``issue_adapter``, ``issue_adapter_resolved``), captured directly
            from the file-modification step. Preferred over rereading
            ``.github/agdt-config.json``, which may reflect a stale worktree
            once the PR workflow restores the user's original branch.
        version_pin: The ``agdt_version`` pin resolved by ``check_version_guard()``
            for this run, or ``None`` when the repository is unpinned.
        ssl_hosts: Effective certificate-prefetch host set for this setup run.
        startup_fingerprint: Pre-captured fingerprint from
            ``capture_startup_fingerprint()`` taken at setup startup.  Passed
            through to ``cleanup_specialized_output()`` so that a stale run
            cannot remove an artifact published by a concurrent newer run after
            startup.
    """
    if git_root is None or skip_repo_steps:
        from agentic_devtools.state import get_state_dir

        from .expectations_specializer import _StartupFingerprintState, cleanup_specialized_output

        try:
            state_dir = (
                startup_fingerprint.state_dir
                if isinstance(startup_fingerprint, _StartupFingerprintState)
                else get_state_dir()
            )
            result = cleanup_specialized_output(
                state_dir,
                status="skipped",
                reason="Setup expectations specialization skipped (repository steps are skipped)",
                startup_fingerprint=startup_fingerprint,
            )
            if result.status == "error":
                print(
                    f"  ⚠ Failed to clean up stale setup-expectations-specialized.md: {result.reason}",
                    file=sys.stderr,
                )
        except OSError as exc:
            print(f"  ⚠ Failed to clean up stale setup-expectations-specialized.md: {exc}", file=sys.stderr)
        print("  ℹ Setup expectations specialization skipped (repository steps are skipped)")
        return

    from agentic_devtools.state import get_state_dir

    from .expectations_specializer import (
        RepositoryConfiguration,
        _StartupFingerprintState,
        resolve_general_doc_path,
        run_specialization,
    )
    from .platform_detection import _get_origin_remote_url

    remote_url = _get_origin_remote_url(str(git_root))
    repo = _specialization_repo_identifier(remote_url)
    issue_adapter = getattr(args, "issue_adapter", None)
    if resolved_platform:
        persisted_issue_adapter = resolved_platform.get("issue_adapter")
        # Only treat the persisted adapter as authoritative when this run's
        # own resolution marked it as genuinely resolved (not the ambiguous
        # default-Jira fallback) — mirrors `_resolve_saved_injection_axes()`.
        if resolved_platform.get(_ISSUE_ADAPTER_RESOLVED_KEY) is True and isinstance(persisted_issue_adapter, str):
            issue_adapter = issue_adapter or persisted_issue_adapter
    config = RepositoryConfiguration(
        repo=repo or f"local/{re.sub(r'[^A-Za-z0-9_.-]+', '-', git_root.name).strip('-') or 'repository'}",
        issue_adapter=str(issue_adapter or "unresolved"),
        has_npm=npm_enabled,
        ssl_hosts=() if args.system_only else ssl_hosts,
        system_only=bool(args.system_only),
        version_pin=version_pin,
        effective_flags=_effective_specialization_flags(args, npm_enabled=npm_enabled),
    )
    try:
        state_dir = (
            startup_fingerprint.state_dir
            if isinstance(startup_fingerprint, _StartupFingerprintState)
            else get_state_dir()
        )
        result = run_specialization(
            config,
            state_dir,
            resolve_general_doc_path(),
            startup_fingerprint=startup_fingerprint,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"  ⚠ Setup expectations specialization failed: {exc}", file=sys.stderr)
        _cleanup_stale_specialization_artifact(
            f"Setup expectations specialization failed: {exc}",
            startup_fingerprint=startup_fingerprint,
        )
        return
    if result.status == "success":
        print("  ✓ Wrote repository-specialized setup expectations")
    elif result.status == "skipped":
        print(f"  ℹ Setup expectations specialization skipped: {result.reason}")
    else:
        print(f"  ⚠ Setup expectations specialization failed: {result.reason}", file=sys.stderr)


def _effective_specialization_flags(
    args: argparse.Namespace,
    *,
    npm_enabled: bool,
) -> dict[str, str | bool | None]:
    """Return specialization metadata for setup controls.

    The mapping uses CLI flag names (for example ``"--system-only"``) for
    direct parser inputs and includes a small number of derived booleans
    (currently ``"autorun_enabled"`` and ``"npm_enabled"``) so the metadata
    captures the effective runtime behavior, not just the raw argv surface.
    """
    return {
        "--system-only": bool(getattr(args, "system_only", False)),
        "--no-verify-ssl": bool(getattr(args, "no_verify_ssl", False)),
        "--no-persist-env": bool(getattr(args, "no_persist_env", False)),
        "--overwrite-env": bool(getattr(args, "overwrite_env", False)),
        "--skip-platform-detection": bool(getattr(args, "skip_platform_detection", False)),
        "--issue-adapter": getattr(args, "issue_adapter", None),
        "--skip-templates": bool(getattr(args, "skip_templates", False)),
        "--reconfigure": bool(getattr(args, "reconfigure", False)),
        "--defaults": bool(getattr(args, "defaults", False)),
        "--skip-pr-workflow": bool(getattr(args, "skip_pr_workflow", False)),
        "--force-old-version": bool(getattr(args, "force_old_version", False)),
        "--npm": bool(getattr(args, "npm", False)),
        "--no-npm": bool(getattr(args, "no_npm", False)),
        "--run": getattr(args, "cli_run", None) is True,
        "--no-run": getattr(args, "cli_no_run", None) is True,
        "--no-refresh-models": bool(getattr(args, "no_refresh_models", False)),
        "--refresh-issue-types": bool(getattr(args, "refresh_issue_types", False)),
        "--dry-run": bool(getattr(args, "dry_run", False)),
        "--yes": bool(getattr(args, "yes", False)),
        "autorun_enabled": getattr(args, "autorun_enabled", None),
        "npm_enabled": npm_enabled,
    }


def _perform_standalone_refresh(
    args: argparse.Namespace,
    git_root: Path | None,
    dry_run: bool,
    skip_repo_steps: bool,
) -> RefreshOutcome:
    """Run the standalone ``--refresh-issue-types`` path and return its outcome.

    Emits the same human-readable stdout/stderr messages as the interactive
    setup flow and returns a machine-readable :class:`RefreshOutcome` describing
    whether discovery ran, was skipped (with a taxonomy reason), or failed.

    Precedence of skip reasons is preserved from the historical inline logic:
    ``--skip-platform-detection`` → missing git root → ``--force-old-version``
    → missing platform config → dry-run → discovery.  Skip reasons take
    precedence over ``dry_run`` (which only affects message wording and the
    final discovery branch).
    """
    from agentic_devtools.cli.setup.refresh_outcome import RefreshOutcome

    if args.skip_platform_detection:
        if dry_run:
            print("  ○ would refresh issue types — skipped (--skip-platform-detection)")
        else:
            import logging as _logging  # noqa: PLC0415

            _logging.getLogger(__name__).debug("Issue type refresh suppressed by --skip-platform-detection")
        return RefreshOutcome.skipped("skip_platform_detection")

    if git_root is None:
        if dry_run:
            print("  ○ would refresh issue types — skipped (no git root)")
        else:
            print(
                "  ⚠ Cannot refresh issue types: not inside a git repository.",
                file=sys.stderr,
            )
        return RefreshOutcome.skipped("missing_git_root")

    if skip_repo_steps:
        if dry_run:
            print("  ○ would refresh issue types — skipped (--force-old-version)")
        else:
            print(
                "  ⚠ Cannot refresh issue types: repo file modifications are disabled in --force-old-version mode.",
                file=sys.stderr,
            )
        return RefreshOutcome.skipped("force_old_version")

    if not (git_root / ".github" / "agdt-config.json").exists():
        if dry_run:
            print("  ○ would refresh issue types — skipped (no platform configuration)")
        else:
            print(
                "  ⚠ Cannot refresh issue types: no platform configuration found."
                " Run `agdt-setup` first to configure platform settings.",
                file=sys.stderr,
            )
        return RefreshOutcome.skipped("missing_config")

    if dry_run:
        print("  ○ would refresh issue types")
        return RefreshOutcome.skipped("dry_run")

    from agentic_devtools.cli.setup.issue_type_discovery import (  # noqa: PLC0415
        discover_issue_types,
    )

    try:
        outcome = discover_issue_types(git_root, force_refresh=True, standalone=True)
    except Exception as exc:  # noqa: BLE001 - standalone refresh must never crash setup
        # str(exc) can be empty for bare exceptions like RuntimeError(); fall back to
        # the type name so RefreshOutcome.failed() never raises ValueError itself.
        error_msg = str(exc) or type(exc).__name__
        print(f"  ⚠ Issue type refresh failed ({error_msg})", file=sys.stderr)
        return RefreshOutcome.failed("unexpected_error", error_msg)
    if outcome.status == "failed":
        print(f"  ⚠ Issue type refresh failed ({outcome.error})", file=sys.stderr)
    return outcome


def build_setup_parser() -> argparse.ArgumentParser:
    """Build the ``agdt-setup`` argument parser.

    Factored out of :func:`setup_cmd` so the flag set can be inspected without
    executing the command — running ``agdt-setup`` (even with ``--help``) is
    prohibited inside the agentic-devtools repository:

    .. code-block:: python

        from agentic_devtools.cli.setup.commands import build_setup_parser

        flags = {opt for act in build_setup_parser()._actions for opt in act.option_strings}

    Returns:
        A fully configured :class:`argparse.ArgumentParser` for ``agdt-setup``.
    """
    parser = argparse.ArgumentParser(
        prog="agdt-setup",
        description="Full setup: install managed CLIs and verify all dependencies.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--system-only",
        action="store_true",
        default=False,
        help="Skip managed installs; only verify already-installed dependencies.",
    )
    parser.add_argument(
        "--no-verify-ssl",
        action="store_true",
        default=False,
        help="Disable SSL certificate verification (insecure; use only on trusted networks).",
    )
    parser.add_argument(
        "--no-persist-env",
        action="store_true",
        default=False,
        help="Do not persist environment variables to shell profile.",
    )
    parser.add_argument(
        "--overwrite-env",
        action="store_true",
        default=False,
        help="Overwrite existing environment variable lines in shell profile.",
    )
    parser.add_argument(
        "--skip-platform-detection",
        action="store_true",
        default=False,
        help="Skip automatic platform detection step.",
    )
    parser.add_argument(
        "--issue-adapter",
        choices=sorted(_VALID_ISSUE_ADAPTERS),
        default=None,
        help=(
            "Override the issue-adapter axis for skill filtering. "
            "Code hosting detection still runs independently unless --skip-platform-detection is also supplied."
        ),
    )
    parser.add_argument(
        "--skip-templates",
        action="store_true",
        default=False,
        help="Skip workflow template generation and commit template creation/validation.",
    )
    parser.add_argument(
        "--reconfigure",
        action="store_true",
        default=False,
        help="Re-prompt for all project configuration values and Copilot model selection, even if already set.",
    )
    parser.add_argument(
        "--defaults",
        action="store_true",
        default=False,
        help="Skip interactive prompts and apply safe defaults for Phase 0 configuration.",
    )
    parser.add_argument(
        "--skip-pr-workflow",
        action="store_true",
        default=False,
        help="Skip the automatic branch/PR workflow for repo file changes.",
    )
    parser.add_argument(
        "--force-old-version",
        action="store_true",
        default=False,
        help=(
            "Bypass the version guard when the installed version is older"
            " than the project pin. Repo file modifications are skipped"
            " only in that case; has no effect when the version already"
            " satisfies the pin."
        ),
    )
    npm_group = parser.add_mutually_exclusive_group()
    npm_group.add_argument(
        "--npm",
        action="store_true",
        default=False,
        help="Force npm certificate and configuration work regardless of npm footprint.",
    )
    npm_group.add_argument(
        "--no-npm",
        action="store_true",
        default=False,
        help="Skip npm certificate and configuration work regardless of npm footprint.",
    )
    run_group = parser.add_mutually_exclusive_group()
    run_group.add_argument(
        "--run",
        dest="cli_run",
        action="store_const",
        const=True,
        default=None,
        help=(
            "Resolve autorun_enabled as True, overriding CI/TTY detection"
            " and the AGDT_SETUP_RUN/AGDT_SETUP_NO_AUTORUN environment"
            " variables. Also overrides workflow-state and branch-created"
            " suppressions: when a setup branch was created, the generated"
            " script is executed from a temporary worktree of that branch."
        ),
    )
    run_group.add_argument(
        "--no-run",
        dest="cli_no_run",
        action="store_const",
        const=True,
        default=None,
        help=(
            "Resolve autorun_enabled as False, overriding CI/TTY detection"
            " and the AGDT_SETUP_RUN/AGDT_SETUP_NO_AUTORUN environment"
            " variables."
        ),
    )
    parser.add_argument(
        "--no-refresh-models",
        action="store_true",
        default=False,
        help=(
            "Skip live Copilot model discovery (the ACP handshake) and reuse the"
            " cached model inventory instead. Setup refreshes the inventory by"
            " default."
        ),
    )
    parser.add_argument(
        "--refresh-issue-types",
        action="store_true",
        default=False,
        help="Force re-discovery of issue types from the configured provider without full reconfiguration.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help=(
            "Preview what setup would do without making any changes, including a"
            " manifest diff of the agent/prompt/skill files that would be added,"
            " overwritten and deleted."
        ),
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        default=False,
        help=(
            "Confirm deletion of managed agdt.* skill files under .github/ and"
            " managed skill directories under .agents/skills/ that are no longer"
            " in the source set (and legacy .agdt/ migration entries). Without this"
            " flag a run with pending deletions prints the delete list and exits"
            " non-zero without changing agent/prompt/skill items."
        ),
    )
    return parser


def setup_cmd() -> None:
    """Full setup: install Copilot CLI + GitHub CLI, then verify all dependencies.

    The parser is built by :func:`build_setup_parser` so that the flag set can
    be inspected without executing this command.

    Usage:
        agdt-setup [--system-only] [--no-verify-ssl] [--no-persist-env] [--overwrite-env]
                   [--reconfigure] [--no-refresh-models] [--defaults]
                   [--skip-pr-workflow] [--dry-run] [--yes]

    Options:
        --system-only   Skip managed installs into ~/.agdt/bin/; only verify
                        already-installed dependencies.
        --no-verify-ssl Disable SSL certificate verification (insecure; use
                        only on trusted networks).
        --no-persist-env  Do not persist env vars to shell profile.
        --overwrite-env   Overwrite existing env var lines in shell profile.
        --reconfigure     Re-prompt for all project configuration values
                          and Copilot model selection, even if already set.
        --no-refresh-models  Skip live Copilot model discovery and reuse the
                          cached model inventory.
        --defaults        Skip interactive Phase 0 prompts; apply safe defaults.
        --skip-pr-workflow  Skip the automatic branch/PR workflow for repo file
                            changes; apply changes directly to the current branch.
        --dry-run         Preview what setup would do, including the skill
                          manifest diff, without making any changes.
        --yes             Confirm deletion of managed agdt.* skill files under
                          .github/ and managed skill directories under
                          .agents/skills/ that are no longer in the source set
                          (and legacy .agdt/ migration entries).
    """
    parser = build_setup_parser()
    args = parser.parse_args()

    from .autorun_resolution import resolve_autorun_enabled

    args.autorun_enabled = resolve_autorun_enabled(args.cli_run, args.cli_no_run)

    import time as _time
    from datetime import UTC
    from datetime import datetime as _datetime

    from .exit_codes import ExitCode
    from .phase_markers import GENERATION_END, GENERATION_START, PhaseMarkerEmitter
    from .phases import AUTORUN_SETUP_PHASE, PHASES
    from .report import SCHEMA_VERSION, PhaseResult, SetupReport, write_report

    report = SetupReport(
        schema_version=SCHEMA_VERSION,
        timestamp=_datetime.now(tz=UTC).isoformat(),
        exit_code=ExitCode.AUTORUN_FAILED,
        exit_code_name=ExitCode.AUTORUN_FAILED.name,
        autorun_enabled=args.autorun_enabled,
        mode="dry-run" if args.dry_run else "setup",
    )

    dry_run: bool = args.dry_run

    class _PhaseTracker:
        """Context manager recording per-phase timing and status."""

        def __init__(self, phase_name: str) -> None:
            self.phase_name = phase_name
            self._start: float = 0.0

        def __enter__(self) -> _PhaseTracker:
            self._start = _time.monotonic()
            return self

        def __exit__(self, exc_type: type | None, exc_val: BaseException | None, exc_tb: object) -> None:
            elapsed_ms = int((_time.monotonic() - self._start) * 1000)
            if exc_type is not None:
                report.record(
                    PhaseResult(name=self.phase_name, status="failed", duration_ms=elapsed_ms, error=str(exc_val))
                )
            else:
                report.record(PhaseResult(name=self.phase_name, status="success", duration_ms=elapsed_ms))
            # Return None — do not suppress exceptions

    from .post_autorun_version_check import capture_startup_version

    startup_version = capture_startup_version()

    original_no_verify = os.environ.get("AGDT_NO_VERIFY_SSL")
    _git_root_str: str | None = None
    phase_markers = PhaseMarkerEmitter()
    _specialization_attempted = False
    _specialization_startup_fingerprint: tuple[int, int, int] | None | object = (
        _capture_specialization_startup_fingerprint(dry_run=dry_run)
    )
    try:
        phase_markers.emit(GENERATION_START)

        if args.no_verify_ssl:
            if dry_run:
                print("  ○ would set AGDT_NO_VERIFY_SSL=1")
                print()
            else:
                os.environ["AGDT_NO_VERIFY_SSL"] = "1"
                print("  ⚠  SSL verification disabled. Use only on trusted networks.")
                print()

        # ── Version guard (must run before any local-only or file-modifying steps) ──
        from agentic_devtools.state import _get_git_repo_root

        git_root = _get_git_repo_root()
        _git_root_str = str(git_root) if git_root else None

        from agentic_devtools.cli.setup.version_guard import check_version_guard

        with _PhaseTracker(PHASES[0]):  # version_check
            guard_result = check_version_guard(git_root, args.force_old_version)

        if guard_result.action == "block":
            report.exit_code = ExitCode.VERSION_BLOCKED
            report.exit_code_name = ExitCode.VERSION_BLOCKED.name
            report.details = {"reason": "version_blocked"}
            if args.refresh_issue_types and not args.reconfigure:
                from agentic_devtools.cli.setup.refresh_outcome import RefreshOutcome  # noqa: PLC0415

                report.set_refresh_outcome(RefreshOutcome.skipped("version_blocked"))
                for phase_name in PHASES[1:]:
                    report.record(PhaseResult(name=phase_name, status="skipped"))
            report.git_root = _git_root_str
            write_report(report)
            if not dry_run:
                _cleanup_stale_specialization_artifact(
                    "Setup expectations specialization skipped (version blocked)",
                    startup_fingerprint=_specialization_startup_fingerprint,
                )
            sys.exit(ExitCode.VERSION_BLOCKED)

        if dry_run and guard_result.action == "upgrade":
            print(f"  ○ would upgrade to version {guard_result.target_version}")

        skip_repo_steps = guard_result.action == "force"
        specialization_version_pin = guard_result.pinned_version

        # ── Standalone --refresh-issue-types early return ──────────────
        if args.refresh_issue_types and not args.reconfigure:
            outcome = _perform_standalone_refresh(args, git_root, dry_run, skip_repo_steps)
            report.set_refresh_outcome(outcome)
            for phase_name in PHASES[1:]:
                report.record(PhaseResult(name=phase_name, status="skipped"))
            report.exit_code = ExitCode.OK
            report.exit_code_name = ExitCode.OK.name
            report.git_root = _git_root_str
            write_report(report)
            if not dry_run:
                _cleanup_stale_specialization_artifact(
                    "Setup expectations specialization skipped (standalone refresh)",
                    startup_fingerprint=_specialization_startup_fingerprint,
                )
            sys.exit(ExitCode.OK)

        print(_BANNER)
        print()

        unified_path = None
        npmrc_result = None
        npmrc_written = False
        specialization_ssl_hosts: tuple[str, ...] = ()
        npm_enabled = _resolve_npm_enabled(args, git_root if git_root else Path.cwd())
        persist_env = not args.no_persist_env and not args.system_only
        if dry_run:
            # ── Dry-run: skip all mutator phases, print "would …" messages ──
            copilot_ok = True
            gh_ok = True
            if not args.system_only:
                report.record(PhaseResult(name=PHASES[1], status="skipped", duration_ms=0))
                unified_path, npmrc_result = _prefetch_certs(npm_enabled=npm_enabled, dry_run=True)
                report.record(PhaseResult(name=PHASES[2], status="skipped", duration_ms=0))
                install_copilot_cli(dry_run=True)
                install_gh_cli(dry_run=True)
            else:
                unified_path = None
                npmrc_result = None
                report.record(PhaseResult(name=PHASES[1], status="skipped", duration_ms=0))
                report.record(PhaseResult(name=PHASES[2], status="skipped", duration_ms=0))

            if (unified_path or npmrc_result) and git_root:
                _register_setup_artifacts(
                    git_root,
                    unified_path,
                    npmrc_result,
                    dry_run=True,
                )

            # dependency_check is read-only — still runs under dry-run
            with _PhaseTracker(PHASES[3]):  # dependency_check
                statuses = check_all_dependencies()
                print_dependency_report(statuses)

            report.record(PhaseResult(name=PHASES[4], status="skipped", duration_ms=0))
            _persist_env_vars_to_profile(
                npmrc_path=npmrc_result,
                unified_path=unified_path,
                persist_env=persist_env,
                overwrite_env=args.overwrite_env,
                dry_run=True,
                npm_enabled=npm_enabled,
            )

            # Bypass MISSING_REQUIRED_DEP exit under dry-run (FR-010)
            any_required_missing = any(s.required and not s.found for s in statuses)
            if any_required_missing:
                print("  ℹ Required dependencies missing (would block in non-dry-run mode).")

            # Print "would …" messages for file_modifications phase
            if git_root is None:
                print("  ○ would ensure .agdt/.gitignore — skipped (no git root)")
                print("  ○ would inject agent/prompt/skill files — skipped (no git root)")
                print("  ○ would generate setup scripts — skipped (no git root)")
                print("  ○ would ensure root .gitignore negation rules — skipped (no git root)")
                print("  ○ would ensure .github/copilot/settings.json — skipped (no git root)")
            elif skip_repo_steps:
                print("  ○ would ensure .agdt/.gitignore — skipped (--force-old-version)")
                print("  ○ would inject agent/prompt/skill files — skipped (--force-old-version)")
                if not args.system_only:
                    print("  ○ would prompt project configuration — skipped (--force-old-version)")
                    print("  ○ would configure Copilot model selection — skipped (--force-old-version)")
                    print("  ○ would populate available models inventory — skipped (--force-old-version)")
                    if not args.skip_platform_detection:
                        print("  ○ would detect and save platform configuration — skipped (--force-old-version)")
                    print("  ○ would discover Jira instance metadata — skipped (--force-old-version)")
                    print("  ○ would discover issue types — skipped (--force-old-version)")
                    print("  ○ would configure Phase 0 settings — skipped (--force-old-version)")
                    if not args.skip_templates:
                        print("  ○ would generate workflow templates — skipped (--force-old-version)")
                        print("  ○ would ensure commit template — skipped (--force-old-version)")
                        print("  ○ would ensure PR title/body templates — skipped (--force-old-version)")
                print("  ○ would generate setup scripts — skipped (--force-old-version)")
                print("  ○ would ensure root .gitignore negation rules — skipped (--force-old-version)")
                print("  ○ would ensure .github/copilot/settings.json — skipped (--force-old-version)")
                print("  ○ would pin agdt_version in project.json — skipped (--force-old-version)")
            else:
                print("  ○ would ensure .agdt/.gitignore")
                _preview_skill_injection(git_root)
                if not args.system_only:
                    print("  ○ would prompt project configuration")
                    print("  ○ would configure Copilot model selection")
                    print("  ○ would populate available models inventory")
                    if not args.skip_platform_detection:
                        print("  ○ would detect and save platform configuration")
                    print("  ○ would discover Jira instance metadata")
                    print("  ○ would discover issue types")
                    print("  ○ would configure Phase 0 settings")
                    if not args.skip_templates:
                        print("  ○ would generate workflow templates")
                        print("  ○ would ensure commit template")
                        print("  ○ would ensure PR title/body templates")
                print("  ○ would generate setup scripts")
                print("  ○ would ensure root .gitignore negation rules")
                print("  ○ would ensure .github/copilot/settings.json")
                print("  ○ would pin agdt_version in project.json")
                if not args.system_only and not args.skip_pr_workflow and not skip_repo_steps:
                    print("  ○ would run setup changes via PR workflow")
            report.record(PhaseResult(name=PHASES[5], status="skipped", duration_ms=0))
            report.record(PhaseResult(name=PHASES[6], status="skipped", duration_ms=0))

            # Dry-run complete — write report and exit OK
            print()
            print("Dry-run complete — no changes were made.")
            report.exit_code = ExitCode.OK
            report.exit_code_name = ExitCode.OK.name
            report.git_root = _git_root_str
            write_report(report)
            sys.exit(ExitCode.OK)

        elif args.system_only:
            print("Skipping managed installs (--system-only).")
            print()
            copilot_ok = True
            gh_ok = True
            report.record(PhaseResult(name=PHASES[1], status="skipped"))
            report.record(PhaseResult(name=PHASES[2], status="skipped"))
        else:
            selected_ssl_hosts: list[str] = []
            with _PhaseTracker(PHASES[1]):  # certificate_prefetch
                unified_path, npmrc_result = _prefetch_certs(
                    npm_enabled=npm_enabled,
                    selected_hosts_out=selected_ssl_hosts,
                )
            specialization_ssl_hosts = tuple(selected_ssl_hosts)
            npmrc_written = npmrc_result is not None
            if (unified_path or npmrc_result) and git_root:
                _register_setup_artifacts(
                    git_root,
                    unified_path,
                    npmrc_result,
                )
            print()

            with _PhaseTracker(PHASES[2]):  # cli_installation
                copilot_ok = install_copilot_cli()
                print()
                gh_ok = install_gh_cli()

        with _PhaseTracker(PHASES[3]):  # dependency_check
            statuses = check_all_dependencies()
            print_dependency_report(statuses)

        with _PhaseTracker(PHASES[4]):  # environment_persistence
            _persist_env_vars_to_profile(
                npmrc_path=npmrc_result if npmrc_written else None,
                unified_path=unified_path,
                persist_env=persist_env,
                overwrite_env=args.overwrite_env,
                npm_enabled=npm_enabled,
            )

        any_required_missing = any(s.required and not s.found for s in statuses)
        if any_required_missing:
            print("Setup failed: required dependencies are missing. See above for details.")
            report.record(PhaseResult(name=PHASES[5], status="skipped"))
            report.exit_code = ExitCode.MISSING_REQUIRED_DEP
            report.exit_code_name = ExitCode.MISSING_REQUIRED_DEP.name
            report.details = {"warnings": False}
            report.git_root = _git_root_str
            write_report(report)
            _cleanup_stale_specialization_artifact(
                "Setup expectations specialization skipped (required dependencies are missing)",
                startup_fingerprint=_specialization_startup_fingerprint,
            )
            sys.exit(ExitCode.MISSING_REQUIRED_DEP)

        # Ensure .agdt/.gitignore exists in the current repo (if any)
        from agentic_devtools.agdt_gitignore import ensure_agdt_gitignore

        # Captures this run's resolved platform configuration (issue adapter,
        # code hosting, and the ``issue_adapter_resolved`` marker) so that
        # specialization can use it directly instead of rereading
        # ``.github/agdt-config.json`` afterwards.  A post-hoc reread is
        # unreliable when the PR workflow restores the user's original
        # branch before specialization runs (see run_setup_with_pr_workflow),
        # since the newly persisted config then only exists on the setup
        # branch's worktree, not the restored one.
        resolved_platform_config: dict[str, Any] | None = None

        # ── File-modifying steps (may be wrapped by the PR workflow) ───
        def _run_file_modifying_steps(git_root: Path) -> None:
            nonlocal resolved_platform_config, specialization_version_pin
            # Track whether any repo-mutating step succeeded so we only pin
            # agdt_version when at least one file modification was applied.
            repo_mutations_succeeded = False

            if ensure_agdt_gitignore(git_root):
                print("  ✓ Ensured .agdt/.gitignore exists")
                repo_mutations_succeeded = True
            else:
                print(
                    "  ⚠ Failed to create/update .agdt/.gitignore — check repository state or directory permissions",
                    file=sys.stderr,
                )

            # ── Project configuration prompts ───────────────────────────────
            if not args.system_only:
                refresh_models = not args.no_refresh_models
                _prompt_project_config(force_prompt=args.reconfigure)
                # Discovery runs first so that the model prompt can reuse the
                # freshly written cache instead of spawning a second handshake.
                _populate_available_models(refresh_models=refresh_models)
                # The prompt never re-runs discovery: it reads the cache that
                # _populate_available_models just refreshed (or deliberately left alone).
                _prompt_copilot_model(force_prompt=args.reconfigure, refresh_models=False)
            # ────────────────────────────────────────────────────────────────

            # ── Platform & Workflow Setup (before injection) ──────────
            # Platform resolution runs BEFORE skill injection so that the
            # resolved axes can be forwarded to inject_skills_with_summary.
            platform_config: dict[str, Any] = {}
            platform_config_saved = False
            detection_failed = False
            # Injection axes are tracked separately from platform_config so that
            # DEFAULT_ISSUE_ADAPTER / DEFAULT_CODE_HOSTING fallbacks written into
            # platform_config (for persistence) are never mistaken for a genuine
            # detection or CLI override.  Only positive detection results and
            # explicit --issue-adapter values should activate a filter axis.
            raw_inj_issue_adapter: str | None = None
            raw_inj_code_hosting: str | None = None
            issue_adapter_resolved = False
            configured_issue_adapter_value: str | None = None
            configured_issue_adapter_authoritative = False
            configured_code_hosting_value: str | None = None
            try:
                is_interactive = sys.stdin.isatty()
            except (OSError, AttributeError):
                is_interactive = False
            if not args.system_only:
                print()
                print("─── Platform & Workflow Setup ────────────────────────────────")

                # Step 1: Platform detection + adapter configuration
                try:
                    if args.issue_adapter is not None:
                        from agentic_devtools.cli.setup.platform_detection import (  # noqa: PLC0415
                            detect_platforms,
                        )
                        from agentic_devtools.config import (  # noqa: PLC0415
                            DEFAULT_CODE_HOSTING,
                            load_platform_config,
                            save_platform_config,
                        )
                        from agentic_devtools.skill_classification import (  # noqa: PLC0415
                            resolve_platform_context,
                        )

                        # Load existing config to preserve fields like github.repo
                        # or azure_devops.project; only override issue_adapter.
                        platform_config = load_platform_config(str(git_root))
                        _cfg_issue_adapter, _cfg_code_hosting = resolve_platform_context(platform_config)
                        configured_code_hosting_value = _cfg_code_hosting
                        platform_config["issue_adapter"] = args.issue_adapter
                        platform_config[_ISSUE_ADAPTER_RESOLVED_KEY] = True
                        # Explicit CLI override → the issue-adapter axis is genuinely resolved.
                        raw_inj_issue_adapter = args.issue_adapter
                        issue_adapter_resolved = True

                        # FR-002: code hosting detection still runs independently
                        # even when --issue-adapter is given.
                        if not args.skip_platform_detection:
                            try:
                                det_result = detect_platforms(str(git_root))
                                det_hosting = det_result.detected_code_hosting
                                if det_hosting is None:
                                    # Detection found no host — persist catch-all and
                                    # leave injection unrestricted (FR-003).  A stale
                                    # configured value must not filter when the current
                                    # detection cannot confirm it.
                                    platform_config["code_hosting"] = DEFAULT_CODE_HOSTING
                                    raw_inj_code_hosting = None
                                else:
                                    # Detection succeeded; always use the fresh detected
                                    # hosting to avoid stale persisted values filtering
                                    # injection after hosting migration.
                                    platform_config["code_hosting"] = det_hosting
                                    raw_inj_code_hosting = det_hosting
                            except Exception:  # noqa: BLE001
                                detection_failed = True  # triggers inject-all fallback (FR-003)

                        if save_platform_config(str(git_root), platform_config):
                            print(f"  ✓ Issue adapter configured: {args.issue_adapter}")
                            repo_mutations_succeeded = True
                            platform_config_saved = True
                        else:
                            detection_failed = True  # failed persistence -> inject-all fallback (FR-003)
                            print(
                                "  ⚠ Failed to save platform configuration — check directory permissions",
                                file=sys.stderr,
                            )
                    elif not args.skip_platform_detection:
                        from agentic_devtools.cli.setup.platform_detection import (  # noqa: PLC0415
                            confirm_and_override,
                            detect_platforms,
                        )
                        from agentic_devtools.config import (  # noqa: PLC0415
                            DEFAULT_CODE_HOSTING,
                            DEFAULT_ISSUE_ADAPTER,
                            VALID_CODE_HOSTING,
                            VALID_ISSUE_ADAPTERS,
                            load_repo_config,
                            save_platform_config,
                        )
                        from agentic_devtools.skill_classification import (  # noqa: PLC0415
                            resolve_platform_context,
                        )

                        # FR-002 / FR-004 priority inputs: existing configured values
                        # (excluding default fallback semantics) are authoritative
                        # before detection for injection-axis resolution.
                        try:
                            repo_cfg = load_repo_config(str(git_root))
                            raw_platform = repo_cfg.get("platform")
                            if isinstance(raw_platform, dict):
                                _cfg_issue_adapter, _cfg_code_hosting = resolve_platform_context(raw_platform)
                                configured_code_hosting_value = _cfg_code_hosting
                                _raw_issue_adapter = raw_platform.get("issue_adapter")
                                if isinstance(_raw_issue_adapter, str) and _raw_issue_adapter in VALID_ISSUE_ADAPTERS:
                                    configured_issue_adapter_value = _raw_issue_adapter
                                resolved_marker = raw_platform.get(_ISSUE_ADAPTER_RESOLVED_KEY)
                                if isinstance(resolved_marker, bool):
                                    configured_issue_adapter_authoritative = (
                                        resolved_marker and configured_issue_adapter_value is not None
                                    )
                                elif _ISSUE_ADAPTER_RESOLVED_KEY in raw_platform:
                                    # Marker present but malformed (e.g. null or "false").
                                    # A non-boolean value is not a valid "resolved" signal,
                                    # so treat the adapter as unresolved / non-authoritative
                                    # rather than falling through to the legacy path.
                                    configured_issue_adapter_authoritative = False
                                else:
                                    # Legacy config with the marker absent: only non-default
                                    # adapters are independently authoritative. Markerless
                                    # DEFAULT_ISSUE_ADAPTER ("jira") is ambiguous because
                                    # older setup runs persisted it as a generated fallback.
                                    configured_issue_adapter_authoritative = (
                                        configured_issue_adapter_value is not None
                                        and configured_issue_adapter_value != DEFAULT_ISSUE_ADAPTER
                                    )
                        except Exception:  # noqa: BLE001
                            configured_issue_adapter_value = None
                            configured_issue_adapter_authoritative = False
                            configured_code_hosting_value = None

                        result = detect_platforms(str(git_root))
                        # Extract raw injection axes from the detection result (no
                        # default fallbacks).  These track only what was actually
                        # found; DEFAULT_ISSUE_ADAPTER / DEFAULT_CODE_HOSTING go into
                        # platform_config for persistence but must NOT drive injection
                        # filtering, because they cannot be distinguished from a
                        # genuine detection by _resolve_injection_axes.
                        if configured_issue_adapter_authoritative:
                            issue_adapter_resolved = True
                            raw_inj_issue_adapter, _ = resolve_platform_context(
                                {"issue_adapter": configured_issue_adapter_value}
                            )
                        else:
                            raw_inj_issue_adapter = None
                            for _platform in result.detected_issue_platforms:
                                if _platform in VALID_ISSUE_ADAPTERS:
                                    raw_inj_issue_adapter = _platform
                                    issue_adapter_resolved = True
                                    break

                        if result.detected_code_hosting is not None:
                            raw_inj_code_hosting = result.detected_code_hosting
                        else:
                            raw_inj_code_hosting = configured_code_hosting_value
                        if is_interactive:
                            selection_state: dict[str, bool] = {}
                            platform_config = confirm_and_override(
                                result,
                                selection_state=selection_state,
                            )
                            # Update each injection axis independently based on whether
                            # the user explicitly overrode that axis. Comparing against
                            # the detection-derived default (with fallback) ensures that
                            # an override on one axis never promotes the other axis's
                            # persisted default into a genuine resolution.
                            if selection_state.get("issue_adapter_explicit"):
                                raw_inj_issue_adapter = platform_config.get("issue_adapter")
                                issue_adapter_resolved = True
                            if selection_state.get("code_hosting_explicit"):
                                raw_inj_code_hosting = platform_config.get("code_hosting")
                            elif configured_code_hosting_value is not None and result.detected_code_hosting is None:
                                # Keep configured hosting only when detection could
                                # not determine a host in this run.
                                platform_config["code_hosting"] = configured_code_hosting_value

                            if (
                                not selection_state.get("issue_adapter_explicit")
                                and configured_issue_adapter_authoritative
                                and configured_issue_adapter_value is not None
                            ):
                                platform_config["issue_adapter"] = configured_issue_adapter_value
                                issue_adapter_resolved = True
                            # Otherwise no interactive override occurred and the
                            # detection-derived raw axes set above remain in effect.
                        else:
                            # No TTY — skip interactive confirmation, use detection
                            # result directly for config persistence (FR-003/FR-006).
                            # Load the raw platform section from the existing persisted
                            # config so we only update the detected axes
                            # (issue_adapter, code_hosting, and provider-detail
                            # sub-dicts); this preserves existing values such as
                            # phase_0, Jira settings, and forward-compatible unknown
                            # keys that detection does not recreate.
                            # We use load_repo_config (not load_platform_config) so
                            # that phase_0 is only present if it was already in the
                            # file; load_platform_config always injects phase_0
                            # defaults, which would trigger an unnecessary
                            # _prompt_phase_0_config idempotent mirror on the next run.
                            try:
                                import copy as _copy  # noqa: PLC0415

                                from agentic_devtools.config import load_repo_config  # noqa: PLC0415

                                raw_cfg = load_repo_config(str(git_root))
                                raw_platform = raw_cfg.get("platform")
                                platform_config = _copy.deepcopy(raw_platform) if isinstance(raw_platform, dict) else {}
                            except Exception:  # noqa: BLE001
                                platform_config = {}
                            # Select only a valid adapter and a valid catch-all hosting
                            # value so that load_platform_config does not silently
                            # coerce them (mirrors _build_config_from_result).
                            # When detection finds nothing, preserve the existing
                            # configured axis so a temporarily-unavailable remote
                            # does not erase an authoritative persisted setting.
                            if configured_issue_adapter_authoritative and configured_issue_adapter_value is not None:
                                # Preserve an authoritative configured adapter (e.g. a
                                # legacy explicit "jira" config) instead of letting
                                # detection silently rewrite it in an unattended run.
                                # detect_platforms() omits Jira on a GitHub-hosted repo,
                                # so without this guard an unattended setup would overwrite
                                # the adapter with GitHub, contradicting FR-002. This mirrors
                                # the interactive and --system-only paths.
                                platform_config["issue_adapter"] = configured_issue_adapter_value
                                issue_adapter_resolved = True
                            else:
                                _detected_adapter: str | None = None
                                for _platform in result.detected_issue_platforms:
                                    if _platform in VALID_ISSUE_ADAPTERS:
                                        _detected_adapter = _platform
                                        break
                                if _detected_adapter is not None:
                                    platform_config["issue_adapter"] = _detected_adapter
                                    issue_adapter_resolved = True
                                else:
                                    # Detection found no issue platform; preserve a valid
                                    # configured adapter and its resolved marker.
                                    _existing_adapter = platform_config.get("issue_adapter")
                                    if isinstance(_existing_adapter, str) and _existing_adapter in VALID_ISSUE_ADAPTERS:
                                        platform_config["issue_adapter"] = _existing_adapter
                                        _existing_resolved_marker = platform_config.get(_ISSUE_ADAPTER_RESOLVED_KEY)
                                        issue_adapter_resolved = (
                                            _existing_resolved_marker
                                            if isinstance(_existing_resolved_marker, bool)
                                            else False
                                        )
                                    else:
                                        platform_config["issue_adapter"] = DEFAULT_ISSUE_ADAPTER
                                        issue_adapter_resolved = False
                            _det_hosting = result.detected_code_hosting
                            if _det_hosting is not None:
                                platform_config["code_hosting"] = _det_hosting
                            else:
                                # Detection found no host; preserve the configured
                                # hosting axis if it is a recognized valid value.
                                _existing_hosting = platform_config.get("code_hosting")
                                if (
                                    not isinstance(_existing_hosting, str)
                                    or _existing_hosting not in VALID_CODE_HOSTING
                                ):
                                    platform_config["code_hosting"] = DEFAULT_CODE_HOSTING
                            # Normalize provider sub-sections: ensure they are dicts
                            # (a config such as "github": null is valid JSON but would
                            # cause setdefault to fail with AttributeError).
                            if not isinstance(platform_config.get("jira"), dict):
                                platform_config["jira"] = {}
                            if not isinstance(platform_config.get("github"), dict):
                                platform_config["github"] = {}
                            if not isinstance(platform_config.get("azure_devops"), dict):
                                platform_config["azure_devops"] = {}
                            if result.github_repo:
                                platform_config["github"]["repo"] = result.github_repo
                            if result.azure_devops_project:
                                platform_config["azure_devops"]["project"] = result.azure_devops_project
                        platform_config[_ISSUE_ADAPTER_RESOLVED_KEY] = issue_adapter_resolved
                        if save_platform_config(str(git_root), platform_config):
                            print("  ✓ Platform configuration saved")
                            repo_mutations_succeeded = True
                            platform_config_saved = True
                        else:
                            detection_failed = True  # failed persistence -> inject-all fallback (FR-003)
                            print(
                                "  ⚠ Failed to save platform configuration — check directory permissions",
                                file=sys.stderr,
                            )
                except Exception as exc:  # noqa: BLE001
                    detection_failed = True
                    print(f"  ⚠ Platform setup failed ({exc}) — skipping", file=sys.stderr)
            else:
                # --system-only: skip detection/save but use only the raw persisted
                # platform section for injection-axis resolution. This avoids
                # synthesised defaults from load_platform_config() (e.g., "jira").
                # Each axis is updated independently: only activate an axis if the
                # stored value is not a DEFAULT fallback, since defaults are written
                # even when no platform was detected and cannot be distinguished from
                # a genuine detection — resolving both axes jointly would promote the
                # DEFAULT_ISSUE_ADAPTER fallback into a spurious restriction.
                try:
                    raw_inj_issue_adapter, raw_inj_code_hosting = _resolve_saved_injection_axes(git_root)
                except Exception:  # noqa: BLE001
                    pass  # no persisted config — inject-all fallback is acceptable

            # ── Skill injection (after platform resolution) ────────────
            # Inject bundled agent/prompt/skill files where supported. Skill injection is a
            # best-effort optional feature: guard the import so that agdt-setup still
            # works even if the module is missing or uses syntax/features not supported
            # by the current interpreter.
            inject_skills_with_summary = None  # type: ignore[assignment]
            try:
                from agentic_devtools.skill_injector import (  # noqa: PLC0415
                    inject_skills_with_summary as _inject_with_summary,
                )

                inject_skills_with_summary = _inject_with_summary
            except (SyntaxError, ImportError) as exc:
                print(
                    f"  ⚠ Failed to import skill injector ({exc!r}) — skipping agent/prompt/skill file injection",
                    file=sys.stderr,
                )

            if inject_skills_with_summary is not None:
                # Resolve filter-capable platform axes from explicitly-tracked raw
                # detection results / CLI override values.  Returns (None, None) on
                # skip/exception/no-TTY per FR-003 — meaning inject-all fallback.
                inj_issue_adapter, inj_code_hosting = _resolve_injection_axes(
                    raw_inj_issue_adapter,
                    raw_inj_code_hosting,
                    skip_platform_detection=args.skip_platform_detection,
                    detection_failed=detection_failed,
                    is_interactive=is_interactive,
                )

                # FR-004: warn when hosting is unresolved but filtering IS active
                if inj_issue_adapter is not None and inj_code_hosting is None:
                    print(
                        "  ⚠ Code hosting could not be detected — hosting axis unrestricted for skill filtering",
                        file=sys.stderr,
                    )

                inj_success, inj_summary = inject_skills_with_summary(
                    git_root,
                    issue_adapter=inj_issue_adapter,
                    code_hosting=inj_code_hosting,
                    assume_yes=args.yes,
                )
                if inj_success:
                    print(_format_injection_summary(inj_summary, inj_issue_adapter, inj_code_hosting))
                    repo_mutations_succeeded = True
                elif getattr(inj_summary, "deletions_blocked", False):
                    # Pending deletions without --yes: the injector printed the
                    # delete list and changed nothing. Stop rather than continue
                    # with a partially-applied setup.
                    raise RuntimeError(
                        "Skill injection would delete managed skill entries —"
                        " re-run `agdt-setup --dry-run` to review the manifest diff,"
                        " then `agdt-setup --yes` to approve the deletions."
                    )
                else:
                    print(
                        "  ⚠ Failed to inject agent/prompt/skill files — this may be due to"
                        " directory permissions or missing/corrupted bundled skills",
                        file=sys.stderr,
                    )

            # ── Remaining Platform & Workflow Setup steps ──────────────
            if not args.system_only:
                jira_preflight_connectivity: tuple[bool, str | None] | None = None
                jira_preflight_warning_emitted = False
                # Step 1.5: Jira instance discovery (non-fatal, cache-aware)
                try:
                    from agentic_devtools.cli.jira.discovery import (  # noqa: PLC0415
                        get_instance_metadata,
                        load_cached_instance_metadata,
                    )

                    if platform_config.get("issue_adapter") == "jira":
                        _force = args.reconfigure or getattr(args, "refresh_issue_types", False)
                        _from_cache = not _force and load_cached_instance_metadata() is not None
                        _meta = None
                        if _force or not _from_cache:
                            from agentic_devtools.cli.setup.provider_connectivity import (  # noqa: PLC0415
                                check_provider_connectivity,
                            )

                            _connected, _connectivity_error = check_provider_connectivity("jira", git_root, timeout=5.0)
                            jira_preflight_connectivity = (_connected, _connectivity_error)
                            if not _connected:
                                _error_message = _connectivity_error or "Provider unreachable"
                                print(
                                    f"  ⚠ Jira discovery skipped: jira is unreachable ({_error_message})",
                                    file=sys.stderr,
                                )
                                jira_preflight_warning_emitted = True
                            else:
                                from agentic_devtools.adapters import resolve_jira_config  # noqa: PLC0415

                                _jira_config = resolve_jira_config(git_root)
                                _meta = get_instance_metadata(force_refresh=_force, config=_jira_config)
                        else:
                            _meta = get_instance_metadata(force_refresh=_force)
                        if _meta:
                            _suffix = " (cached)" if _from_cache else ""
                            print(
                                f"  ✅ Jira v{_meta['version']}"
                                f" ({_meta['deploymentType']}) — {_meta['baseUrl']}{_suffix}"
                            )
                except Exception as exc:  # noqa: BLE001
                    print(f"  ⚠ Jira discovery skipped ({exc})", file=sys.stderr)

                # Step 1.6: Issue type discovery (non-fatal, cache-aware)
                if platform_config_saved:
                    try:
                        from agentic_devtools.cli.setup.issue_type_discovery import (  # noqa: PLC0415
                            discover_issue_types,
                        )

                        _force_types = args.reconfigure or args.refresh_issue_types
                        discover_issue_types(
                            git_root,
                            force_refresh=_force_types,
                            skip_platform_detection=args.skip_platform_detection,
                            preflight_connectivity=jira_preflight_connectivity,
                            preflight_warning_emitted=jira_preflight_warning_emitted,
                        )
                    except Exception as exc:  # noqa: BLE001
                        print(f"  ⚠ Issue type discovery skipped ({exc})", file=sys.stderr)

                # Step 1b: Phase 0 configuration prompts
                try:
                    from agentic_devtools.cli.setup.phase_0 import (  # noqa: PLC0415
                        _prompt_phase_0_config,
                    )

                    use_defaults = getattr(args, "defaults", False)
                    force_prompt = args.reconfigure
                    if use_defaults and force_prompt:
                        print(
                            "  ⚠ --reconfigure is ignored when --defaults is set. "
                            "Use --reconfigure alone to re-prompt interactively, "
                            "or --defaults alone to skip prompts.",
                            file=sys.stderr,
                        )
                        force_prompt = False
                    _prompt_phase_0_config(force_prompt=force_prompt, use_defaults=use_defaults)
                except Exception as exc:  # noqa: BLE001
                    print(f"  ⚠ Phase 0 configuration skipped ({exc})", file=sys.stderr)

                # Step 2: Template generation
                try:
                    if not args.skip_templates:
                        from agentic_devtools.cli.setup.workflow_templates import (  # noqa: PLC0415
                            generate_default_templates,
                        )

                        generated = generate_default_templates(git_root / ".agdt" / "workflow-definitions")
                        if generated:
                            for path in generated:
                                print(f"  ✓ Generated template: {path}")
                            repo_mutations_succeeded = True
                        else:
                            print(
                                "  ℹ Workflow templates already exist (use --skip-templates to suppress this message)"
                            )
                except Exception as exc:  # noqa: BLE001
                    print(f"  ⚠ Template generation failed ({exc}) — skipping", file=sys.stderr)

                # Step 3: Commit message template
                try:
                    if not args.skip_templates:
                        from agentic_devtools.cli.setup.commit_template_setup import (  # noqa: PLC0415
                            ensure_commit_template,
                            validate_commit_template,
                        )

                        created = ensure_commit_template(git_root)
                        if created:
                            print("  ✓ Created default commit template: .agdt/config/commit-template.j2")
                            repo_mutations_succeeded = True
                        else:
                            print("  ℹ Commit template already exists")

                        warnings_list = validate_commit_template(git_root)
                        for warning in warnings_list:
                            print(f"  ⚠ {warning}", file=sys.stderr)
                except Exception as exc:  # noqa: BLE001
                    print(f"  ⚠ Commit template setup failed ({exc}) — skipping", file=sys.stderr)

                # Step 4: PR templates (title + body)
                try:
                    if not args.skip_templates:  # pragma: no cover — tested via unit tests on ensure_pr_*
                        from agentic_devtools.cli.pr_template import (  # noqa: PLC0415
                            ensure_pr_body_template,
                            ensure_pr_title_template,
                        )

                        created_title = ensure_pr_title_template(git_root)
                        if created_title:
                            print("  ✓ Created default PR title template: .agdt/config/pr-title-template.j2")
                            repo_mutations_succeeded = True
                        else:
                            print("  ℹ PR title template already exists")

                        mutated_body = ensure_pr_body_template(git_root)
                        if mutated_body:
                            print("  ✓ Ensured PR body template is present: .agdt/config/pull-request-template.j2")
                            repo_mutations_succeeded = True
                        else:
                            print("  ℹ PR body template already exists (no changes needed)")
                except Exception as exc:  # noqa: BLE001  # pragma: no cover
                    print(f"  ⚠ PR template setup failed ({exc}) — skipping", file=sys.stderr)

            # ── Script Generation Phase ────────────────────────────────
            print()
            print("─── Setup Script Generation ─────────────────────────────────")
            try:
                _generate_setup_scripts(git_root)
                repo_mutations_succeeded = True
            except Exception as exc:  # noqa: BLE001
                print(f"  ⚠ Script generation failed ({exc}) — skipping", file=sys.stderr)

            # ── Root gitignore negation rules for project.json tracking ──
            # Must run AFTER _generate_setup_scripts() because update_gitignore()
            # (called by _generate_setup_scripts) may add the .agdt/* ignore rule
            # on first-time setups.  The negation rules need that anchor to exist.
            from agentic_devtools.cli.setup.gitignore_negations import ensure_root_gitignore_negations

            if ensure_root_gitignore_negations(git_root):
                print("  ✓ Added .gitignore negation rules for .agdt/config/project.json")
                repo_mutations_succeeded = True

            # ── Copilot Settings (.github/copilot/settings.json) ───────

            if ensure_copilot_settings(git_root):
                print("  ✓ Merged repository plugin settings into .github/copilot/settings.json")
                repo_mutations_succeeded = True

            # ── Pin agdt_version in project.json (LAST step) ───────────
            # Only write the version pin when at least one repo-mutating step
            # above succeeded.  This avoids bumping the pin when earlier steps
            # failed, which could block teammates on older versions.
            if repo_mutations_succeeded:
                try:
                    from agentic_devtools import __version__ as _current_version
                    from agentic_devtools.cli.config.project_config import (
                        load_project_config as _load_cfg,
                    )
                    from agentic_devtools.cli.config.project_config import (
                        save_project_config as _save_cfg,
                    )

                    cfg = _load_cfg(git_root=git_root)
                    cfg["agdt_version"] = _current_version
                    _save_cfg(cfg, git_root=git_root)
                    specialization_version_pin = _current_version
                    print(f"  ✓ Pinned agdt_version={_current_version} in .agdt/config/project.json")
                except Exception as exc:  # noqa: BLE001
                    print(f"  ⚠ Failed to pin agdt_version ({exc}) — skipping", file=sys.stderr)

            # Capture this run's resolved platform config for specialization
            # (see the ``resolved_platform_config`` comment above).
            resolved_platform_config = dict(platform_config)
            if git_root is not None and (args.system_only or args.skip_platform_detection):
                # In --system-only mode, platform_config is empty because
                # platform detection/save is skipped. In
                # --skip-platform-detection mode, platform_config also stays
                # empty unless the user supplied an explicit --issue-adapter.
                # Load the raw persisted platform section directly so that
                # specialization can still capture authoritative persisted
                # adapters (including non-filter-capable values like
                # "markdown") without changing the inject-all behavior of
                # _resolve_injection_axes() for skip-platform-detection runs.
                try:
                    from agentic_devtools.config import load_repo_config  # noqa: PLC0415

                    _raw_platform = load_repo_config(str(git_root)).get("platform")
                    if isinstance(_raw_platform, dict):
                        resolved_platform_config = dict(_raw_platform)
                        resolved_platform_config.update(platform_config)
                except Exception as exc:  # noqa: BLE001
                    print(
                        f"  ⚠ Failed to load raw platform section for specialization ({exc}) — using defaults",
                        file=sys.stderr,
                    )
            if args.system_only and raw_inj_issue_adapter:
                # Filter-capable resolved value takes precedence when present.
                resolved_platform_config["issue_adapter"] = raw_inj_issue_adapter
                resolved_platform_config[_ISSUE_ADAPTER_RESOLVED_KEY] = True

        # ── Run file-modifying steps (with or without PR workflow) ─────
        file_mod_phase_start = _time.monotonic()
        try:
            use_pr_workflow = (
                not args.system_only and git_root is not None and not args.skip_pr_workflow and not skip_repo_steps
            )
            branch_created: str | None = None
            if use_pr_workflow:
                from agentic_devtools import __version__ as _version
                from agentic_devtools.cli.setup.pr_workflow import run_setup_with_pr_workflow

                repo_root = cast(Path, git_root)
                pr_result = run_setup_with_pr_workflow(lambda: _run_file_modifying_steps(repo_root), _version)
                branch_created = pr_result.get("branch_created") if pr_result else None
                if pr_result["branch_created"]:
                    print(f"  ✓ Setup changes committed to branch '{pr_result['branch_created']}'")
                if pr_result["pr_created"]:
                    print("  ✓ Pull request created for setup changes")
                elif pr_result["branch_created"]:
                    print(f"  ⚠ {pr_result['message']}")
                else:
                    print(f"  ℹ {pr_result['message']}")
            else:
                if not skip_repo_steps:
                    if git_root is not None:
                        _run_file_modifying_steps(git_root)
                    else:
                        print()
                        print("─── Setup Script Generation ─────────────────────────────────")
                        print("  ℹ Not inside a git repository — skipping script generation")
            file_mod_elapsed = int((_time.monotonic() - file_mod_phase_start) * 1000)
            file_mod_status = "skipped" if skip_repo_steps or git_root is None else "success"
            report.record(PhaseResult(name=PHASES[5], status=file_mod_status, duration_ms=file_mod_elapsed))
        except Exception as file_mod_exc:  # noqa: BLE001
            # Ensure the file_modifications phase is always present in the report,
            # even when an unexpected exception fires mid-phase.
            file_mod_elapsed = int((_time.monotonic() - file_mod_phase_start) * 1000)
            report.record(
                PhaseResult(
                    name=PHASES[5],
                    status="failed",
                    duration_ms=file_mod_elapsed,
                    error=str(file_mod_exc),
                )
            )
            report.exit_code = ExitCode.REPO_MUTATION_FAILED
            report.exit_code_name = ExitCode.REPO_MUTATION_FAILED.name
            report.details = {"error_type": type(file_mod_exc).__name__}
            report.git_root = _git_root_str
            write_report(report)
            print(f"  ❌ Repository mutation failed: {file_mod_exc}", file=sys.stderr)
            _cleanup_stale_specialization_artifact(
                "Setup expectations specialization skipped (repository mutation failed)",
                startup_fingerprint=_specialization_startup_fingerprint,
            )
            sys.exit(ExitCode.REPO_MUTATION_FAILED)

        _specialization_attempted = True
        _specialize_setup_expectations(
            git_root,
            args,
            npm_enabled=npm_enabled,
            skip_repo_steps=skip_repo_steps,
            resolved_platform=resolved_platform_config,
            version_pin=specialization_version_pin,
            ssl_hosts=specialization_ssl_hosts,
            startup_fingerprint=_specialization_startup_fingerprint,
        )

        # --- Phase 7: Autorun setup-dev-tools.py ---
        from .autorun import _autorun_setup_dev_tools

        phase_markers.emit(GENERATION_END)

        _child_invoked = _autorun_setup_dev_tools(
            autorun_enabled=args.autorun_enabled,
            git_root=git_root,
            system_only=args.system_only,
            skip_repo_steps=skip_repo_steps,
            report=report,
            branch_created=branch_created,
            explicit_run=args.cli_run is True,
        )

        # --- Post-autorun version comparison ---
        # Only compare versions when the child was actually invoked; a
        # pre-invocation failure (e.g. worktree creation error) records
        # ``failed`` in the phase but never ran a child that could have
        # upgraded the package, so a version difference should not override
        # the actual failure with UPGRADED_RERUN_NEEDED (exit 4).
        from .post_autorun_version_check import check_post_autorun_version

        _autorun_phase: PhaseResult | None = None
        for _phase in report.phases:
            if _phase.name == AUTORUN_SETUP_PHASE and _phase.status in ("success", "failed"):
                _autorun_phase = _phase
                break

        if _child_invoked:
            _post_version = check_post_autorun_version(startup_version)
            if _post_version is not None and _post_version != startup_version:
                print(
                    f"  ℹ Package version changed from {startup_version} to {_post_version}."
                    f" Please re-run `agdt-setup` to pick up version {_post_version}.",
                    file=sys.stderr,
                )
                report.exit_code = ExitCode.UPGRADED_RERUN_NEEDED
                report.exit_code_name = ExitCode.UPGRADED_RERUN_NEEDED.name
                report.git_root = _git_root_str
                write_report(report)
                sys.exit(ExitCode.UPGRADED_RERUN_NEEDED)

        # --- Auto-run failure propagation ─────────────────────────────
        if _autorun_phase is not None and _autorun_phase.status == "failed":
            from .report import _resolve_report_path

            report.exit_code = ExitCode.AUTORUN_FAILED
            report.exit_code_name = ExitCode.AUTORUN_FAILED.name
            report.details = {"autorun_error": _autorun_phase.error}
            report.git_root = _git_root_str
            write_report(report)
            print(
                f"  ❌ Auto-run of setup-dev-tools.py failed: {_autorun_phase.error or 'see the setup report'}."
                f" Setup report: {_resolve_report_path(None)}",
                file=sys.stderr,
            )
            sys.exit(ExitCode.AUTORUN_FAILED)

        print()
        if not copilot_ok or not gh_ok:
            print("Setup complete with warnings. See above for details.")
            report.exit_code = ExitCode.WARNINGS
            report.exit_code_name = ExitCode.WARNINGS.name
            report.details = {"warnings": True}
            report.git_root = _git_root_str
            write_report(report)
            sys.exit(ExitCode.WARNINGS)
        else:
            print("Setup complete! ✅")
            report.exit_code = ExitCode.OK
            report.exit_code_name = ExitCode.OK.name
            report.git_root = _git_root_str
            write_report(report)
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001
        report.exit_code = ExitCode.AUTORUN_FAILED
        report.exit_code_name = ExitCode.AUTORUN_FAILED.name
        report.details = {"error_type": type(exc).__name__}
        report.git_root = _git_root_str
        write_report(report)
        print(f"  ❌ Internal error: {exc}", file=sys.stderr)
        if not dry_run and not _specialization_attempted:
            _cleanup_stale_specialization_artifact(
                "Setup expectations specialization skipped (internal error before specialization)",
                startup_fingerprint=_specialization_startup_fingerprint,
            )
        sys.exit(ExitCode.AUTORUN_FAILED)
    finally:
        # Close the generation phase for early-exit paths that never reached the
        # auto-run step; PhaseMarkerEmitter makes the emission idempotent.
        phase_markers.emit(GENERATION_END)
        # Restore the original AGDT_NO_VERIFY_SSL state so that the env var does
        # not leak into the calling process when agdt-setup is invoked from within
        # a larger script or automation pipeline.
        if original_no_verify is None:
            os.environ.pop("AGDT_NO_VERIFY_SSL", None)
        else:
            os.environ["AGDT_NO_VERIFY_SSL"] = original_no_verify


def setup_copilot_cli_cmd() -> None:
    """Install the GitHub Copilot CLI standalone binary into ``~/.agdt/bin/``.

    Usage:
        agdt-setup-copilot-cli [--system-only] [--no-verify-ssl] [--no-persist-env]
                               [--overwrite-env] [--dry-run]

    Options:
        --system-only   Skip the managed install.
        --no-verify-ssl Disable SSL certificate verification.
        --no-persist-env  Do not persist env vars to shell profile.
        --overwrite-env   Overwrite existing env var lines in shell profile.
        --dry-run         Preview what setup would do without making changes.
    """
    parser = argparse.ArgumentParser(
        prog="agdt-setup-copilot-cli",
        description="Install the GitHub Copilot CLI standalone binary into ~/.agdt/bin/.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--system-only",
        action="store_true",
        default=False,
        help="Skip managed install.",
    )
    parser.add_argument(
        "--no-verify-ssl",
        action="store_true",
        default=False,
        help="Disable SSL certificate verification (insecure; use only on trusted networks).",
    )
    parser.add_argument(
        "--no-persist-env",
        action="store_true",
        default=False,
        help="Do not persist environment variables to shell profile.",
    )
    parser.add_argument(
        "--overwrite-env",
        action="store_true",
        default=False,
        help="Overwrite existing environment variable lines in shell profile.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Preview what setup would do without making any changes.",
    )
    args = parser.parse_args()

    original_no_verify = os.environ.get("AGDT_NO_VERIFY_SSL")
    try:
        if args.no_verify_ssl:
            if args.dry_run:
                print("  ○ would set AGDT_NO_VERIFY_SSL=1")
            else:
                os.environ["AGDT_NO_VERIFY_SSL"] = "1"
                print("  ⚠  SSL verification disabled. Use only on trusted networks.")

        if args.system_only:
            print("Skipping managed install of Copilot CLI (--system-only).")
            return

        unified_path, npmrc_result = _prefetch_certs(npm_enabled=True, dry_run=args.dry_run)
        print()

        ok = install_copilot_cli(dry_run=args.dry_run)
        if not ok:
            sys.exit(1)

        _persist_env_vars_to_profile(
            npmrc_path=npmrc_result,
            unified_path=unified_path,
            persist_env=not args.no_persist_env,
            overwrite_env=args.overwrite_env,
            npm_enabled=True,
            dry_run=args.dry_run,
        )
    finally:
        # Restore the original AGDT_NO_VERIFY_SSL state.
        if original_no_verify is None:
            os.environ.pop("AGDT_NO_VERIFY_SSL", None)
        else:
            os.environ["AGDT_NO_VERIFY_SSL"] = original_no_verify


def setup_gh_cli_cmd() -> None:
    """Install the GitHub CLI (``gh``) into ``~/.agdt/bin/``.

    Usage:
        agdt-setup-gh-cli [--system-only] [--no-verify-ssl] [--no-persist-env]
                          [--overwrite-env] [--dry-run]

    Options:
        --system-only   Skip the managed install.
        --no-verify-ssl Disable SSL certificate verification.
        --no-persist-env  Do not persist env vars to shell profile.
        --overwrite-env   Overwrite existing env var lines in shell profile.
        --dry-run         Preview what setup would do without making changes.
    """
    parser = argparse.ArgumentParser(
        prog="agdt-setup-gh-cli",
        description="Install the GitHub CLI (gh) into ~/.agdt/bin/.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--system-only",
        action="store_true",
        default=False,
        help="Skip managed install.",
    )
    parser.add_argument(
        "--no-verify-ssl",
        action="store_true",
        default=False,
        help="Disable SSL certificate verification (insecure; use only on trusted networks).",
    )
    parser.add_argument(
        "--no-persist-env",
        action="store_true",
        default=False,
        help="Do not persist environment variables to shell profile.",
    )
    parser.add_argument(
        "--overwrite-env",
        action="store_true",
        default=False,
        help="Overwrite existing environment variable lines in shell profile.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Preview what setup would do without making any changes.",
    )
    args = parser.parse_args()

    original_no_verify = os.environ.get("AGDT_NO_VERIFY_SSL")
    try:
        if args.no_verify_ssl:
            if args.dry_run:
                print("  ○ would set AGDT_NO_VERIFY_SSL=1")
            else:
                os.environ["AGDT_NO_VERIFY_SSL"] = "1"
                print("  ⚠  SSL verification disabled. Use only on trusted networks.")

        if args.system_only:
            print("Skipping managed install of GitHub CLI (--system-only).")
            return

        unified_path, npmrc_result = _prefetch_certs(npm_enabled=True, dry_run=args.dry_run)
        print()

        ok = install_gh_cli(dry_run=args.dry_run)
        if not ok:
            sys.exit(1)

        _persist_env_vars_to_profile(
            npmrc_path=npmrc_result,
            unified_path=unified_path,
            persist_env=not args.no_persist_env,
            overwrite_env=args.overwrite_env,
            npm_enabled=True,
            dry_run=args.dry_run,
        )
    finally:
        # Restore the original AGDT_NO_VERIFY_SSL state.
        if original_no_verify is None:
            os.environ.pop("AGDT_NO_VERIFY_SSL", None)
        else:
            os.environ["AGDT_NO_VERIFY_SSL"] = original_no_verify


def setup_certs_cmd() -> None:
    """Prefetch and refresh CA certificate bundles for all setup hosts.

    Fetches the certificate chain for external hosts used during setup and
    stores the PEM bundles in ``~/.agdt/certs/``.  When npm footprint is
    detected (or ``--npm`` is passed), also writes an ``~/.agdt/npmrc`` file
    that configures npm to use the cached CA bundle for ``registry.npmjs.org``.

    Run this command when you encounter SSL errors during setup on a
    corporate network with a custom CA certificate.

    Usage:
        agdt-setup-certs [--no-verify-ssl] [--no-persist-env] [--overwrite-env]
                         [--npm | --no-npm] [--dry-run]
    """
    parser = argparse.ArgumentParser(
        prog="agdt-setup-certs",
        description="Prefetch and refresh CA certificate bundles for all setup hosts.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--no-verify-ssl",
        action="store_true",
        default=False,
        help="Disable SSL certificate verification (insecure; use only on trusted networks).",
    )
    parser.add_argument(
        "--no-persist-env",
        action="store_true",
        default=False,
        help="Do not persist environment variables to shell profile.",
    )
    parser.add_argument(
        "--overwrite-env",
        action="store_true",
        default=False,
        help="Overwrite existing environment variable lines in shell profile.",
    )
    npm_group = parser.add_mutually_exclusive_group()
    npm_group.add_argument(
        "--npm",
        action="store_true",
        default=False,
        help="Force npm certificate and configuration work regardless of npm footprint.",
    )
    npm_group.add_argument(
        "--no-npm",
        action="store_true",
        default=False,
        help="Skip npm certificate and configuration work regardless of npm footprint.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Preview what setup would do without making any changes.",
    )
    args = parser.parse_args()

    from agentic_devtools.state import _get_git_repo_root

    original_no_verify = os.environ.get("AGDT_NO_VERIFY_SSL")
    try:
        if args.no_verify_ssl:
            if args.dry_run:
                print("  ○ would set AGDT_NO_VERIFY_SSL=1")
            else:
                os.environ["AGDT_NO_VERIFY_SSL"] = "1"
                print("  ⚠  SSL verification disabled. Use only on trusted networks.")

        git_root = _get_git_repo_root()
        npm_enabled = _resolve_npm_enabled(args, git_root if git_root else Path.cwd())

        if args.dry_run:
            print("Previewing CA certificate bundle refresh...")
        else:
            print("Refreshing CA certificate bundles...")
        print()
        unified_path, npmrc_result = _prefetch_certs(npm_enabled=npm_enabled, dry_run=args.dry_run)

        _persist_env_vars_to_profile(
            npmrc_path=npmrc_result,
            unified_path=unified_path,
            persist_env=not args.no_persist_env,
            overwrite_env=args.overwrite_env,
            npm_enabled=npm_enabled,
            dry_run=args.dry_run,
        )
    finally:
        # Restore the original AGDT_NO_VERIFY_SSL state.
        if original_no_verify is None:
            os.environ.pop("AGDT_NO_VERIFY_SSL", None)
        else:
            os.environ["AGDT_NO_VERIFY_SSL"] = original_no_verify


def check_corrupted_artifacts_status() -> tuple[DependencyStatus, list[Path]]:
    """Check for corrupted install artifacts and return a pseudo-DependencyStatus.

    ``found=True`` means the environment is clean (no corruption detected).
    ``found=False`` means corrupted artifacts were found and repair is needed.

    Returns:
        A tuple of (DependencyStatus, detected_artifacts).
    """
    from .script_generators.required_setup import detect_corrupted_artifacts

    try:
        artifacts = detect_corrupted_artifacts()
    except OSError:
        # If scanning fails (e.g., site-packages inaccessible), treat as healthy.
        artifacts = []
    status = DependencyStatus(
        name="corrupted-install-artifacts",
        found=len(artifacts) == 0,
        required=True,
        category="Required",
    )
    if artifacts:
        # Store the detected list so the repair step can reuse it (NFR-003: single scan).
        # Serialize to str so repair_details stays JSON-serializable (Path is not).
        status.repair_details["detected_artifacts"] = [str(a) for a in artifacts]
    return status, artifacts


def register_stale_install_repair(registry: object) -> None:
    """Register the corrupted-install-artifacts repair factory.

    The factory lazily imports ``doctor_repair`` only at dispatch time (FR-008).

    Args:
        registry: A ``RepairRegistry`` instance to register the factory into.
    """
    from .fixloop import ErrorClass

    def _factory():  # type: ignore[no-untyped-def]
        from .doctor_repair import repair_corrupted_artifacts

        return repair_corrupted_artifacts

    registry.register(ErrorClass.STALE_PARTIAL_INSTALL, _factory)  # type: ignore[attr-defined]


def setup_check_cmd() -> None:
    """Verify all external CLI dependencies and print their status.

    Does not install dependencies directly. With ``--fix``, registered repair
    factories may be dispatched and can perform installation steps.

    Usage:
        agdt-setup-check [--fix] [--json]

    Flags:
        --fix   Enable repair-dispatch mode.  When problems are detected and a
                repair factory is registered in the doctor's RepairRegistry for
                the corresponding ErrorClass, that factory is invoked to obtain
                and run the repair function.  The report ``mode`` is
                ``"check-fix"`` when this flag is present.
        --json  Emit the structured ``SetupReport`` as JSON to stdout instead of
                the human-readable dependency table.  Combinable with ``--fix``.
    """
    import argparse as _argparse
    import json as _json

    parser = _argparse.ArgumentParser(prog="agdt-setup-check")
    parser.add_argument("--fix", action="store_true", default=False)
    parser.add_argument("--json", action="store_true", default=False)
    args = parser.parse_args()

    statuses = check_all_dependencies()

    # Synthesize CA-bundle DependencyStatus (FR-009).
    ca_bundle_path = Path.home() / ".agdt" / "certs" / "unified-ca-bundle.pem"
    try:
        ca_stat = ca_bundle_path.stat()
    except (FileNotFoundError, OSError):
        ca_found = False
        ca_path_value: str | None = None
    else:
        ca_found = False
        if ca_bundle_path.is_file() and ca_stat.st_size > 0:
            try:
                ca_content = ca_bundle_path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                ca_found = False
            else:
                ca_found = _count_certificates_in_pem(ca_content) >= 1
        ca_path_value = str(ca_bundle_path) if ca_found else None

    ca_status = DependencyStatus(
        name="ca-bundle",
        found=ca_found,
        path=ca_path_value,
        required=True,
        install_hint="run: agdt-setup-certs",
        category="Required",
    )
    statuses.append(ca_status)

    # Detect corrupted install artifacts.
    corruption_status, detected_artifacts = check_corrupted_artifacts_status()

    if args.fix or args.json:
        from .doctor import get_default_registry, run_doctor
        from .repairs.registration import register_default_repairs

        statuses.append(corruption_status)
        register_default_repairs()
        register_stale_install_repair(get_default_registry())
        result = run_doctor(statuses, fix=args.fix)
        report = result.report

        if args.json:
            print(_json.dumps(report.to_dict(), indent=2))
        else:
            print_dependency_report(statuses)
            for outcome in result.repair_outcomes:
                name = outcome.dependency.name
                if outcome.success and outcome.applied:
                    label = "fixed"
                elif outcome.success and not outcome.applied:
                    label = "ok (no-op)"
                else:
                    label = f"failed ({outcome.error_message})" if outcome.error_message else "failed"
                print(f"  {name}: {label}")
            if report.exit_code == 0:
                print("OK")

        sys.exit(report.exit_code)

    # ── Backward-compatible check-only path (no flags) ────────────────────────
    # Print corruption warning to stderr if artifacts detected (dry-run preview).
    if not corruption_status.found and detected_artifacts:
        grouped: dict[str, list[str]] = {}
        for art in detected_artifacts:
            parent = str(art.parent)
            grouped.setdefault(parent, []).append(art.name)
        print(
            "\n⚠️  Corrupted install artifacts detected (run with --fix to repair):",
            file=sys.stderr,
        )
        for parent_dir, names in grouped.items():
            print(f"  {parent_dir}{os.sep}", file=sys.stderr)
            for name in names:
                print(f"    {name}", file=sys.stderr)
        print(file=sys.stderr)

    print_dependency_report(statuses)

    any_required_missing = any(s.required and not s.found for s in statuses)
    if any_required_missing:
        from .exit_codes import ExitCode as _CheckExitCode

        sys.exit(_CheckExitCode.MISSING_REQUIRED_DEP)
