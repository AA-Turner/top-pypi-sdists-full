"""Managed client writers that expand a bare LLM gateway host into API URLs."""

from __future__ import annotations

import enum
import errno
import ipaddress
import json
import platform
from datetime import datetime
from pathlib import Path
from typing import Any, TypedDict, cast
from urllib.parse import urlsplit

from runlayer_cli.hook_install.clients import (
    _codex_features_toml_file,
    _reown_to_console_user,
    _write_config,
)
from runlayer_cli.hook_install.paths import (
    InstallScope,
    enterprise_claude_code_managed_dir,
    user_claude_code_dir,
)
from runlayer_cli.hook_install.safe_fs import (
    console_home_anchor,
    is_unsafe_windows_mdm_path,
    maybe_safe_read_file,
    path_has_link_or_reparse_point,
)
from runlayer_cli.tolerant_json import loads as tolerant_json_loads


class RouteResult(str, enum.Enum):
    WRITTEN = "written"
    UNCHANGED = "unchanged"
    DRIFTED = "drifted"
    FAILED = "failed"


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
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_API_KEY",
    "CLAUDE_CODE_OAUTH_TOKEN",
    "CLAUDE_CODE_USE_BEDROCK",
    "CLAUDE_CODE_USE_VERTEX",
    "CLAUDE_CODE_USE_FOUNDRY",
)


def route(base_url: str, key: str, *, scope: InstallScope) -> RouteResult:
    """Route Claude Code and Codex through the configured bare gateway host."""
    gateway_url = _validate_gateway_url(base_url, scope=scope)
    if gateway_url is None or not key:
        return RouteResult.FAILED

    try:
        writes = (
            _prepare_claude_route(gateway_url, key, scope=scope),
            _prepare_codex_route(gateway_url, key, scope=scope),
        )
        for prepared in writes:
            _apply_prepared_write(prepared)
    except (OSError, ValueError):
        return RouteResult.FAILED

    results = {prepared["result"] for prepared in writes}
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
    """Remove only Runlayer-owned routing keys from both clients."""
    first_error: OSError | ValueError | None = None
    for prepare in (_prepare_claude_unroute, _prepare_codex_unroute):
        try:
            prepared = prepare(scope=scope)
            _apply_prepared_write(prepared)
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
    if is_unsafe_windows_mdm_path(
        path,
        mdm=mdm,
        path_check=path_has_link_or_reparse_point,
    ):
        raise OSError(errno.ELOOP, "unsafe Windows MDM path", path)

    home = _home_for_path(path, mdm=mdm)
    existing_file = maybe_safe_read_file(path, home=home)
    if existing_file is None:
        if path.exists() or path.is_symlink():
            raise OSError(errno.EIO, "unreadable routing config", path)
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
    # User files hold credentials; MDM files must stay readable by client processes.
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
    key: str,
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

    desired_env = {
        "ANTHROPIC_BASE_URL": f"{gateway_url}/anthropic",
        "ANTHROPIC_AUTH_TOKEN": key,
        "ANTHROPIC_API_KEY": key,
        "CLAUDE_CODE_OAUTH_TOKEN": "",
        "CLAUDE_CODE_USE_BEDROCK": "",
        "CLAUDE_CODE_USE_VERTEX": "",
        "CLAUDE_CODE_USE_FOUNDRY": "",
    }
    matches = all(
        existing_env.get(name) == value for name, value in desired_env.items()
    )
    rendered: str | None = None
    if not matches:
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
        existing_env = settings.get("env")
        if isinstance(existing_env, dict):
            changed = False
            for name in _CLAUDE_ENV_KEYS:
                if name in existing_env:
                    del existing_env[name]
                    changed = True
            if changed:
                settings["env"] = existing_env
                rendered = json.dumps(settings, indent=2) + "\n"
    return _prepared_write(
        path,
        previous,
        rendered,
        existing["mode"],
        existing["home"],
        mdm=mdm,
    )


def _is_table_header(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("[") and stripped.endswith("]")


def _assignment(line: str, key: str) -> str | None:
    stripped = line.strip()
    if stripped.startswith("#"):
        return None
    name, separator, value = stripped.partition("=")
    if separator and name.strip() == key:
        return value.strip()
    return None


def _codex_matches(content: str, desired: dict[str, str]) -> bool:
    in_provider = False
    before_first_table = True
    provider_sections = 0
    top_values: list[str] = []
    provider_values: dict[str, list[str]] = {name: [] for name in desired}
    for line in content.splitlines():
        if _is_table_header(line):
            in_provider = line.strip() == "[model_providers.runlayer]"
            before_first_table = False
            if in_provider:
                provider_sections += 1
            continue
        if before_first_table:
            value = _assignment(line, "model_provider")
            if value is not None:
                top_values.append(value)
        if in_provider:
            for name in desired:
                value = _assignment(line, name)
                if value is not None:
                    provider_values[name].append(value)

    return (
        provider_sections == 1
        and top_values == ['"runlayer"']
        and all(
            provider_values[name] == [_toml_string(value)]
            for name, value in desired.items()
        )
    )


def _without_runlayer_codex_config(
    content: str,
    *,
    remove_any_model_provider: bool = False,
) -> str:
    lines = content.splitlines()
    out: list[str] = []
    in_provider = False
    before_first_table = True
    for line in lines:
        if _is_table_header(line):
            in_provider = line.strip() == "[model_providers.runlayer]"
            before_first_table = False
            if not in_provider:
                out.append(line)
            continue
        if in_provider:
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


def _render_codex_route(content: str, desired: dict[str, str]) -> str:
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
            "[model_providers.runlayer]",
            f"name = {_toml_string(desired['name'])}",
            f"base_url = {_toml_string(desired['base_url'])}",
            f"wire_api = {_toml_string(desired['wire_api'])}",
            "experimental_bearer_token = "
            f"{_toml_string(desired['experimental_bearer_token'])}",
        )
    )
    return "\n".join(lines) + "\n"


def _prepare_codex_route(
    base_url: str,
    key: str,
    *,
    scope: InstallScope,
) -> _PreparedWrite:
    path = _codex_features_toml_file(scope)
    mdm = scope == InstallScope.MDM
    existing = _read_existing(path, mdm=mdm)
    previous = existing["content"]
    content = previous or ""
    desired = {
        "name": "Runlayer",
        "base_url": f"{base_url}/openai/v1",
        "wire_api": "responses",
        "experimental_bearer_token": key,
    }
    rendered: str | None = None
    if not _codex_matches(content, desired):
        rendered = _render_codex_route(content, desired)
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
