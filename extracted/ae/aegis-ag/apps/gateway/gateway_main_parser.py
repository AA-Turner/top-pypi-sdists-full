"""Gateway parser, account, and status helpers."""

from __future__ import annotations
import asyncio
from argparse import SUPPRESS, ArgumentParser, Namespace
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
import getpass
import apps.cli.wizard as cli_wizard
import importlib.util
import json
import os
from pathlib import Path
import re
import shlex
import signal
import subprocess
import sys
import time
from wsgiref.simple_server import make_server

from apps.cli.runtime import CliRuntime
from apps.cli.shell import (
    Align,
    BRAND_ACCENT,
    BRAND_ACCENT_STRONG,
    BRAND_LIGHT,
    BRAND_MUTED,
    Console,
    Group,
    Panel,
    RICH_AVAILABLE,
    Table,
    Text,
    _resolve_aegis_version,
    render_guardian_mark,
)
from apps.provider_runtime import load_runtime_local_secret_env
from apps.runtime_layout import default_cli_state_dir, default_gateway_state_dir, default_profile_dir
from packages.gateway_core import DEFAULT_GATEWAY_ACCOUNT_ID
from packages.state import write_profile_manifest

from . import (
    DEFAULT_DISCORD_BOT_TOKEN_ENV,
    DEFAULT_FEISHU_APP_ID_ENV,
    DEFAULT_FEISHU_APP_SECRET_ENV,
    DEFAULT_FEISHU_EVENT_PATH,
    FEISHU_ADAPTER_ID,
    GatewayHttpService,
    GatewayManagedRuntime,
    GatewayManagedService,
    SUPPORTED_DISCORD_TRANSPORTS,
    SUPPORTED_FEISHU_TRANSPORTS,
    build_gateway_app,
    build_gateway_plugin_registry,
    create_gateway_web_app,
)
from .discord import DISCORD_PY_PIP_SPEC, DiscordGatewayService
from .feishu import FEISHU_SDK_PIP_SPEC, FeishuGatewayService

try:
    from prompt_toolkit.application import Application
    from prompt_toolkit.key_binding import KeyBindings as PromptKeyBindings
    from prompt_toolkit.layout.containers import HSplit, Window
    from prompt_toolkit.layout.controls import FormattedTextControl
    from prompt_toolkit.layout.layout import Layout
    from prompt_toolkit.shortcuts import input_dialog
    from prompt_toolkit.styles import Style as PromptStyle

    PROMPT_TOOLKIT_DIALOGS_AVAILABLE = True
except ModuleNotFoundError:  # pragma: no cover - optional wizard polish
    Application = None
    PromptKeyBindings = None
    HSplit = None
    Window = None
    FormattedTextControl = None
    Layout = None
    input_dialog = None
    PromptStyle = None
    PROMPT_TOOLKIT_DIALOGS_AVAILABLE = False


from .gateway_main_runtime import *  # noqa: F401,F403
from .gateway_main_wizard import *  # noqa: F401,F403

def _secret_reference_id(*, account_id: str, secret_key: str) -> str:
    normalized_account = re.sub(r"[^a-z0-9]+", "-", account_id.strip().lower()).strip("-") or "default"
    normalized_key = secret_key.replace("_", "-")
    return f"secret-feishu-{normalized_account}-{normalized_key}"

def _default_feishu_secret_env_var(*, account_id: str, secret_key: str) -> str:
    if account_id == DEFAULT_GATEWAY_ACCOUNT_ID:
        if secret_key == "app_id":
            return DEFAULT_FEISHU_APP_ID_ENV
        if secret_key == "app_secret":
            return DEFAULT_FEISHU_APP_SECRET_ENV
    normalized_account = re.sub(r"[^A-Za-z0-9]+", "_", account_id.strip()).strip("_").upper() or "DEFAULT"
    suffix = "APP_ID" if secret_key == "app_id" else "APP_SECRET"
    return f"AEGIS_FEISHU_{normalized_account}_{suffix}"

def _build_feishu_secret_reference(
    *,
    account_id: str,
    secret_key: str,
    env_var: str,
) -> dict[str, object]:
    return {
        "reference_id": _secret_reference_id(account_id=account_id, secret_key=secret_key),
        "provider_id": FEISHU_ADAPTER_ID,
        "secret_name": secret_key,
        "secret_key": secret_key,
        "metadata": {"env_var": env_var},
    }

def _find_feishu_account(
    accounts: Sequence[Mapping[str, object]],
    *,
    account_id: str,
) -> Mapping[str, object] | None:
    for account in accounts:
        current_account_id = str(account.get("account_id") or DEFAULT_GATEWAY_ACCOUNT_ID)
        if current_account_id == account_id:
            return account
    return None

def _account_secret_env_var(
    account_payload: Mapping[str, object] | None,
    *,
    secret_key: str,
) -> str | None:
    if account_payload is None:
        return None
    env_payload = _mapping(account_payload.get("env")) or {}
    direct = env_payload.get(secret_key)
    if direct is not None:
        text = str(direct).strip()
        if text:
            return text
    secret_refs = account_payload.get("secret_references")
    if not isinstance(secret_refs, list):
        return None
    for item in secret_refs:
        if not isinstance(item, Mapping):
            continue
        if str(item.get("secret_key") or "") != secret_key:
            continue
        metadata = _mapping(item.get("metadata")) or {}
        for key in ("env_var", "env", "environment_variable"):
            candidate = metadata.get(key)
            if candidate is None:
                continue
            text = str(candidate).strip()
            if text:
                return text
    return None

def _payload_string_list(value: object) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, (list, tuple)):
        raise SystemExit("allowlist fields must be JSON arrays when already present in profile.json")
    resolved: list[str] = []
    for item in value:
        text = str(item).strip()
        if text:
            resolved.append(text)
    return list(dict.fromkeys(resolved))

def _resolved_cli_account_id(args: Namespace) -> str | None:
    raw_account_id = getattr(args, "account_id", None)
    direct = _optional_text(raw_account_id) if isinstance(raw_account_id, str) else None
    if direct is not None:
        return direct
    raw_account_id_flag = getattr(args, "account_id_flag", None)
    if not isinstance(raw_account_id_flag, str):
        return None
    return _optional_text(raw_account_id_flag)

def _render_feishu_account_line(account: Mapping[str, object], *, prefix: str = "feishu_account") -> str:
    parts = [
        str(account.get("account_id") or DEFAULT_GATEWAY_ACCOUNT_ID),
        f"credentials={account.get('credentials_status') or '<unknown>'}",
        f"surface={account.get('surface') or '<unset>'}",
        f"event_path={account.get('event_path') or '<unset>'}",
    ]
    resolved_app_id = str(account.get("resolved_app_id") or "").strip()
    if resolved_app_id:
        parts.append(f"app_id={resolved_app_id}")
    return f"{prefix}: " + " · ".join(parts)

def _selected_account_payloads(
    description: Mapping[str, object],
    *,
    account_id: str | None,
    provider: str,
) -> tuple[Mapping[str, object], ...]:
    accounts = tuple(account for account in tuple(description.get("accounts") or ()) if isinstance(account, Mapping))
    if account_id is None:
        return accounts
    matched = tuple(
        account
        for account in accounts
        if str(account.get("account_id") or DEFAULT_GATEWAY_ACCOUNT_ID) == account_id
    )
    if matched:
        return matched
    raise SystemExit(f"unknown {provider} account: {account_id}")

def _default_discord_bot_token_env_var(*, account_id: str) -> str:
    if account_id == DEFAULT_GATEWAY_ACCOUNT_ID:
        return DEFAULT_DISCORD_BOT_TOKEN_ENV
    normalized_account = re.sub(r"[^A-Za-z0-9]+", "_", account_id.strip()).strip("_").upper() or "DEFAULT"
    return f"AEGIS_DISCORD_{normalized_account}_BOT_TOKEN"

def _find_discord_account(
    accounts: Sequence[Mapping[str, object]],
    *,
    account_id: str,
) -> Mapping[str, object] | None:
    for account in accounts:
        current_account_id = str(account.get("account_id") or DEFAULT_GATEWAY_ACCOUNT_ID)
        if current_account_id == account_id:
            return account
    return None

def _resolved_discord_bot_token_env_var(
    *,
    explicit_env_var: object,
    existing_account: Mapping[str, object] | None,
    account_id: str,
) -> str:
    if explicit_env_var is not None:
        text = str(explicit_env_var).strip()
        if text:
            return text
    env_payload = _mapping(existing_account.get("env")) if existing_account is not None else None
    if env_payload is not None:
        candidate = env_payload.get("bot_token")
        if candidate is not None:
            text = str(candidate).strip()
            if text:
                return text
    return _default_discord_bot_token_env_var(account_id=account_id)

def _is_unconfigured_default_discord_account(
    account_payload: Mapping[str, object],
    *,
    state_dir: Path,
    cli_state_dir: Path | None = None,
) -> bool:
    account_id = str(account_payload.get("account_id") or DEFAULT_GATEWAY_ACCOUNT_ID)
    if account_id != DEFAULT_GATEWAY_ACCOUNT_ID:
        return False
    env_var = _account_secret_env_var(account_payload, secret_key="bot_token")
    if env_var is None or env_var != DEFAULT_DISCORD_BOT_TOKEN_ENV:
        return False
    if _payload_string_list(account_payload.get("allow_guild_ids")):
        return False
    if _payload_string_list(account_payload.get("allow_channel_ids")):
        return False
    runtime_payload = _mapping(account_payload.get("runtime")) or {}
    if runtime_payload:
        return False
    runtime_environ = _gateway_runtime_environ(state_dir, cli_state_dir=cli_state_dir)
    if str(runtime_environ.get(DEFAULT_DISCORD_BOT_TOKEN_ENV) or "").strip():
        return False
    if str(runtime_environ.get(LEGACY_DISCORD_BOT_TOKEN_ENV) or "").strip():
        return False
    return True

def _upsert_discord_account(
    accounts: Sequence[Mapping[str, object]],
    account_payload: Mapping[str, object],
    *,
    state_dir: Path | None = None,
    cli_state_dir: Path | None = None,
) -> list[dict[str, object]]:
    target_account_id = str(account_payload.get("account_id") or DEFAULT_GATEWAY_ACCOUNT_ID)
    if (
        target_account_id != DEFAULT_GATEWAY_ACCOUNT_ID
        and state_dir is not None
        and len(accounts) == 1
        and _is_unconfigured_default_discord_account(
            accounts[0],
            state_dir=state_dir,
            cli_state_dir=cli_state_dir,
        )
    ):
        return [{str(key): value for key, value in account_payload.items()}]
    updated: list[dict[str, object]] = []
    replaced = False
    for account in accounts:
        current_account_id = str(account.get("account_id") or DEFAULT_GATEWAY_ACCOUNT_ID)
        if current_account_id == target_account_id:
            updated.append({str(key): value for key, value in account_payload.items()})
            replaced = True
        else:
            updated.append({str(key): value for key, value in account.items()})
    if not replaced:
        updated.append({str(key): value for key, value in account_payload.items()})
    return updated

def _resolved_feishu_secret_env_var(
    *,
    explicit_env_var: object,
    existing_account: Mapping[str, object] | None,
    account_id: str,
    secret_key: str,
) -> str:
    if explicit_env_var is not None:
        text = str(explicit_env_var).strip()
        if text:
            return text
    return _account_secret_env_var(existing_account, secret_key=secret_key) or _default_feishu_secret_env_var(
        account_id=account_id,
        secret_key=secret_key,
    )

def _upsert_feishu_account(
    accounts: Sequence[Mapping[str, object]],
    account_payload: Mapping[str, object],
) -> list[dict[str, object]]:
    target_account_id = str(account_payload.get("account_id") or DEFAULT_GATEWAY_ACCOUNT_ID)
    resolved = [dict(account) for account in accounts]
    for index, account in enumerate(resolved):
        account_id = str(account.get("account_id") or DEFAULT_GATEWAY_ACCOUNT_ID)
        if account_id == target_account_id:
            resolved[index] = dict(account_payload)
            return resolved
    resolved.append(dict(account_payload))
    return resolved

def _remove_account_payload(
    accounts: Sequence[Mapping[str, object]],
    *,
    account_id: str,
) -> tuple[list[dict[str, object]], dict[str, object]]:
    updated: list[dict[str, object]] = []
    removed: dict[str, object] | None = None
    for account in accounts:
        current_account_id = str(account.get("account_id") or DEFAULT_GATEWAY_ACCOUNT_ID)
        if current_account_id == account_id:
            removed = {str(key): value for key, value in account.items()}
            continue
        updated.append({str(key): value for key, value in account.items()})
    if removed is None:
        raise SystemExit(f"unknown gateway account: {account_id}")
    return updated, removed

def _discord_account_secret_env_vars(account_payload: Mapping[str, object]) -> tuple[str, ...]:
    env_payload = _mapping(account_payload.get("env")) or {}
    env_var = _optional_text(env_payload.get("bot_token"))
    return (env_var,) if env_var is not None else ()

def _feishu_account_secret_env_vars(account_payload: Mapping[str, object]) -> tuple[str, ...]:
    env_vars: list[str] = []
    env_payload = _mapping(account_payload.get("env")) or {}
    for key in ("app_id", "app_secret"):
        env_var = _optional_text(env_payload.get(key))
        if env_var is not None:
            env_vars.append(env_var)
    secret_refs = account_payload.get("secret_references")
    if isinstance(secret_refs, list):
        for item in secret_refs:
            if not isinstance(item, Mapping):
                continue
            metadata = _mapping(item.get("metadata")) or {}
            env_var = _optional_text(
                metadata.get("env_var") or metadata.get("env") or metadata.get("environment_variable")
            )
            if env_var is not None:
                env_vars.append(env_var)
    return tuple(dict.fromkeys(env_vars))

def _resolved_defaults(
    *,
    default_profile_dir_override: Path | None = None,
    default_state_dir_override: Path | None = None,
    default_control_profile_dir_override: Path | None = None,
    default_control_state_dir_override: Path | None = None,
) -> dict[str, Path]:
    return {
        "profile_dir": default_profile_dir_override or default_profile_dir(),
        "state_dir": default_state_dir_override or default_gateway_state_dir(),
        "cli_profile_dir": default_control_profile_dir_override or default_profile_dir(),
        "cli_state_dir": default_control_state_dir_override or default_cli_state_dir(),
    }

def _add_common_gateway_options(parser: ArgumentParser, *, defaults: dict[str, Path]) -> None:
    parser.add_argument("--profile-dir", type=Path, default=defaults["profile_dir"])
    parser.add_argument("--state-dir", type=Path, default=defaults["state_dir"])
    parser.add_argument("--cli-profile-dir", type=Path, default=defaults["cli_profile_dir"])
    parser.add_argument("--cli-state-dir", type=Path, default=defaults["cli_state_dir"])
    parser.add_argument("--workspace-id", default="workspace:gateway")

def _add_http_server_options(parser: ArgumentParser) -> None:
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8788)

def _add_optional_account_argument(parser: ArgumentParser, *, help_text: str) -> None:
    parser.add_argument("account_id", nargs="?", help=help_text)

def _add_required_account_argument(parser: ArgumentParser, *, help_text: str) -> None:
    parser.add_argument("account_id", nargs="?", help=help_text)

def _add_discord_runtime_target_options(
    parser: ArgumentParser,
    *,
    include_account_id: bool = False,
) -> None:
    parser.set_defaults(runtime_target="configured")
    parser.add_argument(
        "--transport",
        dest="runtime_target",
        choices=("configured", "gateway"),
        default="configured",
        help=SUPPRESS,
    )
    if include_account_id:
        parser.add_argument("--account-id", dest="account_id_flag", help=SUPPRESS)

def _add_discord_start_options(parser: ArgumentParser) -> None:
    _add_discord_runtime_target_options(parser, include_account_id=True)
    _add_optional_account_argument(
        parser,
        help_text="Discord account id. Omit to start all enabled accounts.",
    )
    parser.add_argument(
        "--detach",
        action="store_true",
        help="Start the Discord gateway transport in a background process and return immediately.",
    )

def _add_discord_status_options(parser: ArgumentParser) -> None:
    _add_discord_runtime_target_options(parser, include_account_id=True)
    _add_optional_account_argument(
        parser,
        help_text="Discord account id. Omit to inspect the provider-wide runtime and all accounts.",
    )

def _add_discord_stop_options(parser: ArgumentParser) -> None:
    _add_discord_runtime_target_options(parser, include_account_id=True)
    _add_optional_account_argument(
        parser,
        help_text="Discord account id. Omit to stop the configured provider runtime.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=10.0,
        help="Seconds to wait for a graceful shutdown before failing or forcing.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Send SIGKILL when the process does not exit within --timeout.",
    )

def _add_discord_restart_options(parser: ArgumentParser) -> None:
    _add_discord_runtime_target_options(parser, include_account_id=True)
    _add_optional_account_argument(
        parser,
        help_text="Discord account id. Omit to restart all enabled accounts on the configured runtime.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=10.0,
        help="Seconds to wait for the previous process to exit before failing or forcing.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Send SIGKILL when the previous process does not exit within --timeout.",
    )

def _add_discord_logs_options(parser: ArgumentParser) -> None:
    _add_discord_runtime_target_options(parser, include_account_id=True)
    _add_required_account_argument(
        parser,
        help_text="Discord account id whose runtime log you want to inspect.",
    )
    parser.add_argument(
        "--tail",
        type=int,
        default=80,
        help="Show the last N log lines before exiting or following. Use 0 to suppress the initial excerpt.",
    )
    parser.add_argument(
        "--follow",
        action="store_true",
        help="Keep streaming appended log output until interrupted.",
    )
    parser.add_argument(
        "--path",
        action="store_true",
        help="Print the resolved log file path and exit.",
    )

def _add_discord_add_options(parser: ArgumentParser) -> None:
    _add_optional_account_argument(
        parser,
        help_text="Discord account id. Omit to create or update the reserved `default` account.",
    )
    parser.add_argument("--account-id", dest="account_id_flag", help=SUPPRESS)
    parser.add_argument(
        "--transport",
        choices=SUPPORTED_DISCORD_TRANSPORTS,
        default=None,
        help="Configured transport to persist for this Discord account (defaults to existing or gateway).",
    )
    parser.add_argument(
        "--bot-token-env-var",
        default=None,
        help="Environment variable alias used to resolve the Discord bot token.",
    )
    parser.add_argument(
        "--bot-token",
        default=None,
        help="Optional raw Discord bot token to store in the local gateway secret file instead of profile.json.",
    )
    wizard_group = parser.add_mutually_exclusive_group()
    wizard_group.add_argument(
        "--wizard",
        dest="wizard",
        action="store_true",
        default=None,
        help="Force the interactive Discord setup wizard even when command-line flags are present.",
    )
    wizard_group.add_argument(
        "--no-wizard",
        dest="wizard",
        action="store_false",
        help="Skip the interactive wizard and write configuration directly from CLI arguments.",
    )
    parser.add_argument(
        "--allow-guild-id",
        action="append",
        default=None,
        help="Optional guild allowlist entry. Repeat to allow multiple guilds.",
    )
    parser.add_argument(
        "--allow-channel-id",
        action="append",
        default=None,
        help="Optional channel or parent-channel allowlist entry. Repeat to allow multiple channels.",
    )
    parser.add_argument(
        "--default-clone-id",
        help="Default local clone id for the Discord control bridge.",
    )
    parser.add_argument(
        "--default-session-id",
        help="Optional default local session id for the Discord control bridge.",
    )
    parser.add_argument(
        "--auto-create-clone",
        action="store_true",
        help="Allow the Discord control bridge to auto-create the default clone when it is missing.",
    )
    parser.add_argument(
        "--allow-group-chats",
        action="store_true",
        help="Allow the Discord control bridge to accept guild and group chats.",
    )
    enabled_group = parser.add_mutually_exclusive_group()
    enabled_group.add_argument(
        "--enabled",
        dest="enabled",
        action="store_true",
        default=None,
        help=SUPPRESS,
    )
    enabled_group.add_argument(
        "--disabled",
        dest="enabled",
        action="store_false",
        help=SUPPRESS,
    )
    account_enabled_group = parser.add_mutually_exclusive_group()
    account_enabled_group.add_argument(
        "--account-enabled",
        dest="account_enabled",
        action="store_true",
        default=None,
        help=SUPPRESS,
    )
    account_enabled_group.add_argument(
        "--account-disabled",
        dest="account_enabled",
        action="store_false",
        help=SUPPRESS,
    )

def _add_feishu_runtime_target_options(
    parser: ArgumentParser,
    *,
    include_account_id: bool = False,
) -> None:
    parser.set_defaults(runtime_target="configured")
    parser.add_argument(
        "--transport",
        dest="runtime_target",
        choices=("configured", "long-connection"),
        default="configured",
        help=SUPPRESS,
    )
    if include_account_id:
        parser.add_argument("--account-id", dest="account_id_flag", help=SUPPRESS)

def _add_feishu_start_options(parser: ArgumentParser) -> None:
    _add_feishu_runtime_target_options(parser, include_account_id=True)
    _add_optional_account_argument(
        parser,
        help_text="Feishu account id. Omit to use the configured runtime target.",
    )
    parser.add_argument(
        "--detach",
        action="store_true",
        help="Start the Feishu transport in a background process and return immediately.",
    )
    _add_http_server_options(parser)

def _add_feishu_status_options(parser: ArgumentParser) -> None:
    _add_feishu_runtime_target_options(parser, include_account_id=True)
    _add_optional_account_argument(
        parser,
        help_text="Feishu account id. Omit to inspect the provider-wide runtime and all accounts.",
    )

def _add_feishu_stop_options(parser: ArgumentParser) -> None:
    _add_feishu_runtime_target_options(parser, include_account_id=True)
    _add_optional_account_argument(
        parser,
        help_text="Feishu account id. Omit to stop the configured provider runtime.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=10.0,
        help="Seconds to wait for a graceful shutdown before failing or forcing.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Send SIGKILL when the process does not exit within --timeout.",
    )

def _add_feishu_restart_options(parser: ArgumentParser) -> None:
    _add_feishu_runtime_target_options(parser, include_account_id=True)
    _add_optional_account_argument(
        parser,
        help_text="Feishu account id. Omit to restart the configured provider runtime.",
    )
    _add_http_server_options(parser)
    parser.add_argument(
        "--timeout",
        type=float,
        default=10.0,
        help="Seconds to wait for the previous process to exit before failing or forcing.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Send SIGKILL when the previous process does not exit within --timeout.",
    )

def _add_feishu_logs_options(parser: ArgumentParser) -> None:
    _add_feishu_runtime_target_options(parser, include_account_id=True)
    _add_required_account_argument(
        parser,
        help_text="Feishu account id whose runtime log you want to inspect.",
    )
    parser.add_argument(
        "--tail",
        type=int,
        default=80,
        help="Show the last N log lines before exiting or following. Use 0 to suppress the initial excerpt.",
    )
    parser.add_argument(
        "--follow",
        action="store_true",
        help="Keep streaming appended log output until interrupted.",
    )
    parser.add_argument(
        "--path",
        action="store_true",
        help="Print the resolved log file path and exit.",
    )

def _add_feishu_add_options(parser: ArgumentParser) -> None:
    _add_optional_account_argument(
        parser,
        help_text="Feishu account id. Omit to create or update the reserved `default` account.",
    )
    parser.add_argument("--account-id", dest="account_id_flag", help=SUPPRESS)
    parser.add_argument(
        "--transport",
        choices=SUPPORTED_FEISHU_TRANSPORTS,
        default=None,
        help="Configured transport to persist for this Feishu account (defaults to existing or long-connection).",
    )
    parser.add_argument(
        "--event-path",
        default=None,
        help="Legacy webhook event path to persist for compatibility (defaults to existing or /feishu/events); long-connection does not use it directly.",
    )
    parser.add_argument(
        "--app-id-env-var",
        default=None,
        help="Environment variable alias used to resolve the Feishu App ID.",
    )
    parser.add_argument(
        "--app-secret-env-var",
        default=None,
        help="Environment variable alias used to resolve the Feishu App Secret / API key.",
    )
    parser.add_argument(
        "--app-id",
        "--api-id",
        dest="app_id",
        default=None,
        help="Optional raw Feishu App ID to store in the local gateway secret file instead of profile.json.",
    )
    parser.add_argument(
        "--app-secret",
        "--api-key",
        dest="app_secret",
        default=None,
        help="Optional raw Feishu App Secret / API key to store in the local gateway secret file instead of profile.json.",
    )
    wizard_group = parser.add_mutually_exclusive_group()
    wizard_group.add_argument(
        "--wizard",
        dest="wizard",
        action="store_true",
        default=None,
        help="Force the interactive Feishu setup wizard even when command-line flags are present.",
    )
    wizard_group.add_argument(
        "--no-wizard",
        dest="wizard",
        action="store_false",
        help="Skip the interactive wizard and write configuration directly from CLI arguments.",
    )
    enabled_group = parser.add_mutually_exclusive_group()
    enabled_group.add_argument(
        "--enabled",
        dest="enabled",
        action="store_true",
        default=None,
        help=SUPPRESS,
    )
    enabled_group.add_argument(
        "--disabled",
        dest="enabled",
        action="store_false",
        help=SUPPRESS,
    )
    parser.add_argument(
        "--default-clone-id",
        help="Default local clone id for the Feishu control bridge.",
    )
    parser.add_argument(
        "--default-session-id",
        help="Optional default local session id for the Feishu control bridge.",
    )
    parser.add_argument(
        "--auto-create-clone",
        action="store_true",
        help="Allow the Feishu control bridge to auto-create the default clone when it is missing.",
    )
    parser.add_argument(
        "--allow-group-chats",
        action="store_true",
        help="Allow the Feishu control bridge to accept group chats.",
    )

def _build_registry():
    return build_gateway_plugin_registry()

def _build_app(args: Namespace, *, registry=None):
    args.state_dir.mkdir(parents=True, exist_ok=True)
    app, _, _ = build_gateway_app(
        profile_dir=str(args.profile_dir),
        state_dir=str(args.state_dir),
        workspace_id=args.workspace_id,
        runtime_environ=_gateway_runtime_environ(
            args.state_dir,
            cli_state_dir=args.cli_state_dir,
        ),
        plugin_registry=registry,
    )
    return app

def _service_kwargs_for(service_key: str, args: Namespace) -> dict[str, object]:
    if service_key == "discord":
        return {
            "default_cli_profile_dir": (
                None if args.cli_profile_dir is None else str(args.cli_profile_dir)
            ),
            "default_cli_state_dir": (
                None if args.cli_state_dir is None else str(args.cli_state_dir)
            ),
            "environ": _gateway_runtime_environ(
                args.state_dir,
                cli_state_dir=args.cli_state_dir,
            ),
            "runtime_dependency_ensurer": _ensure_discord_sdk_available,
            "runtime_state_dir": Path(args.state_dir),
        }
    if service_key == "feishu":
        return {
            "default_cli_profile_dir": (
                None if args.cli_profile_dir is None else str(args.cli_profile_dir)
            ),
            "default_cli_state_dir": (
                None if args.cli_state_dir is None else str(args.cli_state_dir)
            ),
            "environ": _gateway_runtime_environ(
                args.state_dir,
                cli_state_dir=args.cli_state_dir,
            ),
            "runtime_dependency_ensurer": _ensure_feishu_sdk_available,
        }
    return {}

def _build_services(
    args: Namespace,
    *,
    service_keys: Iterable[str] | None = None,
):
    registry = _build_registry()
    app = _build_app(args, registry=registry)
    manifest = app.loaded_profile.manifest if app.loaded_profile is not None else None
    resolved_keys = (
        tuple(service_keys)
        if service_keys is not None
        else registry.configured_service_keys(manifest)
    )
    services = {
        key: registry.create_service(
            key,
            app=app,
            **_service_kwargs_for(key, args),
        )
        for key in resolved_keys
    }
    return app, services

def _build_service(
    args: Namespace,
    *,
    service_key: str,
    respect_enabled: bool = False,
):
    registry = _build_registry()
    app = _build_app(args, registry=registry)
    service = registry.create_service(
        service_key,
        app=app,
        respect_enabled=respect_enabled,
        **_service_kwargs_for(service_key, args),
    )
    return service

def _build_feishu_service(args: Namespace) -> FeishuGatewayService:
    service = _build_service(args, service_key="feishu", respect_enabled=False)
    if not isinstance(service, FeishuGatewayService):
        raise TypeError("gateway service plugin 'feishu' must build FeishuGatewayService")
    return service

def _build_discord_service(args: Namespace) -> DiscordGatewayService:
    service = _build_service(args, service_key="discord", respect_enabled=False)
    if not isinstance(service, DiscordGatewayService):
        raise TypeError("gateway service plugin 'discord' must build DiscordGatewayService")
    return service

def _build_managed_service(args: Namespace, *, service_key: str) -> GatewayManagedService:
    service = _build_service(args, service_key=service_key, respect_enabled=False)
    if not isinstance(service, GatewayManagedService):
        raise TypeError(
            f"gateway service plugin '{service_key}' must build a managed gateway service"
        )
    return service

def _describe_payload(service_key: str, service) -> dict[str, object]:
    return {
        "gateway": dict(service.app.setup_summary()),
        service_key: dict(service.describe()),
    }

def _describe_services_payload(
    app,
    services: Mapping[str, object],
) -> dict[str, object]:
    payload: dict[str, object] = {
        "gateway": dict(app.setup_summary()),
        "services": {
            key: dict(service.describe())
            for key, service in services.items()
            if hasattr(service, "describe")
        },
    }
    for key, service in services.items():
        if hasattr(service, "describe"):
            payload[key] = dict(service.describe())
    return payload

def _print_json(payload: dict[str, object]) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, default=str))

def _next_steps(service) -> tuple[str, ...]:
    description = service.describe()
    accounts = tuple(description.get("accounts") or ())
    control = dict(description.get("control") or {})
    steps: list[str] = []
    if description.get("sdk_dependency_status") == "missing_optional_dependency":
        steps.append("Aegis will auto-install the Feishu SDK when you run `aegis gateway` or `aegis gateway feishu start`.")
    if any(account.get("credentials_status") != "configured" for account in accounts if isinstance(account, dict)):
        env_vars: list[str] = []
        secret_reference_ids: list[str] = []
        for account in accounts:
            if not isinstance(account, dict):
                continue
            credential_env_vars = account.get("credential_env_vars")
            if isinstance(credential_env_vars, (list, tuple)):
                env_vars.extend(
                    value for value in credential_env_vars if isinstance(value, str) and value
                )
            else:
                env_vars.extend(
                    value
                    for value in (
                        account.get("app_id_env_var"),
                        account.get("app_secret_env_var"),
                    )
                    if isinstance(value, str) and value
                )
            secret_refs = account.get("secret_reference_ids")
            if isinstance(secret_refs, (list, tuple)):
                secret_reference_ids.extend(
                    value for value in secret_refs if isinstance(value, str) and value
                )
        if env_vars:
            steps.append(
                "Complete Feishu IM setup again with `aegis gateway` to store the App ID and App Secret locally, or export these advanced credential aliases manually: "
                + ", ".join(dict.fromkeys(env_vars))
            )
        elif secret_reference_ids:
            steps.append(
                "Complete Feishu IM setup again with `aegis gateway` or configure the active Feishu runtime secrets referenced by: "
                + ", ".join(dict.fromkeys(secret_reference_ids))
            )
    if control.get("runtime_status") != "ready":
        steps.append(
            "Make sure the IM bridge can open the local CLI runtime, or pass `--cli-profile-dir` / `--cli-state-dir` explicitly when the launcher defaults are not correct."
        )
    known_clones = tuple(control.get("known_clones") or ()) if isinstance(control, dict) else ()
    if not known_clones:
        steps.append(
            "Create a local clone first with `aegis clone demo`. Once a clone exists, plain text will route to the most recently active clone by default, and `/use demo` can pin the thread explicitly."
        )
    if not steps:
        steps.append("IM wiring looks healthy. Start it with `aegis gateway feishu start`. ")
    return tuple(steps)

def _render_discord_account_line(account: Mapping[str, object], *, prefix: str = "discord_account") -> str:
    allow_guild_ids = tuple(account.get("allow_guild_ids") or ())
    allow_channel_ids = tuple(account.get("allow_channel_ids") or ())
    parts = [
        str(account.get("account_id") or DEFAULT_GATEWAY_ACCOUNT_ID),
        f"enabled={'yes' if account.get('enabled') is not False else 'no'}",
        f"startup={account.get('startup_status') or '<unknown>'}",
        f"credentials={account.get('credentials_status') or '<unknown>'}",
        f"surface={account.get('surface') or '<unset>'}",
        f"bot_token_env_var={account.get('bot_token_env_var') or '<unset>'}",
        f"allow_guilds={len(allow_guild_ids)}",
        f"allow_channels={len(allow_channel_ids)}",
    ]
    credentials_error = str(account.get("credentials_error") or "").strip()
    if credentials_error:
        parts.append(f"error={credentials_error}")
    return f"{prefix}: " + " · ".join(parts)

def _feishu_async_status_lines(
    description: Mapping[str, object],
    *,
    prefix: str = "",
) -> tuple[str, ...]:
    recent_failures = tuple(description.get("recent_failures") or ())
    lines = [
        f"{prefix}async_delivery_enabled: {'yes' if description.get('async_delivery_enabled') else 'no'}",
        f"{prefix}queue_depth: {description.get('queue_depth') or 0}",
        f"{prefix}running_jobs: {description.get('running_jobs') or 0}",
        f"{prefix}worker_count: {description.get('worker_count') or 0}",
        f"{prefix}recent_failures: {len(recent_failures)}",
    ]
    for index, failure in enumerate(recent_failures[:3], start=1):
        if not isinstance(failure, Mapping):
            continue
        lines.append(
            f"{prefix}failure[{index}]: "
            f"{failure.get('account_id') or DEFAULT_GATEWAY_ACCOUNT_ID} · "
            f"conversation={failure.get('conversation_id') or '<unknown>'} · "
            f"message={failure.get('message_id') or '<unknown>'} · "
            f"summary={failure.get('failure_summary') or '<unknown>'}"
        )
    return tuple(lines)

def _discord_account_status_lines(
    description: Mapping[str, object],
    *,
    prefix: str = "",
) -> tuple[str, ...]:
    account_status = dict(description.get("account_status") or {})
    if not account_status:
        return ()
    blocked_account_ids = tuple(account_status.get("blocked_account_ids") or ())
    disabled_account_ids = tuple(account_status.get("disabled_account_ids") or ())
    return (
        f"{prefix}account_service_status: {account_status.get('service_status') or '<unknown>'}",
        f"{prefix}configured_accounts: {account_status.get('configured_accounts') or 0}",
        f"{prefix}enabled_accounts: {account_status.get('enabled_accounts') or 0}",
        f"{prefix}runnable_accounts: {account_status.get('runnable_accounts') or 0}",
        f"{prefix}blocked_accounts: {account_status.get('blocked_accounts') or 0}",
        f"{prefix}disabled_accounts: {account_status.get('disabled_accounts') or 0}",
        f"{prefix}blocked_account_ids: "
        + (", ".join(str(account_id) for account_id in blocked_account_ids if account_id) or "<none>"),
        f"{prefix}disabled_account_ids: "
        + (", ".join(str(account_id) for account_id in disabled_account_ids if account_id) or "<none>"),
    )

def _discord_portal_checklist() -> tuple[str, ...]:
    return (
        "Open Discord Developer Portal → OAuth2 → URL Generator and include the `bot` scope before inviting the app.",
        "Enable the Discord `MESSAGE_CONTENT` privileged intent for this bot before starting the gateway runtime.",
        "Grant these bot permissions in Discord: `View Channels` (`查看频道`), `Send Messages` (`发送消息`), `Send Messages in Threads` (`在子区内发送消息`), and `Read Message History` (`阅读消息历史记录`).",
    )

def _discord_next_steps(service) -> tuple[str, ...]:
    description = service.describe()
    accounts = tuple(description.get("accounts") or ())
    account_status = dict(description.get("account_status") or {})
    runtime = dict(description.get("runtime") or {})
    runtime_status = str(runtime.get("runtime_status") or "").strip().lower()
    runtime_target = str(runtime.get("target") or description.get("configured_transport") or "gateway")
    enabled_accounts = int(account_status.get("enabled_accounts") or 0)
    runnable_accounts = int(account_status.get("runnable_accounts") or 0)
    blocked_account_ids = tuple(account_status.get("blocked_account_ids") or ())
    service_status = str(account_status.get("service_status") or "").strip().lower()
    steps: list[str] = []
    if description.get("sdk_dependency_status") == "missing_optional_dependency":
        steps.append("Aegis will auto-install Discord support when you run `aegis gateway discord start`.")
    missing_credentials = [
        account
        for account in accounts
        if isinstance(account, dict)
        and account.get("enabled") is not False
        and account.get("credentials_status") != "configured"
    ]
    if missing_credentials:
        env_vars = [
            str(account.get("bot_token_env_var"))
            for account in missing_credentials
            if str(account.get("bot_token_env_var") or "").strip()
        ]
        if env_vars:
            steps.append(
                "Configure the Discord bot token with `aegis gateway discord setup [account-id] --bot-token ...` or export these env vars manually: "
                + ", ".join(dict.fromkeys(env_vars))
            )
    if enabled_accounts == 0:
        steps.append(
            "Enable at least one Discord account for runtime starts by re-running `aegis gateway discord setup [account-id]` before starting the gateway runtime."
        )
    steps.append(
        "Review the Discord developer portal checklist below before starting the gateway runtime."
    )
    if runtime_status == "running":
        if service_status == "degraded" and blocked_account_ids:
            steps.append(
                f"Discord gateway runtime is already running on `{runtime_target}` in degraded mode; blocked enabled accounts were skipped: {', '.join(str(account_id) for account_id in blocked_account_ids if account_id)}."
            )
        else:
            steps.append(f"Discord gateway runtime is already running on `{runtime_target}`.")
    elif service_status == "degraded" and runnable_accounts > 0:
        steps.append(
            "Discord wiring is partially ready. Start it with `aegis gateway discord start`; runnable enabled accounts will connect while blocked accounts are skipped."
        )
    elif service_status == "ready" and runnable_accounts > 0:
        steps.append(
            "Discord wiring looks healthy. Start it with `aegis gateway discord start`."
        )
    return tuple(steps)

def _doctor_lines(service, args: Namespace) -> tuple[str, ...]:
    description = service.describe()
    control = dict(description.get("control") or {})
    lines = [
        "Aegis Gateway doctor",
        f"im_profile_dir: {args.profile_dir}",
        f"im_state_dir: {args.state_dir}",
        f"cli_profile_dir: {args.cli_profile_dir}",
        f"cli_state_dir: {args.cli_state_dir}",
        f"configured_transport: {description.get('configured_transport') or '<unset>'}",
        f"sdk_dependency_status: {description.get('sdk_dependency_status')}",
    ]
    lines.extend(_feishu_async_status_lines(description))
    if description.get("configured_transport_error"):
        lines.append(f"configured_transport_error: {description['configured_transport_error']}")
    for account in _selected_account_payloads(
        description,
        account_id=_resolved_cli_account_id(args),
        provider="feishu",
    ):
        lines.append(_render_feishu_account_line(account))
    lines.append(f"control_runtime_status: {control.get('runtime_status') or '<unknown>'}")
    if control.get("runtime_error"):
        lines.append(f"control_runtime_error: {control['runtime_error']}")
    known_clones = tuple(control.get("known_clones") or ())
    lines.append(
        "control_known_clones: "
        + (", ".join(str(clone) for clone in known_clones if clone) or "<none>")
    )
    lines.append("next_steps:")
    lines.extend(f"- {step}" for step in _next_steps(service))
    return tuple(lines)

def _discord_doctor_lines(service, args: Namespace) -> tuple[str, ...]:
    description = service.describe()
    runtime = dict(description.get("runtime") or {})
    control = dict(description.get("control") or {})
    lines = [
        "Aegis Gateway doctor",
        f"im_profile_dir: {args.profile_dir}",
        f"im_state_dir: {args.state_dir}",
        f"cli_profile_dir: {args.cli_profile_dir}",
        f"cli_state_dir: {args.cli_state_dir}",
        f"configured_transport: {description.get('configured_transport') or '<unset>'}",
        f"sdk_dependency_status: {description.get('sdk_dependency_status') or '<n/a>'}",
        f"runtime_status: {runtime.get('runtime_status') or '<unknown>'}",
        f"control_runtime_status: {control.get('runtime_status') or '<unknown>'}",
        "required_intents: "
        + ", ".join(str(intent) for intent in tuple(description.get("required_intents") or ()) if intent),
    ]
    lines.extend(_discord_account_status_lines(description))
    if description.get("configured_transport_error"):
        lines.append(f"configured_transport_error: {description['configured_transport_error']}")
    if runtime.get("target"):
        lines.append(f"runtime_target: {runtime['target']}")
    if runtime.get("pid") is not None:
        lines.append(f"runtime_pid: {runtime['pid']}")
    if runtime.get("stale_pid_file"):
        lines.append("runtime_stale_pid_file: yes")
    if control.get("runtime_error"):
        lines.append(f"control_runtime_error: {control['runtime_error']}")
    known_clones = tuple(control.get("known_clones") or ())
    lines.append(
        "control_known_clones: "
        + (", ".join(str(clone) for clone in known_clones if clone) or "<none>")
    )
    for account in _selected_account_payloads(
        description,
        account_id=_resolved_cli_account_id(args),
        provider="discord",
    ):
        lines.append(_render_discord_account_line(account))
    lines.append("discord_portal_checklist:")
    lines.extend(f"- {step}" for step in _discord_portal_checklist())
    lines.append("next_steps:")
    lines.extend(f"- {step}" for step in _discord_next_steps(service))
    return tuple(lines)

def _doctor_service_lines(
    service_key: str,
    service,
) -> tuple[str, ...]:
    def render_account_line(account: Mapping[str, object]) -> str:
        parts = [
            str(account.get("account_id") or "<default>"),
            f"credentials={account.get('credentials_status')}",
            f"surface={account.get('surface')}",
        ]
        if account.get("enabled") is not None:
            parts.append(f"enabled={'yes' if account.get('enabled') is not False else 'no'}")
        if account.get("startup_status") is not None:
            parts.append(f"startup={account.get('startup_status')}")
        if account.get("event_path") is not None:
            parts.append(f"event_path={account.get('event_path')}")
        if account.get("bot_token_env_var") is not None:
            parts.append(f"bot_token_env_var={account.get('bot_token_env_var')}")
        allow_guild_ids = tuple(account.get("allow_guild_ids") or ())
        allow_channel_ids = tuple(account.get("allow_channel_ids") or ())
        if allow_guild_ids:
            parts.append(f"allow_guilds={len(allow_guild_ids)}")
        if allow_channel_ids:
            parts.append(f"allow_channels={len(allow_channel_ids)}")
        return f"service[{service_key}].account: " + " · ".join(parts)

    if service_key == "feishu":
        description = service.describe()
        lines = [
            f"service[{service_key}].configured_transport: {description.get('configured_transport') or '<unset>'}",
            f"service[{service_key}].sdk_dependency_status: {description.get('sdk_dependency_status') or '<n/a>'}",
        ]
        lines.extend(_feishu_async_status_lines(description, prefix=f"service[{service_key}]."))
        for account in tuple(description.get("accounts") or ()):
            if not isinstance(account, dict):
                continue
            lines.append(render_account_line(account))
        return tuple(lines)
    description = service.describe() if hasattr(service, "describe") else {}
    lines = [
        f"service[{service_key}].configured_transport: {description.get('configured_transport') or '<unset>'}",
    ]
    if description.get("configured_transport_error"):
        lines.append(
            f"service[{service_key}].configured_transport_error: {description.get('configured_transport_error')}"
        )
    if description.get("sdk_dependency_status") is not None:
        lines.append(
            f"service[{service_key}].sdk_dependency_status: {description.get('sdk_dependency_status')}"
        )
    runtime = dict(description.get("runtime") or {})
    if runtime:
        lines.append(
            f"service[{service_key}].runtime_status: {runtime.get('runtime_status') or '<unknown>'}"
        )
        if runtime.get("target") is not None:
            lines.append(f"service[{service_key}].runtime_target: {runtime.get('target')}")
    for account in tuple(description.get("accounts") or ()):
        if not isinstance(account, dict):
            continue
        lines.append(render_account_line(account))
    return tuple(lines)

def _doctor_services_lines(app, services: Mapping[str, object], args: Namespace) -> tuple[str, ...]:
    lines = [
        "Aegis Gateway doctor",
        f"im_profile_dir: {args.profile_dir}",
        f"im_state_dir: {args.state_dir}",
        f"cli_profile_dir: {args.cli_profile_dir}",
        f"cli_state_dir: {args.cli_state_dir}",
        "registered_services: " + (", ".join(services.keys()) or "<none>"),
    ]
    lines.extend(
        line
        for service_key, service in services.items()
        for line in _doctor_service_lines(service_key, service)
    )
    if "feishu" in services:
        lines.append("next_steps:")
        lines.extend(f"- {step}" for step in _next_steps(services["feishu"]))
    elif "discord" in services:
        lines.append("next_steps:")
        lines.extend(f"- {step}" for step in _discord_next_steps(services["discord"]))
    return tuple(lines)

def _service_runtime_status_summary(service: object, args: Namespace) -> tuple[str, str | None]:
    if not isinstance(service, GatewayManagedService):
        return "unavailable", "service is not a managed runtime"
    try:
        target = service.configured_runtime_target()
        runtime = service.managed_runtime(args=args, target=target)
        state = _runtime_state(runtime)
        return str(state["status"]), None
    except Exception as exc:
        return "unavailable", str(exc)

def _run_status_all(args: Namespace) -> int:
    app, services = _build_services(args)
    print("Aegis Gateway status")
    print(f"im_profile_dir: {args.profile_dir}")
    print(f"im_state_dir: {args.state_dir}")
    if not services:
        print("configured_services: <none>")
        print("next_steps:")
        print("- Run `aegis gateway setup` to configure your first IM account.")
        return 0
    print("configured_services: " + ", ".join(services.keys()))
    for service_key, service in services.items():
        description = service.describe() if hasattr(service, "describe") else {}
        runtime_status, runtime_error = _service_runtime_status_summary(service, args)
        configured_transport = description.get("configured_transport") or "<unset>"
        print(f"service[{service_key}].configured_transport: {configured_transport}")
        print(f"service[{service_key}].runtime_status: {runtime_status}")
        if runtime_error is not None:
            print(f"service[{service_key}].runtime_error: {runtime_error}")
        for account in tuple(description.get("accounts") or ()):
            if not isinstance(account, Mapping):
                continue
            if service_key == "discord":
                print(_render_discord_account_line(account, prefix=f"service[{service_key}].account"))
            elif service_key == "feishu":
                print(_render_feishu_account_line(account, prefix=f"service[{service_key}].account"))
    return 0

__all__ = [
    "_secret_reference_id",
    "_default_feishu_secret_env_var",
    "_build_feishu_secret_reference",
    "_find_feishu_account",
    "_account_secret_env_var",
    "_payload_string_list",
    "_resolved_cli_account_id",
    "_render_feishu_account_line",
    "_selected_account_payloads",
    "_default_discord_bot_token_env_var",
    "_find_discord_account",
    "_resolved_discord_bot_token_env_var",
    "_is_unconfigured_default_discord_account",
    "_upsert_discord_account",
    "_resolved_feishu_secret_env_var",
    "_upsert_feishu_account",
    "_remove_account_payload",
    "_discord_account_secret_env_vars",
    "_feishu_account_secret_env_vars",
    "_resolved_defaults",
    "_add_common_gateway_options",
    "_add_http_server_options",
    "_add_optional_account_argument",
    "_add_required_account_argument",
    "_add_discord_runtime_target_options",
    "_add_discord_start_options",
    "_add_discord_status_options",
    "_add_discord_stop_options",
    "_add_discord_restart_options",
    "_add_discord_logs_options",
    "_add_discord_add_options",
    "_add_feishu_runtime_target_options",
    "_add_feishu_start_options",
    "_add_feishu_status_options",
    "_add_feishu_stop_options",
    "_add_feishu_restart_options",
    "_add_feishu_logs_options",
    "_add_feishu_add_options",
    "_build_registry",
    "_build_app",
    "_service_kwargs_for",
    "_build_services",
    "_build_service",
    "_build_feishu_service",
    "_build_discord_service",
    "_build_managed_service",
    "_describe_payload",
    "_describe_services_payload",
    "_print_json",
    "_next_steps",
    "_render_discord_account_line",
    "_feishu_async_status_lines",
    "_discord_account_status_lines",
    "_discord_portal_checklist",
    "_discord_next_steps",
    "_doctor_lines",
    "_discord_doctor_lines",
    "_doctor_service_lines",
    "_doctor_services_lines",
    "_service_runtime_status_summary",
    "_run_status_all",
]
