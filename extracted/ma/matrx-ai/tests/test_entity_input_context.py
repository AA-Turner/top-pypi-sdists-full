"""The seven id-backed attachment variants survive storage and reach model context."""

from __future__ import annotations

import asyncio
import json
import re

import pytest

from matrx_ai.config.message_config import MessageList, UnifiedMessage
from matrx_ai.config.structured_input_config import (
    AgentAppInputContent,
    AgentInputContent,
    ContextInputContent,
    DocumentInputContent,
    ProjectInputContent,
    TranscriptInputContent,
    TranscriptSessionInputContent,
    WorkbookInputContent,
    reconstruct_structured_input,
)
from matrx_ai.config.structured_input_resolver import resolve_structured_inputs

_FENCE_JSON = re.compile(r"```matrx\n(.*?)\n```", re.DOTALL)

_CASES = (
    ("input_agent", "agent_ids", "agent", AgentInputContent),
    ("input_project", "project_ids", "project", ProjectInputContent),
    ("input_agent_app", "agent_app_ids", "agent_app", AgentAppInputContent),
    ("input_transcript", "transcript_ids", "transcript", TranscriptInputContent),
    (
        "input_transcript_session",
        "transcript_session_ids",
        "transcript_session",
        TranscriptSessionInputContent,
    ),
    ("input_workbook", "workbook_ids", "workbook", WorkbookInputContent),
    ("input_document", "document_ids", "document", DocumentInputContent),
)


def _envelope(text: str) -> dict:
    match = _FENCE_JSON.search(text)
    assert match is not None, text
    return json.loads(match.group(1))


@pytest.mark.parametrize(("block_type", "ids_field", "reference_type", "expected_cls"), _CASES)
def test_reconstructs_and_round_trips_the_canonical_id_field(
    block_type: str,
    ids_field: str,
    reference_type: str,
    expected_cls: type,
) -> None:
    del reference_type
    resource_id = f"{block_type}-id"
    stored = {
        "type": block_type,
        ids_field: [resource_id],
        "template": "compact",
        "convert_to_text": True,
        "optional_context": False,
        "keep_fresh": True,
        "editable": False,
    }

    block = reconstruct_structured_input(stored)

    assert isinstance(block, expected_cls)
    assert block.to_storage_dict()[ids_field] == [resource_id]
    assert block.to_storage_dict()["editable"] is False
    assert block.read_only_resource_ids() == frozenset({resource_id})


@pytest.mark.parametrize(("block_type", "ids_field", "reference_type", "expected_cls"), _CASES)
def test_resolution_emits_a_canonical_reference_envelope_for_model_context(
    block_type: str,
    ids_field: str,
    reference_type: str,
    expected_cls: type,
) -> None:
    resource_ids = [f"{block_type}-1", f"{block_type}-2"]
    block = reconstruct_structured_input({"type": block_type, ids_field: resource_ids})
    assert isinstance(block, expected_cls)

    asyncio.run(block.resolve())
    provider_part = block.to_openai()

    assert provider_part is not None
    envelope = _envelope(provider_part["text"])
    # Kind Directives two-key shell (kind-directives merge, 2026-08-26):
    # __kind FIRST (the streaming detector reads the first key), items second.
    # The retired 4-key matrx_version shell is READ-ONLY platform-wide —
    # minting it was adversarial finding F2 of that campaign's review.
    assert envelope == {
        "__kind": f"directive_v1_reference_{reference_type}",
        "items": [{"id": resource_id} for resource_id in resource_ids],
    }
    assert next(iter(envelope)) == "__kind"


@pytest.mark.parametrize(("block_type", "ids_field", "reference_type", "expected_cls"), _CASES)
def test_message_parse_and_resolver_keep_every_attachment_in_the_provider_path(
    block_type: str,
    ids_field: str,
    reference_type: str,
    expected_cls: type,
) -> None:
    resource_id = f"{block_type}-id"
    message = UnifiedMessage.from_dict(
        {"role": "user", "content": [{"type": block_type, ids_field: [resource_id]}]}
    )
    assert isinstance(message.content[0], expected_cls)

    messages = MessageList([message])
    asyncio.run(resolve_structured_inputs(messages))

    provider_part = message.content[0].to_openai()
    assert provider_part is not None
    assert (
        _envelope(provider_part["text"])["__kind"]
        == f"directive_v1_reference_{reference_type}"
    )


def test_editable_record_inputs_use_only_existing_canonical_tools() -> None:
    assert ProjectInputContent(project_ids=["project-id"], editable=True).editable_tools() == {
        "data"
    }
    assert TranscriptInputContent(
        transcript_ids=["transcript-id"], editable=True
    ).editable_tools() == {"data"}
    assert AgentInputContent(agent_ids=["agent-id"], editable=True).editable_tools() == frozenset()
    assert AgentAppInputContent(
        agent_app_ids=["app-id"], editable=True
    ).editable_tools() == frozenset()


def test_context_snapshot_resolves_to_the_same_id_name_and_data_the_ui_renders() -> None:
    block = ContextInputContent(
        context_id="context-1",
        context_name="Campaign brief",
        context_data={"audience": "Founders", "priority": 3},
    )

    asyncio.run(block.resolve())

    assert '"id": "context-1"' in block.get_output()
    assert '"name": "Campaign brief"' in block.get_output()
    assert '"audience": "Founders"' in block.get_output()
    assert block.to_openai() is not None


@pytest.mark.parametrize(
    ("block_type", "ids_field"),
    [
        ("input_notes", "note_ids"),
        ("input_task", "task_ids"),
    ],
)
@pytest.mark.parametrize("body_key", ["content", "text", "body", "description", "value"])
def test_supported_snapshot_resources_reach_model_context_without_an_id(
    block_type: str,
    ids_field: str,
    body_key: str,
) -> None:
    expected_text = f"Frozen {block_type} from {body_key}"
    block = reconstruct_structured_input(
        {
            "type": block_type,
            ids_field: [{"mode": "snapshot", body_key: expected_text}],
        }
    )
    assert block is not None
    asyncio.run(block.resolve())
    assert expected_text in block.get_output()
    assert block.to_openai() is not None
    assert TranscriptSessionInputContent(
        transcript_session_ids=["session-id"], editable=True
    ).editable_tools() == frozenset()
