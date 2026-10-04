"""Which agent wrote a reply — stamped on every assistant/tool row, carried through
the rebuilt history, and used by remarks to name the agent when more than one
has answered in the conversation.

Use case: a museum's collections team runs a two-agent conversation — an
"Archaeologist" agent dates a shard, a "Conservator" agent proposes treatment —
and the registrar leaves remarks on both replies with her next message.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.config import structured_input_resolver
from matrx_ai.config.message_config import MessageList, UnifiedMessage
from matrx_ai.config.remarks import REMARKS_PART_TYPE
from matrx_ai.config.structured_input_config import RemarksInputContent
from matrx_ai.config.structured_input_resolver import resolve_structured_inputs
from matrx_ai.config.unified_content import TextContent
from matrx_ai.context.app_context import AppContext, clear_app_context, set_app_context
from matrx_ai.persistence import queue_helpers

ARCHAEOLOGIST = "7c1e2f0a-3b4d-4e5f-8a9b-0c1d2e3f4a5b"
CONSERVATOR = "9d2f3a1b-4c5e-4f60-9b0c-1d2e3f4a5b6c"
REGISTRAR = "e4687a9c-acf7-469f-aa12-860eb4d948d0"
NAMES = {ARCHAEOLOGIST: "Archaeologist", CONSERVATOR: "Conservator"}


_TOKENS: list[Any] = []


@pytest.fixture(autouse=True)
def _clear_context():
    yield
    while _TOKENS:
        clear_app_context(_TOKENS.pop())


def _as_agent(agent_id: str | None) -> None:
    _TOKENS.append(set_app_context(AppContext(emitter=None, user_id=REGISTRAR, agent_id=agent_id)))


def _history(dating_agent: str | None, treatment_agent: str | None) -> list[UnifiedMessage]:
    return [
        UnifiedMessage(role="user", id="u-1", content=[TextContent(text="Date this shard.")]),
        UnifiedMessage(
            role="assistant",
            id="a-dating",
            agent_id=dating_agent,
            content=[TextContent(text="Late Bronze Age, around 1200 BCE.")],
        ),
        UnifiedMessage(role="user", id="u-2", content=[TextContent(text="How do we treat it?")]),
        UnifiedMessage(
            role="assistant",
            id="a-treatment",
            agent_id=treatment_agent,
            content=[TextContent(text="Consolidate with Paraloid B-72.")],
        ),
    ]


def _send(history: list[UnifiedMessage], answering: str | None, monkeypatch) -> tuple[str, list]:
    loads: list[set[str]] = []

    async def fake_names(agent_ids: set[str]) -> dict[str, str]:
        loads.append(set(agent_ids))
        return {a: NAMES[a] for a in agent_ids if a in NAMES}

    monkeypatch.setattr(structured_input_resolver, "_load_agent_names", fake_names)
    _as_agent(answering)
    turn = UnifiedMessage.from_dict(
        {
            "role": "user",
            "content": [
                {
                    "type": REMARKS_PART_TYPE,
                    "items": [
                        {"kind": "comment", "target": {"message_id": "a-dating"}, "body": "Cite the stratum."},
                        {"kind": "comment", "target": {"message_id": "a-treatment"}, "body": "Is it reversible?"},
                    ],
                },
                {"type": "text", "text": "Please address both."},
            ],
        }
    )
    asyncio.run(resolve_structured_inputs(MessageList([*history, turn])))
    block = next(c for c in turn.content if isinstance(c, RemarksInputContent))
    return block.metadata["resolved_text"], loads


def test_single_agent_conversation_keeps_your_wording(monkeypatch) -> None:
    text, loads = _send(_history(ARCHAEOLOGIST, ARCHAEOLOGIST), ARCHAEOLOGIST, monkeypatch)
    assert "<!-- comment on your reply 2 back -->" in text
    assert "<!-- comment on your previous reply -->" in text
    assert loads == []  # no name lookup for a one-agent history


def test_multi_agent_conversation_names_the_other_agent(monkeypatch) -> None:
    # The Conservator answers now: its own reply stays "your", the
    # Archaeologist's reply is named — with ONE batched name load.
    text, loads = _send(_history(ARCHAEOLOGIST, CONSERVATOR), CONSERVATOR, monkeypatch)
    assert "<!-- comment on Archaeologist's reply 2 back -->" in text
    assert "<!-- comment on your previous reply -->" in text
    assert loads == [{ARCHAEOLOGIST}]


def test_multi_agent_previous_reply_reads_naturally(monkeypatch) -> None:
    text, _ = _send(_history(ARCHAEOLOGIST, CONSERVATOR), ARCHAEOLOGIST, monkeypatch)
    assert "<!-- comment on Conservator's previous reply -->" in text
    assert "<!-- comment on your reply 2 back -->" in text


@pytest.mark.parametrize(
    "dating, treatment",
    [(None, CONSERVATOR), (ARCHAEOLOGIST, None), (None, None)],
    ids=["dating-unattributed", "treatment-unattributed", "none-attributed"],
)
def test_missing_agent_id_falls_back_to_current_wording(dating, treatment, monkeypatch) -> None:
    text, loads = _send(_history(dating, treatment), CONSERVATOR, monkeypatch)
    assert "<!-- comment on your reply 2 back -->" in text
    assert "<!-- comment on your previous reply -->" in text
    assert loads == []


def test_unknown_agent_name_falls_back_to_current_wording(monkeypatch) -> None:
    deleted = "1f2e3d4c-5b6a-4798-8a7b-6c5d4e3f2a1b"
    text, _ = _send(_history(deleted, CONSERVATOR), CONSERVATOR, monkeypatch)
    assert "<!-- comment on your reply 2 back -->" in text


def test_from_cx_message_carries_agent_id() -> None:
    row = SimpleNamespace(
        role="assistant",
        content=[{"type": "text", "text": "Late Bronze Age."}],
        id="a-dating",
        created_at=None,
        status="active",
        is_visible_to_model=True,
        metadata={},
        user_content=None,
        position=3,
        agent_id=ARCHAEOLOGIST,
    )
    assert UnifiedMessage.from_cx_message(row).agent_id == ARCHAEOLOGIST
    row.agent_id = None
    assert UnifiedMessage.from_cx_message(row).agent_id is None


def _capture(monkeypatch) -> list[dict[str, Any]]:
    captured: list[dict[str, Any]] = []

    def capture(table: str, payload: dict[str, Any], **kwargs: Any) -> str:
        captured.append(payload)
        return "op-id"

    monkeypatch.setattr(queue_helpers, "_queue_or_drop", capture)
    return captured


@pytest.mark.parametrize("role", ["assistant", "tool"])
def test_persist_funnel_stamps_the_running_agent(role, monkeypatch) -> None:
    captured = _capture(monkeypatch)
    _as_agent(ARCHAEOLOGIST)
    queue_helpers.queue_message_create(
        id="m-1", conversation_id="c-1", role=role, content=[], status="active"
    )
    queue_helpers.queue_message_update("m-1", role=role, content=[], status="active")
    assert [p.get("agent_id") for p in captured] == [ARCHAEOLOGIST, ARCHAEOLOGIST]


def test_persist_funnel_never_stamps_user_rows_or_overrides_explicit(monkeypatch) -> None:
    captured = _capture(monkeypatch)
    _as_agent(ARCHAEOLOGIST)
    queue_helpers.queue_message_create(id="m-u", conversation_id="c-1", role="user", content=[])
    # The handoff synthetic row names the CHILD agent explicitly.
    queue_helpers.queue_message_create(
        id="m-h", conversation_id="c-1", role="assistant", content=[], agent_id=CONSERVATOR
    )
    assert "agent_id" not in captured[0]
    assert captured[1]["agent_id"] == CONSERVATOR


def test_persist_funnel_skips_a_malformed_agent_id(monkeypatch) -> None:
    captured = _capture(monkeypatch)
    _as_agent("cmp-not-a-uuid")
    queue_helpers.queue_message_create(id="m-1", conversation_id="c-1", role="assistant", content=[])
    assert "agent_id" not in captured[0]


def test_pinned_version_run_resolves_its_agent(monkeypatch) -> None:
    from matrx_ai.db import _registry, persistence

    version_id = "3a4b5c6d-7e8f-4a0b-9c1d-2e3f4a5b6c7d"
    reads: list[Any] = []

    class _Query:
        def __init__(self, ids: list[str]) -> None:
            self.ids = ids

        async def all(self) -> list[Any]:
            reads.append(self.ids)
            return [SimpleNamespace(id=version_id, agent_id=ARCHAEOLOGIST)]

    class _DefinitionVersion:
        @staticmethod
        def filter(id__in: list[str]) -> _Query:
            return _Query(id__in)

    monkeypatch.setattr(_registry, "get_model", lambda name: _DefinitionVersion)
    monkeypatch.setattr(persistence, "_VERSION_AGENT_IDS", {})
    pinned = SimpleNamespace(agent_id=None, agent_version_id=version_id)
    assert asyncio.run(persistence.pinned_version_agent_id(pinned)) == ARCHAEOLOGIST
    assert asyncio.run(persistence.pinned_version_agent_id(pinned)) == ARCHAEOLOGIST
    assert reads == [[version_id]]  # cached after the first read
    floating = SimpleNamespace(agent_id=CONSERVATOR, agent_version_id=version_id)
    assert asyncio.run(persistence.pinned_version_agent_id(floating)) is None
