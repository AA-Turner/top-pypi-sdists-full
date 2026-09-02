"""Render a ``SkillPreamble`` into the system-prompt segment that prepends
to the agent's system instruction at request prep time.

The whole segment is wrapped in an ``<available_skills>`` XML-like tag —
the established convention in this codebase for injected context blocks
(see ``<data_context>``, ``<web_context>``, ``<observations>``). The
opening tag doubles as the idempotency marker (``SKILL_PREAMBLE_TAG``).

Layout:

    <available_skills>
    You have access to NN skills across:
    - persistence (8) — durable write patterns and data-loss prevention
    - workflow (5) — DAG design, recovery, scheduler
    ...

    Use `skill(action="list", category=...)` to browse,
    `skill(action="search", query=...)` to find,
    `skill(action="get", skill_id=...)` to read.

    <preconfigured_skills>
    - <skill_id> — <description>
    </preconfigured_skills>

    <active_skills>
    <body 1>
    ---
    <body 2>
    </active_skills>
    </available_skills>

The segment is **stable per agent config + skill set**, so the same agent
+ same skills produces byte-identical text on every run. That stability is
what makes provider prompt caching work (A1).
"""

from __future__ import annotations

from matrx_ai.skills.models import SkillPreamble

# Opening tag of the injected block. Also the idempotency marker used by the
# host's preamble injector to avoid prepending twice into one system prompt.
SKILL_PREAMBLE_TAG = "<available_skills>"

_MAX_OVERVIEW_CATEGORIES = 12
_OVERVIEW_DESC_TRUNCATE = 80


def render_overview_lines(
    overview: list[tuple[str, str, int]],
) -> list[str]:
    """Produce the per-category one-liners shown in the preamble.

    Truncates descriptions to keep the budget tight (~200 tokens for the
    whole overview block). If there are more than ``_MAX_OVERVIEW_CATEGORIES``
    top-level categories, the tail is collapsed into an "Other" line.
    """
    if not overview:
        return []

    lines: list[str] = []
    visible = overview[:_MAX_OVERVIEW_CATEGORIES]
    overflow = overview[_MAX_OVERVIEW_CATEGORIES:]

    for key, description, count in visible:
        desc = (description or "").strip()
        if len(desc) > _OVERVIEW_DESC_TRUNCATE:
            desc = desc[: _OVERVIEW_DESC_TRUNCATE - 1].rstrip() + "…"
        if desc:
            lines.append(f"- {key} ({count}) — {desc}")
        else:
            lines.append(f"- {key} ({count})")

    if overflow:
        other_total = sum(c for _, _, c in overflow)
        lines.append(f"- … ({other_total} more in {len(overflow)} other categories)")

    return lines


def render_preamble(preamble: SkillPreamble) -> str:
    """Render the full markdown segment. Empty input → empty string."""
    if not preamble.overview_lines and not preamble.listed_skills and not preamble.included_skills:
        return ""

    parts: list[str] = [SKILL_PREAMBLE_TAG, ""]

    if preamble.overview_lines:
        parts.append(f"You have access to {preamble.total_active_count} skills across:")
        parts.extend(preamble.overview_lines)
        parts.append("")

    parts.append(
        'Use `skill(action="list", category=...)` to browse, '
        '`skill(action="search", query=...)` to find, '
        '`skill(action="get", skill_id=...)` to read.'
    )
    parts.append("")

    if preamble.listed_skills:
        parts.append("<preconfigured_skills>")
        for hint in preamble.listed_skills:
            parts.append(f"- {hint.skill_id} — {hint.description}")
        parts.append("</preconfigured_skills>")
        parts.append("")

    if preamble.included_skills:
        parts.append("<active_skills>")
        parts.append("")
        body_blocks: list[str] = []
        for body in preamble.included_skills:
            body_blocks.append(f"{body.skill_id} — {body.label}\n\n{body.body.rstrip()}")
        parts.append("\n\n---\n\n".join(body_blocks))
        parts.append("")
        parts.append("</active_skills>")

    parts.append("</available_skills>")

    return "\n".join(parts).rstrip() + "\n"
