from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from packages.contracts import ExperienceRecord

from .runtime_snapshot import load_snapshot_session_context_epoch
from .shell_progress import render_tool_trace_text
from .shell_stack import Align, Group, Panel, RICH_AVAILABLE, Table, Text
from .shell_ui import (
    BRAND_ACCENT,
    BRAND_ACCENT_STRONG,
    BRAND_DARK,
    BRAND_LIGHT,
    BRAND_MUTED,
    EXPERIENCE_NOISE_PATTERN,
    GROWTH_HIGHLIGHT_FG,
    GROWTH_LEVEL_PATTERN,
    GROWTH_META_PATTERN,
    GROWTH_PROGRESS_EMPTY,
    GROWTH_PROGRESS_FILLED,
    GROWTH_PROGRESS_WIDTH,
    SETTLED_DIFF_ADD_FG,
    SETTLED_DIFF_CONTEXT_FG,
    SETTLED_DIFF_FILE_FG,
    SETTLED_DIFF_HUNK_FG,
    SETTLED_DIFF_REMOVE_FG,
    SHELL_WELCOME_HEADLINE,
    USER_HISTORY_BG,
    USER_HISTORY_FG,
    compact_line,
    render_growth_mark,
    render_guardian_mark,
    render_highlighted_history_line,
    render_markdown_bold,
    strip_markdown_bold,
)

if TYPE_CHECKING:
    from .shell import ProductizedShell, TranscriptEntry


def render_shell_frame(shell: ProductizedShell):
    session = shell.runtime.inspect_session(shell.session_id)
    continuity = shell.runtime.inspect_continuity(session_id=shell.session_id)
    context_frame = shell.runtime.inspect_context_frame(session.session_id)
    provider = dict(shell.runtime.provider_summary())
    growth = shell.runtime.inspect_growth(session_id=shell.session_id)
    clone_id = shell.runtime.clone_id_for_session(session)
    if RICH_AVAILABLE and Table is not None and Group is not None:
        hero = Table.grid(expand=True)
        console_width = getattr(shell.console.size, "width", 0)
        if console_width and console_width < 132:
            hero.add_column(ratio=1, min_width=48)
            hero.add_row(render_brand_column(shell, session, provider, growth))
            hero.add_row(Text(" "))
            hero.add_row(render_status_column(shell, session, continuity, context_frame, provider, growth))
        else:
            hero.add_column(ratio=13, min_width=72)
            hero.add_column(ratio=12, min_width=42)
            hero.add_row(
                render_brand_column(shell, session, provider, growth),
                render_status_column(shell, session, continuity, context_frame, provider, growth),
            )
        return Panel(
            hero,
            title=f"[bold {BRAND_ACCENT}] 🥚 🐣 Your Own Aegis [/bold {BRAND_ACCENT}]",
            subtitle=f"[bold {BRAND_LIGHT}]🧠 Persistent memory, long-horizon decisions, and long context.[/bold {BRAND_LIGHT}]",
            border_style=BRAND_ACCENT,
            padding=(1, 2),
        )
    logo = "\n".join(
        (
            "    ___    ________ _____ _____ _____",
            "   /   |  / ____/ //_/ // / ___// ___/",
            "  / /| | / / __/ ,< / ,<  \\__ \\\\__ \\",
            " / ___ |/ /_/ / /| / /| |___/ /__/ /",
            "/_/  |_|\\____/_/ |_/_/ |_/____/____/",
        )
    )
    growth_lines = growth_panel_lines(shell, session, continuity, provider, growth)
    lines = [
        SHELL_WELCOME_HEADLINE,
        "🥚 🐣 The Aegis that remembers, reasons, and stays with you.",
        logo,
        "",
        "Persistent memory · long-horizon decisions · long context",
        "",
        "💡 Tips for getting started",
        "Speak directly, or type / to unseal the command palette.",
        "",
        "🌱 Stage",
        *growth_lines,
        "",
        f"clone: {clone_id}",
        f"continuity: {session.session_id[:8]}",
        (
            f"provider: {provider['provider_id']} · "
            f"deliberate: {provider.get('strong_model') or '<unset>'} · "
            f"swift: {provider.get('weak_model') or '<unset>'}"
        ),
    ]
    return Panel(
        Text("\n".join(lines)),
        title=" 🥚 🐣 Your Own Aegis ",
        subtitle=" 🧠 Persistent memory, long-horizon decisions, and long context ",
        border_style="bright_white",
        padding=(1, 2),
    )


def render_brand_column(shell: ProductizedShell, session, provider, growth):
    continuity = shell.runtime.inspect_continuity(session_id=shell.session_id)
    display_name = continuity.profile.state.display_name or "Aegis"
    heading = Text(no_wrap=True)
    heading.append(f"{SHELL_WELCOME_HEADLINE}\n", style=f"bold {BRAND_LIGHT}")
    heading.append("🥚 🐣 The Aegis that remembers, reasons, and stays with you.", style=BRAND_MUTED)
    meta = Text(no_wrap=True)
    meta.append(f"{display_name}\n", style=f"bold {BRAND_LIGHT}")
    meta.append("Persistent memory · long-horizon decisions · long context\n", style=BRAND_MUTED)
    meta.append(f"{growth.identity_line} · Lv.{growth.ascension_level}\n", style=BRAND_ACCENT_STRONG)
    meta.append(
        (
            f"deliberate {provider.get('strong_model') or '<unset>'} · "
            f"swift {provider.get('weak_model') or '<unset>'} · companion mode\n"
        ),
        style=BRAND_LIGHT,
    )
    meta.append(f"{shell.cwd}", style=BRAND_MUTED)
    if Table is None:
        return Group(heading, shell._render_growth_mark(growth.brand_stage_id, level=growth.ascension_level), meta)
    brand = Table.grid(expand=True)
    brand.add_column(no_wrap=True)
    brand.add_row(shell._center_brand_block(heading))
    brand.add_row(shell._center_brand_block(Text(" ")))
    brand.add_row(shell._center_brand_block(shell._render_growth_mark(growth.brand_stage_id, level=growth.ascension_level)))
    brand.add_row(shell._center_brand_block(Text(" ")))
    brand.add_row(shell._center_brand_block(meta))
    return brand


def render_status_column(shell: ProductizedShell, session, continuity, context_frame, provider, growth):
    divider = "─" * 44
    total_skills, self_learned_skills = skill_inventory_counts(shell)
    tips = Text()
    tips.append("💡 Tips for getting started\n", style=f"bold {BRAND_ACCENT}")
    tips.append("Speak directly, or open / to unseal the command palette.\n", style=BRAND_LIGHT)
    tips.append(f"{divider}\n", style=BRAND_DARK)
    tips.append("🌱 Progression\n", style=f"bold {BRAND_ACCENT}")
    tips.append(f"identity · {growth.identity_line}\n", style=BRAND_LIGHT)
    tips.append(f"level · Lv.{growth.ascension_level} · Power {growth.power_score}\n", style=BRAND_LIGHT)
    tips.append("progress · ", style=BRAND_LIGHT)
    tips.append_text(styled_growth_progress_bar(growth))
    tips.append(f" · {growth.progress_percent}%\n", style=BRAND_LIGHT)
    tips.append(f"next · {growth.next_milestone}\n", style=BRAND_LIGHT)
    if growth.active_challenge_tracks:
        tips.append(f"challenge · {growth.active_challenge_tracks[0].summary}\n", style=BRAND_LIGHT)
    tips.append(f"proof · {growth.proof_state}\n", style=BRAND_MUTED)
    tips.append(
        f"stance · {growth.momentum_state} momentum · {growth.dominant_archetype} path\n",
        style=BRAND_LIGHT,
    )
    tips.append(f"skills · {total_skills} current · {self_learned_skills} self-learned\n", style=BRAND_LIGHT)
    tips.append(
        (
            "lifetime · "
            f"{growth.canonical_dialogues} dialogues · "
            f"{growth.canonical_active_days} active days · "
            f"{growth.lifetime_days} days across time\n"
        ),
        style=BRAND_LIGHT,
    )
    tips.append(
        (
            "learning · "
            f"{growth.canonical_experiences} experiences · "
            f"{growth.canonical_promoted_procedures} promoted · "
            f"{growth.state.total_tokens} tokens\n"
        ),
        style=BRAND_LIGHT,
    )
    experiences = shell.runtime.inspect_experiences(session_id=session.session_id, limit=2)
    displayable = displayable_experiences(experiences)
    if displayable:
        tips.append(f"latest · {format_experience_status(displayable[0])}\n", style=BRAND_LIGHT)
    else:
        tips.append("latest · no captured experience yet\n", style=BRAND_MUTED)
    frame = getattr(context_frame, "frame", None)
    if frame is not None:
        clone_id = shell.runtime.clone_id_for_session(session)
        session_epoch = load_snapshot_session_context_epoch(shell.runtime, session_id=session.session_id)
        frozen_focus = _session_epoch_focus_summary(session_epoch)
        frozen_turns = _session_epoch_turn_count(session_epoch)
        tips.append(f"{divider}\n", style=BRAND_DARK)
        tips.append("🧠 Current Context\n", style=f"bold {BRAND_ACCENT}")
        tips.append(
            f"thread · {clone_id} · session {session.session_id[:8]}\n",
            style=BRAND_MUTED,
        )
        tips.append(
            f"thread focus · {frozen_focus}\n",
            style=BRAND_LIGHT,
        )
        tips.append(
            (
                (
                    "session freeze · "
                    f"skills {session_epoch.frozen_skill_count} · "
                    f"tools {session_epoch.frozen_tool_count}"
                    f"{f' · {frozen_turns} turns' if frozen_turns else ''}\n"
                )
                if session_epoch is not None and session_epoch.frozen
                else "session freeze · pending first turn\n"
            ),
            style=BRAND_LIGHT if session_epoch is not None and session_epoch.frozen else BRAND_MUTED,
        )
        tips.append(
            (
                "frozen memory · "
                f"profile {len(frame.session_snapshot.profile_refs)} · "
                f"work {len(frame.session_snapshot.work_refs)} · "
                f"evidence {len(frame.session_snapshot.evidence_refs)}\n"
            ),
            style=BRAND_LIGHT,
        )
        if session_epoch is not None and session_epoch.frozen:
            tips.append(
                (
                    "frozen overlays · "
                    f"{len(frame.procedure_overlay.source_refs)} procedures · "
                    f"{len(frame.workspace_attachments.source_refs)} attachments\n"
                ),
                style=BRAND_LIGHT,
            )
        if frame.rationale:
            tips.append(
                f"why this context · {compact_line(frame.rationale, limit=120)}\n",
                style=BRAND_MUTED,
            )
    return tips


def skill_inventory_counts(shell: ProductizedShell) -> tuple[int, int]:
    skills = tuple(skill for skill in shell.runtime.skill_catalog(session_id=shell.session_id) if skill.enabled)
    authored_root = shell.runtime.paths.authored_skills_dir.expanduser().resolve()
    self_learned = sum(1 for skill in skills if is_self_learned_skill(skill, authored_root=authored_root))
    return (len(skills), self_learned)


def _session_epoch_focus_summary(session_epoch) -> str:
    if session_epoch is None or not session_epoch.frozen:
        return "No session focus is frozen yet; the first real turn will lock it in."
    return compact_line(
        session_epoch.thread_focus or "No durable session focus was frozen for this thread.",
        limit=120,
    )


def _session_epoch_turn_count(session_epoch) -> int:
    if session_epoch is None:
        return 0
    return sum(1 for line in session_epoch.history_lines if line.startswith("user:"))


def is_self_learned_skill(skill, *, authored_root: Path) -> bool:
    source_kind = str(skill.metadata.get("source_kind") or "").strip()
    if source_kind == "aegis-experience":
        return True
    provenance = str(skill.provenance or skill.metadata.get("entry_path") or "").strip()
    if not provenance:
        return False
    try:
        Path(provenance).expanduser().resolve().relative_to(authored_root)
    except (ValueError, OSError):
        return False
    return True


def render_pending_entries(shell: ProductizedShell) -> None:
    pending = shell.transcript[shell._rendered_entries :]
    previous_kind = shell.transcript[shell._rendered_entries - 1].kind if shell._rendered_entries else None
    index = 0
    while index < len(pending):
        entry = pending[index]
        if entry.kind == "assistant" and previous_kind in {"user", "tooltrace"}:
            shell.console.print("")
        if entry.kind == "tooltrace":
            grouped_entries = [entry]
            index += 1
            while index < len(pending) and pending[index].kind == "tooltrace":
                grouped_entries.append(pending[index])
                index += 1
            shell.console.print(render_tooltrace_entries(tuple(grouped_entries)))
            previous_kind = "tooltrace"
            continue
        shell.console.print(render_entry(shell, entry))
        previous_kind = entry.kind
        index += 1
    shell._rendered_entries = len(shell.transcript)
    render_pending_context_compaction_frame(shell)


def render_pending_context_compaction_frame(shell: ProductizedShell) -> None:
    frame = getattr(shell, "_pending_context_compaction_frame", None)
    if not isinstance(frame, dict) or shell._pending_context_compaction_frame_rendered:
        return
    kernel_stage_events = frame.get("kernel_stage_events")
    if not isinstance(kernel_stage_events, tuple):
        return
    shell.console.print(
        shell._render_turn_frame(
            prompt=str(frame.get("prompt") or ""),
            tick=int(frame.get("tick") or 0),
            kernel_stage_events=kernel_stage_events,
        )
    )
    shell._pending_context_compaction_frame_rendered = True


def render_entry(shell: ProductizedShell, entry: TranscriptEntry):
    styles = {
        "assistant": BRAND_LIGHT,
        "user": USER_HISTORY_FG,
        "growth": BRAND_ACCENT_STRONG,
        "tooltrace": BRAND_ACCENT_STRONG,
        "command": BRAND_ACCENT,
        "status": "bright_black",
        "notice": "white",
        "recovery": "yellow",
    }
    if entry.kind == "tooltrace":
        return render_tooltrace_entry(entry)
    if entry.kind in {"assistant", "user", "growth"}:
        if RICH_AVAILABLE:
            return render_chat_entry(shell, entry, accent=styles.get(entry.kind, "white"))
        prefix = "" if entry.kind in {"user", "growth"} else "● "
        lines = [f"{prefix}{strip_markdown_bold(entry.body)}"]
        if entry.meta:
            lines.append(entry.meta)
        return "\n".join(lines) + "\n"
    return Panel(
        Text(entry.body),
        title=entry.title,
        subtitle=entry.meta,
        border_style=styles.get(entry.kind, "white"),
        padding=(0, 1),
    )


def growth_panel_lines(shell: ProductizedShell, session, continuity, provider, growth) -> tuple[str, ...]:
    total_skills, self_learned_skills = skill_inventory_counts(shell)
    lines = [
        f"identity · {growth.identity_line}",
        f"level · Lv.{growth.ascension_level} · Power {growth.power_score}",
        f"progress · {growth_progress_bar(growth)} · {growth.progress_percent}%",
        f"next · {growth.next_milestone}",
    ]
    if growth.active_challenge_tracks:
        lines.append(f"challenge · {growth.active_challenge_tracks[0].summary}")
    lines.append(f"proof · {growth.proof_state}")
    lines.append(f"skills · {total_skills} current · {self_learned_skills} self-learned")
    lines.extend(
        [
            (
                "lifetime · "
                f"{growth.canonical_dialogues} dialogues · "
                f"{growth.canonical_active_days} active days · "
                f"{growth.lifetime_days} days across time"
            ),
            (
                "learning · "
                f"{growth.canonical_experiences} experiences · "
                f"{growth.canonical_promoted_procedures} promoted · "
                f"{growth.state.total_tokens} tokens"
            ),
        ]
    )
    experiences = shell.runtime.inspect_experiences(session_id=session.session_id, limit=2)
    displayable = displayable_experiences(experiences)
    if displayable:
        lines.append(f"latest · {format_experience_status(displayable[0])}")
    else:
        lines.append("latest · no captured experience yet")
    return tuple(lines)


def recent_activity_lines(shell: ProductizedShell, session, continuity, provider) -> tuple[str, ...]:
    growth = shell.runtime.inspect_growth(session_id=session.session_id)
    return growth_panel_lines(shell, session, continuity, provider, growth)


def recent_experience_lines(experiences: tuple[ExperienceRecord, ...]) -> tuple[str, ...]:
    return tuple(f"learning · {format_experience_status(experience)}" for experience in experiences)


def displayable_experiences(experiences: tuple[ExperienceRecord, ...]) -> tuple[ExperienceRecord, ...]:
    filtered = tuple(experience for experience in experiences if should_display_experience(experience))
    return filtered[:2]


def should_display_experience(experience: ExperienceRecord) -> bool:
    title = " ".join(experience.title.split()).strip()
    summary = " ".join(experience.summary.split()).strip()
    text = f"{title} {summary}".strip()
    if not text:
        return False
    lowered = text.lower()
    if EXPERIENCE_NOISE_PATTERN.match(title) or EXPERIENCE_NOISE_PATTERN.match(summary):
        return False
    if "requires an 'action' argument" in lowered:
        return False
    if "controls:" in lowered and "outcome: error" in lowered:
        return False
    return True


def format_experience_status(experience: ExperienceRecord) -> str:
    markers = [experience.status]
    if experience.tool_call_count:
        markers.append(f"tools={experience.tool_call_count}")
    if experience.model_turn_count:
        markers.append(f"turns={experience.model_turn_count}")
    if experience.related_skill_ids:
        markers.append(f"skills={len(experience.related_skill_ids)}")
    title = compact_line(experience.title, limit=68)
    return f"{title} [{', '.join(markers)}]"


def growth_progress_counts(growth, *, width: int = GROWTH_PROGRESS_WIDTH) -> tuple[int, int]:
    filled = min(width, max(0, round(growth.progress_ratio * width)))
    if growth.progress_ratio > 0 and filled == 0:
        filled = 1
    if growth.progress_ratio < 1 and filled == width:
        filled = width - 1
    return filled, width - filled


def growth_progress_bar(growth, *, width: int = GROWTH_PROGRESS_WIDTH) -> str:
    filled, empty = growth_progress_counts(growth, width=width)
    return (GROWTH_PROGRESS_FILLED * filled) + (GROWTH_PROGRESS_EMPTY * empty)


def styled_growth_progress_bar(growth, *, width: int = GROWTH_PROGRESS_WIDTH):
    bar = Text()
    filled, empty = growth_progress_counts(growth, width=width)
    if filled:
        bar.append(GROWTH_PROGRESS_FILLED * filled, style=BRAND_ACCENT_STRONG)
    if empty:
        bar.append(GROWTH_PROGRESS_EMPTY * empty, style=BRAND_MUTED)
    return bar


def render_chat_entry(shell: ProductizedShell, entry: TranscriptEntry, *, accent: str):
    if entry.kind in {"user", "growth"}:
        block = Text()
        lines = strip_markdown_bold(entry.body).splitlines() or [""]
        body_style = f"{USER_HISTORY_FG} on {USER_HISTORY_BG}"
        meta_style = f"{BRAND_MUTED} on {USER_HISTORY_BG}"
        for index, line in enumerate(lines):
            prefix = "› " if index == 0 else "  "
            padded_line = shell._pad_history_line(f"{prefix}{line}")
            if entry.kind == "growth":
                block.append_text(
                    render_highlighted_history_line(
                        padded_line,
                        base_style=body_style,
                        highlight_pattern=GROWTH_LEVEL_PATTERN,
                        highlight_style=f"{GROWTH_HIGHLIGHT_FG} on {USER_HISTORY_BG}",
                    )
                )
            else:
                block.append(padded_line, style=body_style)
            block.append("\n")
        if entry.meta:
            for meta_line in entry.meta.splitlines() or [""]:
                padded_meta = shell._pad_history_line(f"  {meta_line}")
                if entry.kind == "growth":
                    block.append_text(
                        render_highlighted_history_line(
                            padded_meta,
                            base_style=meta_style,
                            highlight_pattern=GROWTH_META_PATTERN,
                            highlight_style=f"{GROWTH_HIGHLIGHT_FG} on {USER_HISTORY_BG}",
                        )
                    )
                else:
                    block.append(padded_meta, style=meta_style)
                block.append("\n")
        return block

    block = Text()
    block.append("● ", style=f"bold {accent}")
    block.append_text(render_markdown_bold(entry.body, base_style=BRAND_LIGHT))
    if entry.meta:
        block.append(f"\n{entry.meta}", style=BRAND_MUTED)
    block.append("\n")
    return block


def render_tooltrace_entry(entry: TranscriptEntry):
    return render_tooltrace_entries((entry,))


def render_tooltrace_entries(entries: tuple[TranscriptEntry, ...]):
    if not RICH_AVAILABLE:
        lines: list[str] = []
        for entry in entries:
            body_lines = entry.body.splitlines() or [entry.body]
            lines.extend(strip_markdown_bold(line).rstrip("\n") for line in body_lines)
            if entry.meta:
                lines.extend(entry.meta.splitlines())
        return "\n".join(line for line in lines if line)

    block = Text()
    for entry_index, entry in enumerate(entries):
        body_lines = entry.body.splitlines() or [entry.body]
        normalized_body_lines = [strip_markdown_bold(line).rstrip("\n") for line in body_lines]
        for line_index, body_line in enumerate(normalized_body_lines):
            if body_line:
                block.append_text(_render_tooltrace_body_line(body_line))
            is_last_body_line = line_index == len(normalized_body_lines) - 1
            if not is_last_body_line or entry.meta or entry_index < len(entries) - 1:
                block.append("\n")
        if entry.meta:
            meta_lines = entry.meta.splitlines() or [entry.meta]
            for meta_index, meta_line in enumerate(meta_lines):
                block.append(meta_line, style=BRAND_MUTED)
                is_last_meta_line = meta_index == len(meta_lines) - 1
                if not is_last_meta_line or entry_index < len(entries) - 1:
                    block.append("\n")
    return block


def _render_tooltrace_body_line(line: str) -> Text:
    if line.startswith("a/") and " → b/" in line:
        return Text(line, style=SETTLED_DIFF_FILE_FG)
    if line.startswith("@@"):
        return Text(line, style=SETTLED_DIFF_HUNK_FG)
    if line.startswith("+"):
        return Text(line, style=SETTLED_DIFF_ADD_FG)
    if line.startswith("-"):
        return Text(line, style=SETTLED_DIFF_REMOVE_FG)
    if line.startswith(" "):
        return Text(line, style=SETTLED_DIFF_CONTEXT_FG)
    if line.startswith("… omitted ") and "diff line(s)" in line:
        return Text(line, style=SETTLED_DIFF_CONTEXT_FG)
    return render_tool_trace_text(line)


def center_brand_block(renderable):
    if Align is None:
        return renderable
    return Align.center(renderable)


def render_growth_mark_for_stage(stage_id: str, *, level: int | None = None):
    return render_growth_mark(stage_id, level=level)


def render_guardian_brand_mark():
    return render_guardian_mark()
