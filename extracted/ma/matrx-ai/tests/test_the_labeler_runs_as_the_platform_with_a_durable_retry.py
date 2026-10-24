"""The labeler is a system process (Arman, 2026-10-18: "it's always going to be the system").

Its held call runs inside the host's platform scope (the platform pays; the run is a hidden
``system_process`` conversation linked to the chat it names), its durable retry is seeded BEFORE
the inline attempt, and the retry never repeats a label that landed nor overwrites a title the
person changed in between.
"""

from __future__ import annotations

import contextlib
from types import SimpleNamespace
from typing import Any

import pytest

import matrx_ai.agent_runners.conversation_labeler as runner
import matrx_ai.agents.services.conversation_labeler as labeler
from matrx_ai import _ext
from matrx_ai.agent_runners.conversation_labeler import LabelResult

CID = "6b7d1d36-6d0b-4c6e-9a5e-2f4c8f0d1a11"
OUTPUT = '{"label": "Tax plan", "description": "Planning taxes", "keywords": ["tax"]}'


class _Rows:
    def __init__(self, row: Any) -> None:
        self.row = row

    def filter(self, **_kw: Any) -> _Rows:
        return self

    def limit(self, _n: int) -> _Rows:
        return self

    async def all(self) -> list[Any]:
        return [self.row] if self.row is not None else []


def _cxm(row: Any) -> Any:
    return SimpleNamespace(conversation=SimpleNamespace(model=_Rows(row)))


@pytest.fixture
def writes(monkeypatch: pytest.MonkeyPatch) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []

    async def update(_cid: str, _uid: str, fields: dict[str, Any]) -> None:
        out.append(fields)

    async def titles(_uid: str) -> list[dict[str, str]]:
        return []

    monkeypatch.setattr(labeler, "_update_conversation_labels", update)
    monkeypatch.setattr(labeler, "_fetch_recent_titles", titles)
    return out


async def test_the_held_call_runs_inside_the_platform_scope(monkeypatch: pytest.MonkeyPatch) -> None:
    events: list[str] = []

    @contextlib.asynccontextmanager
    async def scope(*, feature: str, conversation_id: str | None):
        events.append(f"enter:{feature}:{conversation_id}")
        yield
        events.append("exit")

    async def hold(*_a: Any, **_k: Any) -> Any:
        events.append("hold")
        return SimpleNamespace(model="m")

    async def run(_held: Any, **_kw: Any) -> Any:
        events.append("run")
        return SimpleNamespace(final_text=OUTPUT)

    import matrx_ai.mandates as mandates

    monkeypatch.setitem(_ext._registry, "system_process_scope", scope)
    monkeypatch.setattr(mandates, "hold_code_call", hold)
    monkeypatch.setattr(mandates, "run_held_call", run)
    result = await runner._run_labeler("conversation.label_chat", {}, conversation_id=CID)
    assert result.success and result.output == OUTPUT
    assert events == [f"enter:system_process:{CID}", "hold", "run", "exit"]


async def test_the_retry_is_seeded_beside_the_inline_attempt(
    monkeypatch: pytest.MonkeyPatch, writes: list[dict[str, Any]]
) -> None:
    order: list[str] = []

    async def seed(*, process_key: str, subject_id: str, payload: dict[str, Any], delay_seconds: float) -> None:
        order.append("seed")
        assert (process_key, subject_id) == ("conversation.name", CID)
        assert payload["organization_id"] == "org-1" and payload["title_before"] == "New chat"
        assert delay_seconds > 0

    async def label(**_kw: Any) -> LabelResult:
        order.append("label")
        return LabelResult(success=True, output=OUTPUT)

    async def not_staff(_cid: str) -> bool:
        return False

    monkeypatch.setitem(_ext._registry, "system_process_seed", seed)
    monkeypatch.setattr(labeler, "label_chat_conversation", label)
    monkeypatch.setattr(labeler, "_is_staff_channel_conversation", not_staff)
    monkeypatch.setattr(labeler, "cxm", _cxm(SimpleNamespace(title="New chat", organization_id="org-1")))
    await labeler._run_labeling(CID, "user-1", [{"role": "user", "content": "taxes?"}])
    assert order == ["seed", "label"]
    assert writes == [{"title": "Tax plan", "description": "Planning taxes", "keywords": ["tax"]}]


async def test_the_retry_skips_a_label_that_landed(monkeypatch: pytest.MonkeyPatch, writes: list[dict[str, Any]]) -> None:
    async def must_not_label(**_kw: Any) -> LabelResult:
        raise AssertionError("an already-labeled conversation must not be labeled again")

    monkeypatch.setattr(labeler, "label_chat_conversation", must_not_label)
    monkeypatch.setattr(labeler, "cxm", _cxm(SimpleNamespace(title="Tax plan", description="Planning taxes", keywords=["tax"], deleted_at=None, metadata={})))
    assert await labeler.run_label_retry({"conversation_id": CID, "user_id": "user-1"}) == "skipped:already_labeled"
    assert writes == []


async def test_the_retry_leaves_a_retitled_conversation_alone(
    monkeypatch: pytest.MonkeyPatch, writes: list[dict[str, Any]]
) -> None:
    async def label(**_kw: Any) -> LabelResult:
        return LabelResult(success=True, output=OUTPUT)

    monkeypatch.setattr(labeler, "label_chat_conversation", label)
    monkeypatch.setattr(labeler, "cxm", _cxm(SimpleNamespace(title="My own name", description="", keywords=[], deleted_at=None, metadata={})))
    outcome = await labeler.run_label_retry(
        {"conversation_id": CID, "user_id": "user-1", "conversation_content": "taxes?", "title_before": "New chat"}
    )
    # Retitled since the inline attempt began (by the person, or by a title-only label): left alone.
    assert outcome == "skipped:already_labeled"
    assert writes == []


async def test_the_retry_labels_a_conversation_the_inline_attempt_never_reached(
    monkeypatch: pytest.MonkeyPatch, writes: list[dict[str, Any]]
) -> None:
    async def label(**_kw: Any) -> LabelResult:
        return LabelResult(success=True, output=OUTPUT)

    monkeypatch.setattr(labeler, "label_chat_conversation", label)
    monkeypatch.setattr(labeler, "cxm", _cxm(SimpleNamespace(title="New chat", description="", keywords=[], deleted_at=None, metadata={})))
    outcome = await labeler.run_label_retry(
        {"conversation_id": CID, "user_id": "user-1", "conversation_content": "taxes?", "title_before": "New chat"}
    )
    assert outcome == "succeeded"
    assert writes == [{"title": "Tax plan", "description": "Planning taxes", "keywords": ["tax"]}]


async def test_a_failed_retry_raises_so_the_queue_backs_off(monkeypatch: pytest.MonkeyPatch, writes: list[dict[str, Any]]) -> None:
    async def label(**_kw: Any) -> LabelResult:
        return LabelResult(success=False, output="", error="provider down")

    monkeypatch.setattr(labeler, "label_chat_conversation", label)
    monkeypatch.setattr(labeler, "cxm", _cxm(SimpleNamespace(title="", description="", keywords=[], deleted_at=None, metadata={})))
    with pytest.raises(RuntimeError, match="provider down"):
        await labeler.run_label_retry({"conversation_id": CID, "user_id": "user-1"})
    assert writes == []
