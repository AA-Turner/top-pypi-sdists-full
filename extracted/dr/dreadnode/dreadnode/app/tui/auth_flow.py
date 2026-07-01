"""Authentication helpers and in-memory profile state for the TUI.

Moved out of ``commands.py`` in the consolidation pass. These helpers
drive the ``/login`` command, the auth modal's API-key flow, and the
"active profile with --server override" lookup used by
:class:`ScreenRouter` and :class:`ProfileManager`.

The module-level ``_in_memory_profile`` global is a deliberate override
seam: when the TUI boots with ``--server https://other``, the resolved
profile may differ from the persisted "active" profile on disk. Rather
than rewriting the user config, the TUI sets the in-memory profile at
boot and every subsequent ``_active_profile()`` / ``_platform_client()``
call prefers it.
"""

from dreadnode.app.api.client import ApiClient
from dreadnode.app.config import Profile, UserConfig, urls_match


def _parse_login_args(args: list[str], default_platform_url: str) -> tuple[str, str | None]:
    """Parse ``/login`` arguments into ``(server_url, api_key)``."""
    server_url = default_platform_url
    api_key: str | None = None

    index = 0
    while index < len(args):
        arg = args[index]
        if arg in {"--server", "-s"}:
            index += 1
            if index >= len(args):
                raise ValueError("Usage: /login [api-key] [--server <url>]")
            server_url = args[index]
        elif arg == "apikey":
            index += 1
            if index >= len(args):
                raise ValueError("Usage: /login [api-key] [--server <url>]")
            api_key = args[index]
        elif api_key is None:
            api_key = arg
        else:
            raise ValueError(f"Unknown /login argument: {arg}")
        index += 1

    return server_url, api_key


def _save_profile(profile_name: str, profile: Profile) -> Profile:
    """Persist a server profile to the local config directory."""
    profile._name = profile_name
    user_config = UserConfig.read()
    user_config.save_profile(profile)
    user_config.activate(profile_name)
    user_config.write()
    return profile


def _login_with_api_key(
    server_url: str,
    api_key: str,
    *,
    organization: str | None = None,
    workspace: str | None = None,
    project: str | None = None,
    profile_name: str | None = None,
) -> Profile:
    """Authenticate with the platform using an API key.

    If *profile_name* is given it is used as the config key (allowing custom
    names like ``work`` or ``staging``).  Otherwise the authenticated user's
    username is used, matching the original behaviour.
    """
    from dreadnode.app.config import resolve_default_workspace

    api = ApiClient(server_url, api_key=api_key)
    user = api.get_user()
    if organization is None:
        orgs = api.list_user_organizations()
        if not orgs:
            raise RuntimeError("No organizations found for this account.")
        default_org = orgs[0].key
    else:
        default_org = api.get_organization(organization).key

    if workspace is None:
        default_workspace = resolve_default_workspace(api, default_org).key
    else:
        default_workspace = api.get_workspace(default_org, workspace).key

    if project is None:
        default_project = api.get_default_project_key(default_org, default_workspace)
    else:
        default_project = api.get_project(default_org, default_workspace, project).key

    name = profile_name or user.username

    # Check for existing profile to preserve customizations (e.g. default_model)
    user_config = UserConfig.read()
    existing = user_config.servers.get(name)
    if existing and urls_match(existing.url, server_url):
        existing.api_key = api_key
        existing.email = user.email_address
        existing.username = user.username
        existing.default_organization = default_org
        existing.default_workspace = default_workspace
        existing.default_project = default_project
        return _save_profile(name, existing)

    profile = Profile(
        url=server_url,
        user_key=user.username,
        email=user.email_address,
        username=user.username,
        api_key=api_key,
        default_organization=default_org,
        default_workspace=default_workspace,
        default_project=default_project,
    )
    return _save_profile(name, profile)


# Module-level in-memory profile set by the TUI app during boot.
# When set, _active_profile() and _platform_client() use this instead of
# re-reading from disk — critical for --server overrides where the resolved
# profile differs from the persisted active profile.
_in_memory_profile: tuple[str | None, Profile] | None = None


def _set_in_memory_profile(name: str | None, profile: Profile) -> None:
    """Called by the TUI app after boot/profile-switch to keep helpers in sync."""
    global _in_memory_profile  # noqa: PLW0603
    _in_memory_profile = (name, profile)


def _clear_in_memory_profile() -> None:
    """Called on logout to fall back to disk config."""
    global _in_memory_profile  # noqa: PLW0603
    _in_memory_profile = None


def _active_profile() -> tuple[str | None, Profile | None]:
    """Return the active profile name and config, or ``(None, None)``.

    Prefers the in-memory profile set by the TUI app (which respects
    ``--server`` overrides) over the persisted active profile on disk.
    """
    if _in_memory_profile is not None:
        return _in_memory_profile
    result = UserConfig.read().active_profile
    if result is None:
        return None, None
    return result


def _active_profile_name() -> str | None:
    """Return the active profile name, if any."""
    if _in_memory_profile is not None:
        return _in_memory_profile[0]
    return UserConfig.read().active_profile_name


def _disconnect_profile() -> str | None:
    """Revoke credentials for the active profile but keep the profile shell."""
    user_config = UserConfig.read()
    profile_name = user_config.active_profile_name
    if profile_name is None:
        return None
    user_config.disconnect(profile_name)
    user_config.write()
    return profile_name


def _delete_profile(profile_name: str) -> bool:
    """Delete a specific profile from user config."""
    user_config = UserConfig.read()
    deleted = user_config.delete(profile_name)
    if deleted:
        user_config.write()
    return deleted


def _platform_client() -> tuple[ApiClient, Profile]:
    """Create an ``ApiClient`` from the active profile.

    Raises :class:`RuntimeError` if no profile is authenticated — callers
    use this to bail out of platform-dependent flows with a user-facing
    "Not logged in" message.
    """
    profile_name, profile = _active_profile()
    if profile_name is None or profile is None:
        raise RuntimeError("Not logged in. Use /login first.")
    api = ApiClient(
        profile.url,
        api_key=profile.api_key or None,
    )
    return api, profile
