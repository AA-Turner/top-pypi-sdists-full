"""A request that spends no AI is recorded for a person over their AI usage limit.

Live (2026-11-14): the agent member was over its weekly AI allowance and the tool tester refused to run the
``records`` tool — a database read that spends no AI — with 402 ``usage_limit_reached``. The cause: recording
ANY new request (``ensure_user_request_exists``) asked the AI allowance (``precheck_usage``), and the tool
tester and the tool logger's backstop record a request without starting an AI turn.

THE SEAM: the real ``ensure_user_request_exists`` and the real ``precheck_usage`` with a usage verdict of
"over". Only the row writes are faked (the database boundary). An AI turn is still refused; a request declared
``spends_ai=False`` is recorded. RED before: the keyword did not exist, so no caller could say it.
"""

from __future__ import annotations

import ast
import uuid
from pathlib import Path

import pytest

from matrx_ai.db import conversation_gate
from matrx_ai.providers import usage_gate
from matrx_ai.providers.usage_gate import UsageLimitReachedError

pytestmark = pytest.mark.asyncio

PERSON = "65236360-c402-4218-84df-b5e1693fb7cc"
ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def over_the_cap(monkeypatch):
    monkeypatch.setattr(usage_gate, "_gated_person", lambda ctx: PERSON)
    monkeypatch.setattr(usage_gate, "_already_admitted", lambda ctx: False)
    monkeypatch.setattr(
        usage_gate,
        "_verdict_for",
        lambda uid: usage_gate.UsageVerdict(state="over", refuse=True, enforced=True, usage={"state": "over"}),
    )
    created: list[str] = []

    async def _no_store(*_a, **_kw):
        return False

    async def _create(*, request_id, user_id):
        created.append(request_id)

    class _NoRows:
        async def filter_user_requests(self, **_kw):
            return []

    class _Cxm:
        user_request = _NoRows()

    monkeypatch.setattr(conversation_gate, "_store_pending_user_request", _no_store)
    monkeypatch.setattr(conversation_gate, "_create_user_request", _create)
    monkeypatch.setattr(conversation_gate, "_cxm", lambda: _Cxm())
    return created


async def test_an_ai_turn_is_still_refused_over_the_limit(over_the_cap) -> None:
    with pytest.raises(UsageLimitReachedError):
        await conversation_gate.ensure_user_request_exists(str(uuid.uuid4()), PERSON)
    assert over_the_cap == []


async def test_a_request_that_spends_no_ai_is_recorded(over_the_cap) -> None:
    request_id = str(uuid.uuid4())
    await conversation_gate.ensure_user_request_exists(request_id, PERSON, spends_ai=False)
    assert over_the_cap == [request_id]


def _calls_declaring_no_ai(path: Path) -> list[bool]:
    """For each ``ensure_user_request_exists(...)`` call in ``path``: does it pass ``spends_ai=False``?"""
    out: list[bool] = []
    for node in ast.walk(ast.parse(path.read_text())):
        if isinstance(node, ast.Call) and getattr(node.func, "id", getattr(node.func, "attr", "")) == "ensure_user_request_exists":
            out.append(
                any(k.arg == "spends_ai" and isinstance(k.value, ast.Constant) and k.value.value is False for k in node.keywords)
            )
    return out


def test_the_tool_logger_records_a_lone_tool_call_without_asking_the_allowance() -> None:
    """A tool a workflow, an automation or an MCP client calls directly is recorded by the logger's backstop."""
    calls = _calls_declaring_no_ai(ROOT / "matrx_ai/tools/logger.py")
    assert calls and all(calls), "tools/logger.py must record a lone tool call with spends_ai=False"
