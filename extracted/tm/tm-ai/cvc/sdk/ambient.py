"""
cvc.sdk.ambient — Ambient Legibility: the actual telepathy mechanism (Fable5 Phase 5).

Per FABLE5_SPACE_ROBOTICS_COGNITIVE_INTELLIGENCE.md §4.1:

    "True telepathy means the relevant facts are *already in context*
    before the agent even starts reasoning ... the telepathy IS the
    automatic context injection, not a new communication channel."

The existing SDK gives agents *query* legibility (agent.context(),
agent.inbox(), agent.squad_context()) — the agent must ASK. This module
adds *ambient* legibility — a per-agent cursor over the shared DAG plus
a digest builder that answers, in one call made FOR the agent by its
harness on every reasoning cycle:

    "What changed in my scope since I last acted?"

Design:

  * AmbientCursor — per-agent, persisted in ``.cvc/ambient/<agent_id>.json``.
    Tracks the timestamp/commit of the agent's last reasoning cycle.
    Local-first, tiny, crash-safe (rewrite-on-update of a 100-byte file —
    the DAG itself remains the append-only source of truth; the cursor
    is a bookmark, not a record).

  * ambient_digest(agent) — everything new in the agent's readable scope
    since its cursor, formatted as a compact prompt block with per-fact
    provenance and STALENESS HONESTY (§4.1 latency-aware scoping): each
    entry carries its age, so a hive spanning light-lag distances
    represents its own latency instead of papering over it.

  * The harness calls ``advance()`` after each reasoning cycle. The next
    cycle's digest starts where this one ended. An agent that was offline
    (blackout) automatically receives everything it missed on reconnect —
    the Mars-blackout pattern falls out of the cursor design for free.

Usage (harness side)::

    from cvc.sdk.ambient import AmbientChannel

    channel = AmbientChannel(hive)
    block = channel.digest(agent)        # inject into system prompt
    ...agent reasons...
    channel.advance(agent)               # bookmark: cycle complete
"""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Any

logger = logging.getLogger("cvc.ambient")

# Cap injected facts per cycle — telepathy, not firehose.
DEFAULT_MAX_FACTS = 25
# Facts older than this (seconds) are summarized as a count, not listed.
DEFAULT_FRESH_WINDOW = 6 * 3600


class AmbientChannel:
    """Per-agent ambient context over a HiveMind's shared DAG."""

    AMBIENT_DIR = "ambient"

    def __init__(self, hive: Any) -> None:
        """``hive`` is a cvc.sdk.hivemind.HiveMind instance."""
        self.hive = hive
        cvc_root = Path(getattr(hive.db.config, "cvc_root", ".cvc"))
        self.cursor_dir = cvc_root / self.AMBIENT_DIR
        self.cursor_dir.mkdir(parents=True, exist_ok=True)

    # -- cursor ----------------------------------------------------------------

    def _cursor_path(self, agent_id: str) -> Path:
        safe = agent_id.replace("/", "_").replace("..", "_")
        return self.cursor_dir / f"{safe}.json"

    def get_cursor(self, agent_id: str) -> float:
        """Timestamp of the agent's last completed reasoning cycle (0.0 = never)."""
        p = self._cursor_path(agent_id)
        if p.exists():
            try:
                return float(json.loads(p.read_text(encoding="utf-8"))["last_cycle_at"])
            except Exception:  # noqa: BLE001
                pass
        return 0.0

    def advance(self, agent: Any, at: float | None = None) -> None:
        """Bookmark: this agent completed a reasoning cycle now."""
        agent_id = getattr(agent, "agent_id", str(agent))
        payload = {"agent_id": agent_id, "last_cycle_at": at or time.time()}
        self._cursor_path(agent_id).write_text(
            json.dumps(payload), encoding="utf-8"
        )

    # -- digest ------------------------------------------------------------------

    def digest(
        self,
        agent: Any,
        *,
        max_facts: int = DEFAULT_MAX_FACTS,
        fresh_window: float = DEFAULT_FRESH_WINDOW,
        now: float | None = None,
    ) -> str:
        """Build the ambient context block for one reasoning cycle.

        Returns a compact prompt block of everything that changed in the
        agent's readable scope since its cursor — or an empty string if
        nothing changed (inject nothing; silence is signal too).

        Scope enforcement is delegated to the agent's own scoped reads
        (Router.context_for honors squad/rank isolation), so ambient
        legibility can never leak beyond what the agent could query.
        """
        agent_id = getattr(agent, "agent_id", str(agent))
        cursor = self.get_cursor(agent_id)
        now = now or time.time()

        # Pull generously, then filter by cursor. agent.context() enforces scope.
        try:
            commits = agent.context(limit=200)
        except Exception as e:  # noqa: BLE001
            logger.warning("ambient: scoped read failed for %s: %s", agent_id, e)
            return ""

        new_commits = [
            c for c in commits
            if _ts(c) > cursor
            and _agent(c) != agent_id  # own actions aren't news
        ]
        if not new_commits:
            return ""

        new_commits.sort(key=_ts)

        fresh = [c for c in new_commits if (now - _ts(c)) <= fresh_window]
        stale = [c for c in new_commits if c not in fresh]

        lines: list[str] = [
            "## AMBIENT — changes in your scope since your last cycle",
            "(You already know these. They are facts, not messages. Do not acknowledge them.)",
        ]

        shown = fresh[-max_facts:]
        overflow_fresh = len(fresh) - len(shown)

        for c in shown:
            age = now - _ts(c)
            who = _agent(c) or "unknown"
            action = ""
            meta = getattr(c, "metadata", None)
            if meta is not None:
                action = getattr(meta, "action_type", "") or ""
            msg = (getattr(c, "message", "") or "").strip()
            stamp = _humanize_age(age)
            tag = f"[{action}] " if action else ""
            lines.append(f"- ({stamp}) {who}: {tag}{msg}")

        if overflow_fresh > 0:
            lines.append(f"- …plus {overflow_fresh} more recent changes (recall() for detail).")
        if stale:
            oldest_age = _humanize_age(now - _ts(stale[0]))
            lines.append(
                f"- NOTE: {len(stale)} older changes accumulated while you were "
                f"offline/idle (oldest {oldest_age}) — reconnect backlog. "
                f"Use recall() if mission-relevant."
            )

        return "\n".join(lines)

    # -- one-call harness helper ---------------------------------------------------

    def cycle(self, agent: Any, **digest_kwargs: Any) -> str:
        """digest() + advance() in one call, for simple harness loops.

        Returns the digest built BEFORE advancing, so the block covers
        everything since the previous cycle and the cursor now points here.
        """
        block = self.digest(agent, **digest_kwargs)
        self.advance(agent)
        return block


def _ts(commit: Any) -> float:
    """Commit timestamp lives on CommitMetadata, not the commit itself."""
    meta = getattr(commit, "metadata", None)
    if meta is not None:
        return float(getattr(meta, "timestamp", 0.0) or 0.0)
    return float(getattr(commit, "timestamp", 0.0) or 0.0)


def _agent(commit: Any) -> str | None:
    """Author agent_id lives on CommitMetadata."""
    meta = getattr(commit, "metadata", None)
    if meta is not None:
        return getattr(meta, "agent_id", None)
    return getattr(commit, "agent_id", None)


def _humanize_age(seconds: float) -> str:
    """Honest staleness labels — a hive spanning light-lag must not lie about age."""
    if seconds < 0:
        seconds = 0
    if seconds < 60:
        return f"{int(seconds)}s ago"
    if seconds < 3600:
        return f"{int(seconds // 60)}m ago"
    if seconds < 86400:
        return f"{seconds / 3600:.1f}h ago"
    return f"{seconds / 86400:.1f}d ago"
