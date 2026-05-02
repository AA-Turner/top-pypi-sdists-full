"""CLI main implementation assembled from setup and clone helper modules."""

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



from .cli_main_clone_support import *  # noqa: F401,F403
from .cli_main_setup import *  # noqa: F401,F403
from .cli_main_support import *  # noqa: F401,F403


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


def _run_setup(runtime: CliRuntime, args: argparse.Namespace) -> int:
    provider_id = args.provider_id
    loaded = runtime.current_profile()
    provider_state = provider_setup_defaults(runtime, provider_id)
    initial_clone_name = args.clone_name
    initial_goal = (args.initial_goal or "").strip()
    if args.display_name is not None:
        display_name = args.display_name
    elif initial_clone_name:
        display_name = _display_name_from_clone_name(initial_clone_name)
    else:
        display_name = _suggest_clone_name(runtime)
    mode = "companion"
    personality_preset = _default_personality_preset(
        runtime,
        mode=mode,
        current=(loaded.companion.personality_preset if loaded.companion is not None else None),
    ) or "companion"
    initiative = loaded.companion.initiative if loaded.companion is not None else "gentle"
    requested_clone_text = args.clone_text
    secret_env_var = getattr(args, "secret_env_var", None)
    provider_state.base_url = args.base_url or provider_state.base_url
    provider_state.strong_model = args.strong_model or provider_state.strong_model
    provider_state.weak_model = args.weak_model or provider_state.weak_model or provider_state.strong_model
    provider_state.intent_mode = args.intent_mode or provider_state.intent_mode
    provider_state.api_key = args.api_key
    if provider_state.api_key is None and secret_env_var:
        provider_state.api_key = str(os.environ.get(secret_env_var) or "").strip() or None
    if args.context_window_mode is not None:
        provider_state.context_window_mode = args.context_window_mode
    if args.context_window is not None:
        provider_state.context_window_tokens = int(str(args.context_window).replace(",", ""))

    interactive_birth = _interactive_shell_supported() and not args.non_interactive
    if interactive_birth:
        _print_birth_wizard_intro()
        wizard_state = _run_interactive_birth_wizard(
            runtime,
            display_name=display_name,
            provider_state=provider_state,
        )
        if wizard_state is None:
            _print_birth_paused()
            return 0
        display_name = wizard_state.display_name
        provider_id = wizard_state.provider_id
        provider_state = ProviderSelectionState(
            provider_id=wizard_state.provider_id,
            base_url=wizard_state.base_url,
            api_key=wizard_state.api_key,
            strong_model=wizard_state.strong_model,
            weak_model=wizard_state.weak_model,
            intent_mode=wizard_state.intent_mode,
            reasoning_effort=wizard_state.reasoning_effort,
            context_window_mode=wizard_state.context_window_mode,
            context_window_tokens=wizard_state.context_window_tokens,
        )
    else:
        _print_setup_intro(runtime, provider_id=provider_id)

    base_url = provider_state.base_url
    strong_model = provider_state.strong_model
    weak_model = provider_state.weak_model or provider_state.strong_model
    intent_mode = provider_state.intent_mode
    api_key = provider_state.api_key
    reasoning_effort = provider_state.reasoning_effort
    context_window_mode = provider_state.context_window_mode or "auto"
    context_window_tokens = provider_state.context_window_tokens

    if not base_url or not strong_model or not weak_model:
        raise SystemExit("init requires a provider base URL plus deliberate and swift model ids")
    if context_window_tokens is None and strong_model:
        context_window_tokens = runtime.detect_provider_context_window(
            provider_id=provider_id,
            model_id=strong_model,
            base_url=base_url,
            api_key=api_key,
        )
    if context_window_tokens is None:
        context_window_tokens = 128_000
    guide = runtime.provider_setup_guide(provider_id)
    if (
        guide.auth_type == "api_key"
        and guide.required_secret_keys
        and not api_key
        and not _provider_secret_ready(runtime, provider_id=provider_id)
    ):
        raise SystemExit("init requires a provider key for API-key providers; rerun interactively or pass --api-key")

    updated_identity = runtime.update_identity(
        display_name=display_name,
        mode=mode,
    )
    updated_identity = runtime.update_companion_settings(
        profile_id=updated_identity.state.profile_id,
        initiative=initiative,
        personality_preset=personality_preset,
    )
    charter_text = (
        requested_clone_text.strip()
        if requested_clone_text is not None and requested_clone_text.strip()
        else render_clone_charter(
            display_name=updated_identity.state.display_name,
            personality_preset=personality_preset,
            initiative=initiative,
            mode=updated_identity.state.mode,
        )
    )
    runtime.update_identity_state(
        profile_id=updated_identity.state.profile_id,
        charter_text=(charter_text or DEFAULT_CLONE_TEXT).strip(),
    )

    configured = runtime.set_default_provider(
        provider_id=provider_id,
        profile_id=updated_identity.state.profile_id,
        display_name=updated_identity.state.display_name,
        mode=updated_identity.state.mode,
        base_url=base_url,
        strong_model=strong_model,
        weak_model=weak_model,
        intent_mode=intent_mode,
        api_key=api_key,
        secret_env_var=secret_env_var,
        context_window_tokens=context_window_tokens,
        context_window_mode=context_window_mode,
        reasoning_effort=reasoning_effort,
    )

    report = runtime.provider_doctor()
    provider = report["provider"]
    clone_name = _unique_clone_name(runtime, initial_clone_name or display_name)
    first_clone, first_clone_status = _ensure_clone_ready(
        runtime,
        clone_name=clone_name,
        display_name=display_name,
        profile_id=configured.state.profile_id,
        initial_goal=initial_goal,
    )
    readiness_lines = [
        f"clone · {runtime.clone_id_for_session(first_clone)}",
        f"status · {first_clone_status}",
        f"provider · {provider['display_name'] if 'display_name' in provider else provider['provider_id']}",
        f"strong_model · {provider.get('strong_model') or '<unset>'}",
        f"weak_model · {provider.get('weak_model') or '<unset>'}",
        f"intent_mode · {provider.get('intent_mode') or '<unset>'}",
        f"embedding_bootstrap · {provider.get('embedding_bootstrap_status') or '<unset>'}",
        f"context · {provider.get('context_window_tokens') or '<unset>'}",
        f"status · {report['status']}",
    ]
    if initial_goal:
        readiness_lines.append(f"initial_goal · {initial_goal}")
    birth_sections = [CliCardSection("Ready now", tuple(readiness_lines))]
    if report["status"] == "ready":
        birth_sections.append(
            CliCardSection(
                "Beyond local CLI",
                _gateway_birth_lines(clone_name),
            )
        )
    if interactive_birth and report["status"] == "ready":
        _prompt_im_onboarding(runtime, clone_name=clone_name)
        return ProductizedShell(runtime, session_id=first_clone.session_id, opened="Born new").run()
    _print_cli_card(
        "Aegis init complete",
        f"{display_name} is ready.",
        sections=tuple(birth_sections),
        next_commands=("aegis wake", "aegis clone <name>", "aegis clones")
        if report["status"] == "ready"
        else ("aegis status", "aegis init"),
    )
    return 0

def _run_brain(runtime: CliRuntime, args: argparse.Namespace) -> int:
    action = str(getattr(args, "provider_command", "configure") or "configure")
    if action == "status":
        _print_brain_status(runtime)
        return 0
    if action == "providers":
        _print_brain_provider_inventory(runtime)
        return 0
    if action == "models":
        provider = dict(runtime.provider_summary())
        provider_id = str(args.provider_id or provider.get("provider_id") or DEFAULT_PROVIDER_ID)
        _print_brain_models(runtime, provider_id=provider_id)
        return 0

    profile = runtime.current_profile()
    provider = dict(runtime.provider_summary())
    provider_id = str(args.provider_id or provider.get("provider_id") or DEFAULT_PROVIDER_ID)
    initial_state = provider_setup_defaults(runtime, provider_id)
    initial_state.base_url = str(args.base_url or provider.get("base_url") or initial_state.base_url)
    initial_state.strong_model = str(
        args.strong_model or provider.get("strong_model") or initial_state.strong_model
    )
    initial_state.weak_model = str(
        args.weak_model or provider.get("weak_model") or initial_state.weak_model or initial_state.strong_model
    )
    initial_state.intent_mode = str(args.intent_mode or provider.get("intent_mode") or initial_state.intent_mode)
    initial_state.api_key = args.api_key
    initial_state.reasoning_effort = (
        str(args.reasoning_effort or provider.get("reasoning_effort") or initial_state.reasoning_effort).strip() or None
    )
    if args.context_window_mode is not None:
        initial_state.context_window_mode = args.context_window_mode
    elif provider.get("context_window_mode") is not None:
        initial_state.context_window_mode = str(provider.get("context_window_mode"))
    if args.context_window is not None:
        initial_state.context_window_tokens = int(str(args.context_window).replace(",", ""))
    elif provider.get("context_window_tokens") is not None:
        try:
            initial_state.context_window_tokens = int(provider["context_window_tokens"])
        except (TypeError, ValueError):
            pass

    configured = initial_state
    if _interactive_shell_supported() and not args.non_interactive:
        answer = run_provider_selection_wizard(
            runtime,
            initial_state=initial_state,
            allow_back=True,
        )
        if answer is WIZARD_BACK:
            _print_cli_card(
                "Provider unchanged",
                "No provider or model changes were written.",
                next_commands=("aegis provider", "aegis provider status"),
            )
            return 0
        configured = answer

    guide = runtime.provider_setup_guide(configured.provider_id)
    if (
        guide.auth_type == "api_key"
        and guide.required_secret_keys
        and not configured.api_key
        and not _provider_secret_ready(runtime, provider_id=configured.provider_id)
    ):
        raise SystemExit("provider requires a provider key for API-key providers; rerun interactively or pass --api-key")

    context_window_tokens = configured.context_window_tokens
    if context_window_tokens is None and configured.strong_model:
        context_window_tokens = runtime.detect_provider_context_window(
            provider_id=configured.provider_id,
            model_id=configured.strong_model,
            base_url=configured.base_url,
            api_key=configured.api_key,
        )

    runtime.set_default_provider(
        provider_id=configured.provider_id,
        profile_id=profile.state.profile_id,
        display_name=profile.state.display_name,
        mode=profile.state.mode,
        base_url=configured.base_url,
        strong_model=configured.strong_model,
        weak_model=configured.weak_model,
        intent_mode=configured.intent_mode,
        api_key=configured.api_key,
        context_window_tokens=context_window_tokens,
        context_window_mode=configured.context_window_mode,
        reasoning_effort=configured.reasoning_effort,
    )
    _print_cli_card(
        "Provider updated",
        "Aegis will use the new provider and model posture on the next turn.",
        sections=(
            CliCardSection(
                "Saved",
                (
                    f"provider_id · {configured.provider_id}",
                    f"base_url · {configured.base_url}",
                    f"strong_model · {configured.strong_model}",
                    f"weak_model · {configured.weak_model}",
                    f"intent_mode · {configured.intent_mode}",
                    f"context_window_tokens · {context_window_tokens or '<unset>'}",
                    f"context_window_mode · {configured.context_window_mode}",
                    f"reasoning_effort · {configured.reasoning_effort or '<unset>'}",
                ),
            ),
        ),
        next_commands=("aegis provider status", "aegis wake"),
    )
    return 0

def _run_clone(runtime: CliRuntime, args: argparse.Namespace) -> int:
    report = runtime.provider_doctor()
    if not _provider_session_ready(report):
        _print_clone_blocked(runtime)
        return 1
    raw_clone_name = args.clone_name
    initial_goal = (args.initial_goal or "").strip()
    interactive_shell = _interactive_shell_supported()
    if raw_clone_name is None and not interactive_shell:
        _print_heading("Name needed", "Run aegis clone <name>, or rerun in a TTY and Aegis will ask you.")
        _print_command_hints("aegis clone <name>", "aegis wake", "aegis clones")
        return 1
    if interactive_shell and raw_clone_name is None:
        _print_heading("Aegis clone", "Let's bring another Aegis individual online.")
        wizard_state = _run_interactive_clone_wizard(
            runtime,
            clone_name=raw_clone_name,
        )
        if wizard_state is None:
            _print_clone_paused()
            return 0
        raw_clone_name = wizard_state
    clone_id = _unique_clone_name(runtime, raw_clone_name)
    display_name = args.display_name or _display_name_from_clone_name(raw_clone_name)
    session = runtime.create_clone(
        clone_id=clone_id,
        profile_id=args.profile_id,
        display_name=display_name,
        mode="companion",
        initial_goal=initial_goal,
    )
    if args.message is not None:
        runtime.prepare_session_surface(session.session_id)
        outcome = runtime.explain_next_step(session_id=session.session_id, prompt=args.message)
        _print_clone_created(runtime, session.session_id)
        _print_assistant_turn(runtime, outcome)
        return 0
    if _interactive_shell_supported():
        return ProductizedShell(runtime, session_id=session.session_id, opened="Cloned new", debug=args.debug).run()
    _print_clone_created(runtime, session.session_id)
    return 0

def _run_clones(runtime: CliRuntime, args: argparse.Namespace) -> int:
    if args.clones_command is None:
        _print_clones(runtime)
        return 0
    if args.clones_command == "sessions":
        _print_clone_sessions(runtime, args.clone_id)
        return 0
    if args.clones_command != "bye":
        raise ValueError(f"unknown clones command: {args.clones_command}")
    if args.delete_all:
        if args.clone_id is not None:
            raise ValueError("aegis clones bye accepts either a clone name or --all")
        deleted_clones, deleted_sessions = runtime.delete_all_clones()
        _print_all_clones_retired(deleted_clones, deleted_sessions)
        return 0
    if args.clone_id is None:
        clones = runtime.list_clones(limit=16)
        if not clones:
            _print_no_clones()
            return 1
        if _interactive_shell_supported():
            selected = _prompt_clone_choice(runtime, clones, intent="retire")
            if selected is WIZARD_BACK:
                _print_clone_retire_paused()
                return 0
            clone_id = selected.clone_id
        else:
            raise ValueError("aegis clones bye requires <name> or --all")
    else:
        clone_id = args.clone_id
    deleted_sessions = runtime.delete_clone(clone_id)
    if deleted_sessions == 0:
        raise ValueError(f"unknown clone: {clone_id}")
    _print_clone_retired(clone_id, deleted_sessions)
    return 0

def _run_grow(runtime: CliRuntime, args: argparse.Namespace) -> int:
    if args.message is not None and args.voice_input_file is not None:
        raise ValueError("--message and --voice-input-file cannot be used together")
    if args.voice_output_file is not None and args.voice_input_file is None:
        raise ValueError("--voice-output-file requires --voice-input-file")
    report = runtime.provider_doctor()
    if not _provider_session_ready(report):
        _print_grow_blocked(runtime)
        return 1

    try:
        session_id, opened = _resolve_growth_session(
            runtime,
            session_id=args.session_id,
            clone_id=args.clone_id,
        )
    except _WizardCancelledError:
        _print_cli_card(
            "Grow paused",
            "No clone was selected.",
            next_commands=("aegis wake", "aegis clones", "aegis clone <name>"),
        )
        return 0
    except LookupError:
        _print_no_clones()
        return 1
    if args.voice_input_file is not None:
        runtime.prepare_session_surface(session_id)
        audio_bytes = args.voice_input_file.read_bytes()
        result = runtime.run_voice_turn(
            session_id=session_id,
            audio_bytes=audio_bytes,
            audio_name=args.voice_input_file.name,
            audio_format=args.voice_input_file.suffix.lstrip(".") or None,
            voice_output_enabled=args.voice_output_file is not None,
            input_model_id=args.voice_input_model,
            output_model_id=args.voice_output_model,
            voice_name=args.voice_name,
            output_audio_format=(args.voice_output_file.suffix.lstrip(".") or "mp3")
            if args.voice_output_file is not None
            else "mp3",
        )
        if args.voice_output_file is not None and result.voice_turn.output is not None and result.voice_turn.output.audio_bytes is not None:
            args.voice_output_file.parent.mkdir(parents=True, exist_ok=True)
            args.voice_output_file.write_bytes(result.voice_turn.output.audio_bytes)
        _print_voice_turn(result, output_path=args.voice_output_file)
        if result.kernel_outcome is not None:
            _print_assistant_turn(runtime, result.kernel_outcome)
            return 0
        return 1

    if args.message is not None:
        runtime.prepare_session_surface(session_id)
        outcome = runtime.explain_next_step(session_id=session_id, prompt=args.message)
        _print_assistant_turn(runtime, outcome)
        return 0

    if _interactive_shell_supported():
        return ProductizedShell(runtime, session_id=session_id, opened=opened, debug=args.debug).run()
    runtime.prepare_session_surface(session_id)
    return _run_stream_grow_loop(runtime, session_id, sys.stdin)

def _run_stream_grow_loop(runtime: CliRuntime, session_id: str, stream: Iterable[str]) -> int:
    for line in stream:
        prompt = line.rstrip("\n").strip()
        if not prompt:
            continue
        outcome = runtime.explain_next_step(session_id=session_id, prompt=prompt)
        _print_assistant_turn(runtime, outcome)
    return 0

def _run_default_entry(runtime: CliRuntime) -> int:
    if not _interactive_shell_supported():
        _print_overview(runtime)
        return 0
    if runtime.list_clones(limit=16):
        return _run_grow(runtime, _default_grow_args())
    return _run_setup(runtime, _default_born_args())

def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    runtime = CliRuntime.create(state_dir=args.state_dir, profile_dir=args.profile_dir)

    if args.command is None:
        return _run_default_entry(runtime)
    if args.command == "init":
        return _run_setup(runtime, args)
    if args.command == "provider":
        return _run_brain(runtime, args)
    if args.command == "status":
        _print_doctor(runtime)
        return 0
    if args.command == "clone":
        try:
            return _run_clone(runtime, args)
        except ValueError as error:
            parser.error(str(error))
    if args.command == "clones":
        try:
            return _run_clones(runtime, args)
        except ValueError as error:
            parser.error(str(error))
    if args.command == "wake":
        try:
            return _run_grow(runtime, args)
        except ValueError as error:
            parser.error(str(error))
    parser.error(f"unknown command: {args.command}")
    return 2
