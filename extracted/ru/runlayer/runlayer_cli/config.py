"""Configuration management for Runlayer CLI.

This module handles loading and saving CLI configuration to ~/.runlayer/config.yaml.
New logins store user secrets in the system credential store via credential_store.py.
Existing secrets in config.yaml continue to work as fallback.

Config structure:
    default_host: https://app.runlayer.com
    hosts:
      app.runlayer.com:
        url: https://app.runlayer.com
        org_api_keys:
          mcp-watch: rl_org_aaa
          security-scan: rl_org_bbb
      localhost:8000:
        url: http://localhost:8000
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, TypedDict
from urllib.parse import urlparse

import typer
import yaml

from runlayer_cli.credential_store import get_keyring_store
from runlayer_cli.mdm_config import read_managed_config
from runlayer_cli.paths import get_runlayer_dir
from runlayer_cli.runtime import is_aiwatch_runtime

AI_WATCH_MDM_ORG_KEY_LABEL = "ai_watch_mdm"


class HostConfig(TypedDict, total=False):
    """Configuration for a single host."""

    url: str
    secret: str
    org_api_keys: dict[str, str]


class ConfigData(TypedDict, total=False):
    """Configuration data structure."""

    default_host: str
    hosts: dict[str, HostConfig]


def url_to_host_key(url: str) -> str:
    """Convert URL to config key (hostname:port or just hostname).

    Args:
        url: Full URL including scheme (e.g., https://app.runlayer.com)

    Returns:
        Config key in format hostname or hostname:port
        Port is omitted if it's the default for the scheme (80 for http, 443 for https)
    """
    parsed = urlparse(url)
    host = parsed.hostname or ""
    port = parsed.port

    # Omit port if it's the default for the scheme
    if port and not (
        (parsed.scheme == "https" and port == 443)
        or (parsed.scheme == "http" and port == 80)
    ):
        return f"{host}:{port}"
    return host


def normalize_url(url: str) -> str:
    """Normalize a URL by stripping trailing slashes.

    Args:
        url: URL to normalize

    Returns:
        URL with trailing slashes removed
    """
    return url.rstrip("/")


@dataclass
class Config:
    """CLI configuration with per-host credentials."""

    default_host: Optional[str] = None
    hosts: dict[str, HostConfig] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: ConfigData) -> "Config":
        """Create Config from dictionary."""
        return cls(
            default_host=data.get("default_host"),
            hosts=data.get("hosts", {}),
        )

    def to_dict(self) -> ConfigData:
        """Convert to dictionary for serialization.

        Preserves whatever is in the hosts dict. Secrets appear when stored in
        the file (fallback, failed keyring write, or legacy entries never moved
        by re-login). New logins that use the keyring omit ``secret`` from the
        host entry via ``set_host_credentials``; we do not auto-strip legacy
        plaintext secrets on load.
        """
        result: ConfigData = {}
        if self.default_host:
            result["default_host"] = self.default_host
        if self.hosts:
            result["hosts"] = self.hosts
        return result

    def get_secret_for_host(self, url: str) -> Optional[str]:
        """Get the secret for a specific host URL.

        Checks keyring first, falls back to config file for unmigrated secrets.

        Args:
            url: Full URL including scheme (e.g., https://app.runlayer.com)

        Returns:
            The secret if found and URL matches exactly, None otherwise
        """
        host_config = self._get_host_config(url)
        if not host_config:
            return None
        key = url_to_host_key(normalize_url(url))
        keyring_store = get_keyring_store()
        if keyring_store is not None:
            secret = keyring_store.get_secret(key)
            if secret:
                return secret
        return host_config.get("secret")

    def _get_host_config(self, url: str) -> Optional[HostConfig]:
        """Get host config entry after URL validation."""
        url = normalize_url(url)
        key = url_to_host_key(url)
        host_config = self.hosts.get(key)
        if not host_config:
            return None
        stored_url = normalize_url(host_config.get("url", ""))
        if stored_url != url:
            return None
        return host_config

    def get_org_api_key(self, url: str, name: str) -> Optional[str]:
        """Get a named org API key for a host."""
        host_config = self._get_host_config(url)
        if not host_config:
            return None
        return host_config.get("org_api_keys", {}).get(name)

    def set_org_api_key(self, url: str, name: str, secret: str) -> None:
        """Store a named org API key for a host. Creates host entry if needed."""
        url = normalize_url(url)
        key = url_to_host_key(url)
        host_config = self._get_host_config(url)
        if not host_config:
            if key in self.hosts:
                stored = normalize_url(self.hosts[key].get("url", ""))
                raise ValueError(
                    f"Host scheme mismatch: config has '{stored}' but got '{url}'. "
                    "Use the same scheme as the stored host."
                )
            host_config = HostConfig(url=url)
            self.hosts[key] = host_config
        org_keys = host_config.get("org_api_keys")
        if org_keys is None:
            org_keys = {}
            host_config["org_api_keys"] = org_keys
        org_keys[name] = secret

    def remove_org_api_key(self, url: str, name: str) -> bool:
        """Remove a named org API key. Returns True if found and removed."""
        host_config = self._get_host_config(url)
        if not host_config:
            return False
        org_keys = host_config.get("org_api_keys", {})
        if name not in org_keys:
            return False
        del org_keys[name]
        if not org_keys:
            host_config.pop("org_api_keys", None)
        return True

    def list_org_api_keys(self, url: str) -> dict[str, str]:
        """List org API key names and prefixes for a host."""
        host_config = self._get_host_config(url)
        if not host_config:
            return {}
        org_keys = host_config.get("org_api_keys", {})
        return {name: secret[:12] + "..." for name, secret in org_keys.items()}

    def set_host_credentials(self, url: str, secret: str) -> bool:
        """Set credentials for a specific host.

        Stores the secret in the credential store when available, else in the config file.
        Also updates default_host to this URL. Preserves existing org_api_keys.

        Args:
            url: Full URL including scheme
            secret: API secret/key for this host

        Returns:
            True if secret was stored in the credential store, False if fell back to config file
        """
        url = normalize_url(url)
        key = url_to_host_key(url)

        keyring_store = get_keyring_store()
        stored = False
        if keyring_store is not None:
            stored = keyring_store.set_secret(key, secret)
            if not stored:
                # Remove stale keyring entry so it cannot shadow the config-file secret
                keyring_store.delete_secret(key)

        existing = self.hosts.get(key, {})
        new_config = HostConfig(url=url)
        if not stored:
            new_config["secret"] = secret
        # Preserve org_api_keys if they exist
        existing_org_keys = existing.get("org_api_keys")
        if existing_org_keys:
            new_config["org_api_keys"] = existing_org_keys
        self.hosts[key] = new_config
        self.default_host = url
        return stored

    def clear_host(self, url: str) -> bool:
        """Remove a host's in-memory config entry (scheme-validated).

        This is the delete-side counterpart of ``set_host_credentials``'s
        in-memory mutation. It does NOT touch the keychain or write the YAML —
        that orchestration lives in :func:`clear_host_credentials`, which owns
        the "credential actually cleared" semantics (mirroring how
        ``persist_credentials`` owns "credential actually persisted").

        Args:
            url: Full URL including scheme

        Returns:
            True if a matching host entry was found and removed, False otherwise
            (unknown host, or stored scheme mismatch).
        """
        url = normalize_url(url)
        key = url_to_host_key(url)

        host_config = self.hosts.get(key)
        if not host_config:
            return False

        # Verify the stored URL matches exactly (scheme matters!)
        stored_url = normalize_url(host_config.get("url", ""))
        if stored_url != url:
            return False

        del self.hosts[key]
        # If this was the default host, clear it
        if self.default_host and normalize_url(self.default_host) == url:
            self.default_host = None
        return True

    # Backwards compatibility properties
    @property
    def host(self) -> Optional[str]:
        """Get the default host URL."""
        return self.default_host

    @property
    def secret(self) -> Optional[str]:
        """Get the secret for the default host."""
        if not self.default_host:
            return None
        return self.get_secret_for_host(self.default_host)


def get_config_path() -> Path:
    """Get the path to the config file.

    Returns:
        Path to ~/.runlayer/config.yaml
    """
    return get_runlayer_dir() / "config.yaml"


def _aiwatch_synthesized_config() -> Config:
    """Build a Config from MDM-managed host only, never touching the YAML file.

    The aiwatch binary must resolve host from MDM and secrets from the keychain.
    Returning a bare ``Config()`` would disable the keychain too, because
    ``get_secret_for_host`` only consults the keyring when a matching host entry
    exists (``_get_host_config`` guard). So seed one host entry (url only, no
    secret): the keychain stays live while ``config.yaml`` is never read.
    """
    managed_host = read_managed_config().get("host")
    if not managed_host:
        return Config()
    url = normalize_url(managed_host)
    return Config(default_host=url, hosts={url_to_host_key(url): HostConfig(url=url)})


def load_config() -> Config:
    """Load configuration from the config file.

    Returns:
        Config object with loaded values, or empty Config if file doesn't exist
    """
    if is_aiwatch_runtime():
        return _aiwatch_synthesized_config()

    config_path = get_config_path()

    if not config_path.exists():
        return Config()

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if data is None:
                return Config()
            return Config.from_dict(data)
    except (yaml.YAMLError, OSError) as e:
        typer.secho(
            f"Warning: Could not parse config file at {config_path}: {e}. "
            "Using default configuration.",
            fg=typer.colors.YELLOW,
            err=True,
        )
        return Config()


def save_config(config: Config) -> bool:
    """Save configuration to the config file.

    Creates the config directory if it doesn't exist.
    Sets file permissions to 0600 (user read/write only) for security.

    This is a dumb "did I write the file?" predicate: ``True`` when the YAML was
    written, ``False`` for the aiwatch no-op (aiwatch runtime never writes
    ``config.yaml``). Credential-writing callers should not interpret this bool
    themselves — go through :func:`persist_credentials`, which composes it with
    the keychain write and owns the "credential actually persisted" semantics.

    Args:
        config: Config object to save

    Returns:
        True if the config was persisted to disk, False if this was a no-op.
    """
    if is_aiwatch_runtime():
        # aiwatch never persists to config.yaml; secrets live in the keychain.
        return False

    config_path = get_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)

    with open(config_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(config.to_dict(), f, default_flow_style=False)

    try:
        os.chmod(config_path, 0o600)
    except OSError:
        pass
    return True


class CredentialPersistence(TypedDict):
    """Outcome of persisting a host credential via ``persist_credentials``."""

    persisted: bool
    keyring_used: bool


def persist_credentials(
    config: Config, host: str, api_key: str
) -> CredentialPersistence:
    """Store *api_key* for *host* in the keychain (when available) then save config.

    Collapses the two-step keychain + ``save_config`` write into one call so
    no credential-writing caller interprets ``save_config``'s aiwatch no-op
    return directly. The aiwatch semantics of ``save_config`` stop here. A
    read-only filesystem can raise ``OSError`` from the file write; that's
    treated as "not persisted to file" rather than crashing the caller (the hook
    lazy-enrollment path fires on hosts where the config dir may be unwritable).

    Returns:
        ``persisted`` is True when the credential landed somewhere durable
        (keychain or config file); False means it only lives in the in-memory
        ``Config`` and is lost on exit — the keychain write failed and
        ``config.yaml`` is not written in the aiwatch runtime. ``keyring_used``
        reports whether the keychain accepted the write (drives the
        destination message callers print).
    """
    keyring_used = config.set_host_credentials(host, api_key)
    try:
        file_saved = save_config(config)
    except OSError:
        file_saved = False
    return {"persisted": keyring_used or file_saved, "keyring_used": keyring_used}


class CredentialClearance(TypedDict):
    """Outcome of clearing a host credential via ``clear_host_credentials``."""

    found: bool
    cleared: bool


def clear_host_credentials(config: Config, host: str) -> CredentialClearance:
    """Delete *host*'s credential from the keychain (when available) then save config.

    Delete-side mirror of :func:`persist_credentials`. Collapses the keychain
    delete + ``save_config`` rewrite into one call so no logout caller interprets
    ``save_config``'s aiwatch no-op return directly.

    Returns:
        ``found`` is True when a matching host entry existed (scheme-validated)
        and was removed from the in-memory ``Config``. ``cleared`` is True when
        the credential is durably gone — the keychain delete succeeded OR the
        YAML was rewritten without it. ``cleared`` is False when the keychain
        delete failed AND ``config.yaml`` is not written in this runtime
        (aiwatch): the secret may survive, so the caller must not claim success.
    """
    host = normalize_url(host)
    key = url_to_host_key(host)

    found = config.clear_host(host)
    if not found:
        return {"found": False, "cleared": False}

    keyring_store = get_keyring_store()
    keychain_deleted = True
    if keyring_store is not None:
        keychain_deleted = keyring_store.delete_secret(key)

    try:
        file_saved = save_config(config)
    except OSError:
        file_saved = False

    return {"found": True, "cleared": keychain_deleted or file_saved}


def clear_config() -> None:
    """Clear the configuration file.

    Removes the config file if it exists.
    """
    if is_aiwatch_runtime():
        # aiwatch must not touch the shared config.yaml (read or write/delete).
        return

    config_path = get_config_path()

    if config_path.exists():
        config_path.unlink()


def resolve_host(
    ctx: typer.Context,
    host: Optional[str],
    default_host: Optional[str] = None,
) -> str:
    """Resolve effective host from flag, context chain, or caller-provided default.

    Args:
        ctx: Typer context — walked upward to find a ``host`` in obj.
        host: Explicit ``--host`` value (highest priority).
        default_host: Fallback when neither *host* nor context contain one.
            Callers typically pass ``config.default_host``.
    """
    if not host:
        current = ctx.parent
        while current:
            if current.obj and current.obj.get("host"):
                host = current.obj["host"]
                break
            current = current.parent

    effective = host or default_host
    if not effective:
        typer.secho(
            "Error: No host configured. "
            "Please provide --host or run 'runlayer login --host <url>' first.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(1)
    return normalize_url(effective)


class ResolvedCredentials(TypedDict):
    """Resolved credentials for API authentication."""

    secret: str
    host: str


def set_credentials_in_context(
    ctx: typer.Context,
    secret: Optional[str],
    host: Optional[str],
    org_api_key_name: Optional[str] = None,
) -> None:
    """Store CLI-provided credentials in typer context for resolve_credentials.

    This exists for backwards compatibility: commands previously required --secret
    and --host as direct options. Now they can also be provided via global options
    or config file, but we still accept them at the command level.

    Args:
        ctx: Typer context to store credentials in
        secret: API secret from command-level --secret option
        host: Host URL from command-level --host option
        org_api_key_name: Named org API key to look up from config
    """
    ctx.ensure_object(dict)
    if secret:
        ctx.obj["secret"] = secret
    if host:
        ctx.obj["host"] = host
    if org_api_key_name:
        ctx.obj["org_api_key_name"] = org_api_key_name


def _get_mdm_managed_org_api_key(effective_host: str) -> Optional[str]:
    """Return the org API key from MDM-managed config if it matches *effective_host*.

    Requires the managed config to declare a host that matches ``effective_host``.
    Without a managed host we cannot prove the key is intended for this tenant,
    so we refuse to release it (would leak the secret to a user-supplied --host).
    """
    managed = read_managed_config()
    org_api_key = managed.get("org_api_key")
    if not org_api_key:
        return None
    managed_host = managed.get("host")
    if not managed_host or normalize_url(managed_host) != effective_host:
        return None
    return org_api_key


def _get_mdm_managed_host() -> Optional[str]:
    """Return the host from MDM-managed config, normalized, if present."""
    managed_host = read_managed_config().get("host")
    if not managed_host:
        return None
    return normalize_url(managed_host)


def resolve_credentials(
    ctx: typer.Context,
    require_auth: bool = True,
    allow_org_key: bool = False,
    implicit_org_key_label: Optional[str] = None,
    interactive_login_on_missing: bool = True,
) -> ResolvedCredentials:
    """Resolve credentials from CLI args, config file, or trigger login flow.

    Resolution order:
    1. CLI args (from ctx.obj, set by global --secret/--host options)
    2. Explicit --org-api-key name from ctx.obj
    3. If ``implicit_org_key_label`` is set, try that named org key before the
       user secret (used by ``scan`` to prefer the MDM org key).
    4. Config file user secret (~/.runlayer/config.yaml)

    When ``interactive_login_on_missing`` is False and no secret is found,
    exits with an error instead of starting the interactive login flow.

    Args:
        ctx: Typer context containing CLI args in ctx.obj
        require_auth: If True, trigger login when credentials are missing
        allow_org_key: If True, accept rl_org_ keys without triggering login
        implicit_org_key_label: Try this named org key before the user secret
        interactive_login_on_missing: If False, never start interactive login

    Returns:
        Dict with 'secret' and 'host' keys

    Raises:
        typer.Exit: If host is not provided via CLI or config file
        typer.Exit: If require_auth=True and authentication fails or is cancelled
    """
    cli_secret: Optional[str] = None
    cli_host: Optional[str] = None
    cli_org_api_key_name: Optional[str] = None

    # Walk up context chain for nested subcommands (main -> deploy -> validate)
    current_ctx = ctx
    while current_ctx:
        if current_ctx.obj:
            if cli_secret is None:
                cli_secret = current_ctx.obj.get("secret")
            if cli_host is None:
                cli_host = current_ctx.obj.get("host")
            if cli_org_api_key_name is None:
                cli_org_api_key_name = current_ctx.obj.get("org_api_key_name")
        current_ctx = current_ctx.parent

    config = load_config()

    # Determine effective host
    effective_host = cli_host or config.default_host
    if not effective_host and len(config.hosts) == 1:
        only_host = next(iter(config.hosts.values()))
        effective_host = only_host.get("url")
    # MDM-deployed devices may have an empty config.yaml; fall back to the
    # host pushed via managed plist/registry so scan can authenticate without
    # any prior `runlayer login` run.
    if not effective_host:
        effective_host = _get_mdm_managed_host()
    if not effective_host:
        typer.secho(
            "Error: No host configured. "
            "Please provide --host or run 'runlayer login --host <url>' first.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(1)

    effective_host = normalize_url(effective_host)

    # Determine effective secret
    # Priority: CLI secret > named org key > config secret for this host
    if cli_secret:
        effective_secret = cli_secret
    elif cli_org_api_key_name:
        effective_secret = config.get_org_api_key(effective_host, cli_org_api_key_name)
        if not effective_secret and cli_org_api_key_name == AI_WATCH_MDM_ORG_KEY_LABEL:
            effective_secret = _get_mdm_managed_org_api_key(effective_host)
        if not effective_secret:
            typer.secho(
                f"Error: Org API key '{cli_org_api_key_name}' not found for {effective_host}. "
                "Run 'runlayer org-api-key list' to see available keys.",
                fg=typer.colors.RED,
                err=True,
            )
            raise typer.Exit(1)
    else:
        effective_secret = None
        if implicit_org_key_label:
            effective_secret = config.get_org_api_key(
                effective_host, implicit_org_key_label
            )
        if (
            not effective_secret
            and implicit_org_key_label == AI_WATCH_MDM_ORG_KEY_LABEL
        ):
            effective_secret = _get_mdm_managed_org_api_key(effective_host)
        if not effective_secret:
            effective_secret = config.get_secret_for_host(effective_host)

    # Org API keys (rl_org_) can't fetch servers — trigger login to get a user key
    if (
        effective_secret
        and effective_secret.startswith("rl_org_")
        and require_auth
        and not allow_org_key
        and not cli_secret
        and not cli_org_api_key_name
    ):
        if not interactive_login_on_missing:
            typer.secho(
                "Error: Only an organization API key is available but a user key is required. "
                "Run 'runlayer login' to obtain a user API key.",
                fg=typer.colors.RED,
                err=True,
            )
            raise typer.Exit(1)

        typer.secho(
            "Organization API key detected. Starting login to obtain a user API key...",
            fg=typer.colors.YELLOW,
            err=True,
        )

        from runlayer_cli.commands.auth import login  # avoid circular import

        login(host=effective_host)

        config = load_config()
        effective_secret = config.get_secret_for_host(effective_host)

    if effective_secret:
        return {"secret": effective_secret, "host": effective_host}

    if not require_auth:
        return {"secret": "", "host": effective_host}

    if not interactive_login_on_missing:
        typer.secho(
            "Error: No credentials found. "
            "Run 'runlayer login' or provide --secret to authenticate.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(1)

    typer.secho(
        "No credentials found for this host. Starting login flow...",
        fg=typer.colors.YELLOW,
        err=True,
    )

    from runlayer_cli.commands.auth import login  # avoid circular import

    login(host=effective_host)

    config = load_config()

    # After login, get the secret for this host
    secret_after_login = config.get_secret_for_host(effective_host)
    if not secret_after_login:
        typer.secho(
            "Error: Authentication failed. Please try again with 'runlayer login'.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(1)

    return {"secret": secret_after_login, "host": effective_host}
