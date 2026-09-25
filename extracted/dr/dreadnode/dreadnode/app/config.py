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
    from concurrent.futures import Future

    from dreadnode.app.api.client import ApiClient
    from dreadnode.app.api.models import Organization, Project, User, Workspace

# Default path for user configuration
DEFAULT_CONFIG_PATH = Path.home() / ".dreadnode" / "config.yaml"

# Default platform URL when no profile or override is set
DEFAULT_PLATFORM_URL = "https://app.dreadnode.io"

# Product safety budget for unattended CLI and TUI workflows. Session policies
# remain budget-neutral unless a caller supplies this value explicitly.
DEFAULT_AUTONOMOUS_MAX_STEPS = 100

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


# Keep startup retries brief while allowing independent reads to recover in parallel.
_SCOPE_RETRY_INITIAL_DELAY = 0.1
_SCOPE_RETRY_MAX_DELAY = 1.0
_SCOPE_RETRY_BUDGET_SEC = 8.0
_SCOPE_CALL_TIMEOUT_SEC = 5.0
_ScopeResult = t.TypeVar("_ScopeResult")


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

    def with_scope(
        self,
        *,
        organization: t.Any = UNSET,
        workspace: t.Any = UNSET,
        project: t.Any = UNSET,
    ) -> "Profile":
        """Return a copy whose saved scope is the one given, with no overrides left.

        For scope *switches* — the ``/workspace`` command, the workspace
        picker, cross-workspace resume — where the chosen value has to become
        the effective one. ``model_copy`` carries the ephemeral CLI/env
        overrides across, and those win over the persisted defaults, so a copy
        that only rewrote ``default_*`` would report the old scope from every
        accessor and leave the runtime pointed at it.

        Arguments left ``UNSET`` keep their saved value; ``None`` clears it.
        """
        update: dict[str, t.Any] = {}
        if organization is not UNSET:
            update["default_organization"] = organization
        if workspace is not UNSET:
            update["default_workspace"] = workspace
        if project is not UNSET:
            update["default_project"] = project
        copy = self.model_copy(update=update)
        copy._organization = UNSET
        copy._workspace = UNSET
        copy._project = UNSET
        return copy

    def validate_scope(self, api: "ApiClient") -> None:
        """Validate organization, workspace, project, and user concurrently.

        Retry transient failures independently within an eight-second deadline.
        Runtime configuration can proceed unvalidated after a transport failure
        or deadline expiry; CLI callers propagate the error. Apply resolved
        scope and identity only after every required read succeeds.
        """
        # Lazy imports keep this module cheap on the startup path (ENG-8259).
        import logging
        import random
        import time
        from concurrent.futures import FIRST_EXCEPTION, ThreadPoolExecutor, wait
        from threading import Event

        from dreadnode.core.util import valid_key

        org_key = self.organization
        if not org_key:
            raise RuntimeError("Organization is required")
        if not valid_key(org_key):
            raise RuntimeError(
                f'Invalid Organization Key: "{org_key}". '
                "The expected characters are lowercase letters, numbers, and hyphens (-)."
            )

        ws_key = self.workspace
        if ws_key and not valid_key(ws_key):
            raise RuntimeError(
                f'Invalid Workspace Key: "{ws_key}". '
                "The expected characters are lowercase letters, numbers, and hyphens (-)."
            )

        proj_key = self.project
        if proj_key and not valid_key(proj_key):
            raise RuntimeError(
                f'Invalid Project Key: "{proj_key}". '
                "The expected characters are lowercase letters, numbers, and hyphens (-)."
            )

        deadline = time.monotonic() + _SCOPE_RETRY_BUDGET_SEC
        stopped = Event()

        def read(call: t.Callable[[float], _ScopeResult]) -> _ScopeResult:
            delay = _SCOPE_RETRY_INITIAL_DELAY
            while not stopped.is_set():
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    break
                try:
                    return call(min(_SCOPE_CALL_TIMEOUT_SEC, remaining))
                except Exception as exc:
                    if not _is_transient_network_error(exc):
                        raise
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        raise TimeoutError("Scope validation deadline exceeded") from exc
                    sleep_for = min(delay * (0.5 + random.random()), remaining)
                    logging.getLogger("dreadnode").warning(
                        "Scope read failed (%s: %s), retrying in %.2fs",
                        type(exc).__name__,
                        exc,
                        sleep_for,
                    )
                    # Wake retry sleepers promptly if another read fails.
                    stopped.wait(sleep_for)
                    delay = min(delay * 2, _SCOPE_RETRY_MAX_DELAY)
            raise TimeoutError("Scope validation deadline exceeded")

        def wait_for_reads(*futures: "Future[t.Any]") -> None:
            done, pending = wait(
                futures,
                timeout=max(0.0, deadline - time.monotonic()),
                return_when=FIRST_EXCEPTION,
            )
            for future in done:
                future.result()  # Propagate terminal errors before reporting a deadline.
            if pending or time.monotonic() >= deadline:
                raise TimeoutError("Scope validation deadline exceeded")

        def get_organization(timeout: float) -> "Organization":
            organization = api.get_organization(org_key, timeout=timeout)
            if not organization:
                raise RuntimeError(f"Organization '{org_key}' not found.")
            return organization

        def get_workspace(timeout: float) -> "Workspace":
            if ws_key:
                workspace = api.get_workspace(org_key, ws_key, timeout=timeout)
                if not workspace:
                    raise RuntimeError(
                        f"Workspace '{ws_key}' not found in organization '{org_key}'."
                    )
                return workspace
            workspaces = api.list_workspaces(org_key, timeout=timeout)
            if not workspaces:
                raise RuntimeError(
                    f"No workspaces found in organization '{org_key}'. "
                    "Create a workspace first or specify one explicitly."
                )
            return next((w for w in workspaces if w.is_default), workspaces[0])

        def get_project(workspace_key: str, project_key: str, timeout: float) -> "Project | None":
            try:
                project = api.get_project(org_key, workspace_key, project_key, timeout=timeout)
            except RuntimeError as exc:
                if "404" not in str(exc):
                    raise
                return None  # An absent project is resolved by the caller's creation flow.
            if not project:
                raise RuntimeError(
                    f"Project '{project_key}' not found in workspace '{workspace_key}' "
                    f"of organization '{org_key}'."
                )
            return project

        pool = ThreadPoolExecutor(max_workers=4, thread_name_prefix="dn-scope")
        try:
            org_future = pool.submit(lambda: read(get_organization))
            user_future = pool.submit(lambda: read(lambda timeout: api.get_user(timeout=timeout)))
            workspace_future = pool.submit(lambda: read(get_workspace))
            project_future = (
                pool.submit(lambda: read(lambda timeout: get_project(ws_key, proj_key, timeout)))
                if ws_key and proj_key
                else None
            )
            initial_reads = [org_future, user_future, workspace_future]
            if project_future is not None:
                initial_reads.append(project_future)
            wait_for_reads(*initial_reads)
            workspace = workspace_future.result()
            if proj_key and project_future is None:
                project_future = pool.submit(
                    lambda: read(lambda timeout: get_project(workspace.key, proj_key, timeout))
                )
                wait_for_reads(project_future)

            # Worker threads never mutate the profile, including after a timeout.
            if not ws_key:
                self._workspace = workspace.key
            if project_future is not None:
                project = project_future.result()
                self._project_id = str(project.id) if project else None
                if project is None:
                    self._project = None
            self._user = user_future.result()
        finally:
            stopped.set()
            # Running synchronous HTTP requests cannot be cancelled. They retain
            # their transport timeouts, but cannot retry or change profile state.
            pool.shutdown(wait=False, cancel_futures=True)

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
