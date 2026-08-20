"""What happens to an activity entry this SDK version does not model.

The platform adds activity kinds continuously. Before the fallback, one unknown entry made the
whole activity log unreadable - get_activity_log raised rather than losing that entry's detail.
"""

from typing import Any, Dict, List

import pytest
from pydantic import ValidationError

from xpander_sdk.models.activity import (
    AgentActivityThread,
    AgentActivityThreadGatewayCreateExecution,
    AgentActivityThreadMessage,
    AgentActivityThreadOtherEntry,
    AgentActivityThreadReasoning,
    AgentActivityThreadSubAgentTrigger,
    AgentActivityThreadToolCall,
)

CREATED = "2026-08-19T10:00:00Z"


def parse(*entries: Dict[str, Any]) -> List[Any]:
    """Parse raw activity entries the way get_activity_log does, and return the models."""
    return AgentActivityThread(
        id="t1", created_at=CREATED, messages=list(entries)
    ).messages


class TestKindsThisVersionModels:
    """The fallback accepts anything, so it must never win over a kind that is modelled."""

    def test_a_message_is_still_a_message(self):
        [entry] = parse(
            {
                "id": "e1",
                "created_at": CREATED,
                "role": "user",
                "content": {"text": "hi"},
            }
        )
        assert isinstance(entry, AgentActivityThreadMessage)

    def test_a_tool_call_is_still_a_tool_call(self):
        [entry] = parse(
            {
                "id": "e2",
                "created_at": CREATED,
                "tool_name": "gmail_send",
                "payload": {},
            }
        )
        assert isinstance(entry, AgentActivityThreadToolCall)

    def test_reasoning_is_still_reasoning(self):
        [entry] = parse(
            {
                "id": "e3",
                "created_at": CREATED,
                "type": "think",
                "title": "Deciding",
                "confidence": 0.9,
            }
        )
        assert isinstance(entry, AgentActivityThreadReasoning)

    def test_a_gateway_decision_is_still_itself(self):
        [entry] = parse(
            {
                "id": "e4",
                "created_at": CREATED,
                "agent_id": "a1",
                "reasoning": "",
                "action": "create_execution",
                "created_execution_id": "x1",
            }
        )
        assert isinstance(entry, AgentActivityThreadGatewayCreateExecution)


class TestKindsThisVersionDoesNot:
    def test_an_approval_card_no_longer_breaks_the_log(self):
        [entry] = parse(
            {
                "id": "e5",
                "created_at": CREATED,
                "agent_id": "a1",
                "reasoning": "",
                "action": "tool_approval",
                "request_id": "req-1",
                "tool_label": "Send an email",
            }
        )
        assert isinstance(entry, AgentActivityThreadOtherEntry)

    def test_it_keeps_what_it_could_not_model(self):
        # Degrading to a generic record is the point; losing the payload would not be better.
        [entry] = parse(
            {
                "id": "e6",
                "created_at": CREATED,
                "action": "tool_approval",
                "request_id": "req-1",
            }
        )
        assert entry.id == "e6"
        assert entry.model_dump().get("request_id") == "req-1"

    @pytest.mark.parametrize(
        "action,extra",
        [
            ("ask_for_secret", {"secrets": []}),
            ("ask_user_questions", {"questions": []}),
            ("suggest_tool", {"suggestions": []}),
            ("invite_member", {"email": "a@b.c"}),
            ("tool_approval", {"request_id": "r1"}),
        ],
    )
    def test_every_card_kind_shipped_since_this_union_was_written(self, action, extra):
        # All of these already existed on the platform and already broke the log.
        [entry] = parse(
            {
                "id": "e7",
                "created_at": CREATED,
                "agent_id": "a1",
                "reasoning": "",
                "action": action,
                **extra,
            }
        )
        assert isinstance(entry, AgentActivityThreadOtherEntry)

    def test_one_unknown_entry_does_not_cost_the_known_ones(self):
        entries = parse(
            {
                "id": "e8",
                "created_at": CREATED,
                "role": "user",
                "content": {"text": "hi"},
            },
            {
                "id": "e9",
                "created_at": CREATED,
                "action": "tool_approval",
                "request_id": "r1",
            },
            {"id": "e10", "created_at": CREATED, "tool_name": "search", "payload": {}},
        )
        assert [type(e).__name__ for e in entries] == [
            "AgentActivityThreadMessage",
            "AgentActivityThreadOtherEntry",
            "AgentActivityThreadToolCall",
        ]


class TestTheThreadItself:
    def test_a_thread_still_needs_its_own_identity(self):
        # The fallback is for entries, not for the envelope around them.
        with pytest.raises(ValidationError):
            AgentActivityThread(created_at=CREATED, messages=[])


class TestAnUnmodelledActionIsNeverMatchedPositionally:
    """A card that happens to satisfy an older model must not be read as that model."""

    def test_a_card_carrying_an_object_reasoning_is_not_a_sub_agent_trigger(self):
        # SubAgentTrigger ignores `action` entirely, so agent_id plus an object reasoning
        # satisfies it and would swallow every future card kind.
        [entry] = parse(
            {
                "id": "e11",
                "created_at": CREATED,
                "agent_id": "a1",
                "reasoning": {"thought": "x"},
                "action": "tool_approval",
                "request_id": "r1",
            }
        )
        assert isinstance(entry, AgentActivityThreadOtherEntry)

    def test_a_real_sub_agent_trigger_is_untouched(self):
        [entry] = parse(
            {
                "id": "e12",
                "created_at": CREATED,
                "agent_id": "a1",
                "reasoning": {"thought": "x"},
                "query": "go",
            }
        )
        assert isinstance(entry, AgentActivityThreadSubAgentTrigger)

    def test_a_modelled_action_still_resolves_to_its_own_model(self):
        [entry] = parse(
            {
                "id": "e13",
                "created_at": CREATED,
                "agent_id": "a1",
                "reasoning": "",
                "action": "create_execution",
                "created_execution_id": "x1",
            }
        )
        assert isinstance(entry, AgentActivityThreadGatewayCreateExecution)
