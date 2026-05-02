"""Prompt-inspection helpers extracted from the CLI shell surface."""

from __future__ import annotations

from .runtime_snapshot import load_snapshot_session_context_epoch


def _append_frozen(self) -> None:
    epoch = load_snapshot_session_context_epoch(self.runtime, session_id=self.session_id)
    if epoch is None or not epoch.frozen:
        self._append_entry(
            "notice",
            "Frozen prompt",
            "\n".join(
                [
                    f"session_id: {self.session_id}",
                    "status: pending first turn",
                    "system prompt :: frozen_prefix",
                    "<not frozen yet>",
                    "",
                    "system prompt :: session_snapshot",
                    "<not frozen yet>",
                    "",
                    "user prompt :: base_turn_injections",
                    "<not frozen yet>",
                ]
            ),
        )
        return
    scoped_entries = _current_scoped_skill_entries(self)
    lines = [
        f"session_id: {epoch.session_id}",
        f"frozen_at: {epoch.frozen_at.isoformat() if epoch.frozen_at is not None else '<unknown>'}",
        f"thread_focus: {epoch.thread_focus or '<empty>'}",
        f"frozen_skill_count: {epoch.frozen_skill_count}",
        f"frozen_tool_count: {epoch.frozen_tool_count}",
        "frozen_skill_index:",
        *([f"- {_format_frozen_skill_index_entry(entry)}" for entry in epoch.frozen_skill_index] or ["<empty>"]),
        "",
        "frozen_skill_ids:",
        *([f"- {skill_id}" for skill_id in epoch.frozen_skill_ids] or ["<empty>"]),
        "",
        f"current_scoped_skill_count: {len(scoped_entries)}",
        "current_scoped_skill_entries:",
        *([f"- {entry}" for entry in scoped_entries] or ["<empty>"]),
        "",
        "frozen_skill_disclosures:",
        *(
            [
                f"- {record.display_name or record.skill_id} ({record.skill_id}) | {record.reason}"
                for record in epoch.frozen_skill_disclosures
            ]
            or ["<empty>"]
        ),
        "",
        "latest_skill_disclosures:",
        *(
            [
                f"- {record.display_name or record.skill_id} ({record.skill_id}) | {record.reason}"
                for record in epoch.latest_skill_disclosures
            ]
            or ["<empty>"]
        ),
        "",
        "frozen_tool_ids:",
        *([f"- {tool_id}" for tool_id in epoch.frozen_tool_ids] or ["<empty>"]),
        "",
        "note: frozen_skill_index is the bounded built-in capability shelf captured in the initial prompt; frozen_skill_ids preserve the identifier-only view; current_scoped_skill_entries show the live session-resolved shelf that can still gate governed overlays.",
        "",
        "note: only the initial frozen sections are shown below; append-only session history is intentionally omitted.",
        "",
        "system prompt :: frozen_prefix",
        epoch.frozen_prefix or "<empty>",
        "",
        "system prompt :: session_snapshot",
        epoch.session_snapshot or "<empty>",
        "",
        "user prompt :: base_turn_injections",
        epoch.base_turn_injections or "<empty>",
    ]
    self._append_entry("notice", "Frozen prompt", "\n".join(lines))


def _current_scoped_skill_entries(self) -> tuple[str, ...]:
    runtime = self.runtime
    if runtime.skill_runtime is None:
        return ()
    session = runtime.repository.load_session(self.session_id)
    if session is None:
        return ()
    profile = runtime.inspect_profile(session.profile_id)
    skills = runtime.skill_runtime.resolve_for_context(
        profile_id=profile.state.profile_id,
        workspace_id=session.workspace_id,
        session_id=session.session_id,
        mode=profile.state.mode,
    )
    return tuple(
        " | ".join(
            [
                skill.skill_id,
                skill.display_name,
                f"section={skill.metadata.get('category') or '<unknown>'}",
                f"source={skill.metadata.get('source_id') or '<unknown>'}",
                f"kind={skill.metadata.get('source_kind') or '<unknown>'}",
                f"tier={skill.metadata.get('storage_tier') or '<unknown>'}",
                f"enabled={str(skill.enabled).lower()}",
                f"command=/{skill.metadata.get('slash_command') or skill.skill_id}",
            ]
        )
        for skill in skills
    )


def _format_frozen_skill_index_entry(entry) -> str:
    detail = [
        f"{entry.display_name or entry.skill_id} ({entry.skill_id})",
        f"section={entry.category or '<unknown>'}",
        f"source={entry.source_id or '<unknown>'}",
        f"tier={entry.storage_tier or '<unknown>'}",
        "enabled=true",
    ]
    if entry.slash_command:
        detail.append(f"command=/{entry.slash_command}")
    return " | ".join(detail)
