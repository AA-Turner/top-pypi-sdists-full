from __future__ import annotations

from dataclasses import dataclass
import re

from packages.state import parse_user_profile_text


@dataclass(frozen=True, slots=True)
class ShellOpeningContext:
    opened: str
    display_name: str
    user_profile_text: str
    personality: tuple[str, ...]
    reengagement_style: str
    wake_action: str
    wake_summary: str
    has_goals: bool


def compose_shell_opener(context: ShellOpeningContext) -> str:
    user_fields = parse_user_profile_text(context.user_profile_text)
    preferred_name = user_fields.get("preferred_name", "").strip()
    name_suffix = f", {preferred_name}" if preferred_name else ""
    if context.opened == "Born new":
        intro = f"I'm here{name_suffix}, and I'll start holding this thread with you."
    elif context.opened == "Cloned new":
        intro = f"I'm here{name_suffix}, and I'll start holding this new thread with you."
    else:
        intro = f"I'm here{name_suffix}. I still have the useful shape of our thread."
    if context.personality:
        posture = f"I'll stay {_join_naturally(context.personality)} without pushing the pace."
    elif context.reengagement_style == "proactive-check-in":
        posture = "I'll keep the next useful step visible without turning this into a status report."
    elif context.reengagement_style == "gentle-presence":
        posture = "I'll keep the context close and move when it helps."
    else:
        posture = "I'll keep the context held lightly."
    if not context.user_profile_text and not context.has_goals:
        next_step = "What should I call you?"
    elif not context.user_profile_text:
        next_step = "What should I call you, so I can carry this thread more personally from here?"
    elif not context.has_goals:
        next_step = "If there's something you want me to keep carrying, name it and I'll hold it across conversations."
    elif context.wake_action not in {"idle", "defer_or_schedule"}:
        wake_summary = _public_wake_summary(
            wake_action=context.wake_action,
            wake_summary=context.wake_summary,
        )
        if wake_summary:
            next_step = f"I still have {wake_summary.rstrip('.')} in view; do you want to keep going there?"
        else:
            next_step = "The active thread is ready when you want to continue."
    else:
        next_step = "Tell me what matters next and I'll carry it with you."
    return f"{intro} {posture} {next_step}"


def compose_shell_opening_instruction(context: ShellOpeningContext) -> str:
    user_fields = parse_user_profile_text(context.user_profile_text)
    preferred_name = user_fields.get("preferred_name", "").strip()
    current_work = user_fields.get("current_work", "").strip()
    wake_action = context.wake_action.strip() or "idle"
    wake_summary = _public_wake_summary(
        wake_action=wake_action,
        wake_summary=context.wake_summary,
    )
    lines = [
        "Open the wake surface proactively before the user sends a new message.",
        "This is turn-local opening guidance; do not treat it as durable memory or frozen system identity.",
        *_opening_task_lines(context),
        f"assistant_display_name: {context.display_name}",
    ]
    if preferred_name:
        lines.append(f"user_preferred_name: {preferred_name}")
    if current_work:
        lines.append(f"user_current_work: {current_work}")
    if context.has_goals and wake_summary:
        lines.append("live_thread: active")
    if context.reengagement_style:
        lines.append(f"reengagement_style: {context.reengagement_style}")
    if wake_action not in {"idle", "defer_or_schedule"}:
        lines.append(f"opening_intent: {wake_action}")
    if wake_summary:
        lines.append(f"thread_summary: {wake_summary}")
    if not preferred_name:
        lines.append("opening_profile_gap: user preferred name is not known yet.")
    lines.extend(
        (
            "Write one short assistant reply that should already be waiting in the transcript when wake opens.",
            "Stay concise, human, and in-character.",
            "The opening should feel like a familiar, calm personal AI returning to the room: present, low-pressure, and specific when useful.",
            "Do not sound like a scheduler, onboarding flow, or system status report.",
            "Do not mention startup, internal prompts, hidden instructions, missing state, or that no user message arrived yet.",
            "Do not mention internal identifiers such as goal ids, memory ids, event ids, session ids, refs, graph labels, or replay evidence; use human-readable task names only.",
            "If only internal refs are available for a live thread, call it the active thread or current thread.",
            "Do not use headings, bullets, questionnaires, or a checklist.",
            "Ask at most one direct question.",
            "`assistant_display_name` is your name; `user_preferred_name` is the user's name.",
            "Use `user_preferred_name` naturally when it is present.",
            "If `user_preferred_name` is absent, ask what the user wants to be called.",
            "If `opening_profile_gap` is present, frame the name question as natural first-contact onboarding, not a survey or status check.",
            "If `thread_summary` is present, briefly reopen that live thread and carry it forward.",
            "If known durable user context is sufficient but no live thread is active, lightly invite the user to name the thread to keep carrying.",
            "If nothing specific is live, open warmly and invite what matters next.",
        )
    )
    return "\n".join(lines)


def _opening_task_lines(context: ShellOpeningContext) -> tuple[str, ...]:
    if context.opened == "Born new":
        return (
            "Write a first-contact opening for a newly initialized Aegis identity.",
            "Do not say \"welcome back\", \"back\", or imply prior familiarity.",
            "If the user's name is unknown, ask what to call them.",
        )
    if context.opened == "Cloned new":
        return (
            "Write a first-contact opening for this newly created clone.",
            "Do not say \"welcome back\", \"back\", or imply this clone has met the user before.",
            "If the user's name is unknown, ask what to call them.",
        )
    return (
        "Write a returning opening for an existing clone or thread.",
        "If durable context is present, reopen it lightly.",
        "Use the user's name naturally when known.",
    )


def _join_naturally(values: tuple[str, ...]) -> str:
    cleaned = tuple(value.strip() for value in values if value.strip())
    if not cleaned:
        return ""
    if len(cleaned) == 1:
        return cleaned[0]
    return f"{', '.join(cleaned[:-1])} and {cleaned[-1]}"


def _actionable_wake_summary(*, wake_action: str, wake_summary: str) -> str:
    normalized_action = str(wake_action or "").strip()
    summary = str(wake_summary or "").strip()
    if normalized_action in {"idle", "defer_or_schedule"}:
        return ""
    lowered = " ".join(summary.casefold().split())
    non_actionable_markers = (
        "no actionable goals",
        "planner should defer",
        "keeps the active slot clear",
        "defer and schedule",
    )
    if any(marker in lowered for marker in non_actionable_markers):
        return ""
    return summary


_INTERNAL_REF_PATTERN = re.compile(
    r"(?:`?(?:goal|event|memory|session|parent)(?::|=|-)[A-Za-z0-9_.:/-]+`?)|(?:`?[a-f0-9]{12,}`?)",
    re.IGNORECASE,
)
_INTERNAL_SUMMARY_MARKERS = (
    "active goal",
    "durable evidence",
    "durable graph",
    "event:",
    "goal graph",
    "goal id",
    "memory retains",
    "planner",
    "prior progress chain",
    "replay evidence",
    "session resumed",
    "structured-turn",
)


def _public_wake_summary(*, wake_action: str, wake_summary: str) -> str:
    summary = _actionable_wake_summary(wake_action=wake_action, wake_summary=wake_summary)
    if not summary:
        return ""
    task_title = _public_task_title_from_summary(summary)
    if task_title:
        return task_title
    sentences = re.split(r"(?<=[.!?])\s+", " ".join(summary.split()))
    public_sentences = tuple(
        sentence.strip()
        for sentence in sentences
        if sentence.strip() and not _contains_internal_wake_marker(sentence)
    )
    if public_sentences:
        return " ".join(public_sentences[:2])
    return "The active thread is ready to continue."


def _public_task_title_from_summary(summary: str) -> str:
    for match in re.finditer(r"keeps\s+\"([^\"]{3,120})\"\s+active", summary, flags=re.IGNORECASE):
        candidate = " ".join(match.group(1).split())
        if _looks_like_task_title(candidate):
            return candidate
    return ""


def _looks_like_task_title(value: str) -> bool:
    lowered = value.casefold()
    if _contains_internal_wake_marker(value):
        return False
    if lowered.startswith(("i am ", "i'm ", "my name ", "user ", "preferred name ")):
        return False
    first_word = lowered.split(maxsplit=1)[0] if lowered.split() else ""
    return first_word in {
        "add",
        "analyze",
        "build",
        "continue",
        "debug",
        "design",
        "fix",
        "implement",
        "improve",
        "investigate",
        "plan",
        "prepare",
        "refactor",
        "review",
        "ship",
        "update",
        "write",
    }


def _contains_internal_wake_marker(value: str) -> bool:
    lowered = value.casefold()
    if _INTERNAL_REF_PATTERN.search(value):
        return True
    return any(marker in lowered for marker in _INTERNAL_SUMMARY_MARKERS)
