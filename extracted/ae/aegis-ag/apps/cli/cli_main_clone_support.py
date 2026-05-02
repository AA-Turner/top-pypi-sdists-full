"""Clone and wake rendering helpers for the CLI entrypoint."""

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
from .turn_metrics import cache_hit_metric_line
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

def _print_doctor(runtime: CliRuntime) -> None:
    provider = runtime.provider_doctor()
    voice = runtime.voice_doctor()
    security = runtime.security_doctor()
    clones = runtime.list_clones(limit=5)
    active = provider["provider"]
    status_lines = (
        f"provider_status · {provider['status']}",
        f"voice_status · {voice['status']}",
        f"security_status · {security['status']}",
        f"active_provider_id · {active['provider_id']}",
        f"active_provider_source · {active['source']}",
        f"active_provider_strong_model · {active.get('strong_model') or '<unset>'}",
        f"active_provider_weak_model · {active.get('weak_model') or '<unset>'}",
        f"active_provider_intent_mode · {active.get('intent_mode') or '<unset>'}",
        f"active_provider_embedding_bootstrap · {active.get('embedding_bootstrap_status') or '<unset>'}",
    )
    provider_checks = tuple(
        f"{check['check']} · {check['status']}{f' · {check['summary']}' if check.get('summary') else ''}"
        for check in provider["checks"]
    )
    voice_checks = tuple(
        f"{check['check']} · {check['status']}{f' · {check['summary']}' if check.get('summary') else ''}"
        for check in voice["checks"]
    )
    security_checks = tuple(
        f"{check['check']} · {check['status']}{f' · {check['summary']}' if check.get('summary') else ''}"
        for check in security["checks"]
    )
    voice_identity_lines = tuple(
        line
        for line in (
            f"voice_supported_path · {voice['supported_path']}" if voice.get("supported_path") else "",
            f"voice_identity_binding · {voice['identity_binding']}" if voice.get("identity_binding") else "",
            f"voice_identity_summary · {voice['voice_identity_summary']}" if voice.get("voice_identity_summary") else "",
        )
        if line
    )
    extra_lines = (
        (f"probe_summary · {provider['probe_summary']}",) if provider["probe_summary"] else ()
    )
    sections = [CliCardSection("Readiness", status_lines)]
    if provider_checks:
        sections.append(CliCardSection("Provider checks", provider_checks))
    if voice_checks:
        sections.append(CliCardSection("Voice checks", voice_checks))
    if voice_identity_lines:
        sections.append(CliCardSection("Voice identity", voice_identity_lines))
    if security_checks:
        sections.append(CliCardSection("Security checks", security_checks))
    if extra_lines:
        sections.append(CliCardSection("Probe", extra_lines))
    _print_cli_card(
        "Aegis status",
        "Readiness before the wake surface opens.",
        sections=tuple(sections),
        next_commands=("aegis wake", "aegis clone <name>", "aegis clones")
        if provider["status"] == "ready" and clones
        else ("aegis clone <name>", "aegis wake", "aegis clones")
        if provider["status"] == "ready"
        else ("aegis init",),
    )

def _print_clone_created(runtime: CliRuntime, session_id: str) -> None:
    session = runtime.inspect_session(session_id)
    clone_id = runtime.clone_id_for_session(session)
    goals = runtime.inspect_goals(session_id)
    ready_lines = [
        f"clone_id · {clone_id}",
        f"session_id · {session.session_id}",
        f"profile_id · {session.profile_id}",
        f"status · {session.status}",
    ]
    if goals:
        ready_lines.append(f"active_goal · {goals[0].title}")
    _print_cli_card(
        "Aegis clone",
        "A new Aegis individual is ready.",
        sections=(
            CliCardSection(
                "Ready now",
                tuple(ready_lines),
            ),
        ),
        next_commands=("aegis wake", f"aegis wake --clone-id {clone_id}", "aegis clones"),
    )

def _print_clone_paused() -> None:
    _print_cli_card(
        "Aegis clone paused",
        "No new clone was created.",
        next_commands=("aegis clone <name>", "aegis wake", "aegis clones"),
    )

def _print_clones(runtime: CliRuntime) -> None:
    clones = runtime.list_clones(limit=24)
    if not clones:
        _print_cli_card(
            "Aegis clones",
            "Named Aegis individuals with their own continuity lines.",
            sections=(CliCardSection("Current state", ("No clones yet.",)),),
            next_commands=("aegis clone <name>",),
        )
        return
    clone_lines = tuple(
        f"{clone.clone_id} · latest {clone.latest_session_id[:8]} · {clone.session_count} session{'s' if clone.session_count != 1 else ''} · {clone.latest_status}"
        for clone in clones
    )
    _print_cli_card(
        "Aegis clones",
        "Named Aegis individuals with their own continuity lines.",
        sections=(CliCardSection("Available clones", clone_lines),),
        next_commands=(
            "aegis wake",
            "aegis clone <name>",
            "aegis clones sessions <name>",
            "aegis clones bye <name>",
            "aegis clones bye --all",
        ),
    )

def _print_clone_sessions(runtime: CliRuntime, clone_id: str) -> None:
    session_ids = runtime.session_ids_for_clone(clone_id)
    if not session_ids:
        raise ValueError(f"unknown clone: {clone_id}")
    session_lines: list[str] = []
    for index, session_id in enumerate(session_ids):
        session = runtime.inspect_session(session_id)
        line = f"{session.session_id} · {session.status} · updated {session.updated_at.isoformat()}"
        if index == 0:
            line += " · latest"
        session_lines.append(line)
        if session.parent_session_id:
            session_lines.append(f"resumed from · {session.parent_session_id[:8]}")
    _print_cli_card(
        "Clone sessions",
        "Durable continuity lines currently attached to one named Aegis clone.",
        sections=(CliCardSection(f"Clone {clone_id}", tuple(session_lines)),),
        next_commands=(
            f"aegis wake --session-id {session_ids[0]}",
            f"aegis wake --clone-id {clone_id}",
            "aegis clones",
        ),
    )

def _print_clone_retired(clone_id: str, deleted_sessions: int) -> None:
    _print_cli_card(
        "Clone retired",
        "A named Aegis continuity line has been cleared.",
        sections=(
            CliCardSection(
                "Retired now",
                (
                    f"clone_id · {clone_id}",
                    f"deleted_sessions · {deleted_sessions}",
                ),
            ),
        ),
        next_commands=("aegis clones", "aegis clone <name>", "aegis wake"),
    )

def _print_clone_retire_paused() -> None:
    _print_cli_card(
        "Clone retire paused",
        "No clone was cleared.",
        next_commands=("aegis clones", "aegis wake", "aegis clone <name>"),
    )

def _print_all_clones_retired(deleted_clones: int, deleted_sessions: int) -> None:
    _print_cli_card(
        "All clones retired",
        "Every named Aegis clone has been cleared.",
        sections=(
            CliCardSection(
                "Retired now",
                (
                    f"deleted_clones · {deleted_clones}",
                    f"deleted_sessions · {deleted_sessions}",
                ),
            ),
        ),
        next_commands=("aegis clone <name>", "aegis init", "aegis status"),
    )

def _prompt_clone_choice(runtime: CliRuntime, clones, *, intent: str = "enter") -> object:
    prompt = (
        "Multiple Aegis clones are available. Pick one before entering wake."
        if intent == "enter"
        else "Multiple Aegis clones are available. Pick one before clearing it."
    )
    if _wizard_dialogs_supported():
        default_clone = clones[0].clone_id
        choices = tuple(
            WizardChoice(
                value=clone.clone_id,
                label=(
                    f"{clone.clone_id} · {clone.session_count} session{'s' if clone.session_count != 1 else ''} · "
                    f"{_display_name_from_clone_name(clone.clone_id)}"
                ),
                detail=f"latest continuity {clone.latest_session_id[:8]} · {clone.latest_status}",
            )
            for clone in clones
        )
        selected_id = _wizard_choice_prompt(
            "Choose clone",
            prompt,
            choices,
            default=default_clone,
            allow_back=True,
        )
        if selected_id is WIZARD_BACK:
            return WIZARD_BACK
        for clone in clones:
            if clone.clone_id == selected_id:
                return clone
    _print_cli_card(
        "Choose clone",
        prompt,
        sections=(
            CliCardSection(
                "Available clones",
                tuple(
                    f"{index}. {clone.clone_id} · latest {clone.latest_session_id[:8]} · {clone.session_count} session{'s' if clone.session_count != 1 else ''} · {clone.latest_status} · {_display_name_from_clone_name(clone.clone_id)}"
                    for index, clone in enumerate(clones, start=1)
                ),
            ),
        ),
    )
    while True:
        answer = input("clone: ").strip()
        if answer.isdigit():
            index = int(answer)
            if 1 <= index <= len(clones):
                return clones[index - 1]
        for clone in clones:
            if clone.clone_id == answer:
                return clone
        print("  enter a clone number or clone id from the list above")

def _resolve_growth_session(
    runtime: CliRuntime,
    *,
    session_id: str | None = None,
    clone_id: str | None = None,
) -> tuple[str, str]:
    if session_id is not None:
        return runtime.inspect_session(session_id).session_id, "Opened existing"
    if clone_id is not None:
        selected = runtime.latest_session_for_clone(clone_id)
        if selected is None:
            raise ValueError(f"unknown clone: {clone_id}")
        resumed = runtime.resume(selected.session_id).session
        return resumed.session_id, f"Opened thread {clone_id}"
    clones = runtime.list_clones(limit=16)
    if not clones:
        raise LookupError("no-clones")
    if len(clones) == 1:
        resumed = runtime.resume(clones[0].latest_session_id).session
        return resumed.session_id, f"Opened thread {clones[0].clone_id}"
    if _interactive_shell_supported():
        selected = _prompt_clone_choice(runtime, clones)
        if selected is WIZARD_BACK:
            raise _WizardCancelledError("wake")
        resumed = runtime.resume(selected.latest_session_id).session
        return resumed.session_id, f"Opened thread {selected.clone_id}"
    raise ValueError("multiple clones are available; pass --clone-id or enter wake from an interactive TTY")

def _print_clone_blocked(runtime: CliRuntime) -> None:
    report = runtime.provider_doctor()
    provider = report["provider"]
    checks = tuple(
        f"{check['check']} · {check['status']}{f' · {check['summary']}' if check.get('summary') else ''}"
        for check in report["checks"]
    )
    sections = [
        CliCardSection(
            "Current readiness",
            (
                f"provider_status · {report['status']}",
                f"active_provider_id · {provider['provider_id']}",
                f"active_provider_source · {provider['source']}",
            ),
        )
    ]
    if checks:
        sections.append(CliCardSection("Provider checks", checks))
    _print_cli_card(
        "Clone blocked",
        "Finish init before creating another Aegis clone.",
        sections=tuple(sections),
        next_commands=("aegis init", "aegis status"),
    )

def _print_grow_blocked(runtime: CliRuntime) -> None:
    report = runtime.provider_doctor()
    provider = report["provider"]
    checks = tuple(
        f"{check['check']} · {check['status']}{f' · {check['summary']}' if check.get('summary') else ''}"
        for check in report["checks"]
    )
    sections = [
        CliCardSection(
            "Current readiness",
            (
                f"provider_status · {report['status']}",
                f"active_provider_id · {provider['provider_id']}",
                f"active_provider_source · {provider['source']}",
            ),
        )
    ]
    if checks:
        sections.append(CliCardSection("Provider checks", checks))
    _print_cli_card(
        "Wake blocked",
        "Finish init and status checks before entering the wake surface.",
        sections=tuple(sections),
        next_commands=("aegis init", "aegis status"),
    )

def _provider_session_ready(report: dict[str, object]) -> bool:
    raw_checks = tuple(report.get("checks", ()))
    if not raw_checks:
        return str(report.get("status", "")).strip().lower() == "ready"
    checks = {
        str(check.get("check")): str(check.get("status"))
        for check in raw_checks
        if isinstance(check, dict)
    }
    return (
        checks.get("provider_profile") == "configured"
        and checks.get("credentials") in {"available", "not-required"}
    )

def _print_no_clones() -> None:
    _print_cli_card(
        "No clones yet",
        "Create an Aegis clone before entering the wake surface.",
        next_commands=("aegis clone <name>", "aegis status"),
    )

def _print_assistant_turn(runtime: CliRuntime, outcome, *, title: str = "Aegis turn") -> None:
    provider = dict(runtime.provider_summary())
    lines = [
        f"session_id · {outcome.session.session_id}",
        f"profile_id · {outcome.profile.profile_id}",
        f"provider_id · {provider['provider_id']}",
        f"provider_strong_model · {provider.get('strong_model') or '<unset>'}",
        f"provider_weak_model · {provider.get('weak_model') or '<unset>'}",
        f"provider_intent_mode · {provider.get('intent_mode') or '<unset>'}",
        f"execution · {outcome.execution.summary}",
        f"goals_in_play · {len(outcome.goals)}",
        f"memory_hits · {len(outcome.memories)}",
    ]
    cache_metric = cache_hit_metric_line(outcome.execution)
    if cache_metric:
        lines.append(cache_metric.replace(":", " ·", 1))
    if outcome.plan is not None:
        lines.append(f"plan_rationale · {outcome.plan.rationale}")
    _print_cli_card(
        title,
        "One wake turn completed.",
        sections=(CliCardSection("Turn summary", tuple(lines)),),
    )

def _print_voice_turn(result, *, output_path: Path | None = None) -> None:
    lines = [
        f"voice_input_outcome · {result.input_resolution.outcome}",
        f"voice_input_summary · {result.input_resolution.summary}",
        f"voice_policy_decision · {result.voice_turn.policy_result.decision.value}",
    ]
    if result.voice_turn.output is not None:
        lines.append(f"voice_output_mode · {result.voice_turn.output.delivery_mode}")
        lines.append(f"voice_output_enabled · {result.voice_turn.output.voice_enabled}")
        if result.voice_turn.output.metadata.get("voice_identity_summary"):
            lines.append(
                f"voice_identity_summary · {result.voice_turn.output.metadata['voice_identity_summary']}"
            )
    if output_path is not None:
        lines.append(f"voice_output_file · {output_path}")
    _print_cli_card(
        "Voice turn",
        "Aegis completed one voice-first turn.",
        sections=(CliCardSection("Voice summary", tuple(lines)),),
    )

__all__ = [
    "DEFAULT_PROVIDER_ID",
    "DEFAULT_CLONE_INITIAL_GOAL",
    "DEFAULT_CLONE_NAME_SUGGESTIONS",
    "CLI_THEME_TITLE_GLYPH",
    "CLI_THEME_BULLET",
    "CLI_THEME_WELCOME_GLYPH",
    "CLI_THEME_SUBTITLE",
    "_print_doctor",
    "_print_clone_created",
    "_print_clone_paused",
    "_print_clones",
    "_print_clone_sessions",
    "_print_clone_retired",
    "_print_clone_retire_paused",
    "_print_all_clones_retired",
    "_prompt_clone_choice",
    "_resolve_growth_session",
    "_print_clone_blocked",
    "_print_grow_blocked",
    "_provider_session_ready",
    "_print_no_clones",
    "_print_assistant_turn",
    "_print_voice_turn",
]
