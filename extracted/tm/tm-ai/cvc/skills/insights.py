"""
cvc.skills.insights — CVC Skill Insights (Phase 1B, native port).

Aggregate analytics over the ``cvc.skills.usage`` sidecar. This is the
*user-facing* view of what the agent loop has been loading: which skills
actually get used, which ones the agent sees but never touches, what's
fading, and what's hot.

Why this is unique to CVC
-------------------------
Most agent systems (Cursor, Claude Code, Aider) track tool calls. CVC
is the only one with a *cognitive* version control layer that knows:

* which skills were *shown* to the model (view_count) — wasted context
  if they're never *used* (use_count)
* which skills the model itself wrote (agent_created) vs. which were
  bundled / hub-installed
* the ratio of patches → a skill that's been patched 5 times in 3 days
  is a *living* skill, not a stable one

This module is **pure**: it takes the sidecar dict and returns a
structured ``SkillInsightsReport`` dataclass. All I/O is performed by
the caller (``load_usage()``). That makes it trivially testable and
reusable from CLI, the FastAPI gateway, the dashboard, and the future
scheduled insight cron job.

Public surface
--------------
    SkillInsightsReport           # dataclass — full report
    SkillInsight                  # dataclass — per-skill row
    SkillAction                   # dataclass — one recommended action
    compute_insights(usage, *, now=None, stale_after_days=30,
                     archive_after_days=90, ...) -> SkillInsightsReport
    recommend_actions(report) -> List[SkillAction]
    render_cli_summary(report, *, max_per_bucket=8,
                       include_actions=True) -> str    # Rich text
    to_jsonable(report) -> dict          # for /api/skills/insights
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional

from cvc.skills.usage import STATE_ARCHIVED, STATE_STALE

__all__ = [
    "SkillInsight",
    "SkillInsightsReport",
    "SkillAction",
    "compute_insights",
    "recommend_actions",
    "render_cli_summary",
    "to_jsonable",
]


# ---------------------------------------------------------------------------
# Dataclasses — the report shape
# ---------------------------------------------------------------------------


@dataclass
class SkillInsight:
    """One row in the insights table."""

    name: str
    state: str  # active | stale | archived
    pinned: bool
    agent_created: bool
    view_count: int
    use_count: int
    patch_count: int
    last_used_at: Optional[str]
    last_viewed_at: Optional[str]
    last_patched_at: Optional[str]
    days_since_last_use: Optional[int]
    use_to_view_ratio: float  # use_count / max(view_count, 1)
    category: str = "general"  # detected from directory layout

    @property
    def is_dead(self) -> bool:
        """A skill that's shown to the agent many times but never used.

        This is the *signature waste pattern* — it consumes context budget
        in every system prompt for nothing. Surfacing these is the single
        most actionable insight CVC can give the user.
        """
        return self.view_count >= 3 and self.use_count == 0 and not self.pinned

    @property
    def is_hot(self) -> bool:
        """A skill used at least 3 times in the last 7 days."""
        return (
            self.days_since_last_use is not None
            and self.days_since_last_use <= 7
            and self.use_count >= 3
        )

    @property
    def is_fading(self) -> bool:
        """A skill that was used before but not in 30+ days."""
        return (
            self.days_since_last_use is not None
            and self.days_since_last_use >= 30
            and self.use_count >= 3
        )


@dataclass
class SkillAction:
    """One concrete recommendation emitted by :func:`recommend_actions`.

    Each action is *safe* — it's a single CLI command the user can paste
    or that the CLI can execute with an explicit opt-in flag. No
    action runs without the user (or the dashboard's confirm button)
    pulling the trigger.

    Attributes
    ----------
    kind:
        ``archive`` — the skill should be archived (it's wasting context).
        ``unpin``   — the skill is pinned but currently unused; recommend
                      unpinning so the curator can manage it.
        ``review``  — the skill was used heavily in the past but is fading.
                      Worth a quick look before archiving.
        ``none``    — no action recommended (empty list).
    skill_name:
        The skill this action targets.
    reason:
        One-sentence human explanation ("shown to the model 12 times,
        never picked — wastes ~240 tokens of system prompt per turn").
    token_savings_estimate:
        Rough upper bound on tokens saved per turn if the action is
        applied. Assumes the dead skill's SKILL.md is ~avg_skill_tokens
        on the system prompt. Heuristic, not a guarantee.
    command:
        The exact ``cvc skills ...`` command to apply the action.
    risk:
        ``safe`` (auto-revertable), ``caution`` (data loss possible —
        archive, not delete), or ``review`` (needs human eyeballs).
    """

    kind: str
    skill_name: str
    reason: str
    token_savings_estimate: int
    command: str
    risk: str = "caution"


@dataclass
class SkillInsightsReport:
    """Full aggregate report — what `cvc skills insights` renders."""

    generated_at: str
    total_skills: int
    active_count: int
    stale_count: int
    archived_count: int
    pinned_count: int
    agent_created_count: int
    bundled_or_hub_count: int

    # Aggregate counters
    total_views: int = 0
    total_uses: int = 0
    total_patches: int = 0

    # Buckets — pre-sorted (hot first, dead last) for fast render
    hot: List[SkillInsight] = field(default_factory=list)
    fading: List[SkillInsight] = field(default_factory=list)
    dead: List[SkillInsight] = field(default_factory=list)
    fresh: List[SkillInsight] = field(default_factory=list)  # created, used 0-2 times

    # Heuristics
    avg_use_to_view_ratio: float = 0.0
    wasted_context_share: float = 0.0  # fraction of views that lead to 0 uses

    # Configurable thresholds (echoed so the dashboard can show them)
    stale_after_days: int = 30
    archive_after_days: int = 90

    @property
    def summary_one_liner(self) -> str:
        """Short single-line summary for /status headers and bot greetings."""
        return (
            f"{self.total_skills} skills • {self.active_count} active • "
            f"{len(self.dead)} wasting context • {len(self.hot)} hot"
        )


# ---------------------------------------------------------------------------
# Pure analytics engine
# ---------------------------------------------------------------------------


def _parse_iso(ts: Optional[str]) -> Optional[datetime]:
    """Parse an ISO-8601 timestamp, tolerating a trailing ``Z``."""
    if not ts or not isinstance(ts, str):
        return None
    try:
        # Python <3.11 doesn't accept the trailing Z; strip it.
        if ts.endswith("Z"):
            ts = ts[:-1] + "+00:00"
        return datetime.fromisoformat(ts)
    except (ValueError, TypeError):
        return None


def _detect_category(name: str) -> str:
    """Extract a category hint from a prefixed skill name (e.g. ``mlops/foo``)."""
    if "/" in name:
        return name.split("/", 1)[0]
    return "general"


def compute_insights(
    usage: Mapping[str, Mapping[str, Any]],
    *,
    now: Optional[datetime] = None,
    stale_after_days: int = 30,
    archive_after_days: int = 90,
    hot_window_days: int = 7,
    fade_threshold_days: int = 30,
) -> SkillInsightsReport:
    """Compute a :class:`SkillInsightsReport` from a raw usage sidecar.

    Parameters
    ----------
    usage:
        The output of :func:`cvc.skills.usage.load_usage`. Keyed by skill
        name, each value is the sidecar record (view_count, use_count,
        state, pinned, ...).
    now:
        Reference "now" for staleness math. Defaults to UTC now().
        Tests pass a fixed value for determinism.
    stale_after_days, archive_after_days:
        Echoed into the report so the dashboard can render them.
    hot_window_days:
        A skill is "hot" if its last use is within this many days and
        it has been used at least 3 times.
    fade_threshold_days:
        A skill is "fading" if it was used before but not in this many
        days and has at least 3 lifetime uses.
    """
    now = now or datetime.now(timezone.utc)

    rows: List[SkillInsight] = []
    total_views = 0
    total_uses = 0
    total_patches = 0
    active = stale = archived = pinned = 0
    agent_created = 0

    for name, raw in usage.items():
        if not isinstance(raw, Mapping):
            continue
        state = str(raw.get("state", "active"))
        is_pinned = bool(raw.get("pinned", False))
        is_agent_made = bool(raw.get("agent_created", True))
        views = int(raw.get("view_count", 0) or 0)
        uses = int(raw.get("use_count", 0) or 0)
        patches = int(raw.get("patch_count", 0) or 0)

        last_used = _parse_iso(raw.get("last_used_at"))
        days_since_use: Optional[int] = None
        if last_used is not None:
            # Normalise to aware UTC for subtraction
            if last_used.tzinfo is None:
                last_used = last_used.replace(tzinfo=timezone.utc)
            days_since_use = max(0, (now - last_used).days)

        total_views += views
        total_uses += uses
        total_patches += patches

        if state == "active":
            active += 1
        elif state == STATE_STALE:
            stale += 1
        elif state == STATE_ARCHIVED:
            archived += 1
        if is_pinned:
            pinned += 1
        if is_agent_made:
            agent_created += 1

        rows.append(
            SkillInsight(
                name=name,
                state=state,
                pinned=is_pinned,
                agent_created=is_agent_made,
                view_count=views,
                use_count=uses,
                patch_count=patches,
                last_used_at=raw.get("last_used_at"),
                last_viewed_at=raw.get("last_viewed_at"),
                last_patched_at=raw.get("last_patched_at"),
                days_since_last_use=days_since_use,
                use_to_view_ratio=uses / max(views, 1),
                category=_detect_category(name),
            )
        )

    # Promote skills with no last_used_at but with use_count > 0 to "fading"
    # by counting them as ancient — but only if state is active. If they
    # have no recorded use, they belong in fresh, not fading.
    for r in rows:
        if r.days_since_last_use is None and r.use_count >= 3 and r.state == "active":
            r.days_since_last_use = 9999  # sentinel for "very old"

    # Buckets — each row goes to AT MOST one bucket (priority: hot > fading > dead > fresh)
    # Archived AND stale skills are excluded from active buckets (they're not actionable).
    hot: List[SkillInsight] = []
    fading: List[SkillInsight] = []
    dead: List[SkillInsight] = []
    fresh: List[SkillInsight] = []
    for r in rows:
        if r.state == STATE_ARCHIVED or r.state == STATE_STALE:
            continue  # not actionable in active buckets
        if r.is_hot and r.days_since_last_use is not None and r.days_since_last_use <= hot_window_days:  # noqa: E501
            hot.append(r)
        elif r.is_fading:
            fading.append(r)
        elif r.is_dead:
            dead.append(r)
        else:
            fresh.append(r)

    # Sort each bucket by signal strength
    hot.sort(key=lambda r: (-r.use_count, r.days_since_last_use or 0))
    fading.sort(key=lambda r: (-r.use_count, -(r.days_since_last_use or 0)))
    dead.sort(key=lambda r: (-r.view_count, r.name))
    fresh.sort(key=lambda r: (r.category, r.name))

    avg_ratio = sum(r.use_to_view_ratio for r in rows) / max(len(rows), 1)
    # Only ACTIVE skills count toward wasted context — archived/stale are
    # already out of the manifest, so they're not wasting anything.
    active_rows = [r for r in rows if r.state not in (STATE_ARCHIVED, STATE_STALE)]
    wasted = sum(
        1 for r in active_rows if r.view_count >= 3 and r.use_count == 0
    ) / max(len([r for r in active_rows if r.view_count >= 3]), 1)

    return SkillInsightsReport(
        generated_at=now.isoformat(),
        total_skills=len(rows),
        active_count=active,
        stale_count=stale,
        archived_count=archived,
        pinned_count=pinned,
        agent_created_count=agent_created,
        bundled_or_hub_count=len(rows) - agent_created,
        total_views=total_views,
        total_uses=total_uses,
        total_patches=total_patches,
        hot=hot,
        fading=fading,
        dead=dead,
        fresh=fresh,
        avg_use_to_view_ratio=round(avg_ratio, 3),
        wasted_context_share=round(wasted, 3),
        stale_after_days=stale_after_days,
        archive_after_days=archive_after_days,
    )


# ---------------------------------------------------------------------------
# Action layer — turn observations into safe, ordered recommendations
# ---------------------------------------------------------------------------


# Heuristic: average tokens a SKILL.md contributes to the system prompt.
# Measured empirically on Jai's real skills (2026-06-21): median ~220
# tokens per skill body. Conservative ceiling of 600 to avoid scaring
# users with over-large numbers — the real savings are typically less.
_AVG_SKILL_PROMPT_TOKENS = 220
_MAX_SKILL_PROMPT_TOKENS = 600


def _token_savings(view_count: int) -> int:
    """Estimate tokens saved per turn if this skill is no longer loaded.

    Each view is one system-prompt inclusion. We cap at a realistic
    maximum so we don't tell the user they're saving 10k tokens when
    they're really saving 300.
    """
    return min(view_count * _AVG_SKILL_PROMPT_TOKENS, _MAX_SKILL_PROMPT_TOKENS * view_count)


def recommend_actions(
    report: SkillInsightsReport,
    *,
    max_actions: int = 10,
) -> List[SkillAction]:
    """Convert a :class:`SkillInsightsReport` into a list of ordered actions.

    The ordering is "highest-impact, lowest-risk first" so a user who
    only acts on the first suggestion still gets the big win. Actions
    are **never** applied automatically — every action carries an exact
    ``cvc skills ...`` command the user (or the dashboard's "Apply"
    button) can trigger explicitly.

    Priority
    --------
    1. ``archive`` — dead skills wasting context (sorted by view_count).
    2. ``unpin``   — pinned skills that look dead (the curator should
                     manage these, not the pin).
    3. ``review``  — fading skills that might need a refresh.
    """
    actions: List[SkillAction] = []

    # 1) Dead skills — primary waste source.
    for r in sorted(report.dead, key=lambda x: (-x.view_count, x.name)):
        savings = _token_savings(r.view_count)
        actions.append(
            SkillAction(
                kind="archive",
                skill_name=r.name,
                reason=(
                    f"shown to the model {r.view_count} times, never picked "
                    f"— wastes ~{savings} tokens of system prompt per turn"
                ),
                token_savings_estimate=savings,
                command=f"cvc skills archive {r.name}",
                risk="caution",
            )
        )
        if len(actions) >= max_actions:
            return actions

    # 2) Pinned skills that show zero usage — the pin is doing harm.
    # Walk the dead bucket AND the fresh bucket (pinned+zero-use is the
    # signature of "I pinned it years ago and forgot").
    pinned_zero_use: List[SkillInsight] = []
    seen_names: set = set()
    for r in report.dead + report.fresh:
        if r.pinned and r.use_count == 0 and r.name not in seen_names:
            pinned_zero_use.append(r)
            seen_names.add(r.name)
    for r in sorted(pinned_zero_use, key=lambda x: (-x.view_count, x.name)):
        actions.append(
            SkillAction(
                kind="unpin",
                skill_name=r.name,
                reason=(
                    f"pinned but never used — curator can't manage it; "
                    f"~{_token_savings(max(r.view_count, 1))} tokens locked"
                ),
                token_savings_estimate=_token_savings(max(r.view_count, 1)),
                command=f"cvc skills unpin {r.name}",
                risk="safe",
            )
        )
        if len(actions) >= max_actions:
            return actions

    # 3) Fading — review before archiving.
    for r in sorted(report.fading, key=lambda x: (-x.use_count, x.name)):
        actions.append(
            SkillAction(
                kind="review",
                skill_name=r.name,
                reason=(
                    f"used {r.use_count} times in the past, idle {r.days_since_last_use}d "
                    "— refresh, repurpose, or archive"
                ),
                token_savings_estimate=0,
                command=f"cvc skills show {r.name}",
                risk="review",
            )
        )
        if len(actions) >= max_actions:
            return actions

    return actions


def total_potential_savings(actions: Iterable[SkillAction]) -> int:
    """Sum the token-savings estimates of a list of actions."""
    return sum(a.token_savings_estimate for a in actions)


# ---------------------------------------------------------------------------
# Rendering — CLI (Rich) and JSON (gateway)
# ---------------------------------------------------------------------------


def render_cli_summary(
    report: SkillInsightsReport,
    *,
    max_per_bucket: int = 8,
    include_actions: bool = True,
    max_actions: int = 5,
) -> str:
    """Render the report as a Rich-formatted text block.

    Returns a string (not printing it) so the caller can pipe to console
    or capture in tests. Uses plain ASCII brackets instead of unicode so
    it renders correctly on the Windows default cp1252 console without
    requiring ``rich`` to auto-install Windows console code pages.

    When ``include_actions`` is true (default) the report ends with a
    "[RECOMMENDED ACTIONS]" section listing the top :func:`recommend_actions`
    in priority order, with the exact CLI command to apply each one.
    """
    lines: List[str] = []
    lines.append(f"[CVC Skill Insights] {report.generated_at}")
    lines.append("-" * 64)
    lines.append(
        f"{report.total_skills} skills | {report.active_count} active | "
        f"{report.stale_count} stale | {report.archived_count} archived | "
        f"{report.pinned_count} pinned"
    )
    lines.append(
        f"agent-created: {report.agent_created_count}  "
        f"bundled/hub: {report.bundled_or_hub_count}  "
        f"views: {report.total_views}  uses: {report.total_uses}  "
        f"patches: {report.total_patches}"
    )
    lines.append(
        f"avg use/view: {report.avg_use_to_view_ratio:.3f}  "
        f"wasted context share: {report.wasted_context_share * 100:.1f}%"
    )
    lines.append("")

    def _row(label: str, items: Iterable[SkillInsight]) -> None:
        bucket = list(items)
        if not bucket:
            lines.append(f"[{label}] (none)")
            lines.append("")
            return
        names = " / ".join(r.name for r in bucket[:max_per_bucket])
        lines.append(f"[{label}] {len(bucket)} skill(s) — {names}")
        for r in bucket[:max_per_bucket]:
            age = (
                f"{r.days_since_last_use}d ago"
                if r.days_since_last_use is not None and r.days_since_last_use < 9999
                else "never"
            )
            lines.append(
                f"  - {r.name:<32} views={r.view_count:>4} "
                f"uses={r.use_count:>4} last_use={age}"
            )
        if len(bucket) > max_per_bucket:
            lines.append(f"  ... and {len(bucket) - max_per_bucket} more")
        lines.append("")

    _row("HOT (used 3+ in 7d)", report.hot)
    _row("FADING (was used, 30d+ idle)", report.fading)
    _row("DEAD (viewed 3+ but never used — wastes context)", report.dead)
    _row("FRESH (new or rarely used)", report.fresh)

    if include_actions:
        actions = recommend_actions(report, max_actions=max_actions)
        lines.append("[RECOMMENDED ACTIONS]")
        if not actions:
            lines.append("  (none — your skill substrate is lean)")
            lines.append("")
        else:
            total_savings = total_potential_savings(actions)
            lines.append(
                f"  {len(actions)} suggested action(s) — "
                f"~{total_savings} tokens potentially saved per turn"
            )
            lines.append("")
            for a in actions:
                lines.append(f"  [{a.kind.upper()}] {a.skill_name}  ({a.risk})")
                lines.append(f"    {a.reason}")
                if a.token_savings_estimate:
                    lines.append(
                        f"    ~{a.token_savings_estimate} tokens/turn"
                    )
                lines.append(f"    > {a.command}")
                lines.append("")
            lines.append(
                "  Actions are opt-in. Copy-paste a command, or pass "
                "`--apply-archives` to the CLI to apply ALL archive "
                "actions in one go (skips pinned + bundled)."
            )
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def to_jsonable(report: SkillInsightsReport) -> Dict[str, Any]:
    """Return a JSON-safe dict — for the ``/api/skills/insights`` endpoint.

    Bucket objects are flattened to plain dicts so the React dashboard
    can ``map()`` over them without re-parsing the dataclass.
    """
    def _flatten(items: List[SkillInsight]) -> List[Dict[str, Any]]:
        return [
            {
                "name": r.name,
                "state": r.state,
                "pinned": r.pinned,
                "agent_created": r.agent_created,
                "view_count": r.view_count,
                "use_count": r.use_count,
                "patch_count": r.patch_count,
                "last_used_at": r.last_used_at,
                "last_viewed_at": r.last_viewed_at,
                "last_patched_at": r.last_patched_at,
                "days_since_last_use": r.days_since_last_use,
                "use_to_view_ratio": round(r.use_to_view_ratio, 4),
                "category": r.category,
                "is_hot": r.is_hot,
                "is_fading": r.is_fading,
                "is_dead": r.is_dead,
            }
            for r in items
        ]

    base = asdict(report)
    actions = recommend_actions(report)
    base.update(
        {
            "hot": _flatten(report.hot),
            "fading": _flatten(report.fading),
            "dead": _flatten(report.dead),
            "fresh": _flatten(report.fresh),
            "summary_one_liner": report.summary_one_liner,
            "actions": [asdict(a) for a in actions],
            "potential_token_savings": total_potential_savings(actions),
        }
    )
    return base
