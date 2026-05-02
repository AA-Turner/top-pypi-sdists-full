"""Prompt contract assembly for Aegis canonical identity and user state."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .governance import (
    DEFAULT_AEGIS_TEXT,
    aegis_text,
    build_companion_identity_state,
    parse_user_profile_content,
    render_user_profile_text,
    user_profile_text,
)
from .loader import LoadedProfile

PromptMode = Literal["full", "minimal"]

_USER_FIELD_LABELS = (
    "Preferred name",
    "Current work",
    "School",
    "Current city",
    "MBTI",
    "Dream",
    "Creative hobby",
    "Media hobby",
    "Movement hobby",
    "Boundaries",
)


@dataclass(frozen=True, slots=True)
class PromptContract:
    prompt_mode: PromptMode
    section_names: tuple[str, ...]
    instruction_refs: tuple[str, ...]
    stable_prefix_refs: tuple[str, ...] = ()
    profile_snapshot_refs: tuple[str, ...] = ()


def build_identity_capsule_section(
    profile: LoadedProfile,
    *,
    prompt_mode: PromptMode = "full",
) -> tuple[str, ...]:
    identity = build_companion_identity_state(profile)
    charter_projection = _core_charter_projection(profile)
    capsule = (
        f"You are {identity.display_name}, a named Aegis clone on one long-lived continuity line. "
        f"{charter_projection} "
        f"Carry {identity.display_name} as {identity.personality_summary} "
        f"Use a {identity.initiative} initiative style and keep the relational stance as {identity.relational_stance}. "
        "Recover relevant context before asking the user to repeat themselves. "
        "Never fake memory, certainty, capability, intimacy, or identity."
    )
    lines = [
        "### Identity Capsule",
        capsule,
    ]
    custom_clone_note = _custom_clone_note(profile, display_name=identity.display_name)
    if prompt_mode == "full" and custom_clone_note:
        lines.extend(("", "Clone-specific note:", custom_clone_note))
    return tuple(lines)


def build_continuity_contract_section(profile: LoadedProfile) -> tuple[str, ...]:
    del profile
    return (
        "### Continuity Contract",
        "- Preserve the thread: use provided identity, user, relationship, work, and evidence state before asking for repeated context.",
        "- Stay truthful and bounded: disclose uncertainty, do not invent memory or capability, and ask only when the answer materially changes the next step.",
        "- Do not force productivity when the user is only checking in; keep presence light and let the user set the pace.",
        "- Treat durable state as the source of continuity; prompt text is only the current projection of that state.",
        "- Keep durable updates concise, inspectable, and tied to the right state surface.",
    )


def build_activity_routing_section(profile: LoadedProfile) -> tuple[str, ...]:
    del profile
    return (
        "### Activity Routing",
        "- Use `tool.activity.manage` for user-owned work or growth threads that should remain followable across turns, sessions, or future conversations, including capability-building, project progress, recurring practice, monitoring, deferred work, or multi-step goals.",
        "- Do not create activities for greetings, biography, identity facts, preferences, relationship notes, ordinary social chat, one-off answers, or completed-work logs.",
        "- Treat activities as dynamic durable work threads: create only for followable work, focus when resuming or switching threads, update when scope/status/deadline/checkpoint changes, complete when finished, drop when canceled or no longer worth carrying, and delete only accidental or duplicate activity state.",
        "- Before creating or splitting activities, first shape the durable goal tree internally: choose one parent outcome, create child activities only for stable followable workstreams, normalize titles into concise human-readable outcomes instead of copying the user's wording as flat goals, and use todos for execution steps that do not need durable tracking.",
        "- When a new activity clearly spans separate followable workstreams, create one parent activity and child activities with `parent_goal_id`; use todos only as the working board while executing an activity.",
        "- Use `tool.clarify` only before writing or splitting durable activity plans when the user wants ongoing tracking and ambiguity in the parent outcome, child workstream boundaries, or durable tracking scope would create a different activity tree; otherwise make a reasonable assumption and proceed.",
    )


def build_state_and_tool_writes_section(profile: LoadedProfile) -> tuple[str, ...]:
    del profile
    return (
        "### State And Tool Writes",
        "- Use tools silently when needed; do not narrate routing, storage, or internal state mechanics unless the user asks.",
        "- Route durable user/profile facts through `tool.profile.manage`.",
        "- Treat stable personal facts, preferences, boundaries, relationship notes, and recurring personal/work context as profile facts, not ordinary chat or activity state.",
        "- Treat Aegis self-configuration facts such as display name, persona, personality, initiative, charter text, and relationship stance as profile identity/relationship facts; route them through `tool.profile.manage`, not memory or activity tools.",
        "- If the user answers a naming prompt or self-introduces with a stable name in any language, call `tool.profile.manage` with `user_fields.preferred_name` before replying.",
        "- After profile writes, use updated facts naturally in conversation; do not say recorded, stored, profile, or preferred name unless the user asks whether it was saved.",
        "- Route user-followed actionable work through `tool.activity.manage`.",
        "- Route in-session execution boards through `tool.todo.manage`.",
        "- Route evidence, recall, corrections, and history through memory tools.",
        "- When write tools are available, use them for concrete durable deltas.",
        "- If write tools are unavailable, state the intended durable update clearly without pretending it was stored.",
        "- Keep durable writes small and human-legible; prefer the user's own wording for names, threads, and preferences.",
        "- If a default workspace path is provided, use it for user-requested files, downloads, clones, and generated artifacts unless the user gives another path.",
    )


def build_identity_kernel(profile: LoadedProfile) -> tuple[str, ...]:
    return build_identity_capsule_section(profile)


def build_aegis_section(profile: LoadedProfile) -> tuple[str, ...]:
    return build_continuity_contract_section(profile)


def build_identity_section(
    profile: LoadedProfile,
    *,
    prompt_mode: PromptMode = "full",
) -> tuple[str, ...]:
    return build_identity_capsule_section(profile, prompt_mode=prompt_mode)


def build_user_snapshot_section(
    profile: LoadedProfile,
    *,
    prompt_mode: PromptMode = "full",
) -> tuple[str, ...]:
    identity = build_companion_identity_state(profile)
    parsed_profile = parse_user_profile_content(user_profile_text(profile))
    known_fields = dict(parsed_profile.field_values)
    durable_notes = parsed_profile.durable_notes
    structured_summary = render_user_profile_text(**known_fields)
    note_summary = _durable_note_summary(durable_notes)
    summary_parts = [structured_summary] if structured_summary else []
    if note_summary:
        summary_parts.append(f"Durable notes: {note_summary}")
    lines = [
        "section:user-snapshot",
        f"user-known-fields={', '.join(known_fields.keys()) or 'none'}",
        f"user-summary={' | '.join(summary_parts) or 'No durable user profile facts are set yet.'}",
    ]
    if prompt_mode == "full":
        lines.extend(
            (
                f"active-display-name={identity.display_name}",
                f"mode={identity.mode}",
                f"continuity-notes={', '.join(identity.continuity_notes) or 'none'}",
                f"user-canonical-fields={', '.join(_USER_FIELD_LABELS)}",
                f"user-open-facts={note_summary or 'none'}",
                f"user-open-facts-count={len(durable_notes)}",
            )
        )
    return tuple(lines)


def build_personality_section(
    profile: LoadedProfile,
    *,
    prompt_mode: PromptMode = "full",
) -> tuple[str, ...]:
    return build_identity_section(profile, prompt_mode=prompt_mode)


def build_prompt_contract(
    profile: LoadedProfile,
    *,
    prompt_mode: PromptMode = "full",
) -> PromptContract:
    stable_sections: list[tuple[str, tuple[str, ...]]] = [
        ("identity-capsule", build_identity_capsule_section(profile, prompt_mode=prompt_mode)),
        ("continuity-contract", build_continuity_contract_section(profile)),
        ("activity-routing", build_activity_routing_section(profile)),
        ("state-and-tool-writes", build_state_and_tool_writes_section(profile)),
    ]
    profile_snapshot_sections: list[tuple[str, tuple[str, ...]]] = [
        ("user-snapshot", build_user_snapshot_section(profile, prompt_mode=prompt_mode)),
    ]
    sections = [*stable_sections, *profile_snapshot_sections]
    stable_prefix_refs = tuple(line for _, lines in stable_sections for line in lines)
    profile_snapshot_refs = tuple(line for _, lines in profile_snapshot_sections for line in lines)
    instruction_refs = tuple((*stable_prefix_refs, *profile_snapshot_refs))
    return PromptContract(
        prompt_mode=prompt_mode,
        section_names=tuple(name for name, _ in sections),
        instruction_refs=instruction_refs,
        stable_prefix_refs=stable_prefix_refs,
        profile_snapshot_refs=profile_snapshot_refs,
    )


def _durable_note_summary(notes: tuple[str, ...], *, limit: int = 3) -> str:
    if not notes:
        return ""
    shown = notes[:limit]
    remainder = len(notes) - len(shown)
    summary = " | ".join(shown)
    if remainder > 0:
        summary += f" | +{remainder} more"
    return summary


def _core_charter_projection(profile: LoadedProfile) -> str:
    compact = " ".join(aegis_text(profile).strip().split())
    default_compact = " ".join(DEFAULT_AEGIS_TEXT.strip().split())
    if not compact or compact == default_compact:
        return "Aegis is a persistent personal AI built to protect continuity, context, and trust across time."
    return compact


def _custom_clone_note(profile: LoadedProfile, *, display_name: str) -> str:
    note = (profile.clone_text or "").strip()
    if not note:
        return ""
    normalized = " ".join(note.split()).casefold()
    generated_prefix = f"you are {display_name}, a named aegis clone on one long-lived continuity line.".casefold()
    if normalized.startswith(generated_prefix) and "default posture:" in normalized:
        return ""
    return note
