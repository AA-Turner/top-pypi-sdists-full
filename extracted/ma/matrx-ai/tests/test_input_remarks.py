"""input_remarks: the person's comments/choices/edits/answers/interactions on earlier
replies reach the model as markdown-native text with a location it can resolve.

Use case: Harbor Dental's front-desk manager is working with an agent on the
new-patient intake flow and the reminder-text cadence; she remarks on earlier
replies and sends the remarks with her next message.
"""

from __future__ import annotations

import asyncio
import copy
import typing

import pytest
from pydantic import TypeAdapter, ValidationError

from matrx_ai.config.message_config import MessageList, UnifiedMessage
from matrx_ai.config.models.structured_input import RemarksInputContentModel
from matrx_ai.config.remarks import REMARKS_PART_TYPE, RemarkItem
from matrx_ai.config.structured_input_config import RemarksInputContent
from matrx_ai.config.structured_input_resolver import resolve_structured_inputs
from matrx_ai.config.unified_content import TextContent, reconstruct_content
from matrx_ai.db.message_parts import (
    RemarksInputPart,
    UserInputPart,
    validate_message_content,
)


def _history() -> list[UnifiedMessage]:
    """Three assistant TURNS; the most recent is a tool loop (assistant → tool → assistant)."""
    return [
        UnifiedMessage(role="user", id="u-1", content=[TextContent(text="Draft the intake form.")]),
        UnifiedMessage(role="assistant", id="a-intake", content=[TextContent(text="Here is the form.")]),
        UnifiedMessage(role="user", id="u-2", content=[TextContent(text="Pick a cache for slots.")]),
        UnifiedMessage(role="assistant", id="a-cache", content=[TextContent(text="SQLite or Redis.")]),
        UnifiedMessage(role="user", id="u-3", content=[TextContent(text="Now the reminder texts.")]),
        UnifiedMessage(role="assistant", id="a-reminder-call", content=[]),
        UnifiedMessage(role="tool", id="t-reminder", content=[]),
        UnifiedMessage(role="assistant", id="a-reminder", content=[TextContent(text="Reminders at 48h and 2h.")]),
    ]


def _send(items: list[dict], typed: str = "Go ahead with these changes.") -> str:
    """Send one user turn carrying the remarks through the real resolver; return the provider text."""
    turn = UnifiedMessage.from_dict(
        {
            "role": "user",
            "content": [
                {"type": REMARKS_PART_TYPE, "items": copy.deepcopy(items)},
                {"type": "text", "text": typed},
            ],
        }
    )
    asyncio.run(resolve_structured_inputs(MessageList([*_history(), turn])))
    remarks = [c for c in turn.content if isinstance(c, RemarksInputContent)]
    assert len(remarks) == 1
    provider = remarks[0].to_anthropic()
    assert provider is not None
    return provider["text"]


# ── projection, one per kind (each a different expected text) ───────────────

_PROJECTIONS = [
    (
        {
            "kind": "comment",
            "target": {"message_id": "a-reminder"},
            "quote": "Reminders at 48h and 2h.",
            "body": "Patients say 2h is too late to rebook.",
        },
        "<!-- comment c1 on your previous reply -->\n"
        "> Reminders at 48h and 2h.\n\n"
        "Patients say 2h is too late to rebook.",
    ),
    (
        {
            "kind": "choice",
            "target": {"message_id": "a-cache"},
            "quote": "Cache strategy",
            "body": "I chose SQLite.",
        },
        "<!-- choice c1 in your reply 2 back -->\n> Cache strategy\n\nI chose SQLite.",
    ),
    (
        {
            "kind": "edit",
            "target": {"message_id": "a-intake"},
            "diff": "- Contact us anytime for help.\n+ Call us weekdays, 9 to 5.",
        },
        "<!-- edit c1 to your reply 3 back -->\n"
        "```diff\n- Contact us anytime for help.\n+ Call us weekdays, 9 to 5.\n```",
    ),
    (
        {
            "kind": "answers",
            "title": "Intake questions",
            "target": {"message_id": "a-intake"},
            "answers": [
                {"question": "Accepts Delta Dental PPO", "answer": True, "name": "accepts_delta", "type": "noul"},
                {"question": "Chairs on Saturdays", "answer": 3.0, "type": "score"},
                {"question": "Languages at the desk", "answer": ["English", "Spanish"]},
            ],
        },
        '<!-- answers c1 to "Intake questions" in your reply 3 back -->\n'
        "- Accepts Delta Dental PPO: Yes\n"
        "- Chairs on Saturdays: 3\n"
        "- Languages at the desk: English, Spanish",
    ),
    (
        {
            "kind": "interaction",
            "title": "Reminder cadence",
            "target": {"record_token": "note", "record_id": "n-1", "record_title": "Q3 recall plan"},
            "body": "Moved the second reminder from 2h to 24h.",
        },
        '<!-- interaction c1 with "Reminder cadence" in note “Q3 recall plan” -->\n'
        "Moved the second reminder from 2h to 24h.",
    ),
]


@pytest.mark.parametrize(("item", "expected"), _PROJECTIONS, ids=lambda v: v["kind"] if isinstance(v, dict) else "")
def test_each_kind_projects_to_its_markdown_with_a_resolvable_location(item: dict, expected: str) -> None:
    assert _send([item]) == expected


def test_several_remarks_project_in_order_separated_by_a_blank_line() -> None:
    items = [_PROJECTIONS[1][0], _PROJECTIONS[0][0]]
    second = _PROJECTIONS[0][1].replace("comment c1", "comment c2", 1)
    assert _send(items) == _PROJECTIONS[1][1] + "\n\n" + second


# ── turn counting ────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    ("message_id", "expected_location"),
    [
        # Both rows of the tool loop are ONE turn — the previous reply.
        ("a-reminder-call", "your previous reply"),
        ("a-reminder", "your previous reply"),
        ("a-cache", "your reply 2 back"),
        ("a-intake", "your reply 3 back"),
    ],
)
def test_location_counts_assistant_turns_not_rows_when_a_tool_loop_sits_between(
    message_id: str, expected_location: str
) -> None:
    text = _send([{"kind": "comment", "target": {"message_id": message_id}, "body": "Keep this."}])
    assert text.splitlines()[0] == f"<!-- comment c1 on {expected_location} -->"


def test_location_is_counted_from_the_containing_message_and_frozen_there() -> None:
    history = _history()
    first = UnifiedMessage.from_dict(
        {
            "role": "user",
            "content": [
                {"type": REMARKS_PART_TYPE, "items": [{"kind": "comment", "target": {"message_id": "a-reminder"}, "body": "Too late."}]}
            ],
        }
    )
    messages = MessageList([*history, first])
    asyncio.run(resolve_structured_inputs(messages))
    frozen = first.content[0].metadata["resolved_text"]
    assert frozen.startswith("<!-- comment c1 on your previous reply -->")

    # The conversation moves on two turns; the earlier remark must NOT be re-counted.
    stored = reconstruct_content(first.content[0].to_storage_dict())
    later = MessageList(
        [
            *history,
            UnifiedMessage(role="user", id="u-4", content=[stored]),
            UnifiedMessage(role="assistant", id="a-5", content=[TextContent(text="Updated.")]),
            UnifiedMessage(role="user", id="u-5", content=[TextContent(text="Thanks.")]),
        ]
    )
    asyncio.run(resolve_structured_inputs(later))
    assert stored.metadata["resolved_text"] == frozen


# ── fallback wording ─────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    ("item", "first_line"),
    [
        (
            {"kind": "comment", "target": {"message_id": "trimmed-away"}, "quote": "Bring your insurance card.", "body": "Add photo ID."},
            "<!-- comment c1 on the passage quoted below -->",
        ),
        (
            {"kind": "edit", "target": {"message_id": "trimmed-away"}, "diff": "- 48h\n+ 72h"},
            "<!-- edit c1 to an earlier reply -->",
        ),
        (
            {"kind": "comment", "quote": "Bring your insurance card.", "body": "Add photo ID."},
            "<!-- comment c1 on the passage quoted below -->",
        ),
        (
            {"kind": "comment", "target": {"record_token": "task"}, "body": "Assign to Maria."},
            "<!-- comment c1 on a task -->",
        ),
    ],
)
def test_a_target_outside_the_loaded_history_falls_back_to_honest_wording(item: dict, first_line: str) -> None:
    assert _send([item]).splitlines()[0] == first_line


def test_a_title_cannot_close_the_hidden_marker_early() -> None:
    text = _send(
        [{"kind": "answers", "title": "Intake --> step 2", "target": {"message_id": "a-intake"}, "answers": [{"question": "Parking", "answer": "Lot B"}]}]
    )
    first = text.splitlines()[0]
    assert first.count("-->") == 1 and first.endswith("-->")


# ── placement: after the person's typed text ─────────────────────────────────


def test_remarks_ride_after_the_persons_typed_text_in_the_same_turn() -> None:
    turn = UnifiedMessage.from_dict(
        {
            "role": "user",
            "content": [
                {"type": REMARKS_PART_TYPE, "items": [_PROJECTIONS[0][0]]},
                {"type": "text", "text": "Go ahead with these changes."},
            ],
        }
    )
    asyncio.run(resolve_structured_inputs(MessageList([*_history(), turn])))
    assert [type(c).__name__ for c in turn.content] == ["TextContent", "RemarksInputContent"]


# ── storage, decode, request contract ────────────────────────────────────────


def test_a_stored_remarks_block_round_trips_through_the_one_decoder_and_validates() -> None:
    items = [p[0] for p in _PROJECTIONS]
    block = RemarksInputContent(items=items)
    stored = validate_message_content([block.to_storage_dict()])[0]
    assert stored["type"] == "input_remarks"
    rebuilt = reconstruct_content(stored)
    assert isinstance(rebuilt, RemarksInputContent)
    assert [RemarkItem.model_validate(i) for i in rebuilt.items] == [RemarkItem.model_validate(i) for i in items]


def test_the_request_side_union_accepts_a_remarks_part() -> None:
    dumped = TypeAdapter(UserInputPart).validate_python(
        {"type": "input_remarks", "items": [_PROJECTIONS[1][0]]}
    )
    assert dumped["type"] == "input_remarks"
    assert dumped["items"][0]["body"] == "I chose SQLite."


@pytest.mark.parametrize(
    "bad",
    [
        {"type": "input_remarks", "items": [{"kind": "comment", "body": "ok", "sentiment": "angry"}]},
        {"type": "input_remarks", "items": [{"kind": "comment", "target": {"message_id": "a", "position": 3}, "body": "ok"}]},
        {"type": "input_remarks", "items": [{"kind": "comment", "body": "ok"}], "remarks_version": 2},
        {"type": "input_remarks", "items": [{"kind": "answers", "answers": [{"question": "Q", "answer": "A", "note": "x"}]}]},
    ],
    ids=["item", "target", "part", "answer"],
)
def test_an_undeclared_field_is_refused_at_every_level(bad: dict) -> None:
    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        RemarksInputPart.model_validate(bad)


@pytest.mark.parametrize(
    "bad",
    [
        {"type": "input_remarks", "items": []},
        {"type": "input_remarks", "items": [{"kind": "comment"}]},
        {"type": "input_remarks", "items": [{"kind": "answers", "body": "see below"}]},
        {"type": "input_remarks", "items": [{"kind": "applause", "body": "nice"}]},
        {"type": "input_remarks", "items": [{"kind": "answers", "answers": [{"question": "Q", "answer": "A", "name": "Has Spaces"}]}]},
    ],
    ids=["no-items", "empty-item", "answers-without-answers", "unknown-kind", "non-snake-name"],
)
def test_an_empty_or_malformed_remark_is_refused(bad: dict) -> None:
    with pytest.raises(ValidationError):
        RemarksInputPart.model_validate(bad)


def test_every_literal_spelling_of_the_part_type_is_the_one_constant() -> None:
    for cls in (RemarksInputPart, RemarksInputContent, RemarksInputContentModel):
        assert typing.get_args(typing.get_type_hints(cls)["type"]) == (REMARKS_PART_TYPE,), cls
