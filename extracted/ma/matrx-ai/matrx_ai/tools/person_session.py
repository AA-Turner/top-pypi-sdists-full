"""Run a tool's database work AS THE PERSON calling it — RLS makes the decision.

The privileged pool connection bypasses row-level security, so a tool that
loads a record by id on it can read or edit anyone's record. A tool that acts
on a person's own data opens ``as_the_person()`` around its ORM calls: the host
switches the transaction to the person's database identity (Supabase
``authenticated`` + their JWT claims) and Postgres RLS decides what exists for
them. The tool never re-implements access — no ``created_by ==`` or
``organization_id ==`` checks.

Unconfigured host → ``PersonSessionUnavailable``: the tool refuses loudly. It
never falls back to the privileged connection.
"""

from __future__ import annotations

import functools
import time
import traceback
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any

from matrx_ai._ext import get_acting_as_caller

if TYPE_CHECKING:
    from matrx_ai.tools.models import ToolContext, ToolResult


class PersonSessionUnavailable(RuntimeError):
    """The host did not provide a way to act as the calling person."""


PERSON_SESSION_UNAVAILABLE_MESSAGE = (
    "This server cannot act as you on your records right now (no per-person database "
    "session is configured), so the request was refused rather than run with elevated "
    "access. An operator must wire `acting_as_caller` into matrx_ai.configure()."
)


@asynccontextmanager
async def as_the_person() -> AsyncIterator[None]:
    """Hold the calling person's RLS session for the enclosed ORM work."""
    factory = get_acting_as_caller()
    if factory is None:
        raise PersonSessionUnavailable(PERSON_SESSION_UNAVAILABLE_MESSAGE)
    async with factory():
        yield


# ---------------------------------------------------------------------------
# The ONE wrapper a tool action uses to run as the person.
# ---------------------------------------------------------------------------


class _RollBack(Exception):
    """Leave the person's session with a ROLLBACK, carrying the refusal out."""

    def __init__(self, result: ToolResult) -> None:
        super().__init__(result.error.message if result.error else "")
        self.result = result


ToolFn = Callable[[dict[str, Any], "ToolContext"], Awaitable["ToolResult"]]


def acts_as_the_person(
    tool_name: str, *, subject: str = "your records"
) -> Callable[[ToolFn], ToolFn]:
    """Run a tool action inside the caller's RLS session; RLS decides access.

    Every ORM call the action makes sees exactly what the person may see and
    writes exactly what they may write. A failed action leaves through
    ROLLBACK, so nothing half-done commits. If the session cannot be opened the
    action REFUSES with ``error_type='unavailable'`` — it never runs on the
    privileged connection. ``subject`` names what the action works on in the
    message of an unexpected failure ("Could not act on <subject>: ...").
    """

    def wrap(fn: ToolFn) -> ToolFn:
        @functools.wraps(fn)
        async def run(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
            from matrx_ai.tools.models import ToolError, ToolResult

            started_at = time.time()
            try:
                async with as_the_person():
                    result = await fn(args, ctx)
                    if not result.success:
                        raise _RollBack(result)
                    return result
            except _RollBack as refused:
                return refused.result
            except PersonSessionUnavailable as e:
                return ToolResult(
                    success=False,
                    error=ToolError(error_type="unavailable", message=str(e)),
                    started_at=started_at, completed_at=time.time(),
                    tool_name=tool_name, call_id=ctx.call_id,
                )
            except Exception as e:
                return ToolResult(
                    success=False,
                    error=ToolError(
                        error_type="execution",
                        message=f"Could not act on {subject}: {e}",
                        traceback=traceback.format_exc(),
                        is_retryable=True,
                    ),
                    started_at=started_at, completed_at=time.time(),
                    tool_name=tool_name, call_id=ctx.call_id,
                )

        run.__acts_as_the_person__ = True  # type: ignore[attr-defined]
        return run

    return wrap


async def person_may_change(model: Any, pk: dict[str, Any]) -> bool:
    """Would Postgres let the calling person UPDATE this row? RLS answers.

    ``SELECT ... FOR UPDATE`` applies the table's UPDATE policy (USING) on top
    of its SELECT policy, so the row comes back only when the person may change
    it — no write, no trigger, no app-side permission logic. The row lock lasts
    until the enclosing person session ends. Opens (or reuses) the person
    session itself, so it can never answer from the privileged connection.
    """
    async with as_the_person():
        rows = await model.filter(**pk).select_for_update().values(*pk.keys())
    return bool(rows)
