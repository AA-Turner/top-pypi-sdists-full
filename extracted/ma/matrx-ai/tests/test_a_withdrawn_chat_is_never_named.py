"""A withdrawn chat is never named (P1-CHAT, "I did not mean to send that").

Live (2026-11-15, conversation 56925365…): the person pressed Stop 250 ms after Enter, before any
reply was drawn. The run read its input and stopped with nothing; the title agent, scheduled when
the conversation opened, still named the chat "Elin Lighthouse Keeper Story". The host's withdraw
door stamps ``chat.conversation.metadata.withdrawn``; the labeler reads it before the model call and
again before the write, so a withdrawn chat gets no label, whenever the withdrawal lands.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

import matrx_ai.agents.services.conversation_labeler as labeler
from matrx_ai import _ext
from matrx_ai.agent_runners.conversation_labeler import LabelResult

CID = "56925365-08b5-4f3e-8432-04a6b1ecb804"
OUTPUT = '{"label": "Elin Lighthouse Keeper Story", "description": "A story", "keywords": ["story"]}'
FIRST_TURN = [{"role": "user", "content": "Write a 600-word story about a lighthouse keeper named Elin."}]
WITHDRAWN = {"withdrawn": {"request_id": "18ed8845-6354-4379-827b-0e9e544213a5", "reason": "stopped_before_reply"}}


class _Rows:
    def __init__(self, row: Any) -> None:
        self.row = row

    def filter(self, **_kw: Any) -> _Rows:
        return self

    def limit(self, _n: int) -> _Rows:
        return self

    async def all(self) -> list[Any]:
        return [self.row]


def _row(**fields: Any) -> Any:
    base = {"title": None, "description": "", "keywords": [], "named_by": "auto",
            "organization_id": "org-1", "deleted_at": None, "metadata": {}}
    base.update(fields)
    return SimpleNamespace(**base)


@pytest.fixture
def run(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    seen: dict[str, Any] = {"writes": [], "labels": [], "during_label": None}

    async def update(_cid: str, _uid: str, fields: dict[str, Any]) -> None:
        seen["writes"].append(fields)

    async def titles(_uid: str) -> list[dict[str, str]]:
        return []

    async def label(**_kw: Any) -> LabelResult:
        seen["labels"].append(1)
        if seen["during_label"]:
            seen["during_label"]()
        return LabelResult(success=True, output=OUTPUT)

    async def not_staff(_cid: str) -> bool:
        return False

    async def no_seed(**_kw: Any) -> None:
        return None

    monkeypatch.setattr(labeler, "_update_conversation_labels", update)
    monkeypatch.setattr(labeler, "_fetch_recent_titles", titles)
    monkeypatch.setattr(labeler, "label_chat_conversation", label)
    monkeypatch.setattr(labeler, "_is_staff_channel_conversation", not_staff)
    monkeypatch.setitem(_ext._registry, "system_process_seed", no_seed)
    return seen


async def test_a_chat_withdrawn_before_the_namer_runs_is_never_named(monkeypatch: pytest.MonkeyPatch, run: dict[str, Any]) -> None:
    row = _row(metadata=dict(WITHDRAWN))
    monkeypatch.setattr(labeler, "cxm", SimpleNamespace(conversation=SimpleNamespace(model=_Rows(row))))
    await labeler._run_labeling(CID, "user-1", FIRST_TURN)
    assert run["labels"] == [], "the namer ran (and was paid for) on a withdrawn chat"
    assert run["writes"] == []


async def test_a_chat_withdrawn_while_the_namer_runs_gets_no_label(monkeypatch: pytest.MonkeyPatch, run: dict[str, Any]) -> None:
    row = _row()
    monkeypatch.setattr(labeler, "cxm", SimpleNamespace(conversation=SimpleNamespace(model=_Rows(row))))
    run["during_label"] = lambda: setattr(row, "metadata", dict(WITHDRAWN))
    await labeler._run_labeling(CID, "user-1", FIRST_TURN)
    assert run["labels"] == [1]
    assert run["writes"] == [], "a chat withdrawn mid-namer was titled anyway"


async def test_control_a_chat_that_was_not_withdrawn_is_named(monkeypatch: pytest.MonkeyPatch, run: dict[str, Any]) -> None:
    row = _row()
    monkeypatch.setattr(labeler, "cxm", SimpleNamespace(conversation=SimpleNamespace(model=_Rows(row))))
    await labeler._run_labeling(CID, "user-1", FIRST_TURN)
    assert run["writes"] and run["writes"][0]["title"] == "Elin Lighthouse Keeper Story"
