import contextlib
import os
import re
import typing as t
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlparse

import yaml
from pydantic import BaseModel, Field, PrivateAttr

if t.TYPE_CHECKING:
    from dreadnode.app.api.client import ApiClient
    from dreadnode.app.api.models import User, Workspace

# Default path for user configuration
DEFAULT_CONFIG_PATH = Path.home() / ".dreadnode" / "config.yaml"

# Default platform URL when no profile or override is set
DEFAULT_PLATFORM_URL = "https://app.dreadnode.io"

# Hostnames that are equivalent for URL comparison
_LOCALHOST_ALIASES = frozenset({"localhost", "127.0.0.1", "::1"})


def _normalize_url(url: str) -> str:
    """Normalize a URL for comparison: strip trailing slash, canonicalize localhost variants."""
    parsed = urlparse(url.rstrip("/"))
    host = parsed.hostname or ""
    if host in _LOCALHOST_ALIASES:
        host = "localhost"
    port = parsed.port
    # Rebuild with normalized host
    netloc = host if port is None else f"{host}:{port}"
    return f"{parsed.scheme}://{netloc}{parsed.path}"


def urls_match(a: str, b: str) -> bool:
    """Compare two URLs, treating localhost/127.0.0.1/::1 as equivalent."""
    return _normalize_url(a) == _normalize_url(b)


class _UnsetType:
    """Sentinel type distinguishing 'no override' from 'overridden to None'."""

    _instance: t.ClassVar["_UnsetType | None"] = None

    def __new__(cls) -> "_UnsetType":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self) -> str:
        return "UNSET"

    def __bool__(self) -> bool:
        return False


UNSET = _UnsetType()
"""Singleton sentinel for PrivateAttr defaults."""

# Network error class names that should trigger retry in validate_scope.
# Checked by class name to avoid importing httpx at module level.
_TRANSIENT_ERROR_NAMES = frozenset(
    {
        "ConnectTimeout",
        "ConnectError",
        "ReadTimeout",
        "NetworkError",
        "RemoteProtocolError",
    }
)


def _is_transient_network_error(exc: BaseException) -> bool:
    """Return True if *exc* looks like a transient network/transport error."""
    cls_name = type(exc).__name__
    return cls_name in _TRANSIENT_ERROR_NAMES or isinstance(
        exc, (OSError, ConnectionError, TimeoutError)
    )


class Profile(BaseModel):
    """Server connection profile: credentials, scope defaults, and cached identity.

    Scope properties (``.organization``, ``.workspace``, ``.project``) return the
    active override if set, otherwise the saved default.  Overrides are held in
    Pydantic ``PrivateAttr`` fields and are **never serialized** — they exist only
    for the lifetime of the in-memory object.

    Typical usage::

        profile = base.with_overrides(workspace="other-ws")
        profile.validate_scope(api)   # confirm scope, fill gaps
        api.list_datasets(profile.organization)
    """

    # --- Persisted fields ---

    url: str
    user_key: str | None = None
    email: str | None = None
    username: str | None = None
    api_key: str | None = None
    default_model: str | None = None
    custom_model_ids: list[str] = Field(default_factory=list)
    default_organization: str | None = None
    default_workspace: str | None = None
    default_project: str | None = None
    last_used_at: str | None = None

    # --- Ephemeral state (excluded from serialization) ---
    # UNSET means "no override; fall through to default".
    # None means "explicitly overridden to nothing".

    _name: str | None = PrivateAttr(default=None)
    _organization: t.Any = PrivateAttr(default=UNSET)
    _workspace: t.Any = PrivateAttr(default=UNSET)
    _project: t.Any = PrivateAttr(default=UNSET)
    _project_id: str | None = PrivateAttr(default=None)
    _user: "User | None" = PrivateAttr(default=None)

    # --- Identity ---

    @property
    def name(self) -> str | None:
        """Profile name (the key in UserConfig.servers).  Ephemeral, never serialized."""
        return self._name

    # --- Scope properties: override ?? default ---

    @property
    def organization(self) -> str | None:
        if self._organization is not UNSET:
            return self._organization
        return self.default_organization

    @property
    def workspace(self) -> str | None:
        if self._workspace is not UNSET:
            return self._workspace
        return self.default_workspace

    @property
    def project(self) -> str | None:
        if self._project is not UNSET:
            return self._project
        return self.default_project

    @property
    def project_id(self) -> str | None:
        return self._project_id

    # --- Throwing accessors (safe to call after validate_scope / connect) ---

    @property
    def org_key(self) -> str:
        """Organization key.  Raises if not set."""
        value = self.organization
        if value is None:
            raise RuntimeError("Organization not set — call validate_scope() or connect() first")
        return value

    @property
    def workspace_key(self) -> str:
        """Workspace key.  Raises if not set."""
        value = self.workspace
        if value is None:
            raise RuntimeError("Workspace not set — call validate_scope() or connect() first")
        return value

    @property
    def project_key(self) -> str | None:
        return self.project

    @property
    def user(self) -> "User | None":
        """Validated user object from the server (ephemeral, set by validate_scope)."""
        return self._user

    # --- Override / validation API ---

    def with_overrides(
        self,
        *,
        url: str | None = None,
        api_key: str | None = None,
        organization: str | None = None,
        workspace: str | None = None,
        project: str | None = None,
    ) -> "Profile":
        """Return a copy with non-None values overlaid as ephemeral overrides.

        .. note::

            Scope fields (organization, workspace, project) use PrivateAttr
            overrides and are never serialized.  ``url`` and ``api_key`` mutate
            the copy's persisted fields directly — the copy must not be written
            back to disk.  TODO: give url/api_key the same PrivateAttr treatment
            (requires renaming base fields + serialization aliases).
        """
        copy = self.model_copy()
        if url is not None:
            copy.url = url
        if api_key is not None:
            copy.api_key = api_key
        if organization is not None:
            copy._organization = organization
        if workspace is not None:
            copy._workspace = workspace
        if project is not None:
            copy._project = project
        return copy

    def validate_scope(self, api: "ApiClient") -> None:
        """Validate scope against server, fill gaps.  Mutates private attrs only.

        - Confirms organization exists and user has access.
        - Validates workspace if set, or auto-resolves the default workspace.
        - Validates project if set (404 → None).
        - Fetches and caches the authenticated user.

        Retries up to 3 times on transient network errors (connect timeout,
        connection refused, etc.) to handle flaky sandbox-to-API connectivity.
        """
        import time

        max_attempts = 3
        backoff = [2.0, 5.0]

        for attempt in range(1, max_attempts + 1):
            try:
                self._validate_scope_inner(api)
            except Exception as exc:
                # Only retry transient network errors, not logic errors
                if not _is_transient_network_error(exc):
                    raise
                if attempt == max_attempts:
                    raise
                delay = backoff[attempt - 1]
                import logging

                logging.getLogger("dreadnode").warning(
                    "validate_scope attempt %d/%d failed (%s: %s), retrying in %.0fs",
                    attempt,
                    max_attempts,
                    type(exc).__name__,
                    exc,
                    delay,
                )
                time.sleep(delay)
            else:
                return

    def _raise_project_not_found(self, proj_key: str) -> t.NoReturn:
        """Raise a project not found error."""
        raise RuntimeError(
            f"Project '{proj_key}' not found in workspace '{self.workspace_key}' of organization '{self.org_key}'."
        ) from None

    def _validate_scope_inner(self, api: "ApiClient") -> None:
        """Core validation logic, separated for retry wrapping."""
        from dreadnode.core.util import valid_key

        org_key = self.organization
        if not org_key:
            raise RuntimeError("Organization is required")
        if not valid_key(org_key):
            raise RuntimeError(
                f'Invalid Organization Key: "{org_key}". '
                "The expected characters are lowercase letters, numbers, and hyphens (-)."
            )

        organization = api.get_organization(org_key)
        if not organization:
            raise RuntimeError(f"Organization '{org_key}' not found.")

        ws_key = self.workspace
        if ws_key:
            if not valid_key(ws_key):
                raise RuntimeError(
                    f'Invalid Workspace Key: "{ws_key}". '
                    "The expected characters are lowercase letters, numbers, and hyphens (-)."
                )
            workspace = api.get_workspace(org_key, ws_key)
            if not workspace:
                raise RuntimeError(f"Workspace '{ws_key}' not found in organization '{org_key}'.")
        else:
            workspaces = api.list_workspaces(org_key)
            if not workspaces:
                raise RuntimeError(
                    f"No workspaces found in organization '{org_key}'. "
                    "Create a workspace first or specify one explicitly."
                )
            workspace = next(
                (w for w in workspaces if w.is_default),
                workspaces[0],
            )
            self._workspace = workspace.key

        proj_key = self.project
        if proj_key:
            if not valid_key(proj_key):
                raise RuntimeError(
                    f'Invalid Project Key: "{proj_key}". '
                    "The expected characters are lowercase letters, numbers, and hyphens (-)."
                )
            try:
                proj = api.get_project(org_key, self.workspace_key, proj_key)
                if proj:
                    self._project_id = str(proj.id)
                else:
                    self._raise_project_not_found(proj_key)
            except RuntimeError as e:
                if "404" not in str(e):
                    raise
                # Project doesn't exist — clear it (404 → None behavior)
                self._project = None
                self._project_id = None

        self._user = api.get_user()

    def promote_scope_to_defaults(self) -> None:
        """Promote active overrides to saved defaults (for login, workspace switch)."""
        if self._organization is not UNSET:
            self.default_organization = self._organization
        if self._workspace is not UNSET:
            self.default_workspace = self._workspace
        if self._project is not UNSET:
            self.default_project = self._project

    def promote_identity_to_defaults(self) -> None:
        """Write cached identity from validate_scope() back to persisted fields."""
        if self._user:
            self.username = self._user.username
            self.email = self._user.email_address or self.email
            self.user_key = self._user.username


class ProfileError(Exception):
    """Raised when profile resolution or validation fails.

    Extends Exception directly (not RuntimeError) so the CLI meta handler
    can distinguish user-facing profile errors from unexpected crashes.
    """


_PROFILE_NAME_PATTERN = re.compile(r"^[a-zA-Z0-9_.-]+$")


def validate_profile_name(name: str) -> str:
    """Validate a profile name for use as a filesystem-safe identifier.

    Raises ``ValueError`` on invalid names.
    """
    if not name or name.strip(".") == "":
        raise ValueError("Profile name must not be empty or only dots.")
    if ".." in name:
        raise ValueError("Profile name cannot contain '..'.")
    if _PROFILE_NAME_PATTERN.fullmatch(name) is None:
        raise ValueError("Profile name contains invalid characters.")
    return name


class UserConfig(BaseModel):
    """User configuration: named profiles with an active cursor.

    CRUD methods (``save_profile``, ``activate``, ``delete``, ``disconnect``)
    mutate ``self`` but do **not** call ``write()`` — the caller controls
    persistence timing.
    """

    active: str | None = None
    servers: dict[str, Profile] = {}

    def _update_active(self) -> None:
        """If active is not set, set it to the first available server."""
        if self.active not in self.servers:
            self.active = next(iter(self.servers)) if self.servers else None

    @property
    def active_profile_name(self) -> str | None:
        """Get the name of the active profile."""
        self._update_active()
        return self.active

    @property
    def active_profile(self) -> tuple[str, Profile] | None:
        """Return ``(name, profile)`` for the active profile, or ``None``."""
        name = self.active_profile_name
        if name is not None and name in self.servers:
            return name, self.servers[name]
        return None

    # --- Persistence ---

    @classmethod
    def read(cls, path: Path | None = None) -> "UserConfig":
        """Read the user configuration from the file system or return an empty instance."""
        path = path or DEFAULT_CONFIG_PATH
        if not path.exists():
            return cls()

        with path.open("r") as f:
            config = cls.model_validate(yaml.safe_load(f))

        # Stamp profile names from dict keys (PrivateAttr, lost during deserialization)
        for name, profile in config.servers.items():
            profile._name = name
        return config

    def write(self, path: Path | None = None) -> None:
        """Write the user configuration to the file system."""
        path = path or DEFAULT_CONFIG_PATH
        self._update_active()

        if not path.parent.exists():
            path.parent.mkdir(parents=True, mode=0o700)

        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w") as f:
            yaml.dump(self.model_dump(mode="json", exclude_none=True), f)

    # --- CRUD (mutate self, don't write) ---

    def get(self, name: str) -> Profile | None:
        """Get a profile by name, or ``None``."""
        profile = self.servers.get(name)
        if profile is not None:
            profile._name = name
        return profile

    def save_profile(self, profile: Profile) -> None:
        """Add or update a named profile.  Updates ``last_used_at``.

        The profile must have a name set (via ``profile._name``).
        """
        name = profile.name
        if name is None:
            raise ValueError("profile has no name — set profile._name before saving")
        validate_profile_name(name)
        profile.last_used_at = datetime.now(UTC).isoformat()
        self.servers[name] = profile

    def activate(self, name: str) -> None:
        """Set the active profile cursor.  Raises if name not found."""
        if name not in self.servers:
            raise ProfileError(f"profile not found: {name}")
        self.active = name

    def delete(self, name: str) -> bool:
        """Remove a profile.  Clears active if it was the deleted profile."""
        validate_profile_name(name)
        if name not in self.servers:
            return False
        self.servers.pop(name)
        if self.active == name:
            self.active = None
        return True

    def disconnect(self, name: str) -> None:
        """Clear ``api_key`` on a profile but keep the shell.  Clears active if it matches."""
        validate_profile_name(name)
        profile = self.servers.get(name)
        if profile:
            profile.api_key = None
        if self.active == name:
            self.active = None

    def find_by_url(self, url: str) -> tuple[str, Profile] | None:
        """Find the best profile matching a server URL.

        Priority: active profile (if matches) > connected + most recent > disconnected + most recent.
        """
        # Prefer active profile when it matches
        active_name = self.active_profile_name
        if active_name:
            active = self.servers.get(active_name)
            if active and urls_match(active.url, url) and active.api_key:
                return active_name, active

        # Collect all matching profiles
        matches = [
            (name, profile)
            for name, profile in self.servers.items()
            if urls_match(profile.url, url)
        ]
        if not matches:
            return None

        # Sort: connected first, then by last_used_at descending
        connected = sorted(
            [(n, p) for n, p in matches if p.api_key],
            key=lambda x: x[1].last_used_at or "",
            reverse=True,
        )
        disconnected = sorted(
            [(n, p) for n, p in matches if not p.api_key],
            key=lambda x: x[1].last_used_at or "",
            reverse=True,
        )

        if connected:
            return connected[0]
        if disconnected:
            return disconnected[0]
        return None

    # --- Legacy accessors (used by existing code, to be removed in later phases) ---

    def get_server_config(self, profile: str | None = None) -> Profile:
        """Get the server configuration for the given profile."""
        profile = profile or self.active
        if not profile:
            raise RuntimeError("No profile is set, use [bold]dreadnode login[/] to authenticate")

        if profile not in self.servers:
            raise RuntimeError(f"No server configuration for profile: {profile}")

        return self.servers[profile]

    def set_server_config(self, config: Profile, profile: str | None = None) -> "UserConfig":
        """Set the server configuration for the given profile."""
        resolved_profile = profile or self.active
        if resolved_profile is None:
            raise RuntimeError("No profile specified and no active profile set")
        self.servers[resolved_profile] = config
        return self

    def get_profile_server(self, profile: str | None = None) -> str | None:
        """Get the server URL from the user config for a given profile."""
        with contextlib.suppress(RuntimeError):
            server_config = self.get_server_config(profile)
            return server_config.url
        return None

    def get_profile_api_key(self, profile: str | None = None) -> str | None:
        """Get the API key from the user config for a given profile."""
        with contextlib.suppress(RuntimeError):
            server_config = self.get_server_config(profile)
            return server_config.api_key
        return None


# ---------------------------------------------------------------------------
# Workspace resolution helper
# ---------------------------------------------------------------------------


def resolve_default_workspace(api: "ApiClient", org_key: str) -> "Workspace":
    """Auto-resolve the default workspace for an organization.

    Picks the workspace marked ``is_default``, or the first available workspace.
    Raises if the organization has no workspaces.
    """
    workspaces = api.list_workspaces(org_key)
    if not workspaces:
        raise RuntimeError(
            f"No workspaces found in organization '{org_key}'. "
            "Create a workspace first or specify one explicitly."
        )
    for ws in workspaces:
        if ws.is_default:
            return ws
    return workspaces[0]
