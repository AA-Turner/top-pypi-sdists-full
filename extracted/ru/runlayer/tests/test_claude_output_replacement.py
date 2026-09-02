import json

import pytest

from runlayer_cli.hook.clients import Client, HookResponse


def test_claude_block_redacts_structured_output_without_original_keys() -> None:
    sensitive_key = "SSN 482-61-9357"
    original_output = {
        sensitive_key: "Olivia Harper",
        "metadata": {
            "content": "secret customer data",
            "lines": ["secret first line", 7, False, None],
        },
    }

    response = json.loads(
        HookResponse(Client.CLAUDE_CODE, "PostToolUse").block_output(
            "scanner blocked output",
            tool_name="Write",
            original_output=original_output,
        )
    )

    replacement = "[Runlayer blocked this tool output] scanner blocked output"
    assert response["hookSpecificOutput"]["updatedToolOutput"] == {
        "runlayer_redacted": replacement,
    }
    assert sensitive_key not in json.dumps(response)
    assert "secret customer data" not in json.dumps(response)
    assert "secret first line" not in json.dumps(response)


def test_claude_mask_redacts_structured_output_when_backend_returns_text() -> None:
    response_text = HookResponse(Client.CLAUDE_CODE, "PostToolUse").mask_output(
        "customer data [REDACTED]",
        tool_name="mcp__customer__read_record",
        original_output={
            "filePath": "/tmp/customer-record.csv",
            "content": "secret customer data",
        },
    )

    assert response_text is not None
    response = json.loads(response_text)
    assert response["hookSpecificOutput"]["updatedToolOutput"] == {
        "runlayer_redacted": "customer data [REDACTED]",
    }
    assert "secret customer data" not in response_text


def test_claude_mask_preserves_matching_backend_json_replacement() -> None:
    masked_output = {
        "filePath": "/tmp/[REDACTED].csv",
        "content": "customer data [REDACTED]",
    }

    response_text = HookResponse(Client.CLAUDE_CODE, "PostToolUse").mask_output(
        json.dumps(masked_output),
        tool_name="Write",
        original_output={
            "filePath": "/tmp/customer-record.csv",
            "content": "secret customer data",
        },
    )

    assert response_text is not None
    response = json.loads(response_text)
    assert response["hookSpecificOutput"]["updatedToolOutput"] == masked_output


def test_claude_mask_accepts_sanitized_object_with_changed_keys() -> None:
    sensitive_key = "SSN 482-61-9357"
    masked_output = {"redacted_identifier": "[REDACTED]"}

    response_text = HookResponse(Client.CLAUDE_CODE, "PostToolUse").mask_output(
        json.dumps(masked_output),
        tool_name="mcp__customer__read_record",
        original_output={sensitive_key: "Olivia Harper"},
    )

    assert response_text is not None
    response = json.loads(response_text)
    assert response["hookSpecificOutput"]["updatedToolOutput"] == masked_output
    assert sensitive_key not in response_text


def test_claude_block_wraps_mcp_list_output_in_text_content_block() -> None:
    """An MCP ``tool_response`` is a content-block list, so the replacement must
    stay object-shaped. A bare string inside the list is rejected by the Messages
    API (``tool_result.content.0: Input should be an object``), and because Claude
    Code persists ``updatedToolOutput`` into the transcript it poisons every
    later turn of the session, not just the blocked one."""
    original_output = [{"type": "text", "text": "secret customer data"}]

    response = json.loads(
        HookResponse(Client.CLAUDE_CODE, "PostToolUse").block_output(
            "scanner blocked output",
            tool_name="mcp__customer__read_record",
            original_output=original_output,
        )
    )

    replacement = "[Runlayer blocked this tool output] scanner blocked output"
    assert response["hookSpecificOutput"]["updatedToolOutput"] == [
        {"type": "text", "text": replacement},
    ]
    assert "secret customer data" not in json.dumps(response)


def test_claude_mask_wraps_mcp_list_output_in_text_content_block() -> None:
    response_text = HookResponse(Client.CLAUDE_CODE, "PostToolUse").mask_output(
        "customer data [REDACTED]",
        tool_name="mcp__customer__read_record",
        original_output=[{"type": "text", "text": "secret customer data"}],
    )

    assert response_text is not None
    response = json.loads(response_text)
    assert response["hookSpecificOutput"]["updatedToolOutput"] == [
        {"type": "text", "text": "customer data [REDACTED]"},
    ]
    assert "secret customer data" not in response_text


@pytest.mark.parametrize("tool_name", ["mcp__customer__read_record", "Read"])
def test_claude_list_replacement_items_stay_json_objects(tool_name: str) -> None:
    original_output = [
        {"type": "text", "text": "secret first block"},
        {"type": "text", "text": "secret second block"},
    ]

    response = json.loads(
        HookResponse(Client.CLAUDE_CODE, "PostToolUse").block_output(
            "scanner blocked output",
            tool_name=tool_name,
            original_output=original_output,
        )
    )

    updated = response["hookSpecificOutput"]["updatedToolOutput"]
    assert isinstance(updated, list)
    assert all(isinstance(item, dict) for item in updated)
    assert "secret first block" not in json.dumps(response)
    assert "secret second block" not in json.dumps(response)


@pytest.mark.parametrize(
    ("original_output", "expected_output"),
    [
        ("secret", "[REDACTED]"),
        (True, False),
        (7, 0),
        (1.5, 0.0),
        (None, None),
    ],
)
def test_claude_mask_redacts_top_level_json_scalars_with_matching_type(
    original_output: object,
    expected_output: object,
) -> None:
    response_text = HookResponse(Client.CLAUDE_CODE, "PostToolUse").mask_output(
        "[REDACTED]",
        tool_name="mcp__server__tool",
        original_output=original_output,
    )

    assert response_text is not None
    response = json.loads(response_text)
    assert response["hookSpecificOutput"]["updatedToolOutput"] == expected_output
