"""Durable per-run checkpoint for the batch orchestrator.

Persists the accumulated :class:`~pysae_ai_tools.agent.models.Outcome` list to disk so a
crashed or interrupted batch resumes without re-processing merged tickets. Each entry is
upserted by ``(project_path, ticket_iid)`` and carries its own ``created`` (first time the
ticket was recorded) and ``last_updated`` (last mutation) — a success later demoted by the
deploy watch keeps ``created`` and bumps ``last_updated``. Writes are atomic (tmp file +
``os.replace``) so a crash mid-write cannot corrupt the checkpoint.
"""

import json
import os
from collections.abc import Callable
from datetime import datetime, timezone
from pathlib import Path

from .models import Outcome


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load(path: Path) -> list[Outcome]:
    """The checkpoint's outcomes (empty when the file is absent or empty)."""
    if not path.exists():
        return []
    raw = json.loads(path.read_text(encoding="utf-8") or "[]")
    return [Outcome.model_validate(entry) for entry in raw]


def _write(path: Path, outcomes: list[Outcome]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(
        json.dumps([o.model_dump() for o in outcomes], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    os.replace(tmp, path)


def append(path: Path, outcome: Outcome, *, now: Callable[[], str] = _now) -> list[Outcome]:
    """Upsert ``outcome`` by ``(project_path, ticket_iid)``; preserve ``created``, bump ``last_updated``."""
    outcomes = load(path)
    stamp = now()
    for i, existing in enumerate(outcomes):
        if existing.project_path == outcome.project_path and existing.ticket_iid == outcome.ticket_iid:
            outcome.created = existing.created or stamp
            outcome.last_updated = stamp
            outcomes[i] = outcome
            break
    else:
        outcome.created = outcome.created or stamp
        outcome.last_updated = stamp
        outcomes.append(outcome)
    _write(path, outcomes)
    return outcomes


def clear(path: Path) -> None:
    """Remove the checkpoint file (no-op when absent)."""
    path.unlink(missing_ok=True)
