"""What a subscription follows, as the live routes' query: one run, experiment or project (none: the team), the
kinds, and a producer's writer session (twin: app/live)."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any
from uuid import UUID

from pydantic import ValidationError

from ...generated.live import LivePollQuery, LiveQuery


def make_query(
    *,
    run: str | None = None,
    experiment: str | None = None,
    project: str | None = None,
    kinds: str | Sequence[str] | None = None,
    writer: str | UUID | None = None,
) -> LiveQuery:
    """The stream's query, checked here as the server checks it: one scope at most, well-formed kinds, a writer
    only with its run. Raises ValueError with the first problem, in words."""
    try:
        return LiveQuery(run=run or None, experiment=experiment or None, project=project or None,
                         kinds=join_kinds(kinds), writer=writer or None)
    except ValidationError as exc:
        raise ValueError(_describe(exc)) from None


def make_poll_query(query: LiveQuery, *, since: int | None, wait: float, limit: int) -> LivePollQuery:
    """The long-poll's query: the stream's, plus a cursor, a wait and a page size. Raises ValueError."""
    try:
        return LivePollQuery(**query.model_dump(exclude={"since"}), since=since, wait=wait, limit=limit)
    except ValidationError as exc:
        raise ValueError(_describe(exc)) from None


def join_kinds(kinds: str | Sequence[str] | None) -> str | None:
    """`["samples.*", "run.status"]` or `"samples.*,run.status"` -> the `kinds=` value; None for every kind."""
    if kinds is None:
        return None
    parts = kinds.split(",") if isinstance(kinds, str) else list(kinds)
    joined = ",".join(part.strip() for part in parts if part and part.strip())
    return joined or None


def to_query_parameters(query: LiveQuery) -> dict[str, Any]:
    """The query string: unset fields left out, `since` included only when set."""
    return {name: value for name, value in query.model_dump(mode="json", exclude_none=True).items()}


def _describe(exc: ValidationError) -> str:
    """The first problem pydantic found, as a sentence (`name one scope, not run and project`)."""
    first = exc.errors()[0]
    where = ".".join(str(part) for part in first.get("loc", ()))
    message = str(first.get("msg", exc)).removeprefix("Value error, ")
    return f"{where}: {message}" if where else message
