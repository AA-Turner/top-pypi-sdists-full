"""Factory for IssueProvider instances.

Resolves the configured issue adapter from (in priority order):
  1. Explicit ``provider`` argument (CLI ``--provider`` override)
  2. ``.github/agdt-config.json`` → ``platform.issue_adapter``
  3. State key ``platform.issue_adapter``
  4. Environment variable ``AGDT_ISSUE_ADAPTER``

Raises :class:`~agentic_devtools.epic_tree.errors.ConfigError` when the
value is missing, unrecognised, or the reserved ``"markdown"`` adapter.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING

from agentic_devtools.cli.subprocess_utils import run_safe
from agentic_devtools.config import load_repo_config
from agentic_devtools.epic_tree.errors import ConfigError

if TYPE_CHECKING:
    from agentic_devtools.adapters.github_provider import GitHubProvider
    from agentic_devtools.adapters.jira_provider import JiraProvider

_SUPPORTED_ADAPTERS = ("github", "jira")
_CONFIG_FILE = ".github/agdt-config.json"


def get_issue_provider(
    repo_path: str | Path,
    *,
    provider: str | None = None,
) -> GitHubProvider | JiraProvider:
    """Return a provider instance based on platform configuration.

    Both :class:`~agentic_devtools.adapters.github_provider.GitHubProvider`
    and :class:`~agentic_devtools.adapters.jira_provider.JiraProvider` conform
    to the :class:`~agentic_devtools.adapters.issue_provider.IssueProvider`
    protocol.  The return type is annotated as the union of the two concrete
    classes rather than the protocol itself so that callers keep access to any
    provider-specific attributes without an additional cast.

    Resolution priority:
      1. Explicit ``provider`` argument (CLI ``--provider`` override)
      2. ``platform.issue_adapter`` in ``.github/agdt-config.json``
      3. State key ``platform.issue_adapter``
      4. Environment variable ``AGDT_ISSUE_ADAPTER``

    Args:
        repo_path: Absolute path to the target repository root.
            Accepts both ``str`` and :class:`~pathlib.Path`.
        provider: Optional explicit adapter name override (e.g. from CLI
            ``--provider`` argument). Takes highest priority when set.

    Returns:
        A :class:`GitHubProvider` or :class:`JiraProvider` instance.

    Raises:
        ConfigError: If the adapter is not configured or not recognised.
    """
    repo_path_str = str(repo_path)
    adapter_name = _resolve_adapter_name(repo_path_str, provider=provider)
    return _instantiate_provider(adapter_name, repo_path_str)


def resolve_provider_name(repo_path: str | Path, *, provider: str | None = None) -> str:
    """Resolve the effective provider name without constructing a provider.

    Public wrapper around :func:`_resolve_adapter_name` that lets callers
    resolve the single effective provider identity once and reuse it — for
    example passing it to both :func:`~agentic_devtools.epic_tree.loader.load_epic_tree`
    (for provider-specific validation) and :func:`get_issue_provider` (for
    mutation), guaranteeing both operate on the same normalized name.

    Resolution priority mirrors :func:`get_issue_provider`:

      1. Explicit ``provider`` argument (CLI ``--provider`` override)
      2. ``platform.issue_adapter`` in ``.github/agdt-config.json``
      3. State key ``platform.issue_adapter``
      4. Environment variable ``AGDT_ISSUE_ADAPTER``

    Args:
        repo_path: Absolute path to the target repository root.  Accepts both
            ``str`` and :class:`~pathlib.Path`.
        provider: Optional explicit adapter name override.  Takes highest
            priority when a non-empty string.

    Returns:
        The normalized (lowercased, stripped) provider name — one of
        ``"github"`` or ``"jira"``.

    Raises:
        ConfigError: If the provider is not configured or not recognised.
    """
    return _resolve_adapter_name(str(repo_path), provider=provider)


def _resolve_adapter_name(repo_path: str, *, provider: str | None = None) -> str:
    """Resolve the adapter name from provider arg, config, state, or env var.

    Resolution priority:
      1. Explicit ``provider`` argument (CLI ``--provider`` override)
      2. ``platform.issue_adapter`` in ``.github/agdt-config.json``
      3. State key ``platform.issue_adapter``
      4. Environment variable ``AGDT_ISSUE_ADAPTER``
    """
    # Structural validation: platform must be a dict if present (hard error,
    # preempts all adapter-name sources including explicit provider arg)
    config = load_repo_config(repo_path)
    platform = config.get("platform")

    if platform is not None and not isinstance(platform, dict):
        raise ConfigError(
            config_path=_CONFIG_FILE,
            field_name="platform",
            message=(
                f"'platform' in .github/agdt-config.json must be a mapping, "
                f"got {type(platform).__name__}; "
                f"set 'platform.issue_adapter' to 'github' or 'jira'"
            ),
        )

    # Source 1: Explicit provider argument (CLI --provider override)
    if provider is not None:
        if not isinstance(provider, str):
            raise ConfigError(
                config_path="CLI argument --provider",
                field_name="--provider",
                message=(
                    f"The --provider argument must be a string, "
                    f"got {type(provider).__name__}; "
                    f"specify one of {list(_SUPPORTED_ADAPTERS)}."
                ),
            )
        stripped = provider.strip()
        if stripped:
            return _validate_adapter_name(
                stripped,
                config_path="CLI argument --provider",
                field_name="--provider",
            )

    # Source 2: .github/agdt-config.json platform.issue_adapter
    if isinstance(platform, dict):
        if "issue_adapter" in platform:
            adapter_name = platform.get("issue_adapter")
            if not isinstance(adapter_name, str):
                raise ConfigError(
                    config_path=_CONFIG_FILE,
                    field_name="platform.issue_adapter",
                    message=(
                        "'platform.issue_adapter' in .github/agdt-config.json must be a string, "
                        f"got {type(adapter_name).__name__}; set it to 'github' or 'jira'."
                    ),
                )
            if adapter_name.strip():
                return _validate_adapter_name(
                    str(adapter_name),
                    config_path=_CONFIG_FILE,
                    field_name="platform.issue_adapter",
                )

    # Source 3: State key
    state_value = None
    try:
        from agentic_devtools.state import get_value

        state_value = get_value("platform.issue_adapter")
    except Exception:
        pass

    if state_value is not None:
        if not isinstance(state_value, str):
            raise ConfigError(
                config_path="agdt state",
                field_name="platform.issue_adapter",
                message=(
                    f"State key 'platform.issue_adapter' must be a string, "
                    f"got {type(state_value).__name__}; "
                    f"run: agdt-set platform.issue_adapter github  (or jira)"
                ),
            )
        if state_value.strip():
            return _validate_adapter_name(
                state_value,
                config_path="agdt state",
                field_name="platform.issue_adapter",
            )

    # Source 4: Environment variable
    env_value = os.environ.get("AGDT_ISSUE_ADAPTER", "").strip()
    if env_value:
        return _validate_adapter_name(
            env_value,
            config_path="environment variable AGDT_ISSUE_ADAPTER",
            field_name="AGDT_ISSUE_ADAPTER",
        )

    # No configuration found
    raise ConfigError(
        config_path=_CONFIG_FILE,
        field_name="platform.issue_adapter",
        message=(
            f"Issue adapter not configured. "
            f"Specify one of {list(_SUPPORTED_ADAPTERS)} using one of: "
            f"the --provider CLI flag (overrides for this invocation only), "
            f"'platform.issue_adapter' in .github/agdt-config.json (repo default), "
            f"state key 'platform.issue_adapter' (agdt-set platform.issue_adapter <name>), "
            f"or environment variable AGDT_ISSUE_ADAPTER."
        ),
    )


def _validate_adapter_name(
    name: str,
    *,
    config_path: str = _CONFIG_FILE,
    field_name: str = "platform.issue_adapter",
) -> str:
    """Validate the adapter name is supported for hierarchy operations.

    Args:
        name: The raw adapter name to validate.
        config_path: Source attribution — where the value came from.
        field_name: Source attribution — the specific field/key name.

    Returns:
        The normalized (lowercased, stripped) adapter name.

    Raises:
        ConfigError: If the adapter name is not supported.
    """
    name_lower = name.lower().strip()

    if name_lower == "markdown":
        raise ConfigError(
            config_path=config_path,
            field_name=field_name,
            message=(
                f"'markdown' is valid only for read/normalize operations via get_adapter(). "
                f"Hierarchy-creation via IssueProvider requires one of {list(_SUPPORTED_ADAPTERS)}."
            ),
        )

    if name_lower not in _SUPPORTED_ADAPTERS:
        raise ConfigError(
            config_path=config_path,
            field_name=field_name,
            message=(
                f"Unrecognised issue adapter '{name}'. "
                f"Supported values for hierarchy operations: {list(_SUPPORTED_ADAPTERS)}."
            ),
        )

    return name_lower


def _validate_repo_slug(slug: str) -> None:
    """Validate that a repository slug is in ``owner/repo`` format.

    Raises:
        ConfigError: If the slug is malformed or contains whitespace.
    """
    parts = slug.split("/")
    if (
        len(parts) != 2
        or not parts[0]
        or not parts[1]
        or any(c.isspace() for c in parts[0])
        or any(c.isspace() for c in parts[1])
    ):
        raise ConfigError(
            config_path=_CONFIG_FILE,
            field_name="platform.github.repo",
            message=(
                f"Repository slug must be in 'owner/repo' format, got '{slug}'. "
                f"Set 'platform.github.repo' to a valid 'owner/repo' value."
            ),
        )


def _validate_github_auth() -> None:
    """Validate GitHub CLI authentication via ``gh auth status``.

    Raises:
        ConfigError: If ``gh`` is not installed, auth check times out,
            or the user is not authenticated.
    """
    try:
        result = run_safe(
            ["gh", "auth", "status"],
            capture_output=True,
            text=True,
            shell=False,
            timeout=10,
        )
    except FileNotFoundError:
        raise ConfigError(
            config_path="gh CLI",
            field_name="gh auth status",
            message=("Install the GitHub CLI (`gh`) from https://cli.github.com and ensure it is on your PATH."),
        )
    except subprocess.TimeoutExpired:
        raise ConfigError(
            config_path="gh CLI",
            field_name="gh auth status",
            message=(
                "The `gh auth status` check timed out. Verify your `gh` CLI "
                "installation and network connectivity, then re-run."
            ),
        )

    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip()
        hint = f" (exit code {result.returncode}: {detail})" if detail else f" (exit code {result.returncode})"
        raise ConfigError(
            config_path="gh CLI",
            field_name="gh auth status",
            message=(f"`gh auth status` failed{hint}. If not authenticated, run `gh auth login` and re-run."),
        )


def _validate_jira_prerequisites(jira_config: dict, repo_path: str) -> tuple[str, str]:
    """Validate Jira prerequisites: project_key, base_url, auth token.

    Args:
        jira_config: The ``platform.jira`` section from config.
        repo_path: Repository path (unused, reserved for future use).

    Returns:
        A tuple of ``(project_key, base_url)``.

    Raises:
        ConfigError: If any prerequisite is missing or invalid.
    """
    # Validate project_key
    if isinstance(jira_config, dict):
        project_key = jira_config.get("project_key", "")
    else:
        project_key = ""
    if not isinstance(project_key, str) or not project_key.strip():
        raise ConfigError(
            config_path=_CONFIG_FILE,
            field_name="platform.jira.project_key",
            message="Jira issue adapter requires a non-empty 'platform.jira.project_key'.",
        )
    project_key = project_key.strip()

    # Resolve base_url: config -> env
    base_url = jira_config.get("base_url", "") if isinstance(jira_config, dict) else ""
    if isinstance(base_url, str):
        base_url = base_url.strip()
    else:
        base_url = ""
    if not base_url:
        base_url = os.environ.get("JIRA_BASE_URL", "").strip()
    if not base_url:
        raise ConfigError(
            config_path=_CONFIG_FILE,
            field_name="platform.jira.base_url",
            message=(
                "Jira issue adapter requires a base URL. "
                "Set 'platform.jira.base_url' in .github/agdt-config.json "
                "or the JIRA_BASE_URL environment variable."
            ),
        )

    # Validate auth token
    token = os.environ.get("JIRA_API_TOKEN", "").strip() or os.environ.get("JIRA_COPILOT_PAT", "").strip()
    if not token:
        raise ConfigError(
            config_path="environment",
            field_name="JIRA_API_TOKEN / JIRA_COPILOT_PAT",
            message=(
                "Jira issue adapter requires an auth token. "
                "Set JIRA_API_TOKEN or JIRA_COPILOT_PAT environment variable."
            ),
        )

    # Validate basic-auth identity when scheme is basic or any identity env var is set.
    # JiraProvider switches to Basic auth whenever an identity env var is present (even if
    # scheme is not "basic"), so a whitespace-only value must be caught here rather than
    # reaching JiraProvider and producing an invalid Authorization header.
    auth_scheme = os.environ.get("JIRA_AUTH_SCHEME", "").lower().strip()
    identity_var_set = any(os.environ.get(k) is not None for k in ("JIRA_USER_EMAIL", "JIRA_EMAIL", "JIRA_USERNAME"))
    if auth_scheme == "basic" or identity_var_set:
        identity = (
            os.environ.get("JIRA_USER_EMAIL", "").strip()
            or os.environ.get("JIRA_EMAIL", "").strip()
            or os.environ.get("JIRA_USERNAME", "").strip()
        )
        if not identity:
            raise ConfigError(
                config_path="environment",
                field_name="JIRA_USER_EMAIL / JIRA_EMAIL / JIRA_USERNAME",
                message=(
                    "Jira basic auth requires an identity. "
                    "Set JIRA_USER_EMAIL, JIRA_EMAIL, or JIRA_USERNAME environment variable."
                ),
            )

    return project_key, base_url


def _instantiate_provider(adapter_name: str, repo_path: str) -> GitHubProvider | JiraProvider:
    """Instantiate the correct provider based on the adapter name."""
    if adapter_name == "github":
        from agentic_devtools.adapters.github_provider import GitHubProvider
        from agentic_devtools.config import load_platform_config

        platform_config = load_platform_config(repo_path)
        _gh = platform_config.get("github")
        gh: dict[str, object] = _gh if isinstance(_gh, dict) else {}

        def _clean(value: object) -> str:
            return value.strip() if isinstance(value, str) else ""

        repo_slug = _clean(gh.get("repo"))
        if not repo_slug:
            repo_owner = _clean(gh.get("repo_owner"))
            repo_name = _clean(gh.get("repo_name"))
            repo_slug = f"{repo_owner}/{repo_name}" if repo_owner and repo_name else ""
        if not repo_slug:
            raise ConfigError(
                config_path=_CONFIG_FILE,
                field_name="platform.github.repo",
                message=(
                    "GitHub issue adapter requires repository coordinates. "
                    "Set 'platform.github.repo' to 'owner/repo', or provide both "
                    "'platform.github.repo_owner' and 'platform.github.repo_name'."
                ),
            )

        _validate_repo_slug(repo_slug)
        _validate_github_auth()

        try:
            return GitHubProvider(owner_repo=repo_slug)
        except ValueError as exc:
            raise ConfigError(
                config_path=_CONFIG_FILE,
                field_name="platform.github.repo",
                message=f"Invalid GitHub repository slug: {exc}",
            ) from exc

    if adapter_name == "jira":
        from agentic_devtools.adapters.jira_provider import JiraProvider
        from agentic_devtools.config import load_platform_config

        platform_config = load_platform_config(repo_path)
        jira_config = platform_config.get("jira", {})

        project_key, base_url = _validate_jira_prerequisites(jira_config, repo_path)
        return JiraProvider(project_key=project_key, base_url=base_url)

    # Should never reach here due to _validate_adapter_name
    raise ConfigError(  # pragma: no cover
        config_path=_CONFIG_FILE,
        field_name="platform.issue_adapter",
        message=f"Cannot instantiate adapter '{adapter_name}'.",
    )
