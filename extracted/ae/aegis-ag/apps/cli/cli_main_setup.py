"""Interactive setup helpers for the CLI entrypoint."""

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
    ProviderSelectionState,
    provider_choices as _shared_provider_choices,
    provider_setup_defaults,
    run_provider_selection_wizard,
)
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



from .cli_main_support import *  # noqa: F401,F403

def _default_personality_preset(runtime: CliRuntime, *, mode: str, current: str | None = None) -> str | None:
    if mode != "companion":
        return None
    if current:
        return current
    for preset in runtime.personality_presets():
        if preset.preset_id == "companion":
            return preset.preset_id
    return runtime.personality_presets()[0].preset_id

def _print_birth_wizard_intro() -> None:
    if not RICH_AVAILABLE or Table is None or Panel is None or Group is None:
        _print_heading("Aegis Init", "Let's bring your first Aegis to life.")
        _print_bullet("name the Aegis that will stay with your thread")
        _print_bullet("bind the first model path it will think through")
        _print_bullet("Hand off to aegis wake")
        return
    console = Console(highlight=False, soft_wrap=True)
    brand = Table.grid(expand=True)
    brand.add_column(no_wrap=True)
    hero = Text(justify="center")
    hero.append("🐣 Let's bring your first Aegis to life.\n", style=f"bold {BRAND_LIGHT}")
    hero.append("Name it, bind its first mind, then step into wake.", style=BRAND_MUTED)
    flow = Text()
    flow.append("🧠 Birth flow\n", style=f"bold {BRAND_ACCENT}")
    flow.append("1 · Name your first Aegis\n", style=BRAND_LIGHT)
    flow.append("2 · Bind its first model path\n", style=BRAND_LIGHT)
    flow.append("3 · Hand off to aegis wake", style=BRAND_LIGHT)
    brand.add_row(_center_brand_block(hero))
    brand.add_row(Text(" "))
    brand.add_row(_center_brand_block(render_guardian_mark()))
    brand.add_row(Text(" "))
    layout = Table.grid(expand=True)
    console_width = getattr(console.size, "width", 0)
    if console_width and console_width < 132:
        layout.add_column(ratio=1, min_width=48)
        layout.add_row(brand)
        layout.add_row(Text(" "))
        layout.add_row(flow)
    else:
        layout.add_column(ratio=11, min_width=44)
        layout.add_column(ratio=13, min_width=48)
        layout.add_row(brand, flow)
    console.print(
        Panel(
            layout,
            title=f"[bold {BRAND_ACCENT}] {CLI_THEME_TITLE_GLYPH} Aegis Init v{_resolve_aegis_version()} [/bold {BRAND_ACCENT}]",
            subtitle=f"[bold {BRAND_LIGHT}]Your enduring AI companion, growing with you.[/bold {BRAND_LIGHT}]",
            border_style=BRAND_ACCENT,
            padding=(1, 2),
        )
    )

def _prompt_first_clone_name(default_name: str, *, allow_back: bool = False) -> str | _WizardBackSignal:
    return _wizard_text_prompt(
        "Name Your First Aegis",
        "This first Aegis is yours. What name feels right?",
        default=default_name,
        allow_back=allow_back,
    )

def _run_interactive_clone_wizard(
    runtime: CliRuntime,
    *,
    clone_name: str | None,
) -> str | None:
    current_clone_name = clone_name or _suggest_clone_name(runtime)
    answer = _wizard_text_prompt(
        "Name Another Aegis",
        "What should this new Aegis be called?",
        default=current_clone_name,
        allow_back=True,
    )
    if answer is WIZARD_BACK:
        return None
    return str(answer).strip() or current_clone_name

def _run_interactive_birth_wizard(
    runtime: CliRuntime,
    *,
    display_name: str,
    provider_state: ProviderSelectionState,
) -> BirthWizardState | None:
    state = BirthWizardState(
        display_name=display_name,
        provider_id=provider_state.provider_id,
        base_url=provider_state.base_url,
        strong_model=provider_state.strong_model,
        weak_model=provider_state.weak_model,
        intent_mode=provider_state.intent_mode,
        api_key=provider_state.api_key,
        reasoning_effort=provider_state.reasoning_effort,
        context_window_mode=provider_state.context_window_mode,
        context_window_tokens=provider_state.context_window_tokens,
    )
    steps = ("display_name", "provider_setup")
    step_index = 0
    while step_index < len(steps):
        step = steps[step_index]
        if step == "display_name":
            answer = _prompt_first_clone_name(state.display_name, allow_back=True)
            if answer is WIZARD_BACK:
                return None
            state.display_name = str(answer).strip() or state.display_name
            step_index += 1
            continue
        if step == "provider_setup":
            answer = run_provider_selection_wizard(
                runtime,
                initial_state=ProviderSelectionState(
                    provider_id=state.provider_id,
                    base_url=state.base_url,
                    api_key=state.api_key,
                    strong_model=state.strong_model,
                    weak_model=state.weak_model,
                    intent_mode=state.intent_mode,
                    reasoning_effort=state.reasoning_effort,
                    context_window_mode=state.context_window_mode,
                    context_window_tokens=state.context_window_tokens,
                ),
                allow_back=True,
            )
            if answer is WIZARD_BACK:
                return None
            state.provider_id = answer.provider_id
            state.base_url = answer.base_url
            state.api_key = answer.api_key
            state.strong_model = answer.strong_model
            state.weak_model = answer.weak_model
            state.intent_mode = answer.intent_mode
            state.reasoning_effort = answer.reasoning_effort
            state.context_window_mode = answer.context_window_mode
            state.context_window_tokens = answer.context_window_tokens
            step_index += 1
            continue
    return state

def _print_birth_paused() -> None:
    _print_cli_card(
        "Aegis birth paused",
        "No new identity or provider changes were written.",
        next_commands=("aegis init", "aegis status"),
    )

def _gateway_birth_lines(clone_name: str) -> tuple[str, ...]:
    return (
        f"wire IM · aegis gateway setup --default-clone-id {clone_name}",
        "inspect readiness · aegis gateway doctor",
        "inspect skill packages · aegis skills",
        "launch operator dashboard · aegis dashboard --dry-run",
    )

def _prompt_im_onboarding(runtime: CliRuntime, *, clone_name: str) -> None:
    from apps.gateway.__main__ import run_im_setup

    run_im_setup(
        default_clone_id=clone_name,
        default_profile_dir=runtime.paths.profile_dir,
        default_state_dir=runtime.paths.state_dir / "gateway",
        default_control_profile_dir=runtime.paths.profile_dir,
        default_control_state_dir=runtime.paths.state_dir,
        prompt_title="💬 IM Setup",
        prompt_text="💬 Which IM should Aegis wire before wake opens?",
        allow_skip=True,
    )

def _print_overview(runtime: CliRuntime) -> None:
    provider = dict(runtime.provider_summary())
    doctor = runtime.provider_doctor()
    clones = runtime.list_clones(limit=5)
    if RICH_AVAILABLE and Table is not None and Panel is not None and Group is not None:
        console = Console(highlight=False, soft_wrap=True)
        brand = Table.grid(expand=True)
        brand.add_column(no_wrap=True)
        headline = Text(no_wrap=True)
        headline.append(f"{CLI_THEME_WELCOME_GLYPH} Welcome back !\n", style=f"bold {BRAND_LIGHT}")
        headline.append("Your enduring AI companion, growing with you.", style=BRAND_MUTED)
        capability = Text("🧠 Persistent memory · long-horizon decisions · long context", style=BRAND_MUTED)
        action_lines = Text()
        action_lines.append("💡 First invocations\n", style=f"bold {BRAND_ACCENT}")
        action_lines.append(f"{_format_command_line('aegis init', 'name your first Aegis, shape its charter, and awaken it')}\n", style=BRAND_LIGHT)
        action_lines.append(f"{_format_command_line('aegis wake', 're-enter the live Aegis clone that still keeps the thread')}\n", style=BRAND_LIGHT)
        action_lines.append(f"{_format_command_line('aegis clone <name>', 'call another Aegis individual into the hall')}\n", style=BRAND_LIGHT)
        action_lines.append(f"{_format_command_line('aegis clones', 'inspect or retire named clones')}\n", style=BRAND_LIGHT)
        action_lines.append(f"{_format_command_line('aegis status', 'inspect provider, voice, and security omens')}\n", style=BRAND_LIGHT)
        action_lines.append(f"{_format_command_line('aegis skills', 'inspect, search, install, and toggle skill packages before wake')}\n", style=BRAND_LIGHT)
        action_lines.append(f"{_format_command_line('aegis gateway', 'open IM setup and choose which messenger gate to bind')}\n", style=BRAND_LIGHT)
        action_lines.append(f"{_format_command_line('aegis provider', 'tune provider, model, and context posture before wake')}\n", style=BRAND_LIGHT)
        action_lines.append(f"{_format_command_line('aegis dashboard', 'launch the operator dashboard when this install includes frontend assets')}\n", style=BRAND_LIGHT)
        action_lines.append("\n🔮 Current omens\n", style=f"bold {BRAND_ACCENT}")
        action_lines.append(f"status · {doctor['status']}\n", style=BRAND_MUTED if doctor["status"] != "ready" else BRAND_LIGHT)
        action_lines.append(f"provider · {provider['provider_id']}\n", style=BRAND_MUTED)
        if clones:
            action_lines.append("clones · " + ", ".join(clone.clone_id for clone in clones), style=BRAND_MUTED)
        else:
            action_lines.append("clones · none yet", style=BRAND_MUTED)
        brand.add_row(_center_brand_block(headline))
        brand.add_row(Text(" "))
        brand.add_row(_center_brand_block(render_guardian_mark()))
        brand.add_row(Text(" "))
        brand.add_row(_center_brand_block(capability))
        layout = Table.grid(expand=True)
        layout.add_column(ratio=11, min_width=46)
        layout.add_column(ratio=11, min_width=44)
        layout.add_row(brand, action_lines)
        console.print(
            Panel(
                layout,
                title=f"[bold {BRAND_ACCENT}] {CLI_THEME_TITLE_GLYPH} Aegis v{_resolve_aegis_version()} [/bold {BRAND_ACCENT}]",
                subtitle=f"[bold {BRAND_LIGHT}]Your enduring AI companion, growing with you.[/bold {BRAND_LIGHT}]",
                border_style=BRAND_ACCENT,
                padding=(1, 2),
            )
        )
        return

    _print_heading(f"{CLI_THEME_WELCOME_GLYPH} Welcome back !", "Your enduring AI companion, growing with you.")
    _print_bullet("🧠 Persistent memory · long-horizon decisions · long context")
    _print_command_line("aegis init", "name your first Aegis, shape its charter, and awaken it")
    _print_command_line("aegis wake", "enter the live Aegis clone that still holds the thread")
    _print_command_line("aegis clone <name>", "call another Aegis individual into the hall")
    _print_command_line("aegis clones", "inspect or retire clones")
    _print_command_line("aegis status", "inspect provider, voice, and security omens")
    _print_command_line("aegis skills", "inspect, search, install, and toggle skill packages before wake")
    _print_command_line("aegis gateway", "open IM setup and choose which messenger gate to bind")
    _print_command_line("aegis provider", "tune provider, model, and context posture before wake")
    _print_command_line("aegis dashboard", "launch the operator dashboard when this install includes frontend assets")
    _print_field("status", doctor["status"])
    _print_field("provider", provider["provider_id"])
    _print_field("clones", ", ".join(clone.clone_id for clone in clones) if clones else "none yet")

def _center_brand_block(renderable):
    if Align is None:
        return renderable
    return Align.center(renderable)

def _print_setup_intro(runtime: CliRuntime, *, provider_id: str) -> None:
    guide = runtime.provider_setup_guide(provider_id)
    loaded = runtime.current_profile()
    _print_cli_card(
        "Aegis init",
        "Awaken your first Aegis and hand it off to wake.",
        sections=(
            CliCardSection(
                "Current form",
                (
                    f"name · {loaded.state.display_name}",
                    f"provider · {guide.display_name}",
                    f"transport · {guide.transport_display_name}",
                ),
            ),
            CliCardSection(
                "Awakening rite",
                (
                    "Give it a name",
                    "Bind its first model path",
                    "Optionally wire an IM surface once the first clone is ready",
                    "Retune presence later inside chat if you want",
                    "Finish in aegis wake",
                ),
            ),
        ),
    )

def _default_born_args() -> argparse.Namespace:
    return argparse.Namespace(
        provider_id=DEFAULT_PROVIDER_ID,
        display_name=None,
        clone_text=None,
        clone_name=None,
        initial_goal=None,
        base_url=None,
        strong_model=None,
        weak_model=None,
        intent_mode=None,
        api_key=None,
        context_window_mode=None,
        context_window=None,
        non_interactive=False,
    )

def _default_grow_args() -> argparse.Namespace:
    return argparse.Namespace(
        session_id=None,
        clone_id=None,
        debug=False,
        message=None,
        voice_input_file=None,
        voice_output_file=None,
        voice_input_model="gpt-4o-mini-transcribe",
        voice_output_model="gpt-4o-mini-tts",
        voice_name="alloy",
    )

def _ensure_clone_ready(
    runtime: CliRuntime,
    *,
    clone_name: str,
    display_name: str,
    profile_id: str,
    initial_goal: str | None = None,
) -> tuple[object, str]:
    existing = runtime.latest_session_for_clone(clone_name)
    if existing is not None:
        runtime.seed_initial_goal(existing.session_id, initial_goal or "")
        return existing, "existing"
    session = runtime.create_clone(
        clone_id=clone_name,
        profile_id=profile_id,
        display_name=display_name,
        mode="companion",
        initial_goal=initial_goal,
    )
    return session, "created"

__all__ = [
    "DEFAULT_PROVIDER_ID",
    "DEFAULT_CLONE_INITIAL_GOAL",
    "DEFAULT_CLONE_NAME_SUGGESTIONS",
    "CLI_THEME_TITLE_GLYPH",
    "CLI_THEME_BULLET",
    "CLI_THEME_WELCOME_GLYPH",
    "CLI_THEME_SUBTITLE",
    "_default_personality_preset",
    "_print_birth_wizard_intro",
    "_prompt_first_clone_name",
    "_run_interactive_clone_wizard",
    "_run_interactive_birth_wizard",
    "_print_birth_paused",
    "_gateway_birth_lines",
    "_prompt_im_onboarding",
    "_print_overview",
    "_center_brand_block",
    "_print_setup_intro",
    "_default_born_args",
    "_default_grow_args",
    "_ensure_clone_ready",
]
