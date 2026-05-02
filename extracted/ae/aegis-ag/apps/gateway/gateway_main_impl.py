"""Gateway CLI main implementation assembled from wizard, runtime, and parser helpers."""

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


from .gateway_main_parser import *  # noqa: F401,F403
from .gateway_main_parser import _resolved_cli_account_id
from .gateway_main_runtime import *  # noqa: F401,F403
from .gateway_main_wizard import *  # noqa: F401,F403
from .gateway_main_wizard import (
    GATEWAY_WIZARD_BACK,
    _confirm_gateway_wizard_intro,
    _gateway_wizard_choice_prompt,
    _gateway_wizard_dialogs_supported,
    _gateway_wizard_secret_prompt,
    _gateway_wizard_text_prompt,
    _interactive_shell_supported,
    _print_gateway_discord_wizard_intro,
    _print_gateway_feishu_wizard_intro,
    _print_gateway_setup_paused,
    _run_interactive_discord_wizard,
    _run_interactive_feishu_wizard,
    _shared_wizard_choice_prompt,
    _shared_wizard_text_prompt,
)

def _run_add_discord(args: Namespace) -> int:
    _ensure_discord_sdk_available(reason="Discord setup")
    args.profile_dir.mkdir(parents=True, exist_ok=True)
    manifest = _load_profile_manifest(args.profile_dir)
    gateway_payload = _mapping_payload(manifest.get("gateway"), path="gateway")
    adapters_payload = _mapping_payload(gateway_payload.get("adapters"), path="gateway.adapters")
    discord_payload = _mapping_payload(adapters_payload.get("discord"), path="gateway.adapters.discord")
    control_payload = _mapping_payload(discord_payload.get("control"), path="gateway.adapters.discord.control")

    account_id = _resolved_cli_account_id(args) or DEFAULT_GATEWAY_ACCOUNT_ID
    accounts_value = discord_payload.get("accounts")
    if accounts_value is None:
        existing_accounts: list[dict[str, object]] = []
    elif isinstance(accounts_value, list):
        existing_accounts = []
        for index, account in enumerate(accounts_value):
            if not isinstance(account, Mapping):
                raise SystemExit(
                    f"gateway.adapters.discord.accounts[{index}] must be a JSON object"
                )
            existing_accounts.append({str(key): value for key, value in account.items()})
    else:
        raise SystemExit("gateway.adapters.discord.accounts must be a JSON array")
    existing_account = _find_discord_account(existing_accounts, account_id=account_id)

    transport = (
        str(args.transport or "").strip()
        or str((existing_account or {}).get("surface") or "").strip()
        or str(discord_payload.get("surface") or "").strip()
        or "gateway"
    )
    bot_token_env_var = _resolved_discord_bot_token_env_var(
        explicit_env_var=args.bot_token_env_var,
        existing_account=existing_account,
        account_id=account_id,
    )
    allow_guild_ids = (
        list(dict.fromkeys(str(value).strip() for value in args.allow_guild_id if str(value).strip()))
        if args.allow_guild_id is not None
        else _payload_string_list((existing_account or {}).get("allow_guild_ids"))
    )
    allow_channel_ids = (
        list(dict.fromkeys(str(value).strip() for value in args.allow_channel_id if str(value).strip()))
        if args.allow_channel_id is not None
        else _payload_string_list((existing_account or {}).get("allow_channel_ids"))
    )
    enabled = bool(args.enabled) if args.enabled is not None else True
    account_enabled = (
        bool(args.account_enabled)
        if args.account_enabled is not None
        else bool((existing_account or {}).get("enabled") is not False)
    )
    default_clone_id = (
        str(args.default_clone_id).strip()
        if args.default_clone_id is not None
        else str(control_payload.get("default_clone_id") or "").strip()
    )
    default_session_id = (
        str(args.default_session_id).strip()
        if args.default_session_id is not None
        else str(control_payload.get("default_session_id") or "").strip()
    )
    auto_create_clone = bool(args.auto_create_clone) or bool(control_payload.get("auto_create_clone") is True)
    allow_group_chats = bool(args.allow_group_chats) or bool(control_payload.get("allow_group_chats") is True)
    bot_token_value = str(args.bot_token or "").strip()
    use_wizard = bool(args.wizard) if args.wizard is not None else _interactive_shell_supported()
    if use_wizard:
        if not _print_gateway_discord_wizard_intro():
            _print_gateway_setup_paused("Discord")
            return 0
        wizard_state = _run_interactive_discord_wizard(
            account_id=account_id,
            transport=transport,
            bot_token_value=bot_token_value,
            enabled=enabled,
            account_enabled=account_enabled,
            default_clone_id=default_clone_id,
            default_session_id=default_session_id,
            auto_create_clone=auto_create_clone,
            allow_group_chats=allow_group_chats,
            allow_guild_ids=allow_guild_ids,
            allow_channel_ids=allow_channel_ids,
            cli_profile_dir=args.cli_profile_dir,
            cli_state_dir=args.cli_state_dir,
        )
        if wizard_state is None:
            _print_gateway_setup_paused("Discord")
            return 0
        account_id = wizard_state.account_id
        transport = wizard_state.transport
        bot_token_value = wizard_state.bot_token_value
        enabled = wizard_state.enabled
        account_enabled = wizard_state.account_enabled
        default_clone_id = wizard_state.default_clone_id
        default_session_id = wizard_state.default_session_id
        auto_create_clone = wizard_state.auto_create_clone
        allow_group_chats = wizard_state.allow_group_chats
        allow_guild_ids = list(wizard_state.allow_guild_ids)
        allow_channel_ids = list(wizard_state.allow_channel_ids)

    auto_start = bool(getattr(args, "auto_start", False)) or use_wizard
    args.account_id = account_id
    existing_account = _find_discord_account(existing_accounts, account_id=account_id)
    bot_token_env_var = _resolved_discord_bot_token_env_var(
        explicit_env_var=args.bot_token_env_var,
        existing_account=existing_account,
        account_id=account_id,
    )

    account_payload: dict[str, object] = {
        "account_id": account_id,
        "surface": transport,
        "enabled": account_enabled,
        "env": {"bot_token": bot_token_env_var},
    }
    existing_runtime = _mapping((existing_account or {}).get("runtime"))
    if existing_runtime:
        account_payload["runtime"] = dict(existing_runtime)
    if allow_guild_ids:
        account_payload["allow_guild_ids"] = allow_guild_ids
    if allow_channel_ids:
        account_payload["allow_channel_ids"] = allow_channel_ids

    local_secret_path = _persist_gateway_local_secret_env(
        args.state_dir,
        {bot_token_env_var: bot_token_value},
    )

    if default_clone_id:
        control_payload["default_clone_id"] = default_clone_id
    elif use_wizard:
        control_payload.pop("default_clone_id", None)
    if default_session_id:
        control_payload["default_session_id"] = default_session_id
    elif use_wizard or not default_clone_id:
        control_payload.pop("default_session_id", None)
    if auto_create_clone:
        control_payload["auto_create_clone"] = True
    elif use_wizard:
        control_payload.pop("auto_create_clone", None)
    if allow_group_chats:
        control_payload["allow_group_chats"] = True
    elif use_wizard:
        control_payload.pop("allow_group_chats", None)

    discord_payload["accounts"] = _upsert_discord_account(existing_accounts, account_payload)
    discord_payload["surface"] = transport
    discord_payload["enabled"] = enabled
    if control_payload:
        discord_payload["control"] = control_payload
    else:
        discord_payload.pop("control", None)
    adapters_payload["discord"] = discord_payload
    gateway_payload["adapters"] = adapters_payload
    manifest["gateway"] = gateway_payload

    manifest_path = write_profile_manifest(args.profile_dir, manifest)

    service = _build_discord_service(args)
    print(f"Configured Discord IM in {manifest_path}")
    print(f"Discord account: {account_id}")
    print(f"Discord transport: {transport}")
    if local_secret_path is not None:
        print(f"Local IM secret file: {local_secret_path}")
        print("Raw Discord bot token was stored locally outside profile.json.")
    if auto_start:
        print("Starting the configured Discord bridge in the background...")
        try:
            _start_discord_runtime_after_setup(args, transport=transport)
        except SystemExit as exc:
            print("Discord setup completed, but the bridge did not stay running in the background.")
            print(f"Reason: {exc}")
            print("Next steps:")
            for step in _discord_next_steps(service):
                print(f"- {step}")
            print("- Start it again with `aegis gateway discord start --detach`.")
            return 1
        print("Discord setup is complete.")
        print("Next steps:")
        print("- Check status with `aegis gateway discord status`.")
        print(f"- Follow logs with `aegis gateway discord logs {account_id} --follow`.")
        print(f"- Restart after changes with `aegis gateway discord restart {account_id}`.")
        return 0
    print("Discord account enabled for default runtime starts: " + ("yes" if account_enabled else "no"))
    print("next_steps:")
    for step in _discord_next_steps(service):
        print(f"- {step}")
    print("Discord developer portal checklist:")
    for step in _discord_portal_checklist():
        print(f"- {step}")
    print("- Start the configured bridge with `aegis gateway discord start`.")
    return 0

def _start_discord_runtime_after_setup(args: Namespace, *, transport: str) -> int:
    service = _build_discord_service(args)
    start_args = Namespace(**vars(args))
    start_args.runtime_target = transport or "configured"
    start_args.account_id = None
    start_args.detach = True
    start_args.timeout = float(getattr(start_args, "timeout", 10.0) or 10.0)
    start_args.force = bool(getattr(start_args, "force", False))
    return _run_restart(start_args, service=service)

def _start_feishu_runtime_after_setup(args: Namespace, *, transport: str) -> int:
    service = _build_feishu_service(args)
    start_args = Namespace(**vars(args))
    start_args.runtime_target = transport or "configured"
    if transport == "long-connection" and len(getattr(service, "account_configs", ())) == 1:
        start_args.account_id = None
    start_args.detach = True
    start_args.host = getattr(start_args, "host", "127.0.0.1")
    start_args.port = int(getattr(start_args, "port", 8788) or 8788)
    start_args.timeout = float(getattr(start_args, "timeout", 10.0) or 10.0)
    start_args.force = bool(getattr(start_args, "force", False))
    return _run_restart(start_args, service=service)

def _run_add_feishu(args: Namespace) -> int:
    _ensure_feishu_sdk_available(reason="Feishu setup")
    args.profile_dir.mkdir(parents=True, exist_ok=True)
    manifest = _load_profile_manifest(args.profile_dir)
    gateway_payload = _mapping_payload(manifest.get("gateway"), path="gateway")
    adapters_payload = _mapping_payload(gateway_payload.get("adapters"), path="gateway.adapters")
    feishu_payload = _mapping_payload(adapters_payload.get("feishu"), path="gateway.adapters.feishu")
    control_payload = _mapping_payload(feishu_payload.get("control"), path="gateway.adapters.feishu.control")

    account_id = _resolved_cli_account_id(args) or DEFAULT_GATEWAY_ACCOUNT_ID
    accounts_value = feishu_payload.get("accounts")
    if accounts_value is None:
        existing_accounts: list[dict[str, object]] = []
    elif isinstance(accounts_value, list):
        existing_accounts = []
        for index, account in enumerate(accounts_value):
            if not isinstance(account, Mapping):
                raise SystemExit(
                    f"gateway.adapters.feishu.accounts[{index}] must be a JSON object"
                )
            existing_accounts.append({str(key): value for key, value in account.items()})
    else:
        raise SystemExit("gateway.adapters.feishu.accounts must be a JSON array")

    existing_account = _find_feishu_account(existing_accounts, account_id=account_id)
    transport = (
        str(args.transport)
        if args.transport is not None
        else str(
            (existing_account or {}).get("surface")
            or feishu_payload.get("surface")
            or "long-connection"
        )
    )
    event_path = (
        str(args.event_path)
        if args.event_path is not None
        else str(
            (existing_account or {}).get("event_path")
            or feishu_payload.get("event_path")
            or DEFAULT_FEISHU_EVENT_PATH
        )
    )
    app_id_env_var = _resolved_feishu_secret_env_var(
        explicit_env_var=args.app_id_env_var,
        existing_account=existing_account,
        account_id=account_id,
        secret_key="app_id",
    )
    app_secret_env_var = _resolved_feishu_secret_env_var(
        explicit_env_var=args.app_secret_env_var,
        existing_account=existing_account,
        account_id=account_id,
        secret_key="app_secret",
    )
    app_id_value = str(args.app_id or "").strip()
    app_secret_value = str(args.app_secret or "").strip()
    enabled = bool(args.enabled) if args.enabled is not None else True
    default_clone_id = (
        str(args.default_clone_id).strip()
        if args.default_clone_id is not None
        else str(control_payload.get("default_clone_id") or "").strip()
    )
    default_session_id = (
        str(args.default_session_id).strip()
        if args.default_session_id is not None
        else str(control_payload.get("default_session_id") or "").strip()
    )
    auto_create_clone = bool(args.auto_create_clone) or bool(control_payload.get("auto_create_clone") is True)
    allow_group_chats = bool(args.allow_group_chats) or bool(control_payload.get("allow_group_chats") is True)

    use_wizard = bool(args.wizard) if args.wizard is not None else _interactive_shell_supported()
    if use_wizard:
        if not _print_gateway_feishu_wizard_intro():
            _print_gateway_setup_paused("Feishu")
            return 0
        wizard_state = _run_interactive_feishu_wizard(
            account_id=account_id,
            transport=transport,
            event_path=event_path,
            app_id_env_var=app_id_env_var,
            app_secret_env_var=app_secret_env_var,
            app_id_value=app_id_value,
            app_secret_value=app_secret_value,
            enabled=enabled,
            default_clone_id=default_clone_id,
            default_session_id=default_session_id,
            auto_create_clone=auto_create_clone,
            allow_group_chats=allow_group_chats,
            cli_profile_dir=args.cli_profile_dir,
            cli_state_dir=args.cli_state_dir,
        )
        if wizard_state is None:
            _print_gateway_setup_paused("Feishu")
            return 0
        account_id = wizard_state.account_id
        transport = wizard_state.transport
        event_path = wizard_state.event_path
        app_id_value = wizard_state.app_id_value
        app_secret_value = wizard_state.app_secret_value
        enabled = wizard_state.enabled
        default_clone_id = wizard_state.default_clone_id
        default_session_id = wizard_state.default_session_id
        auto_create_clone = wizard_state.auto_create_clone
        allow_group_chats = wizard_state.allow_group_chats

    auto_start = bool(getattr(args, "auto_start", False)) or use_wizard
    args.account_id = account_id
    existing_account = _find_feishu_account(existing_accounts, account_id=account_id)
    app_id_env_var = _resolved_feishu_secret_env_var(
        explicit_env_var=args.app_id_env_var,
        existing_account=existing_account,
        account_id=account_id,
        secret_key="app_id",
    )
    app_secret_env_var = _resolved_feishu_secret_env_var(
        explicit_env_var=args.app_secret_env_var,
        existing_account=existing_account,
        account_id=account_id,
        secret_key="app_secret",
    )

    account_payload = {
        "account_id": account_id,
        "surface": transport,
        "event_path": event_path,
        "secret_references": [
            _build_feishu_secret_reference(
                account_id=account_id,
                secret_key="app_id",
                env_var=app_id_env_var,
            ),
            _build_feishu_secret_reference(
                account_id=account_id,
                secret_key="app_secret",
                env_var=app_secret_env_var,
            ),
        ],
    }
    feishu_payload["accounts"] = _upsert_feishu_account(existing_accounts, account_payload)
    feishu_payload["surface"] = transport
    feishu_payload["event_path"] = event_path
    feishu_payload["enabled"] = enabled

    if default_clone_id:
        control_payload["default_clone_id"] = default_clone_id
    elif use_wizard:
        control_payload.pop("default_clone_id", None)
    if default_session_id:
        control_payload["default_session_id"] = default_session_id
    elif use_wizard or not default_clone_id:
        control_payload.pop("default_session_id", None)
    if auto_create_clone:
        control_payload["auto_create_clone"] = True
    elif use_wizard:
        control_payload.pop("auto_create_clone", None)
    if allow_group_chats:
        control_payload["allow_group_chats"] = True
    elif use_wizard:
        control_payload.pop("allow_group_chats", None)
    if control_payload:
        feishu_payload["control"] = control_payload
    else:
        feishu_payload.pop("control", None)

    adapters_payload["feishu"] = feishu_payload
    gateway_payload["adapters"] = adapters_payload
    manifest["gateway"] = gateway_payload
    manifest_path = write_profile_manifest(args.profile_dir, manifest)

    local_secret_path = _persist_gateway_local_secret_env(
        args.state_dir,
        {
            app_id_env_var: app_id_value,
            app_secret_env_var: app_secret_value,
        },
    )

    service = _build_feishu_service(args)
    print(f"Configured Feishu IM in {manifest_path}")
    print(f"Feishu account: {account_id}")
    print(f"Feishu transport: {transport}")
    if local_secret_path is not None:
        print(f"Local IM secret file: {local_secret_path}")
        print("Raw Feishu credentials were stored locally outside profile.json.")
    if auto_start:
        print("Starting the configured Feishu bridge in the background...")
        try:
            _start_feishu_runtime_after_setup(args, transport=transport)
        except SystemExit as exc:
            print("Feishu setup completed, but the bridge did not stay running in the background.")
            print(f"Reason: {exc}")
            print("Next steps:")
            for step in _next_steps(service):
                print(f"- {step}")
            print("- Start it again with `aegis gateway feishu start --detach`.")
            return 1
        print("Feishu setup is complete.")
        print("Next steps:")
        print("- Check status with `aegis gateway feishu status`.")
        print(f"- Follow logs with `aegis gateway feishu logs {account_id} --follow`.")
        print(f"- Restart after changes with `aegis gateway feishu restart {account_id}`.")
        return 0
    print("next_steps:")
    for step in _next_steps(service):
        print(f"- {step}")
    print("- Start the configured bridge with `aegis gateway feishu start`.")
    return 0

def _run_remove_discord(args: Namespace) -> int:
    account_id = _resolved_cli_account_id(args)
    if account_id is None:
        raise SystemExit("remove requires <account-id>")
    args.profile_dir.mkdir(parents=True, exist_ok=True)
    manifest = _load_profile_manifest(args.profile_dir)
    gateway_payload = _mapping_payload(manifest.get("gateway"), path="gateway")
    adapters_payload = _mapping_payload(gateway_payload.get("adapters"), path="gateway.adapters")
    discord_payload = _mapping_payload(adapters_payload.get("discord"), path="gateway.adapters.discord")
    accounts_value = discord_payload.get("accounts")
    if not isinstance(accounts_value, list):
        raise SystemExit("gateway.adapters.discord.accounts must be a JSON array")
    remaining_accounts, removed_account = _remove_account_payload(accounts_value, account_id=account_id)
    secret_path = _delete_gateway_local_secret_env(
        args.state_dir,
        _discord_account_secret_env_vars(removed_account),
    )
    if remaining_accounts:
        discord_payload["accounts"] = remaining_accounts
        discord_payload["enabled"] = True
        adapters_payload["discord"] = discord_payload
    else:
        adapters_payload.pop("discord", None)
    if adapters_payload:
        gateway_payload["adapters"] = adapters_payload
        manifest["gateway"] = gateway_payload
    else:
        manifest.pop("gateway", None)
    manifest_path = write_profile_manifest(args.profile_dir, manifest)
    print(f"Removed Discord account: {account_id}")
    print(f"Updated manifest: {manifest_path}")
    if secret_path is not None:
        print(f"Updated local IM secret file: {secret_path}")
    return 0

def _run_remove_feishu(args: Namespace) -> int:
    account_id = _resolved_cli_account_id(args)
    if account_id is None:
        raise SystemExit("remove requires <account-id>")
    args.profile_dir.mkdir(parents=True, exist_ok=True)
    manifest = _load_profile_manifest(args.profile_dir)
    gateway_payload = _mapping_payload(manifest.get("gateway"), path="gateway")
    adapters_payload = _mapping_payload(gateway_payload.get("adapters"), path="gateway.adapters")
    feishu_payload = _mapping_payload(adapters_payload.get("feishu"), path="gateway.adapters.feishu")
    accounts_value = feishu_payload.get("accounts")
    if not isinstance(accounts_value, list):
        raise SystemExit("gateway.adapters.feishu.accounts must be a JSON array")
    remaining_accounts, removed_account = _remove_account_payload(accounts_value, account_id=account_id)
    secret_path = _delete_gateway_local_secret_env(
        args.state_dir,
        _feishu_account_secret_env_vars(removed_account),
    )
    if remaining_accounts:
        feishu_payload["accounts"] = remaining_accounts
        feishu_payload["enabled"] = True
        adapters_payload["feishu"] = feishu_payload
    else:
        adapters_payload.pop("feishu", None)
    if adapters_payload:
        gateway_payload["adapters"] = adapters_payload
        manifest["gateway"] = gateway_payload
    else:
        manifest.pop("gateway", None)
    manifest_path = write_profile_manifest(args.profile_dir, manifest)
    print(f"Removed Feishu account: {account_id}")
    print(f"Updated manifest: {manifest_path}")
    if secret_path is not None:
        print(f"Updated local IM secret file: {secret_path}")
    return 0

def _run_start(service: FeishuGatewayService, args: Namespace) -> int:
    transport = _resolve_runtime_target_argument(args, service=service)

    if transport == "long-connection":
        service.prepare_managed_runtime(action="startup", target=transport)
    if args.detach:
        return _run_start_detached(args, service=service, target=transport)

    if transport == "long-connection":
        account_label = args.account_id or "<default>"
        print("Starting Aegis Gateway Feishu long-connection transport")
        print(f"Feishu account: {account_label}")
        service.start_long_connection(account_id=args.account_id)
        return 0

    app = create_gateway_web_app({"feishu": service}, app=service.app)
    with make_server(args.host, args.port, app) as server:
        event_paths = ", ".join(service.event_paths) or "<none>"
        print(f"Serving Aegis Gateway on http://{args.host}:{args.port}")
        print(f"Feishu event paths: {event_paths}")
        server.serve_forever()
    return 0

def _run_discord_start(service: DiscordGatewayService, args: Namespace) -> int:
    transport = _resolve_runtime_target_argument(args, service=service)
    service.prepare_managed_runtime(action="startup", target=transport)
    if args.detach:
        return _run_start_detached(args, service=service, target=transport)

    account_label = args.account_id or "<all enabled>"
    print("Starting Aegis Gateway Discord gateway transport")
    print(f"Discord account: {account_label}")
    asyncio.run(service.start_gateway(account_id=args.account_id))
    return 0

def _http_services(
    services: Mapping[str, object],
) -> dict[str, GatewayHttpService]:
    return {
        key: service
        for key, service in services.items()
        if isinstance(service, GatewayHttpService)
    }

def _run_serve(args: Namespace) -> int:
    app, services = _build_services(args)
    if not services:
        raise SystemExit("No gateway services are enabled in the active profile manifest.")
    http_services = _http_services(services)
    if not http_services:
        raise SystemExit("No enabled gateway HTTP services are available in the active profile manifest.")
    web_app = create_gateway_web_app(http_services, app=app)
    with make_server(args.host, args.port, web_app) as server:
        print(f"Serving Aegis Gateway on http://{args.host}:{args.port}")
        for key, service in http_services.items():
            event_paths = ", ".join(getattr(service, "http_paths", ())) or "<none>"
            print(f"{key} event paths: {event_paths}")
        server.serve_forever()
    return 0

def _build_legacy_parser(*, defaults: dict[str, Path]) -> ArgumentParser:
    parser = ArgumentParser(description="Run the Aegis Gateway surface locally.")
    _add_feishu_start_options(parser)
    _add_common_gateway_options(parser, defaults=defaults)
    parser.add_argument(
        "--describe",
        action="store_true",
        help="Print the active Feishu IM configuration and exit.",
    )
    parser.add_argument(
        "--doctor",
        action="store_true",
        help="Inspect Feishu IM readiness and next steps.",
    )
    return parser

def legacy_main(
    argv: Sequence[str] | None = None,
    *,
    default_profile_dir: Path | None = None,
    default_state_dir: Path | None = None,
    default_control_profile_dir: Path | None = None,
    default_control_state_dir: Path | None = None,
) -> int:
    defaults = _resolved_defaults(
        default_profile_dir_override=default_profile_dir,
        default_state_dir_override=default_state_dir,
        default_control_profile_dir_override=default_control_profile_dir,
        default_control_state_dir_override=default_control_state_dir,
    )
    parser = _build_legacy_parser(defaults=defaults)
    args = parser.parse_args(list(argv) if argv is not None else None)
    service = _build_feishu_service(args)
    if args.describe:
        _print_json(_describe_payload("feishu", service))
        return 0
    if args.doctor:
        print("\n".join(_doctor_lines(service, args)))
        return 0
    return _run_start(service, args)

def command_main(
    argv: Sequence[str] | None = None,
    *,
    default_profile_dir: Path | None = None,
    default_state_dir: Path | None = None,
    default_control_profile_dir: Path | None = None,
    default_control_state_dir: Path | None = None,
) -> int:
    defaults = _resolved_defaults(
        default_profile_dir_override=default_profile_dir,
        default_state_dir_override=default_state_dir,
        default_control_profile_dir_override=default_control_profile_dir,
        default_control_state_dir_override=default_control_state_dir,
    )
    resolved_argv = list(argv) if argv is not None else list(sys.argv[1:])
    if not resolved_argv:
        resolved_argv = ["status"]
    common = ArgumentParser(add_help=False)
    _add_common_gateway_options(common, defaults=defaults)

    parser = ArgumentParser(prog="aegis gateway", description="Manage IM providers and accounts.")
    subparsers = parser.add_subparsers(dest="command")

    setup = subparsers.add_parser(
        "setup",
        parents=[common],
        help="Open interactive IM setup.",
    )
    setup.add_argument(
        "--default-clone-id",
        default="",
        help="Prefill which clone plain text should route to by default after setup.",
    )
    setup.set_defaults(command_action="setup")

    status = subparsers.add_parser(
        "status",
        parents=[common],
        help="Show status for all providers and accounts.",
    )
    status.set_defaults(command_action="status_all")

    doctor = subparsers.add_parser(
        "doctor",
        parents=[common],
        help="Run health checks for all providers and accounts.",
    )
    doctor.set_defaults(command_action="doctor_all")

    describe = subparsers.add_parser(
        "describe",
        parents=[common],
        help="Print resolved IM provider and account wiring as JSON.",
    )
    describe.set_defaults(command_action="describe_all")


    feishu = subparsers.add_parser("feishu", parents=[common], help="Manage Feishu accounts.")
    feishu.set_defaults(command_action="status", service_key="feishu")
    feishu_subparsers = feishu.add_subparsers(dest="feishu_command")

    feishu_setup = feishu_subparsers.add_parser(
        "setup",
        parents=[common],
        help="Add or update a Feishu account.",
    )
    _add_feishu_add_options(feishu_setup)
    feishu_setup.set_defaults(command_action="add_feishu", service_key="feishu", auto_start=False)

    feishu_remove = feishu_subparsers.add_parser(
        "remove",
        parents=[common],
        help="Remove a Feishu account.",
    )
    _add_required_account_argument(feishu_remove, help_text="Feishu account id to remove.")
    feishu_remove.set_defaults(command_action="remove_feishu", service_key="feishu")

    feishu_start = feishu_subparsers.add_parser(
        "start",
        parents=[common],
        help="Start all or one Feishu account.",
    )
    _add_feishu_start_options(feishu_start)
    feishu_start.set_defaults(command_action="start", service_key="feishu")

    feishu_status = feishu_subparsers.add_parser(
        "status",
        parents=[common],
        help="Show Feishu status.",
    )
    _add_feishu_status_options(feishu_status)
    feishu_status.set_defaults(command_action="status", service_key="feishu")

    feishu_stop = feishu_subparsers.add_parser(
        "stop",
        parents=[common],
        help="Stop all or one Feishu account.",
    )
    _add_feishu_stop_options(feishu_stop)
    feishu_stop.set_defaults(command_action="stop", service_key="feishu")

    feishu_restart = feishu_subparsers.add_parser(
        "restart",
        parents=[common],
        help="Restart all or one Feishu account.",
    )
    _add_feishu_restart_options(feishu_restart)
    feishu_restart.set_defaults(command_action="restart", service_key="feishu")

    feishu_logs = feishu_subparsers.add_parser(
        "logs",
        parents=[common],
        help="Show logs for one Feishu account.",
    )
    _add_feishu_logs_options(feishu_logs)
    feishu_logs.set_defaults(command_action="logs", service_key="feishu")

    feishu_describe = feishu_subparsers.add_parser(
        "describe",
        parents=[common],
        help="Print resolved Feishu account wiring as JSON.",
    )
    feishu_describe.set_defaults(command_action="describe", service_key="feishu")

    feishu_doctor = feishu_subparsers.add_parser(
        "doctor",
        parents=[common],
        help="Check Feishu health.",
    )
    _add_optional_account_argument(
        feishu_doctor,
        help_text="Feishu account id. Omit to inspect all Feishu accounts.",
    )
    feishu_doctor.set_defaults(command_action="doctor", service_key="feishu")

    discord = subparsers.add_parser("discord", parents=[common], help="Manage Discord accounts.")
    discord.set_defaults(command_action="status", service_key="discord")
    discord_subparsers = discord.add_subparsers(dest="discord_command")

    discord_setup = discord_subparsers.add_parser(
        "setup",
        parents=[common],
        help="Add or update a Discord account.",
    )
    _add_discord_add_options(discord_setup)
    discord_setup.set_defaults(command_action="add_discord", service_key="discord", auto_start=False)

    discord_remove = discord_subparsers.add_parser(
        "remove",
        parents=[common],
        help="Remove a Discord account.",
    )
    _add_required_account_argument(discord_remove, help_text="Discord account id to remove.")
    discord_remove.set_defaults(command_action="remove_discord", service_key="discord")

    discord_start = discord_subparsers.add_parser(
        "start",
        parents=[common],
        help="Start all or one Discord account.",
    )
    _add_discord_start_options(discord_start)
    discord_start.set_defaults(command_action="start", service_key="discord")

    discord_status = discord_subparsers.add_parser(
        "status",
        parents=[common],
        help="Show Discord status.",
    )
    _add_discord_status_options(discord_status)
    discord_status.set_defaults(command_action="status", service_key="discord")

    discord_stop = discord_subparsers.add_parser(
        "stop",
        parents=[common],
        help="Stop all or one Discord account.",
    )
    _add_discord_stop_options(discord_stop)
    discord_stop.set_defaults(command_action="stop", service_key="discord")

    discord_restart = discord_subparsers.add_parser(
        "restart",
        parents=[common],
        help="Restart all or one Discord account.",
    )
    _add_discord_restart_options(discord_restart)
    discord_restart.set_defaults(command_action="restart", service_key="discord")

    discord_logs = discord_subparsers.add_parser(
        "logs",
        parents=[common],
        help="Show logs for one Discord account.",
    )
    _add_discord_logs_options(discord_logs)
    discord_logs.set_defaults(command_action="logs", service_key="discord")

    discord_describe = discord_subparsers.add_parser(
        "describe",
        parents=[common],
        help="Print resolved Discord account wiring as JSON.",
    )
    discord_describe.set_defaults(command_action="describe", service_key="discord")

    discord_doctor = discord_subparsers.add_parser(
        "doctor",
        parents=[common],
        help="Check Discord health.",
    )
    _add_optional_account_argument(
        discord_doctor,
        help_text="Discord account id. Omit to inspect all Discord accounts.",
    )
    discord_doctor.set_defaults(command_action="doctor", service_key="discord")

    args = parser.parse_args(resolved_argv)
    if hasattr(args, "account_id_flag"):
        args.account_id = _resolved_cli_account_id(args)
    action = getattr(args, "command_action", None)
    if action is None:
        parser.print_help()
        return 2
    if action == "setup":
        return run_im_setup(
            default_clone_id=str(args.default_clone_id or "").strip(),
            default_profile_dir=args.profile_dir,
            default_state_dir=args.state_dir,
            default_control_profile_dir=args.cli_profile_dir,
            default_control_state_dir=args.cli_state_dir,
        )
    if action == "status_all":
        return _run_status_all(args)
    if action == "describe_all":
        app, services = _build_services(args)
        _print_json(_describe_services_payload(app, services))
        return 0
    if action == "doctor_all":
        app, services = _build_services(args)
        print("\n".join(_doctor_services_lines(app, services, args)))
        return 0
    if action == "serve_all":
        return _run_serve(args)
    if action == "add_discord":
        return _run_add_discord(args)
    if action == "add_feishu":
        return _run_add_feishu(args)
    if action == "remove_discord":
        return _run_remove_discord(args)
    if action == "remove_feishu":
        return _run_remove_feishu(args)

    service_key = str(getattr(args, "service_key", "feishu") or "feishu")
    service: object | None = None
    managed_service: GatewayManagedService | None = None

    def ensure_service() -> object:
        nonlocal service
        if service is None:
            if service_key == "discord":
                service = _build_discord_service(args)
            elif service_key == "feishu":
                service = _build_feishu_service(args)
            else:
                raise SystemExit(f"Unsupported IM service: {service_key}")
        return service

    def ensure_managed_service() -> GatewayManagedService:
        nonlocal managed_service
        if managed_service is None:
            managed_service = _build_managed_service(args, service_key=service_key)
        return managed_service

    if action == "describe":
        _print_json(_describe_payload(service_key, ensure_service()))
        return 0
    if action == "doctor":
        if service_key == "discord":
            print("\n".join(_discord_doctor_lines(ensure_service(), args)))
        else:
            print("\n".join(_doctor_lines(ensure_service(), args)))
        return 0
    if action == "status":
        return _run_status(args, service=ensure_managed_service())
    if action == "stop":
        return _run_stop(args, service=ensure_managed_service())
    if action == "restart":
        return _run_restart(args, service=ensure_managed_service())
    if action == "logs":
        return _run_logs(args, service=ensure_managed_service())
    if service_key == "discord":
        discord_service = ensure_service()
        if not isinstance(discord_service, DiscordGatewayService):
            raise TypeError("gateway service plugin 'discord' must build DiscordGatewayService")
        return _run_discord_start(discord_service, args)
    feishu_service = ensure_service()
    if not isinstance(feishu_service, FeishuGatewayService):
        raise TypeError("gateway service plugin 'feishu' must build FeishuGatewayService")
    return _run_start(feishu_service, args)

def run_im_setup(
    *,
    default_clone_id: str = "",
    default_profile_dir: Path | None = None,
    default_state_dir: Path | None = None,
    default_control_profile_dir: Path | None = None,
    default_control_state_dir: Path | None = None,
    prompt_title: str = "💬 IM Setup",
    prompt_text: str = "💬 Which IM should Aegis configure right now?",
    allow_skip: bool = False,
) -> int:
    answer = _gateway_wizard_choice_prompt(
        prompt_title,
        prompt_text,
        _im_setup_choices(allow_skip=allow_skip),
        default="skip" if allow_skip else "feishu",
        allow_back=not allow_skip,
    )
    if answer is GATEWAY_WIZARD_BACK or answer == "skip":
        return 0
    if answer not in {"feishu", "discord"}:
        raise SystemExit(f"Unsupported IM setup target: {answer}")
    argv = [str(answer), "setup", "--wizard"]
    if default_clone_id:
        argv.extend(["--default-clone-id", default_clone_id])
    return command_main(
        argv,
        default_profile_dir=default_profile_dir,
        default_state_dir=default_state_dir,
        default_control_profile_dir=default_control_profile_dir,
        default_control_state_dir=default_control_state_dir,
    )

def main(
    argv: Sequence[str] | None = None,
    *,
    default_profile_dir: Path | None = None,
    default_state_dir: Path | None = None,
    default_control_profile_dir: Path | None = None,
    default_control_state_dir: Path | None = None,
) -> int:
    return command_main(
        argv,
        default_profile_dir=default_profile_dir,
        default_state_dir=default_state_dir,
        default_control_profile_dir=default_control_profile_dir,
        default_control_state_dir=default_control_state_dir,
    )
