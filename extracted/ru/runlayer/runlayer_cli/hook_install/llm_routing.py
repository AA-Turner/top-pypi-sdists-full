"""Managed LLM routing writers: secret-free configs plus credential file."""

from __future__ import annotations

import enum
import errno
import hashlib
import ipaddress
import json
import platform
from collections.abc import Mapping
from datetime import datetime
from pathlib import Path
from typing import Any, Protocol, TypedDict, cast
from urllib.parse import urlsplit

from runlayer_cli.aiwatch_credential import (
    CLIENT_REFRESH_INTERVAL_SECONDS,
    CREDENTIAL_RELATIVE_PATH,
    MAX_CREDENTIAL_BYTES,
    is_single_token,
    token_cache_path,
)
from runlayer_cli.hook_install.clients import (
    _codex_features_toml_file,
    _reown_to_console_user,
    _write_config,
)
from runlayer_cli.hook_install.paths import (
    HelperCommand,
    InstallScope,
    codex_helper_args,
    enterprise_claude_code_managed_dir,
    render_claude_helper_command,
    resolve_credential_helper,
    user_claude_code_dir,
)
from runlayer_cli.hook_install.safe_fs import (
    FileReadResult,
    console_home_anchor,
    is_unsafe_windows_mdm_path,
    maybe_safe_read_file,
    maybe_safe_unlink,
    path_has_link_or_reparse_point,
)
from runlayer_cli.tolerant_json import loads as tolerant_json_loads


class RouteResult(str, enum.Enum):
    WRITTEN = "written"
    UNCHANGED = "unchanged"
    DRIFTED = "drifted"
    FAILED = "failed"


CLAUDE_CODE_CLIENT = "claude_code"
CODEX_CLIENT = "codex"
CREDENTIAL_CLIENT = "credential"


class _PreparedWrite(TypedDict):
    path: Path
    previous: str | None
    rendered: str | None
    mode: int
    home: Path | None
    mdm: bool
    result: RouteResult


class _ExistingFile(TypedDict):
    content: str | None
    mode: int
    home: Path | None


_CLAUDE_ENV_KEYS = (
    "ANTHROPIC_BASE_URL",
    "CLAUDE_CODE_API_KEY_HELPER_TTL_MS",
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_API_KEY",
    "CLAUDE_CODE_OAUTH_TOKEN",
    "CLAUDE_CODE_USE_BEDROCK",
    "CLAUDE_CODE_USE_VERTEX",
    "CLAUDE_CODE_USE_FOUNDRY",
)
_CLAUDE_HELPER_KEY = "apiKeyHelper"
_CLAUDE_HELPER_TTL_MS = str(CLIENT_REFRESH_INTERVAL_SECONDS * 1000)
_CODEX_PROVIDER_TABLE = "[model_providers.runlayer]"
_CODEX_AUTH_TABLE = "[model_providers.runlayer.auth]"
_CODEX_AUTH_TIMEOUT_MS = 5000
_CODEX_AUTH_REFRESH_MS = CLIENT_REFRESH_INTERVAL_SECONDS * 1000
# Codex accepts one credential slot per provider. Stale slots conflict with auth.
_CODEX_FORBIDDEN_PROVIDER_KEYS = (
    "experimental_bearer_token",
    "env_key",
    "requires_openai_auth",
)


class _CredentialTarget(TypedDict):
    path: Path
    # Link-safe anchor for root ops inside the console home; None when the
    # running user owns the path (USER scope) or on Windows (preflight instead).
    home: Path | None


def _credential_target(scope: InstallScope) -> _CredentialTarget:
    """Resolve the credential path and its trusted anchor from one home lookup.

    Raises OSError when MDM scope resolves no console user: root must never
    manage a per-user secret against its own home. Resolving the anchor
    separately from the path would let a console-user switch between the two
    lookups downgrade a root write to plain, link-following filesystem ops.
    """
    if scope != InstallScope.MDM:
        return {"path": Path.home() / CREDENTIAL_RELATIVE_PATH, "home": None}
    # Deferred: console_user imports safe_fs/credential_gate (import cycle).
    from runlayer_cli.hook_install.console_user import (  # noqa: PLC0415
        find_console_user_home,
    )

    home = find_console_user_home()
    if home is None:
        raise OSError(errno.ENOENT, "no console user home for the routing credential")
    anchor = None if platform.system() == "Windows" else home
    return {"path": home / CREDENTIAL_RELATIVE_PATH, "home": anchor}


def credential_file(scope: InstallScope) -> Path:
    """Path of the exchange credential this scope manages."""
    return _credential_target(scope)["path"]


def _read_credential_file(target: _CredentialTarget, *, mdm: bool) -> _ExistingFile:
    path = target["path"]
    if path.is_symlink():
        raise OSError(
            errno.ELOOP,
            "credential file must not be a symlink",
            path,
        )
    # Bounded read, not a size pre-check: a file grown between lstat and read
    # would still be pulled into memory as root.
    existing_file = _read_existing_bytes(
        path, mdm=mdm, home=target["home"], max_bytes=MAX_CREDENTIAL_BYTES
    )
    if existing_file is None:
        return {"content": None, "mode": 0o644, "home": target["home"]}
    content: str | None
    try:
        content = existing_file["data"].decode("utf-8")
    except UnicodeDecodeError:
        content = None
    if len(existing_file["data"]) > MAX_CREDENTIAL_BYTES:
        content = None
    # Oversized or undecodable is malformed: the helper cannot use it either,
    # so the re-mint overwrites it instead of erroring every hour.
    return {"content": content, "mode": existing_file["mode"], "home": target["home"]}


def current_key(*, scope: InstallScope) -> str | None:
    """Return the exchange credential held in the credential file, if valid."""
    existing = _read_credential_file(
        _credential_target(scope),
        mdm=scope == InstallScope.MDM,
    )
    content = existing["content"]
    if content is None:
        return None
    key = content.strip()
    return key if is_single_token(key) else None


def store_credential(key: str, *, scope: InstallScope) -> RouteResult:
    """Persist one private exchange credential without creating a backup."""
    if not is_single_token(key):
        raise ValueError("credential must be one non-empty token")

    target = _credential_target(scope)
    path = target["path"]
    mdm = scope == InstallScope.MDM
    existing = _read_credential_file(target, mdm=mdm)
    desired = f"{key}\n"
    mode_drift = platform.system() != "Windows" and existing["mode"] != 0o600
    result = RouteResult.UNCHANGED
    if existing["content"] != desired or mode_drift:
        result = (
            RouteResult.WRITTEN if existing["content"] is None else RouteResult.DRIFTED
        )
        _write_config(
            path,
            desired,
            home=target["home"],
            mode=0o600,
            replace_symlink=False,
            mdm=mdm,
        )
    if mdm:
        # Every run, not only on write: a re-own that failed once (best-effort)
        # would otherwise leave a root-owned file the user's helper cannot read.
        _reown_to_console_user(path)
    return result


def _delete_credential(*, scope: InstallScope) -> None:
    target = _credential_target(scope)
    mdm = scope == InstallScope.MDM
    # Both removals run; an undeletable cache must not leave the credential behind.
    cache_error: OSError | None = None
    try:
        _delete_token_cache(target, mdm=mdm)
    except OSError as exc:
        cache_error = exc
    _delete_private_file(
        target["path"],
        home=target["home"],
        mdm=mdm,
        what="credential file",
    )
    if cache_error is not None:
        raise cache_error


def _delete_token_cache(target: _CredentialTarget, *, mdm: bool) -> None:
    _delete_private_file(
        token_cache_path(target["path"]),
        home=target["home"],
        mdm=mdm,
        what="token cache",
    )


def _delete_private_file(
    path: Path,
    *,
    home: Path | None,
    mdm: bool,
    what: str,
) -> None:
    if is_unsafe_windows_mdm_path(
        path,
        mdm=mdm,
        path_check=path_has_link_or_reparse_point,
    ):
        raise OSError(errno.ELOOP, "unsafe Windows MDM path", path)
    removed = maybe_safe_unlink(path, home=home)
    if not removed and (path.is_symlink() or path.exists()):
        raise OSError(errno.EIO, f"{what} could not be removed", path)


def device_key_hash(key: str) -> str:
    """SHA-256 hex of the plaintext device key; must match the backend's hashing."""
    return hashlib.sha256(key.encode()).hexdigest()


def route_detailed(
    base_url: str,
    *,
    scope: InstallScope,
) -> dict[str, RouteResult]:
    """Per-client route outcome keyed ``claude_code`` / ``codex``."""
    gateway_url = _validate_gateway_url(base_url, scope=scope)
    if gateway_url is None:
        return {
            CLAUDE_CODE_CLIENT: RouteResult.FAILED,
            CODEX_CLIENT: RouteResult.FAILED,
        }

    clients = (
        (CLAUDE_CODE_CLIENT, _prepare_claude_route),
        (CODEX_CLIENT, _prepare_codex_route),
    )
    prepared_writes: dict[str, _PreparedWrite] = {}
    results: dict[str, RouteResult] = {}
    for client, prepare in clients:
        try:
            prepared_writes[client] = prepare(gateway_url, scope=scope)
        except (OSError, ValueError):
            results[client] = RouteResult.FAILED

    if results:
        # Fail closed: one unsafe client path aborts every pending write. A
        # client that needed no write still converged, so it stays UNCHANGED.
        for client, prepared in prepared_writes.items():
            results[client] = (
                RouteResult.UNCHANGED
                if prepared["result"] is RouteResult.UNCHANGED
                else RouteResult.FAILED
            )
        return {client: results[client] for client, _prepare in clients}

    for client, prepared in prepared_writes.items():
        try:
            _apply_prepared_write(prepared)
        except (OSError, ValueError):
            results[client] = RouteResult.FAILED
        else:
            results[client] = prepared["result"]
    return results


class RoutingOutcome(TypedDict):
    status: str
    error_message: str | None
    # Hash of the credential this device holds on disk after the step.
    # The status check-in presents it so the backend keeps that key active
    # instead of revoke-then-minting behind a partially written client.
    key_hash: str | None
    wrote: bool
    # Nothing changed and the fetch check-in already reported the truth, so the
    # caller can skip the status check-in (steady state = one check-in).
    steady: bool


class FetchDecision(Protocol):
    """Sends the fetch check-in with the on-disk key hash; returns the backend body."""

    def __call__(
        self, key_hash: str | None, *, rotate: bool
    ) -> Mapping[str, object] | None: ...


def _unroute_outcome(*, scope: InstallScope) -> RoutingOutcome:
    try:
        unroute(scope=scope)
    except (OSError, ValueError) as exc:
        return {
            "status": "error",
            "error_message": f"unroute failed: {exc}",
            "key_hash": None,
            "wrote": False,
            "steady": False,
        }
    return {
        "status": "disabled",
        "error_message": None,
        "key_hash": None,
        "wrote": False,
        "steady": False,
    }


def _route_outcome(
    base_url: str,
    key: str,
    *,
    scope: InstallScope,
    minted: bool,
) -> RoutingOutcome:
    try:
        credential_result = store_credential(key, scope=scope)
    except (OSError, ValueError) as exc:
        return {
            "status": "error",
            "error_message": f"credential: {exc}",
            "key_hash": None,
            "wrote": False,
            "steady": False,
        }
    client_results = route_detailed(base_url, scope=scope)
    results = {CREDENTIAL_CLIENT: credential_result, **client_results}
    values = set(results.values())
    status_values = set(client_results.values()) | (
        {credential_result} if not minted else set()
    )
    mixed = {RouteResult.WRITTEN, RouteResult.UNCHANGED}.issubset(status_values)
    if RouteResult.FAILED in values:
        status = "error"
    elif RouteResult.DRIFTED in status_values or mixed:
        status = "drifted"
    else:
        status = "ok"
    error_message = None
    if status != "ok":
        error_message = "; ".join(
            f"{name}: {result.value}" for name, result in results.items()
        )
    return {
        "status": status,
        "error_message": error_message,
        "key_hash": device_key_hash(key),
        "wrote": bool(values & {RouteResult.WRITTEN, RouteResult.DRIFTED}),
        "steady": not minted and values == {RouteResult.UNCHANGED},
    }


def reconcile_routing(
    *,
    desired: bool,
    base_url: str,
    scope: InstallScope,
    fetch_decision: FetchDecision,
) -> RoutingOutcome | None:
    """Converge both clients on the backend's device-key decision.

    Routing off unroutes without contacting the backend. Otherwise the key on
    disk is hashed and sent via ``fetch_decision``; ``active`` routes with the
    minted key (or the existing one), anything else unroutes. Returns None when
    the fetch failed, leaving disk untouched: a base URL is never written
    without a credential in hand.
    A missing or malformed credential asks the backend to rotate because a
    hash-less steady state would otherwise leave the device keyless forever.
    """
    if not desired:
        return _unroute_outcome(scope=scope)

    try:
        current = current_key(scope=scope)
    except OSError as exc:
        return {
            "status": "error",
            "error_message": f"credential: {exc}",
            "key_hash": None,
            "wrote": False,
            "steady": False,
        }

    response = fetch_decision(
        device_key_hash(current) if current else None,
        rotate=current is None,
    )
    if response is None:
        return None

    if response.get("device_key_status") != "active":
        return _unroute_outcome(scope=scope)

    response_key = response.get("device_key")
    minted = response_key if isinstance(response_key, str) and response_key else None
    key = minted or current
    if key is None:
        return {
            "status": "error",
            "error_message": "backend reported active but no device key available",
            "key_hash": None,
            "wrote": False,
            "steady": False,
        }
    return _route_outcome(base_url, key, scope=scope, minted=minted is not None)


def route(base_url: str, *, scope: InstallScope) -> RouteResult:
    """Route Claude Code and Codex through the configured bare gateway host."""
    results = set(route_detailed(base_url, scope=scope).values())

    if RouteResult.FAILED in results:
        return RouteResult.FAILED
    if RouteResult.DRIFTED in results:
        return RouteResult.DRIFTED
    if RouteResult.WRITTEN in results:
        return RouteResult.WRITTEN
    return RouteResult.UNCHANGED


def _validate_gateway_url(
    base_url: object,
    *,
    scope: InstallScope,
) -> str | None:
    """Normalize an HTTPS host; USER loopback HTTP supports local gateways."""
    if not isinstance(base_url, str):
        return None

    candidate = base_url.strip()
    if (
        not candidate
        or any(character.isspace() for character in candidate)
        or "?" in candidate
        or "#" in candidate
    ):
        return None
    try:
        parsed = urlsplit(candidate)
        hostname = parsed.hostname
        port = parsed.port
    except ValueError:
        return None

    if (
        hostname is None
        or port == 0
        or parsed.username is not None
        or parsed.password is not None
        or parsed.path not in ("", "/")
        or parsed.netloc.endswith(":")
    ):
        return None

    secure = parsed.scheme.lower() == "https"
    local_http = (
        scope == InstallScope.USER
        and parsed.scheme.lower() == "http"
        and _is_loopback_host(hostname)
    )
    if not secure and not local_http:
        return None
    return candidate.rstrip("/")


def _is_loopback_host(hostname: str) -> bool:
    if hostname.rstrip(".").lower() == "localhost":
        return True
    try:
        return ipaddress.ip_address(hostname).is_loopback
    except ValueError:
        return False


def unroute(*, scope: InstallScope) -> None:
    """Remove Runlayer routing from both clients, then delete the token cache and the credential."""
    first_error: OSError | ValueError | None = None
    for prepare in (_prepare_claude_unroute, _prepare_codex_unroute):
        try:
            prepared = prepare(scope=scope)
            _apply_prepared_write(prepared)
        except (OSError, ValueError) as exc:
            if first_error is None:
                first_error = exc
    try:
        _delete_credential(scope=scope)
    except (OSError, ValueError) as exc:
        if first_error is None:
            first_error = exc
    if first_error is not None:
        raise first_error


def _claude_code_config_file(scope: InstallScope) -> Path:
    if scope == InstallScope.MDM:
        return enterprise_claude_code_managed_dir() / "managed-settings.json"
    return user_claude_code_dir() / "settings.json"


def _home_for_path(path: Path, *, mdm: bool) -> Path | None:
    anchor = console_home_anchor(path.parent, mdm=mdm)
    if anchor is None:
        return None
    try:
        path.relative_to(anchor)
    except ValueError:
        return None
    return anchor


def _read_existing(path: Path, *, mdm: bool) -> _ExistingFile:
    return _read_existing_at(path, mdm=mdm, home=_home_for_path(path, mdm=mdm))


def _read_existing_bytes(
    path: Path, *, mdm: bool, home: Path | None, max_bytes: int | None = None
) -> FileReadResult | None:
    """Guarded raw read shared by config and credential files; None when absent.

    Callers keep their own decode policy (a config must be UTF-8, a credential
    that is not is simply malformed).
    """
    if is_unsafe_windows_mdm_path(
        path,
        mdm=mdm,
        path_check=path_has_link_or_reparse_point,
    ):
        raise OSError(errno.ELOOP, "unsafe Windows MDM path", path)
    existing_file = maybe_safe_read_file(path, home=home, max_bytes=max_bytes)
    if existing_file is None and (path.exists() or path.is_symlink()):
        raise OSError(errno.EIO, "unreadable file", path)
    return existing_file


def _read_existing_at(path: Path, *, mdm: bool, home: Path | None) -> _ExistingFile:
    existing_file = _read_existing_bytes(path, mdm=mdm, home=home)
    if existing_file is None:
        return {"content": None, "mode": 0o644, "home": home}
    try:
        existing = existing_file["data"].decode("utf-8")
    except UnicodeDecodeError as exc:
        raise OSError(errno.EINVAL, "routing config must be UTF-8", path) from exc
    return {"content": existing, "mode": existing_file["mode"], "home": home}


def _user_mode_drift(scope: InstallScope, existing: _ExistingFile) -> bool:
    return (
        scope == InstallScope.USER
        and platform.system() != "Windows"
        and existing["mode"] != 0o600
    )


def _prepared_write(
    path: Path,
    previous: str | None,
    rendered: str | None,
    mode: int,
    home: Path | None,
    *,
    mdm: bool,
) -> _PreparedWrite:
    result = RouteResult.UNCHANGED
    if rendered is not None:
        result = RouteResult.WRITTEN if previous is None else RouteResult.DRIFTED
    # User configs stay private; MDM configs must stay readable by clients.
    return {
        "path": path,
        "previous": previous,
        "rendered": rendered,
        "mode": mode if mdm else 0o600,
        "home": home,
        "mdm": mdm,
        "result": result,
    }


def _apply_prepared_write(prepared: _PreparedWrite) -> None:
    rendered = prepared["rendered"]
    if rendered is None:
        return

    path = prepared["path"]
    previous = prepared["previous"]
    if previous is not None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        backup_path = path.with_name(f"{path.stem}.backup_{timestamp}{path.suffix}")
        if is_unsafe_windows_mdm_path(
            backup_path,
            mdm=prepared["mdm"],
            path_check=path_has_link_or_reparse_point,
        ):
            raise OSError(errno.ELOOP, "unsafe Windows MDM backup path", backup_path)
        _write_config(
            backup_path,
            previous,
            home=prepared["home"],
            mode=0o600,
            replace_symlink=False,
            mdm=prepared["mdm"],
        )
        if prepared["mdm"]:
            _reown_to_console_user(backup_path)

    _write_config(
        path,
        rendered,
        home=prepared["home"],
        mode=prepared["mode"],
        replace_symlink=not prepared["mdm"],
        mdm=prepared["mdm"],
    )
    if prepared["mdm"]:
        _reown_to_console_user(path)


def _parse_claude_settings(path: Path, content: str) -> dict[str, Any]:
    try:
        parsed = tolerant_json_loads(content)
    except (ValueError, OSError) as exc:
        raise OSError(
            errno.EINVAL, "invalid Claude Code managed settings", path
        ) from exc
    if not isinstance(parsed, dict):
        raise OSError(
            errno.EINVAL, "Claude Code managed settings must be an object", path
        )
    return cast(dict[str, Any], parsed)


def _prepare_claude_route(
    gateway_url: str,
    *,
    scope: InstallScope,
) -> _PreparedWrite:
    path = _claude_code_config_file(scope)
    mdm = scope == InstallScope.MDM
    existing = _read_existing(path, mdm=mdm)
    previous = existing["content"]
    settings = (
        {}
        if previous is None or not previous.strip()
        else _parse_claude_settings(path, previous)
    )
    existing_env = settings.get("env", {})
    if not isinstance(existing_env, dict):
        raise OSError(errno.EINVAL, "Claude Code managed env must be an object", path)

    helper = render_claude_helper_command(resolve_credential_helper(scope))
    desired_env = {
        "ANTHROPIC_BASE_URL": f"{gateway_url}/anthropic",
        "CLAUDE_CODE_API_KEY_HELPER_TTL_MS": _CLAUDE_HELPER_TTL_MS,
        "ANTHROPIC_AUTH_TOKEN": "",
        "ANTHROPIC_API_KEY": "",
        "CLAUDE_CODE_OAUTH_TOKEN": "",
        "CLAUDE_CODE_USE_BEDROCK": "",
        "CLAUDE_CODE_USE_VERTEX": "",
        "CLAUDE_CODE_USE_FOUNDRY": "",
    }
    matches = settings.get(_CLAUDE_HELPER_KEY) == helper and all(
        existing_env.get(name) == value for name, value in desired_env.items()
    )
    rendered: str | None = None
    if not matches:
        settings[_CLAUDE_HELPER_KEY] = helper
        existing_env.update(desired_env)
        settings["env"] = existing_env
        rendered = json.dumps(settings, indent=2) + "\n"
    elif _user_mode_drift(scope, existing):
        rendered = previous
    return _prepared_write(
        path,
        previous,
        rendered,
        existing["mode"],
        existing["home"],
        mdm=mdm,
    )


def _prepare_claude_unroute(*, scope: InstallScope) -> _PreparedWrite:
    path = _claude_code_config_file(scope)
    mdm = scope == InstallScope.MDM
    existing = _read_existing(path, mdm=mdm)
    previous = existing["content"]
    rendered: str | None = None
    if previous is not None and previous.strip():
        settings = _parse_claude_settings(path, previous)
        changed = False
        helper = settings.get(_CLAUDE_HELPER_KEY)
        if _is_runlayer_helper(helper):
            del settings[_CLAUDE_HELPER_KEY]
            changed = True
        existing_env = settings.get("env")
        if isinstance(existing_env, dict):
            for name in _CLAUDE_ENV_KEYS:
                if name in existing_env:
                    del existing_env[name]
                    changed = True
            settings["env"] = existing_env
        if changed:
            rendered = json.dumps(settings, indent=2) + "\n"
    return _prepared_write(
        path,
        previous,
        rendered,
        existing["mode"],
        existing["home"],
        mdm=mdm,
    )


def _is_runlayer_helper(value: object) -> bool:
    """``<aiwatch> credential claude`` in any of the forms this module writes."""
    if not isinstance(value, str):
        return False
    parts = value.split()
    if parts[-2:] != ["credential", "claude"]:
        return False
    head = parts[:-2]
    if head[-2:] == ["-m", "runlayer_cli.aiwatch"]:
        return True
    if not head:
        return False
    # Separator-agnostic: a quoted Windows path splits on its spaces too.
    name = head[-1].strip('"').replace("\\", "/").rsplit("/", 1)[-1].casefold()
    return name in {"aiwatch", "aiwatch.exe"}


def _is_table_header(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("[") and stripped.endswith("]")


def _assignment(line: str, key: str) -> str | None:
    stripped = line.strip()
    if stripped.startswith("#"):
        return None
    name, separator, value = stripped.partition("=")
    # TOML allows quoted bare keys; a stale slot spelled that way still counts.
    if separator and name.strip().strip("\"'") == key:
        return value.strip()
    return None


def _table_name(line: str) -> str:
    """Canonical header: TOML allows quoted segments and whitespace around dots."""
    segments: list[str] = []
    for raw in line.strip()[1:-1].split("."):
        segment = raw.strip()
        quoted = len(segment) >= 2 and segment[0] == segment[-1] and segment[0] in "\"'"
        segments.append(segment[1:-1] if quoted else segment)
    return "[" + ".".join(segments) + "]"


def _is_runlayer_table(line: str) -> bool:
    name = _table_name(line)
    return name == _CODEX_PROVIDER_TABLE or name.startswith(
        _CODEX_PROVIDER_TABLE[:-1] + "."
    )


def _codex_matches(
    content: str,
    provider: dict[str, str],
    auth: dict[str, str],
) -> bool:
    current_table: str | None = None
    before_first_table = True
    provider_sections = 0
    auth_sections = 0
    other_runlayer_sections = 0
    top_values: list[str] = []
    tracked_provider = (*provider, *_CODEX_FORBIDDEN_PROVIDER_KEYS)
    tracked_auth = (*auth, *_CODEX_FORBIDDEN_PROVIDER_KEYS)
    provider_values: dict[str, list[str]] = {name: [] for name in tracked_provider}
    auth_values: dict[str, list[str]] = {name: [] for name in tracked_auth}
    for line in content.splitlines():
        if _is_table_header(line):
            before_first_table = False
            name = _table_name(line)
            if name == _CODEX_PROVIDER_TABLE:
                current_table = "provider"
                provider_sections += 1
            elif name == _CODEX_AUTH_TABLE:
                current_table = "auth"
                auth_sections += 1
            elif _is_runlayer_table(line):
                current_table = "other_runlayer"
                other_runlayer_sections += 1
            else:
                current_table = None
            continue
        if before_first_table:
            value = _assignment(line, "model_provider")
            if value is not None:
                top_values.append(value)
        if current_table == "provider":
            for name in tracked_provider:
                value = _assignment(line, name)
                if value is not None:
                    provider_values[name].append(value)
        elif current_table == "auth":
            for name in tracked_auth:
                value = _assignment(line, name)
                if value is not None:
                    auth_values[name].append(value)

    return (
        provider_sections == 1
        and auth_sections == 1
        and other_runlayer_sections == 0
        and top_values == ['"runlayer"']
        and all(provider_values[name] == [value] for name, value in provider.items())
        and all(auth_values[name] == [value] for name, value in auth.items())
        and all(not provider_values[name] for name in _CODEX_FORBIDDEN_PROVIDER_KEYS)
        and all(not auth_values[name] for name in _CODEX_FORBIDDEN_PROVIDER_KEYS)
    )


def _without_runlayer_codex_config(
    content: str,
    *,
    remove_any_model_provider: bool = False,
) -> str:
    lines = content.splitlines()
    out: list[str] = []
    in_runlayer = False
    before_first_table = True
    for line in lines:
        if _is_table_header(line):
            in_runlayer = _is_runlayer_table(line)
            before_first_table = False
            if not in_runlayer:
                out.append(line)
            continue
        if in_runlayer:
            continue
        model_provider = _assignment(line, "model_provider")
        remove_model_provider = before_first_table and (
            model_provider == '"runlayer"'
            or (remove_any_model_provider and model_provider is not None)
        )
        if not remove_model_provider:
            out.append(line)
    rendered = "\n".join(out)
    if content.endswith("\n") and rendered:
        rendered += "\n"
    return rendered


def _toml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _toml_array(values: list[str]) -> str:
    return "[" + ", ".join(_toml_string(value) for value in values) + "]"


def _render_codex_route(
    content: str,
    provider: dict[str, str],
    auth: dict[str, str],
) -> str:
    foreign = _without_runlayer_codex_config(
        content,
        remove_any_model_provider=True,
    ).strip("\n")
    lines = ['model_provider = "runlayer"']
    if foreign:
        lines.extend(("", foreign))
    lines.extend(
        (
            "",
            _CODEX_PROVIDER_TABLE,
            *(f"{name} = {literal}" for name, literal in provider.items()),
            "",
            _CODEX_AUTH_TABLE,
            *(f"{name} = {literal}" for name, literal in auth.items()),
        )
    )
    return "\n".join(lines) + "\n"


def _prepare_codex_route(
    base_url: str,
    *,
    scope: InstallScope,
) -> _PreparedWrite:
    path = _codex_features_toml_file(scope)
    mdm = scope == InstallScope.MDM
    existing = _read_existing(path, mdm=mdm)
    previous = existing["content"]
    content = previous or ""
    helper: HelperCommand = resolve_credential_helper(scope)
    provider = {
        "name": _toml_string("Runlayer"),
        "base_url": _toml_string(f"{base_url}/openai/v1"),
        "wire_api": _toml_string("responses"),
    }
    auth = {
        "command": _toml_string(helper["executable"]),
        "args": _toml_array(codex_helper_args(helper)),
        "timeout_ms": str(_CODEX_AUTH_TIMEOUT_MS),
        "refresh_interval_ms": str(_CODEX_AUTH_REFRESH_MS),
    }
    rendered: str | None = None
    if not _codex_matches(content, provider, auth):
        rendered = _render_codex_route(content, provider, auth)
    elif _user_mode_drift(scope, existing):
        rendered = previous
    return _prepared_write(
        path,
        previous,
        rendered,
        existing["mode"],
        existing["home"],
        mdm=mdm,
    )


def _prepare_codex_unroute(*, scope: InstallScope) -> _PreparedWrite:
    path = _codex_features_toml_file(scope)
    mdm = scope == InstallScope.MDM
    existing = _read_existing(path, mdm=mdm)
    previous = existing["content"]
    rendered: str | None = None
    if previous is not None:
        without_routing = _without_runlayer_codex_config(previous)
        if without_routing != previous:
            rendered = without_routing
    return _prepared_write(
        path,
        previous,
        rendered,
        existing["mode"],
        existing["home"],
        mdm=mdm,
    )
