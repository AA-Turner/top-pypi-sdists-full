"""Gateway setup wizard helpers."""

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

@dataclass(frozen=True)
class GatewayRuntimeRecord:
    runtime_id: str
    service_key: str
    target: str
    status: str
    pid: int | None
    pid_path: str
    log_path: str
    record_path: str
    command: tuple[str, ...]
    profile_dir: str
    state_dir: str
    cli_profile_dir: str | None
    cli_state_dir: str | None
    workspace_id: str
    account_id: str | None = None
    host: str | None = None
    port: int | None = None
    started_at: str | None = None
    stopped_at: str | None = None
    last_exit_code: int | None = None
    last_error: str | None = None
    transport: str | None = None

@dataclass(slots=True)
class FeishuGatewayWizardState:
    account_id: str
    transport: str
    event_path: str
    app_id_env_var: str
    app_secret_env_var: str
    app_id_value: str
    app_secret_value: str
    enabled: bool
    default_clone_id: str
    default_session_id: str
    auto_create_clone: bool
    allow_group_chats: bool

@dataclass(slots=True)
class DiscordGatewayWizardState:
    account_id: str
    transport: str
    bot_token_value: str
    enabled: bool
    account_enabled: bool
    default_clone_id: str
    default_session_id: str
    auto_create_clone: bool
    allow_group_chats: bool
    allow_guild_ids: tuple[str, ...]
    allow_channel_ids: tuple[str, ...]

GATEWAY_WIZARD_MAX_VISIBLE_CHOICES = cli_wizard.WIZARD_MAX_VISIBLE_CHOICES
GatewayWizardChoice = cli_wizard.WizardChoice
_GatewayWizardBackSignal = cli_wizard._WizardBackSignal
GATEWAY_WIZARD_BACK = cli_wizard.WIZARD_BACK
_interactive_shell_supported = cli_wizard._interactive_shell_supported
_gateway_wizard_dialogs_supported = cli_wizard._wizard_dialogs_supported
_shared_wizard_choice_prompt = cli_wizard._wizard_choice_prompt
_shared_wizard_text_prompt = cli_wizard._wizard_text_prompt
GATEWAY_LOCAL_SECRET_ENV_FILE = "gateway-local-secrets.json"

def _gateway_wizard_choice_label(choice: GatewayWizardChoice) -> str:
    if not choice.emoji:
        return choice.label
    return f"{choice.emoji}\u00a0{choice.label}"

def _gateway_wizard_choice_window(
    total: int,
    selected: int,
    *,
    max_visible: int = GATEWAY_WIZARD_MAX_VISIBLE_CHOICES,
) -> tuple[int, int]:
    if total <= max_visible:
        return 0, total
    if selected < 0:
        selected = 0
    if selected >= total:
        selected = total - 1
    half = max_visible // 2
    start = max(0, selected - half)
    end = start + max_visible
    if end > total:
        end = total
        start = end - max_visible
    return start, end

def _gateway_wizard_choice_fragments(
    title: str,
    prompt: str,
    choices: tuple[GatewayWizardChoice, ...],
    *,
    selected: int,
    max_visible: int = GATEWAY_WIZARD_MAX_VISIBLE_CHOICES,
    allow_back: bool = False,
) -> list[tuple[str, str]]:
    fragments: list[tuple[str, str]] = [
        ("class:title", f"{title}\n"),
        ("class:prompt", f"{prompt}\n\n"),
    ]
    start, end = _gateway_wizard_choice_window(
        len(choices),
        selected,
        max_visible=max_visible,
    )
    if start > 0:
        fragments.append(("class:hint", f"↑ {start} more above\n"))
    for index in range(start, end):
        choice = choices[index]
        active = index == selected
        marker = "›" if active else " "
        label_style = "class:selected" if active else "class:item"
        detail_style = "class:selected-detail" if active else "class:detail"
        fragments.append((label_style, f"{marker} {_gateway_wizard_choice_label(choice)}\n"))
        fragments.append((detail_style, f"  {choice.detail}\n"))
    if end < len(choices):
        fragments.append(("class:hint", f"↓ {len(choices) - end} more below\n"))
    if allow_back:
        fragments.append(("class:hint", "\nEnter confirms · Esc goes back · ↑/↓ or j/k moves"))
    else:
        fragments.append(("class:hint", "\nEnter confirms · ↑/↓ or j/k moves"))
    return fragments

def _gateway_wizard_choice_menu(
    title: str,
    prompt: str,
    choices: tuple[GatewayWizardChoice, ...],
    *,
    default: str,
    allow_back: bool = False,
) -> str | _GatewayWizardBackSignal:
    if not (
        PROMPT_TOOLKIT_DIALOGS_AVAILABLE
        and Application is not None
        and PromptKeyBindings is not None
        and HSplit is not None
        and Window is not None
        and FormattedTextControl is not None
        and Layout is not None
    ):
        return default
    selected = next(
        (index for index, choice in enumerate(choices) if choice.value == default),
        0,
    )
    result: dict[str, str] = {"value": default}

    def render():
        return _gateway_wizard_choice_fragments(
            title,
            prompt,
            choices,
            selected=selected,
            allow_back=allow_back,
        )

    control = FormattedTextControl(render)
    bindings = PromptKeyBindings()

    @bindings.add("down")
    @bindings.add("j")
    def _move_down(event) -> None:
        nonlocal selected
        selected = (selected + 1) % len(choices)
        event.app.invalidate()

    @bindings.add("up")
    @bindings.add("k")
    def _move_up(event) -> None:
        nonlocal selected
        selected = (selected - 1) % len(choices)
        event.app.invalidate()

    @bindings.add("tab")
    def _move_tab(event) -> None:
        nonlocal selected
        selected = (selected + 1) % len(choices)
        event.app.invalidate()

    @bindings.add("enter")
    def _accept(event) -> None:
        result["value"] = choices[selected].value
        event.app.exit(result=result["value"])

    @bindings.add("escape")
    def _cancel(event) -> None:
        event.app.exit(result=GATEWAY_WIZARD_BACK if allow_back else default)

    application = Application(
        layout=Layout(HSplit([Window(content=control)])),
        key_bindings=bindings,
        style=_gateway_wizard_style(),
        full_screen=True,
        erase_when_done=True,
    )
    answer = application.run()
    if answer is GATEWAY_WIZARD_BACK:
        return GATEWAY_WIZARD_BACK
    return str(answer or default)

def _gateway_prompt_value(
    label: str,
    *,
    default: str | None = None,
    preserve_default_on_empty: bool = True,
) -> str:
    suffix = f" [{default}]" if default else ""
    answer = input(f"{label}{suffix}: ").strip()
    if answer:
        return answer
    if preserve_default_on_empty:
        return default or ""
    return ""

def _gateway_wizard_text_prompt(
    title: str,
    prompt: str,
    *,
    default: str | None = None,
    allow_back: bool = False,
    preserve_default_on_empty: bool = True,
) -> str | _GatewayWizardBackSignal:
    if _gateway_wizard_dialogs_supported():
        answer = _shared_wizard_text_prompt(
            title,
            prompt,
            default=default,
            allow_back=allow_back,
            preserve_default_on_empty=preserve_default_on_empty,
        )
        if answer is GATEWAY_WIZARD_BACK:
            return GATEWAY_WIZARD_BACK
        return str(answer)
    return _gateway_prompt_value(
        prompt,
        default=default,
        preserve_default_on_empty=preserve_default_on_empty,
    )

def _gateway_wizard_choice_prompt(
    title: str,
    prompt: str,
    choices: tuple[GatewayWizardChoice, ...],
    *,
    default: str | None = None,
    allow_back: bool = False,
) -> str | _GatewayWizardBackSignal:
    if not choices:
        return default or ""
    default_value = default or choices[0].value
    if _gateway_wizard_dialogs_supported():
        answer = _shared_wizard_choice_prompt(
            title,
            prompt,
            choices,
            default=default_value,
            allow_back=allow_back,
        )
        if answer is GATEWAY_WIZARD_BACK:
            return GATEWAY_WIZARD_BACK
        return str(answer)
    print(prompt)
    for index, choice in enumerate(choices, start=1):
        marker = "*" if choice.value == default_value else " "
        print(f"  {marker} {index}. {_gateway_wizard_choice_label(choice)} :: {choice.detail}")
    while True:
        answer = input(f"choice [{default_value}]: ").strip()
        if not answer:
            return default_value
        if allow_back and answer.casefold() in {"back", "b"}:
            return GATEWAY_WIZARD_BACK
        if answer.isdigit():
            index = int(answer)
            if 1 <= index <= len(choices):
                return choices[index - 1].value
        normalized = answer.casefold()
        for choice in choices:
            if normalized in {choice.value.casefold(), choice.label.casefold()}:
                return choice.value
        print("  choose a listed number, transport id, or label.")

def _gateway_bool_choices(
    *,
    enabled_label: str,
    enabled_detail: str,
    disabled_label: str,
    disabled_detail: str,
) -> tuple[GatewayWizardChoice, GatewayWizardChoice]:
    return (
        GatewayWizardChoice(
            value="yes",
            label=enabled_label,
            detail=enabled_detail,
            emoji="✅",
        ),
        GatewayWizardChoice(
            value="no",
            label=disabled_label,
            detail=disabled_detail,
            emoji="➖",
        ),
    )

def _gateway_bool_prompt(
    title: str,
    prompt: str,
    *,
    default: bool,
    enabled_label: str,
    enabled_detail: str,
    disabled_label: str,
    disabled_detail: str,
    allow_back: bool = False,
) -> bool | _GatewayWizardBackSignal:
    answer = _gateway_wizard_choice_prompt(
        title,
        prompt,
        _gateway_bool_choices(
            enabled_label=enabled_label,
            enabled_detail=enabled_detail,
            disabled_label=disabled_label,
            disabled_detail=disabled_detail,
        ),
        default="yes" if default else "no",
        allow_back=allow_back,
    )
    if answer is GATEWAY_WIZARD_BACK:
        return GATEWAY_WIZARD_BACK
    return str(answer) == "yes"

def _feishu_transport_choices() -> tuple[GatewayWizardChoice, ...]:
    details = {
        "long-connection": "Use Feishu long connection for a local bridge without webhook setup.",
    }
    return tuple(
        GatewayWizardChoice(
            value=transport,
            label=transport.replace("-", " ").title(),
            detail=details.get(transport, "Use this Feishu ingress transport."),
            emoji="🛰️",
        )
        for transport in SUPPORTED_FEISHU_TRANSPORTS
    )

def _discord_transport_choices() -> tuple[GatewayWizardChoice, ...]:
    details = {
        "gateway": "Use the managed Discord gateway runtime for local IM bring-up.",
    }
    return tuple(
        GatewayWizardChoice(
            value=transport,
            label=transport.replace("-", " ").title(),
            detail=details.get(transport, "Use this Discord ingress transport."),
            emoji="💬",
        )
        for transport in SUPPORTED_DISCORD_TRANSPORTS
    )

def _im_setup_choices(*, allow_skip: bool) -> tuple[GatewayWizardChoice, ...]:
    choices: list[GatewayWizardChoice] = [
        GatewayWizardChoice(
            value="feishu",
            label="Feishu",
            detail="Wire a Feishu bot into Aegis Gateway and route plain text into your local clone runtime.",
            emoji="🪽",
        ),
        GatewayWizardChoice(
            value="discord",
            label="Discord",
            detail="Wire a Discord bot into Aegis Gateway and route messages from DMs, channels, and threads.",
            emoji="💬",
        ),
    ]
    if allow_skip:
        choices.append(
            GatewayWizardChoice(
                value="skip",
                label="Skip for now",
                detail="Stay local for now. You can always run `aegis gateway` later.",
                emoji="➖",
            )
        )
    return tuple(choices)

def _center_brand_block(renderable):
    if Align is None:
        return renderable
    return Align.center(renderable)

def _confirm_gateway_wizard_intro() -> bool:
    return True

def _print_gateway_feishu_wizard_intro() -> bool:
    if not RICH_AVAILABLE or Table is None or Panel is None or Group is None:
        print("💬 Aegis Gateway // Feishu setup")
        print("  - choose the Feishu account you want to wire")
        print("  - bind App ID and App Secret cleanly")
        print("  - keep profile wiring and local credentials separate")
        print("  - check Bot, Events, Long Connection, and Permissions in Feishu")
        return True
    console = Console(highlight=False, soft_wrap=True)
    brand = Table.grid(expand=True)
    brand.add_column(no_wrap=True)
    hero = Text(justify="center")
    hero.append("💬 Bring Feishu into Aegis Gateway.\n", style=f"bold {BRAND_LIGHT}")
    hero.append(
        "A short setup flow for wiring credentials, clone routing, and the Feishu console path with less friction.",
        style=BRAND_MUTED,
    )
    flow = Text()
    flow.append("🧭 IM setup flow\n", style=f"bold {BRAND_ACCENT}")
    flow.append("1 · Choose the Feishu account and long-connection surface\n", style=BRAND_LIGHT)
    flow.append("2 · Paste App ID and App Secret directly into the local IM secret store\n", style=BRAND_LIGHT)
    flow.append("3 · Decide how the control bridge routes clones\n", style=BRAND_LIGHT)
    flow.append("4 · Start the bridge with credentials kept out of profile.json", style=BRAND_LIGHT)
    portal = Text()
    portal.append("Feishu console checklist\n", style=f"bold {BRAND_ACCENT}")
    portal.append("Capability · Add App Capability → Bot\n", style=BRAND_LIGHT)
    portal.append("Events · Event Subscriptions → add `im.message.receive_v1`\n", style=BRAND_LIGHT)
    portal.append("Transport · Use Long Connection for local IM bring-up\n", style=BRAND_LIGHT)
    portal.append(
        "Permissions · Enable `im:message`, `im:message.p2p_msg:readonly`, and `im:message:send_as_bot`",
        style=BRAND_LIGHT,
    )
    brand.add_row(_center_brand_block(hero))
    brand.add_row(Text(" "))
    brand.add_row(_center_brand_block(render_guardian_mark()))
    brand.add_row(Text(" "))
    content = Table.grid(expand=True)
    console_width = getattr(console.size, "width", 0)
    if console_width and console_width < 148:
        content.add_column(ratio=1, min_width=52)
        content.add_row(brand)
        content.add_row(Text(" "))
        content.add_row(flow)
        content.add_row(Text(" "))
        content.add_row(portal)
    else:
        content.add_column(ratio=11, min_width=42)
        content.add_column(ratio=12, min_width=44)
        content.add_column(ratio=12, min_width=44)
        content.add_row(brand, flow, portal)
    console.print(
        Panel(
            content,
            title=f"[bold {BRAND_ACCENT}] IM Feishu Setup v{_resolve_aegis_version()} [/bold {BRAND_ACCENT}]",
            subtitle="[bold {brand}]Polished local bridge setup for Feishu.[/bold {brand}]".replace(
                "{brand}",
                BRAND_LIGHT,
            ),
            border_style=BRAND_ACCENT,
            padding=(1, 2),
        )
    )
    return _confirm_gateway_wizard_intro()

def _print_gateway_discord_wizard_intro() -> bool:
    if not RICH_AVAILABLE or Table is None or Panel is None or Group is None:
        print("💬 Aegis Gateway // Discord setup")
        print("💬 Bring Discord into Aegis Gateway.")
        print("  - choose the Discord account you want to wire")
        print("  - paste the bot token directly into the local IM secret store")
        print("  - choose which clone and session Discord should route into")
        print("  - keep profile wiring and local credentials separate")
        print("  - start the gateway bridge after setup")
        print("Discord portal checklist")
        print("  - check OAuth2 invite scope, MESSAGE_CONTENT, and bot permissions in Discord")
        return True
    console = Console(highlight=False, soft_wrap=True)
    brand = Table.grid(expand=True)
    brand.add_column(no_wrap=True)
    hero = Text(justify="center")
    hero.append("💬 Bring Discord into Aegis Gateway.\n", style=f"bold {BRAND_LIGHT}")
    hero.append(
        "A short setup flow for wiring the bot token, clone routing, and Discord portal steps with less friction.",
        style=BRAND_MUTED,
    )
    flow = Text()
    flow.append("🧭 IM setup flow\n", style=f"bold {BRAND_ACCENT}")
    flow.append("1 · Choose the Discord account and managed gateway surface\n", style=BRAND_LIGHT)
    flow.append("2 · Paste the bot token directly into the local IM secret file\n", style=BRAND_LIGHT)
    flow.append(
        "3 · Choose the clone Discord should route new conversations into, or pin a known session\n",
        style=BRAND_LIGHT,
    )
    flow.append(
        "4 · Decide whether Discord is active in profile views and default runtime starts, then launch the bridge",
        style=BRAND_LIGHT,
    )
    portal = Text()
    portal.append("Discord portal checklist\n", style=f"bold {BRAND_ACCENT}")
    portal.append("OAuth2 · URL Generator → include the `bot` scope when inviting the app\n", style=BRAND_LIGHT)
    portal.append("Bot · Privileged Gateway Intents → enable `MESSAGE_CONTENT`\n", style=BRAND_LIGHT)
    portal.append(
        "Permissions · Grant `View Channels`, `Send Messages`, `Send Messages in Threads`, and `Read Message History`\n",
        style=BRAND_LIGHT,
    )
    portal.append("Runtime · Start with `aegis gateway discord start`", style=BRAND_LIGHT)
    brand.add_row(_center_brand_block(hero))
    brand.add_row(Text(" "))
    brand.add_row(_center_brand_block(render_guardian_mark()))
    brand.add_row(Text(" "))
    content = Table.grid(expand=True)
    console_width = getattr(console.size, "width", 0)
    if console_width and console_width < 148:
        content.add_column(ratio=1, min_width=52)
        content.add_row(brand)
        content.add_row(Text(" "))
        content.add_row(flow)
        content.add_row(Text(" "))
        content.add_row(portal)
    else:
        content.add_column(ratio=11, min_width=42)
        content.add_column(ratio=12, min_width=44)
        content.add_column(ratio=12, min_width=44)
        content.add_row(brand, flow, portal)
    console.print(
        Panel(
            content,
            title=f"[bold {BRAND_ACCENT}] IM Discord Setup v{_resolve_aegis_version()} [/bold {BRAND_ACCENT}]",
            subtitle="[bold {brand}]Polished local bridge setup for Discord.[/bold {brand}]".replace(
                "{brand}",
                BRAND_LIGHT,
            ),
            border_style=BRAND_ACCENT,
            padding=(1, 2),
        )
    )
    return True

def _gateway_wizard_secret_prompt(
    title: str,
    prompt: str,
    *,
    allow_back: bool = False,
) -> str | _GatewayWizardBackSignal:
    if _gateway_wizard_dialogs_supported():
        answer = _shared_wizard_text_prompt(
            title,
            prompt,
            allow_back=allow_back,
            password=True,
        )
        if answer is GATEWAY_WIZARD_BACK:
            return GATEWAY_WIZARD_BACK
        return str(answer).strip()
    hint = " (leave blank to keep the current local value" + (", type back to return" if allow_back else "") + ")"
    answer = getpass.getpass(f"{prompt}{hint}: ").strip()
    if allow_back and answer.casefold() == "back":
        return GATEWAY_WIZARD_BACK
    return answer

def _print_gateway_setup_paused(service_name: str) -> None:
    print(f"{service_name} IM setup paused")
    print("  No IM changes were written.")
    print("  next_commands:")
    print("  - aegis gateway")
    print("  - aegis gateway doctor")

def _ensure_feishu_sdk_available(*, reason: str) -> bool:
    if importlib.util.find_spec("lark_oapi") is not None:
        return False
    command = [
        sys.executable,
        "-m",
        "pip",
        "install",
        "--disable-pip-version-check",
        FEISHU_SDK_PIP_SPEC,
    ]
    print(f"Preparing Feishu support for {reason}...")
    try:
        subprocess.run(command, check=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        rendered = " ".join(shlex.quote(part) for part in command)
        raise SystemExit(
            "Aegis could not automatically install the Feishu SDK. "
            f"Run `{rendered}` and retry."
        ) from exc
    if importlib.util.find_spec("lark_oapi") is None:
        rendered = " ".join(shlex.quote(part) for part in command)
        raise SystemExit(
            "Aegis finished the Feishu SDK install command, but `lark_oapi` is still unavailable. "
            f"Run `{rendered}` manually and retry."
        )
    print("Feishu support is ready.")
    return True

def _ensure_discord_sdk_available(*, reason: str) -> bool:
    if importlib.util.find_spec("discord") is not None:
        return False
    command = [
        sys.executable,
        "-m",
        "pip",
        "install",
        "--disable-pip-version-check",
        DISCORD_PY_PIP_SPEC,
    ]
    print(f"Preparing Discord support for {reason}...")
    try:
        subprocess.run(command, check=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        rendered = " ".join(shlex.quote(part) for part in command)
        raise SystemExit(
            "Aegis could not automatically install Discord support. "
            f"Run `{rendered}` and retry."
        ) from exc
    if importlib.util.find_spec("discord") is None:
        rendered = " ".join(shlex.quote(part) for part in command)
        raise SystemExit(
            "Aegis finished the Discord install command, but `discord.py` is still unavailable. "
            f"Run `{rendered}` manually and retry."
        )
    print("Discord support is ready.")
    return True

def _parse_gateway_id_csv(value: str) -> tuple[str, ...]:
    return tuple(dict.fromkeys(part.strip() for part in value.split(",") if part.strip()))

def _load_gateway_control_runtime(
    *,
    profile_dir: Path | None,
    state_dir: Path | None,
) -> CliRuntime | None:
    if profile_dir is None or state_dir is None:
        return None
    database_path = state_dir / "aegis.sqlite3"
    if not profile_dir.exists() or not state_dir.exists() or not database_path.exists():
        return None
    try:
        return CliRuntime.create(profile_dir=profile_dir, state_dir=state_dir)
    except (OSError, RuntimeError, ValueError, TypeError, KeyError, json.JSONDecodeError):
        return None

def _gateway_clone_choices(
    runtime: CliRuntime,
    *,
    current_clone_id: str,
) -> tuple[GatewayWizardChoice, ...]:
    choices: list[GatewayWizardChoice] = [
        GatewayWizardChoice(
            value=_GATEWAY_NO_DEFAULT_CLONE,
            label="No default clone",
            detail="Leave new IM conversations unpinned until you bind them explicitly.",
            emoji="➖",
        )
    ]
    known_clone_ids: set[str] = set()
    for clone in runtime.list_clones(limit=12):
        clone_id = str(getattr(clone, "clone_id", "")).strip()
        if not clone_id:
            continue
        known_clone_ids.add(clone_id)
        latest_session_id = str(getattr(clone, "latest_session_id", "")).strip()
        latest_status = str(getattr(clone, "latest_status", "")).strip() or "unknown"
        session_count = int(getattr(clone, "session_count", 0) or 0)
        choices.append(
            GatewayWizardChoice(
                value=clone_id,
                label=clone_id,
                detail=(
                    f"latest {latest_session_id[:8] or '<none>'} · "
                    f"{session_count} session{'s' if session_count != 1 else ''} · {latest_status}"
                ),
                emoji="🧬",
            )
        )
    current = current_clone_id.strip()
    if current and current not in known_clone_ids:
        choices.append(
            GatewayWizardChoice(
                value=current,
                label=f"Keep configured clone ({current})",
                detail="Reuse the existing clone id even though it is not in the current local list.",
                emoji="🧭",
            )
        )
    choices.append(
        GatewayWizardChoice(
            value=_GATEWAY_MANUAL_CLONE,
            label="Enter clone id manually",
            detail="Type a clone id when you want to route to a clone that is not in the current list yet.",
            emoji="🆔",
        )
    )
    return tuple(choices)

def _gateway_session_choices(
    runtime: CliRuntime,
    *,
    clone_id: str,
    current_session_id: str,
) -> tuple[GatewayWizardChoice, ...]:
    session_ids = runtime.session_ids_for_clone(clone_id)
    if not session_ids:
        return ()
    choices: list[GatewayWizardChoice] = [
        GatewayWizardChoice(
            value=_GATEWAY_FOLLOW_LATEST_SESSION,
            label="Follow latest session",
            detail="Route unpinned messages into the newest local session for this clone.",
            emoji="🔄",
        )
    ]
    known_session_ids: set[str] = set()
    for index, session_id in enumerate(session_ids):
        known_session_ids.add(session_id)
        try:
            session = runtime.inspect_session(session_id)
        except KeyError:
            detail = "session metadata unavailable"
        else:
            updated_at = getattr(session.updated_at, "isoformat", lambda: str(session.updated_at))()
            detail = f"{session.status} · updated {updated_at}"
            if session.parent_session_id:
                detail += f" · resumed from {session.parent_session_id[:8]}"
            if index == 0:
                detail += " · latest"
        choices.append(
            GatewayWizardChoice(
                value=session_id,
                label=session_id,
                detail=detail,
                emoji="🧵",
            )
        )
    current = current_session_id.strip()
    if current and current not in known_session_ids:
        choices.append(
            GatewayWizardChoice(
                value=current,
                label=f"Keep configured session ({current})",
                detail="Reuse the existing session id even though it is not in the current local list.",
                emoji="🧭",
            )
        )
    return tuple(choices)

def _prompt_gateway_control_binding(
    *,
    runtime: CliRuntime | None,
    current_clone_id: str,
    current_session_id: str,
    allow_back: bool = False,
) -> tuple[str, str] | _GatewayWizardBackSignal:
    resolved_clone_id = current_clone_id.strip()
    resolved_session_id = current_session_id.strip()
    if runtime is None:
        answer = _gateway_wizard_text_prompt(
            "Default Clone",
            "Optional: which clone should plain text fall back to before a thread is pinned? Leave blank to require an explicit bind.",
            default=resolved_clone_id or None,
            allow_back=allow_back,
            preserve_default_on_empty=False,
        )
        if answer is GATEWAY_WIZARD_BACK:
            return GATEWAY_WIZARD_BACK
        clone_id = str(answer).strip()
        if not clone_id:
            return "", ""
        session_id = resolved_session_id if clone_id == resolved_clone_id else ""
        return clone_id, session_id

    while True:
        clone_choices = _gateway_clone_choices(runtime, current_clone_id=resolved_clone_id)
        default_clone_choice = resolved_clone_id or _GATEWAY_NO_DEFAULT_CLONE
        clone_answer = _gateway_wizard_choice_prompt(
            "Default Clone",
            "Choose which active clone new IM conversations should use before the thread is pinned.",
            clone_choices,
            default=default_clone_choice,
            allow_back=allow_back,
        )
        if clone_answer is GATEWAY_WIZARD_BACK:
            return GATEWAY_WIZARD_BACK
        if clone_answer == _GATEWAY_NO_DEFAULT_CLONE:
            return "", ""
        if clone_answer == _GATEWAY_MANUAL_CLONE:
            manual = _gateway_wizard_text_prompt(
                "Default Clone",
                "Type the clone id to use for new IM conversations before the thread is pinned.",
                default=resolved_clone_id or None,
                allow_back=allow_back,
                preserve_default_on_empty=False,
            )
            if manual is GATEWAY_WIZARD_BACK:
                continue
            clone_id = str(manual).strip()
            if not clone_id:
                return "", ""
        else:
            clone_id = str(clone_answer).strip()
        current_clone_session_id = resolved_session_id if clone_id == resolved_clone_id else ""
        known_session_ids = tuple(runtime.session_ids_for_clone(clone_id))
        if not known_session_ids:
            return clone_id, ""
        if len(known_session_ids) == 1:
            only_session_id = known_session_ids[0].strip()
            if not current_clone_session_id or current_clone_session_id == only_session_id:
                return clone_id, only_session_id
        session_choices = _gateway_session_choices(
            runtime,
            clone_id=clone_id,
            current_session_id=current_clone_session_id,
        )
        if not session_choices:
            return clone_id, ""
        default_session_choice = (
            resolved_session_id
            if clone_id == resolved_clone_id and resolved_session_id
            else _GATEWAY_FOLLOW_LATEST_SESSION
        )
        session_answer = _gateway_wizard_choice_prompt(
            "Default Session",
            f"Optional: pick a known local session for clone `{clone_id}`, or follow its latest session automatically.",
            session_choices,
            default=default_session_choice,
            allow_back=allow_back,
        )
        if session_answer is GATEWAY_WIZARD_BACK:
            continue
        if session_answer == _GATEWAY_FOLLOW_LATEST_SESSION:
            return clone_id, ""
        return clone_id, str(session_answer).strip()

def _run_interactive_feishu_wizard(
    *,
    account_id: str,
    transport: str,
    event_path: str,
    app_id_env_var: str,
    app_secret_env_var: str,
    app_id_value: str,
    app_secret_value: str,
    enabled: bool,
    default_clone_id: str,
    default_session_id: str,
    auto_create_clone: bool,
    allow_group_chats: bool,
    cli_profile_dir: Path | None,
    cli_state_dir: Path | None,
) -> FeishuGatewayWizardState | None:
    state = FeishuGatewayWizardState(
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
    )
    control_runtime = _load_gateway_control_runtime(
        profile_dir=cli_profile_dir,
        state_dir=cli_state_dir,
    )
    steps = (
        "app_id_value",
        "app_secret_value",
        "control_binding",
    )
    step_index = 0
    while step_index < len(steps):
        step = steps[step_index]
        if step == "app_id_value":
            answer = _gateway_wizard_text_prompt(
                "Paste App ID",
                "Paste the Feishu App ID to store it in the local IM secret file. Leave blank to keep the current local value if one already exists.",
                default=None,
                allow_back=True,
                preserve_default_on_empty=False,
            )
            if answer is GATEWAY_WIZARD_BACK:
                return None
            state.app_id_value = str(answer).strip()
            step_index += 1
            continue
        if step == "app_secret_value":
            answer = _gateway_wizard_secret_prompt(
                "Paste App Secret",
                "Paste the Feishu App Secret / API key to store it in the local IM secret file.",
                allow_back=True,
            )
            if answer is GATEWAY_WIZARD_BACK:
                step_index -= 1
                continue
            state.app_secret_value = str(answer).strip()
            step_index += 1
            continue
        if step == "control_binding":
            answer = _prompt_gateway_control_binding(
                runtime=control_runtime,
                current_clone_id=state.default_clone_id,
                current_session_id=state.default_session_id,
                allow_back=True,
            )
            if answer is GATEWAY_WIZARD_BACK:
                step_index -= 1
                continue
            state.default_clone_id, state.default_session_id = answer
            step_index += 1
            continue
    return state

def _run_interactive_discord_wizard(
    *,
    account_id: str,
    transport: str,
    bot_token_value: str,
    enabled: bool,
    account_enabled: bool,
    default_clone_id: str,
    default_session_id: str,
    auto_create_clone: bool,
    allow_group_chats: bool,
    allow_guild_ids: Sequence[str],
    allow_channel_ids: Sequence[str],
    cli_profile_dir: Path | None,
    cli_state_dir: Path | None,
) -> DiscordGatewayWizardState | None:
    state = DiscordGatewayWizardState(
        account_id=account_id,
        transport=transport,
        bot_token_value=bot_token_value,
        enabled=enabled,
        account_enabled=account_enabled,
        default_clone_id=default_clone_id,
        default_session_id=default_session_id,
        auto_create_clone=auto_create_clone,
        allow_group_chats=allow_group_chats,
        allow_guild_ids=tuple(str(value).strip() for value in allow_guild_ids if str(value).strip()),
        allow_channel_ids=tuple(str(value).strip() for value in allow_channel_ids if str(value).strip()),
    )
    control_runtime = _load_gateway_control_runtime(
        profile_dir=cli_profile_dir,
        state_dir=cli_state_dir,
    )
    steps = (
        "bot_token_value",
        "control_binding",
    )
    step_index = 0
    while step_index < len(steps):
        step = steps[step_index]
        if step == "bot_token_value":
            answer = _gateway_wizard_secret_prompt(
                "Paste Bot Token",
                "Paste the Discord bot token to store it in the local IM secret file.",
                allow_back=True,
            )
            if answer is GATEWAY_WIZARD_BACK:
                return None
            state.bot_token_value = str(answer).strip()
            step_index += 1
            continue
        if step == "control_binding":
            answer = _prompt_gateway_control_binding(
                runtime=control_runtime,
                current_clone_id=state.default_clone_id,
                current_session_id=state.default_session_id,
                allow_back=True,
            )
            if answer is GATEWAY_WIZARD_BACK:
                step_index -= 1
                continue
            state.default_clone_id, state.default_session_id = answer
            step_index += 1
            continue
    return state

__all__ = [
    "GATEWAY_LOCAL_SECRET_ENV_FILE",
    "GatewayRuntimeRecord",
    "FeishuGatewayWizardState",
    "DiscordGatewayWizardState",
    "_gateway_wizard_choice_label",
    "_gateway_wizard_choice_window",
    "_gateway_wizard_choice_fragments",
    "_gateway_wizard_choice_menu",
    "_gateway_prompt_value",
    "_gateway_wizard_text_prompt",
    "_gateway_wizard_choice_prompt",
    "_gateway_bool_choices",
    "_gateway_bool_prompt",
    "_feishu_transport_choices",
    "_discord_transport_choices",
    "_im_setup_choices",
    "_center_brand_block",
    "_confirm_gateway_wizard_intro",
    "_print_gateway_feishu_wizard_intro",
    "_print_gateway_discord_wizard_intro",
    "_gateway_wizard_secret_prompt",
    "_print_gateway_setup_paused",
    "_ensure_feishu_sdk_available",
    "_ensure_discord_sdk_available",
    "_parse_gateway_id_csv",
    "_load_gateway_control_runtime",
    "_gateway_clone_choices",
    "_gateway_session_choices",
    "_prompt_gateway_control_binding",
    "_run_interactive_feishu_wizard",
    "_run_interactive_discord_wizard",
]
