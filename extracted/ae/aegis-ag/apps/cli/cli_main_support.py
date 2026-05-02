"""Formatting, parser, and shared support for the CLI entrypoint."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import os
import random
import re
import sys
from collections.abc import Iterable
from pathlib import Path

from packages.state import DEFAULT_CLONE_TEXT, render_clone_charter

from .runtime import CliRuntime
from .provider_flow import (
    DELIBERATE_MODEL_LABEL,
    ProviderSelectionState,
    SWIFT_MODEL_LABEL,
    provider_choices as _shared_provider_choices,
    provider_setup_defaults,
    run_provider_selection_wizard,
)

_provider_choices = _shared_provider_choices
from .shell import (
    Align,
    BRAND_ACCENT,
    BRAND_LIGHT,
    BRAND_MUTED,
    Console,
    Group,
    Panel,
    ProductizedShell,
    RICH_AVAILABLE,
    Table,
    Text,
    _resolve_aegis_version,
    render_guardian_mark,
)
from .wizard import (
    WIZARD_BACK,
    WizardChoice,
    _WizardBackSignal,
    _interactive_shell_supported,
    _wizard_choice_prompt,
    _wizard_dialogs_supported,
    _wizard_text_prompt,
)

DEFAULT_PROVIDER_ID = "openai-compatible"
DEFAULT_CLONE_INITIAL_GOAL = "Carry the next durable thread."
DEFAULT_CLONE_NAME_SUGGESTIONS = (
    "Ada",
    "Asher",
    "Avery",
    "Caleb",
    "Chloe",
    "Eden",
    "Eli",
    "Eliza",
    "Felix",
    "Hazel",
    "Iris",
    "Jasper",
    "Julian",
    "Leah",
    "Lena",
    "Leo",
    "Maya",
    "Miles",
    "Milo",
    "Nina",
    "Nora",
    "Owen",
    "Ruby",
    "Rowan",
    "Simon",
    "Silas",
    "Theo",
    "Vera",
    "Zoe",
)
CLI_THEME_TITLE_GLYPH = "🐣"
CLI_THEME_BULLET = "•"
CLI_THEME_WELCOME_GLYPH = "🤝"
CLI_THEME_SUBTITLE = "🧠 Your enduring AI companion, keeping the thread beside you."
CLI_COMMAND_GLYPHS = (
    ("aegis init", "🐣"),
    ("aegis status", "📋"),
    ("aegis wake", "🌙"),
    ("aegis clone", "🐣"),
    ("aegis skills", "📚"),
    ("aegis provider", "🧠"),
    ("aegis gateway", "💬"),
    ("aegis dashboard", "📊"),
)


@dataclass(frozen=True, slots=True)
class CliCardSection:
    title: str
    lines: tuple[str, ...] = ()

class _WizardCancelledError(Exception):
    __slots__ = ("surface",)

    def __init__(self, surface: str) -> None:
        super().__init__(surface)
        self.surface = surface

@dataclass(slots=True)
class BirthWizardState:
    display_name: str
    provider_id: str
    base_url: str
    strong_model: str
    weak_model: str
    intent_mode: str
    api_key: str | None
    reasoning_effort: str | None
    context_window_mode: str
    context_window_tokens: int | None

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="aegis",
        description="Aegis CLI with explicit init, provider, status, clone, clones, and wake entrypoints.",
    )
    parser.add_argument("--state-dir", required=True, type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--profile-dir", required=True, type=Path, help=argparse.SUPPRESS)

    subparsers = parser.add_subparsers(dest="command")

    def _add_init_parser(name: str, *, hidden: bool = False) -> None:
        init = subparsers.add_parser(
            name,
            help=argparse.SUPPRESS if hidden else "Run first-time setup and persist identity, provider readiness, and the first clone session.",
        )
        init.add_argument("--provider-id", default=DEFAULT_PROVIDER_ID)
        init.add_argument("--display-name", default=None)
        init.add_argument("--clone-text", default=None)
        init.add_argument("--clone-name", default=None)
        init.add_argument("--initial-goal", default=None)
        init.add_argument("--base-url", default=None)
        init.add_argument("--strong-model", default=None)
        init.add_argument("--default-model", dest="strong_model", default=None, help=argparse.SUPPRESS)
        init.add_argument("--weak-model", default=None)
        init.add_argument("--intent-mode", default=None)
        init.add_argument("--api-key", default=None)
        init.add_argument("--secret-env-var", default=None)
        init.add_argument("--context-window-mode", default=None)
        init.add_argument("--context-window", default=None)
        init.add_argument("--non-interactive", action="store_true")

    def _add_status_parser(name: str, *, hidden: bool = False) -> None:
        subparsers.add_parser(
            name,
            help=argparse.SUPPRESS if hidden else "Review provider, model, and security readiness before opening the wake surface.",
        )

    def _add_provider_parser(name: str, *, hidden: bool = False) -> None:
        provider = subparsers.add_parser(
            name,
            help=argparse.SUPPRESS if hidden else "Configure or inspect the active provider, model, reasoning effort, and context window.",
        )
        provider.add_argument(
            "provider_command",
            nargs="?",
            default="configure",
            choices=("configure", "status", "providers", "models"),
            help="Choose whether to configure the active provider or inspect provider/model inventory.",
        )
        provider.add_argument("--provider-id", default=None)
        provider.add_argument("--base-url", default=None)
        provider.add_argument("--strong-model", default=None)
        provider.add_argument("--default-model", dest="strong_model", default=None, help=argparse.SUPPRESS)
        provider.add_argument("--weak-model", default=None)
        provider.add_argument("--intent-mode", default=None)
        provider.add_argument("--api-key", default=None)
        provider.add_argument("--reasoning-effort", default=None)
        provider.add_argument("--context-window-mode", default=None)
        provider.add_argument("--context-window", default=None)
        provider.add_argument("--non-interactive", action="store_true")

    def _add_wake_parser(name: str, *, hidden: bool = False) -> None:
        wake = subparsers.add_parser(
            name,
            help=argparse.SUPPRESS if hidden else "Enter an existing Aegis clone through the branded TUI or run one provider-backed turn.",
        )
        wake.add_argument("--session-id", default=None, help="Open a known session directly.")
        wake.add_argument("--clone-id", default=None, help="Open the latest session for a known clone.")
        wake.add_argument("--debug", action="store_true", help="Show runtime diagnostics inside the wake surface.")
        wake.add_argument("--message", default=None, help="Run one wake turn and exit.")
        wake.add_argument(
            "--voice-input-file",
            default=None,
            type=Path,
            help="Run one provider-backed voice turn from an audio file and exit.",
        )
        wake.add_argument(
            "--voice-output-file",
            default=None,
            type=Path,
            help="Write one synthesized voice reply when voice output is enabled.",
        )
        wake.add_argument("--voice-input-model", default="gpt-4o-mini-transcribe")
        wake.add_argument("--voice-output-model", default="gpt-4o-mini-tts")
        wake.add_argument("--voice-name", default="alloy")

    _add_init_parser("init")
    _add_status_parser("status")
    _add_provider_parser("provider")

    clone = subparsers.add_parser(
        "clone",
        help="Clone a fresh Aegis individual and optionally enter it immediately.",
    )
    clone.add_argument("clone_name", nargs="?", help="Name the new Aegis clone.")
    clone.add_argument("--profile-id", default=None)
    clone.add_argument("--display-name", default=None)
    clone.add_argument("--initial-goal", default=None, help="Optionally seed the clone with its first durable goal.")
    clone.add_argument("--debug", action="store_true", help="Show runtime diagnostics inside the wake surface.")
    clone.add_argument("--message", default=None, help="Create the clone, run one turn, and exit.")

    clones = subparsers.add_parser(
        "clones",
        help="Inspect or retire existing Aegis clones.",
    )
    clones_subparsers = clones.add_subparsers(dest="clones_command")
    clone_sessions = clones_subparsers.add_parser(
        "sessions",
        help="List the durable sessions currently attached to one named clone.",
    )
    clone_sessions.add_argument("clone_id", help="Name the Aegis clone to inspect.")
    bye = clones_subparsers.add_parser(
        "bye",
        help="Retire one named clone or clear every clone.",
    )
    bye.add_argument("clone_id", nargs="?", help="Name the Aegis clone to retire.")
    bye.add_argument("--all", action="store_true", dest="delete_all", help="Retire every clone.")

    _add_wake_parser("wake")

    return parser

def _print_heading(title: str, detail: str | None = None) -> None:
    print(f"{CLI_THEME_TITLE_GLYPH} {title}")
    if detail:
        print(f"  {detail}")

def _print_field(label: str, value: object) -> None:
    rendered = ""
    if value is not None:
        rendered = str(value)
    print(f"  {label}: {rendered}")

def _print_bullet(text: str) -> None:
    print(f"  {CLI_THEME_BULLET} {text}")

def _command_hint_glyph(command: str) -> str:
    normalized = " ".join(command.split()).strip()
    for prefix, glyph in CLI_COMMAND_GLYPHS:
        if normalized.startswith(prefix):
            return glyph
    return CLI_THEME_BULLET

def _format_command_hint(command: str) -> str:
    return f"{_command_hint_glyph(command)} {command}"

def _format_command_line(command: str, detail: str) -> str:
    return f"{_command_hint_glyph(command)} {command} · {detail}"

def _print_command_line(command: str, detail: str) -> None:
    print(f"  {_format_command_line(command, detail)}")

def _print_command_hints(*commands: str) -> None:
    if not commands:
        return
    print("  next_invocations:")
    for command in commands:
        print(f"  {_format_command_hint(command)}")

def _print_cli_card(
    title: str,
    detail: str | None = None,
    *,
    sections: tuple[CliCardSection, ...] = (),
    next_commands: tuple[str, ...] = (),
) -> None:
    if RICH_AVAILABLE and Panel is not None and Group is not None:
        console = Console(highlight=False, soft_wrap=True)
        blocks: list[Text] = []
        header = Text()
        if detail:
            header.append(f"{detail}", style=BRAND_MUTED)
            blocks.append(header)
        for section in sections:
            if blocks:
                blocks.append(Text(" "))
            section_text = Text()
            section_text.append(f"{section.title}\n", style=f"bold {BRAND_ACCENT}")
            for line in section.lines:
                section_text.append(f"{CLI_THEME_BULLET} {line}\n", style=BRAND_LIGHT)
            blocks.append(section_text)
        if next_commands:
            if blocks:
                blocks.append(Text(" "))
            command_text = Text()
            command_text.append("Next invocations\n", style=f"bold {BRAND_ACCENT}")
            for command in next_commands:
                command_text.append(f"{_format_command_hint(command)}\n", style=BRAND_LIGHT)
            blocks.append(command_text)
        console.print(
            Panel(
                Group(*blocks) if blocks else Text(""),
                title=f"[bold {BRAND_ACCENT}] {CLI_THEME_TITLE_GLYPH} {title} [/bold {BRAND_ACCENT}]",
                subtitle=f"[bold {BRAND_LIGHT}]{CLI_THEME_SUBTITLE}[/bold {BRAND_LIGHT}]",
                border_style=BRAND_ACCENT,
                padding=(1, 2),
            )
        )
        return

    _print_heading(title, detail)
    for section in sections:
        if section.title:
            print(f"  {section.title}:")
        for line in section.lines:
            _print_bullet(line)
    _print_command_hints(*next_commands)

def _provider_secret_ready(runtime: CliRuntime, *, provider_id: str) -> bool:
    provider_summary = dict(runtime.provider_summary())
    if (
        provider_summary.get("provider_id") == provider_id
        and provider_summary.get("secret_status") in {"stored", "not-required"}
    ):
        return True
    discovered = runtime.discovered_provider(provider_id)
    return discovered.status in {"authenticated", "configured"}

def _print_brain_status(runtime: CliRuntime) -> None:
    provider = dict(runtime.provider_summary())
    provider_id = str(provider.get("provider_id") or DEFAULT_PROVIDER_ID)
    discovered = runtime.discovered_provider(provider_id)
    sections = (
        CliCardSection(
            "Provider",
            (
                f"provider_id · {provider.get('provider_id', '<unset>')}",
                f"display_name · {provider.get('display_name', provider.get('provider_id', '<unset>'))}",
                f"base_url · {provider.get('base_url') or '<unset>'}",
                f"transport · {provider.get('transport_display_name', provider.get('transport_id', '<unset>'))}",
                f"secret_status · {provider.get('secret_status', '<unknown>')}",
                f"secret_source · {provider.get('secret_source', '<unknown>')}",
                f"discovery_status · {discovered.status}",
                f"discovery_source · {discovered.source}",
            ),
        ),
        CliCardSection(
            "Model selection",
            (
                f"{DELIBERATE_MODEL_LABEL.lower()}_model · {provider.get('strong_model') or '<unset>'}",
                f"{SWIFT_MODEL_LABEL.lower()}_model · {provider.get('weak_model') or '<unset>'}",
                f"intent_mode · {provider.get('intent_mode') or '<unset>'}",
                f"embedding_bootstrap_status · {provider.get('embedding_bootstrap_status') or '<unset>'}",
                f"context_window_tokens · {provider.get('context_window_tokens') or '<unset>'}",
                f"context_window_mode · {provider.get('context_window_mode') or '<unset>'}",
                f"reasoning_effort · {provider.get('reasoning_effort') or '<unset>'}",
                f"reasoning_efforts · {', '.join(provider.get('reasoning_efforts', ())) or '<none>'}",
            ),
        ),
    )
    _print_cli_card(
        "Provider status",
        "The active provider and model posture Aegis will use for the next turn.",
        sections=sections,
        next_commands=("aegis provider", "aegis provider providers", "aegis provider models"),
    )

def _print_brain_provider_inventory(runtime: CliRuntime) -> None:
    lines = tuple(
        f"{state.provider_id} · {state.display_name} · {state.transport_display_name} · status={state.status} · source={state.source}"
        for state in runtime.provider_inventory()
        if state.runtime_enabled
    ) or ("<empty>",)
    _print_cli_card(
        "Provider catalog",
        "Providers Aegis can configure right now.",
        sections=(CliCardSection("Catalog", lines),),
        next_commands=("aegis provider", "aegis provider status"),
    )

def _print_brain_models(runtime: CliRuntime, *, provider_id: str) -> None:
    try:
        models = runtime.discover_provider_models(provider_id=provider_id)
    except Exception as error:
        _print_cli_card(
            "Provider models",
            str(error),
            next_commands=("aegis provider", "aegis provider status"),
        )
        return
    lines = tuple(
        f"{model.model_id} · context={model.context_window_tokens or '<unknown>'} · output={model.max_output_tokens or '<unknown>'} · source={model.source}"
        for model in models
    ) or ("<empty>",)
    _print_cli_card(
        "Provider models",
        f"Models Aegis can see for {provider_id}.",
        sections=(CliCardSection("Catalog", lines),),
        next_commands=("aegis provider", "aegis provider status"),
    )

def _slugify_clone_name(value: str) -> str:
    collapsed = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return collapsed or "aegis"

def _display_name_from_clone_name(value: str) -> str:
    collapsed = re.sub(r"[^a-zA-Z0-9]+", " ", value.strip()).strip()
    return collapsed.title() or "Aegis"

def _suggest_clone_name(runtime: CliRuntime | None = None) -> str:
    candidates = DEFAULT_CLONE_NAME_SUGGESTIONS
    if runtime is None:
        return random.choice(candidates)
    available = tuple(
        name
        for name in candidates
        if runtime.latest_session_for_clone(_slugify_clone_name(name)) is None
    )
    return random.choice(available or candidates)


def _unique_clone_name(runtime: CliRuntime, value: str) -> str:
    base_name = _slugify_clone_name(value)
    candidate = base_name
    suffix = 2
    while runtime.latest_session_for_clone(candidate) is not None:
        candidate = f"{base_name}-{suffix}"
        suffix += 1
    return candidate

__all__ = [
    "_provider_choices",
    "DEFAULT_PROVIDER_ID",
    "DEFAULT_CLONE_INITIAL_GOAL",
    "DEFAULT_CLONE_NAME_SUGGESTIONS",
    "CLI_THEME_TITLE_GLYPH",
    "CLI_THEME_BULLET",
    "CLI_THEME_WELCOME_GLYPH",
    "CLI_THEME_SUBTITLE",
    "CLI_COMMAND_GLYPHS",
    "CliCardSection",
    "_WizardCancelledError",
    "BirthWizardState",
    "build_parser",
    "_print_heading",
    "_print_field",
    "_print_bullet",
    "_command_hint_glyph",
    "_format_command_hint",
    "_format_command_line",
    "_print_command_line",
    "_print_command_hints",
    "_print_cli_card",
    "_provider_secret_ready",
    "_print_brain_status",
    "_print_brain_provider_inventory",
    "_print_brain_models",
    "_slugify_clone_name",
    "_display_name_from_clone_name",
    "_suggest_clone_name",
    "_unique_clone_name",
]
