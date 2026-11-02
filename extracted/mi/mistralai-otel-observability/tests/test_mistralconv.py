"""Tests for Mistral and GenAI message conversion compatibility."""

import pytest

from mistralai.observability.otel import mistralconv as conv
from mistralai.observability.otel.mistralconv import (
    MistralConversionError,
    mistral_choices_to_otel_output_messages,
    mistral_messages_to_otel_input_messages,
    otel_input_messages_to_mistral_messages,
    otel_output_messages_to_mistral_choices,
)


def test_text_message_round_trip_normalizes_to_structured_text_chunk() -> None:
    """Text content should round-trip through structured text chunks."""
    messages = [{"role": conv.ROLE_USER, "content": "hello", "name": "alice"}]

    otel = mistral_messages_to_otel_input_messages(messages)
    assert otel == [
        {
            "role": conv.ROLE_USER,
            "name": "alice",
            conv.MISTRAL_FIELD_NAME: "alice",
            "parts": [{"type": conv.TYPE_TEXT, "content": "hello"}],
        }
    ]

    assert otel_input_messages_to_mistral_messages(otel) == [
        {
            "role": conv.ROLE_USER,
            "name": "alice",
            "content": [{"type": conv.TYPE_TEXT, "text": "hello"}],
        }
    ]


def test_media_file_and_unknown_chunks_map_to_otel_parts() -> None:
    """Media, files, and references should map to GenAI parts."""
    messages = [
        {
            "role": conv.ROLE_USER,
            "content": [
                {
                    "type": conv.TYPE_IMAGE_URL,
                    "image_url": {"url": "https://example.com/image.png", "detail": "high"},
                },
                {
                    "type": conv.TYPE_DOCUMENT_URL,
                    "document_url": "https://example.com/doc.pdf",
                    "document_name": "Spec",
                },
                {"type": conv.TYPE_INPUT_AUDIO, "input_audio": "base64-audio"},
                {"type": conv.TYPE_FILE, "file_id": "file_123"},
                {"type": conv.TYPE_REFERENCE, "reference_ids": [1, 2]},
            ],
        }
    ]

    otel = mistral_messages_to_otel_input_messages(messages)

    assert otel[0]["parts"] == [
        {
            "type": conv.TYPE_URI,
            "modality": conv.MODALITY_IMAGE,
            "uri": "https://example.com/image.png",
            conv.MISTRAL_FIELD_DETAIL: "high",
        },
        {
            "type": conv.TYPE_URI,
            "modality": conv.MODALITY_DOCUMENT,
            "uri": "https://example.com/doc.pdf",
            conv.MISTRAL_FIELD_DOCUMENT_NAME: "Spec",
        },
        {
            "type": conv.TYPE_BLOB,
            "modality": conv.MODALITY_AUDIO,
            "content": "base64-audio",
            conv.MISTRAL_FIELD_TYPE: conv.TYPE_INPUT_AUDIO,
        },
        {"type": conv.TYPE_FILE, "modality": conv.MODALITY_DOCUMENT, "file_id": "file_123"},
        {"type": conv.TYPE_REFERENCE, "reference_ids": [1, 2]},
    ]

    assert otel_input_messages_to_mistral_messages(otel) == messages


def test_assistant_tool_calls_are_embedded_in_parts() -> None:
    """Assistant tool calls should be preserved as message parts."""
    messages = [
        {
            "role": conv.ROLE_ASSISTANT,
            "content": None,
            "prefix": True,
            "tool_calls": [
                {
                    "id": "call_1",
                    "type": conv.TOOL_CALL_TYPE_FUNCTION,
                    "index": 0,
                    "function": {"name": "get_weather", "arguments": {"city": "Paris"}},
                }
            ],
        }
    ]

    otel = mistral_messages_to_otel_input_messages(messages)
    assert otel == [
        {
            "role": conv.ROLE_ASSISTANT,
            conv.MISTRAL_FIELD_PREFIX: True,
            "parts": [
                {
                    "type": conv.TYPE_TOOL_CALL,
                    "id": "call_1",
                    "name": "get_weather",
                    "arguments": {"city": "Paris"},
                    conv.MISTRAL_FIELD_INDEX: 0,
                    conv.MISTRAL_FIELD_TYPE: conv.TOOL_CALL_TYPE_FUNCTION,
                }
            ],
        }
    ]

    assert otel_input_messages_to_mistral_messages(otel) == messages


def test_tool_message_round_trip_normalizes_string_response() -> None:
    """Tool response strings should round-trip through structured content."""
    messages = [{"role": conv.ROLE_TOOL, "tool_call_id": "call_1", "name": "get_weather", "content": "sunny"}]

    otel = mistral_messages_to_otel_input_messages(messages)
    assert otel == [
        {
            "role": conv.ROLE_TOOL,
            "name": "get_weather",
            conv.MISTRAL_FIELD_NAME: "get_weather",
            "parts": [{"type": conv.TYPE_TOOL_CALL_RESPONSE, "id": "call_1", "response": "sunny"}],
        }
    ]

    assert otel_input_messages_to_mistral_messages(otel) == [
        {
            "role": conv.ROLE_TOOL,
            "name": "get_weather",
            "tool_call_id": "call_1",
            "content": [{"type": conv.TYPE_TEXT, "text": "sunny"}],
        }
    ]


def test_thinking_chunk_preserves_mistral_thinking_over_flattened_content() -> None:
    """Mistral thinking chunks should keep provider-specific details."""
    messages = [
        {
            "role": conv.ROLE_ASSISTANT,
            "content": [
                {
                    "type": conv.TYPE_THINKING,
                    "closed": False,
                    "thinking": [
                        {"type": conv.TYPE_TEXT, "text": "first"},
                        {"type": conv.TYPE_REFERENCE, "reference_ids": [1]},
                        {"type": conv.TYPE_TEXT, "text": "second"},
                    ],
                }
            ],
        }
    ]

    otel = mistral_messages_to_otel_input_messages(messages)
    assert otel[0]["parts"] == [
        {
            "type": conv.TYPE_REASONING,
            "content": "firstsecond",
            conv.MISTRAL_FIELD_CLOSED: False,
            conv.MISTRAL_FIELD_THINKING: [
                {"type": conv.TYPE_TEXT, "text": "first"},
                {"type": conv.TYPE_REFERENCE, "reference_ids": [1]},
                {"type": conv.TYPE_TEXT, "text": "second"},
            ],
        }
    ]

    synthetic = [{"role": conv.ROLE_ASSISTANT, "parts": [{"type": conv.TYPE_REASONING, "content": "fallback"}]}]
    assert otel_input_messages_to_mistral_messages(synthetic) == [
        {
            "role": conv.ROLE_ASSISTANT,
            "content": [{"type": conv.TYPE_THINKING, "thinking": [{"type": conv.TYPE_TEXT, "text": "fallback"}]}],
        }
    ]
    assert otel_input_messages_to_mistral_messages(otel) == messages


def test_unsupported_otel_parts_are_ignored_on_mistral_conversion() -> None:
    """Unsupported GenAI parts should not break reverse conversion."""
    otel = [
        {
            "role": conv.ROLE_USER,
            "parts": [
                {"type": conv.TYPE_URI, "modality": conv.MODALITY_VIDEO, "uri": "https://example.com/video.mp4"},
                {"type": conv.TYPE_BLOB, "modality": conv.MODALITY_IMAGE, "content": "base64-image"},
                {"type": conv.TYPE_TEXT, "content": "kept"},
            ],
        }
    ]

    assert otel_input_messages_to_mistral_messages(otel) == [
        {"role": conv.ROLE_USER, "content": [{"type": conv.TYPE_TEXT, "text": "kept"}]}
    ]


def test_output_messages_round_trip_choices() -> None:
    """Output messages should round-trip through Mistral choices."""
    choices = [
        {
            "index": 2,
            "finish_reason": conv.FINISH_REASON_TOOL_CALLS,
            "message": {
                "role": conv.ROLE_ASSISTANT,
                "content": "hello",
            },
        }
    ]

    otel = mistral_choices_to_otel_output_messages(choices)
    assert otel == [
        {
            "role": conv.ROLE_ASSISTANT,
            "parts": [{"type": conv.TYPE_TEXT, "content": "hello"}],
            "finish_reason": conv.FINISH_REASON_TOOL_CALLS,
            conv.MISTRAL_FIELD_INDEX: 2,
        }
    ]

    assert otel_output_messages_to_mistral_choices(otel) == [
        {
            "index": 2,
            "finish_reason": conv.FINISH_REASON_TOOL_CALLS,
            "message": {"role": conv.ROLE_ASSISTANT, "content": [{"type": conv.TYPE_TEXT, "text": "hello"}]},
        }
    ]


def test_validation_matches_go_converter() -> None:
    """Validation errors should match the existing Go converter rules."""
    with pytest.raises(MistralConversionError, match="system message content must not be null"):
        mistral_messages_to_otel_input_messages([{"role": conv.ROLE_SYSTEM, "content": None}])

    with pytest.raises(MistralConversionError, match="user message must not contain prefix"):
        mistral_messages_to_otel_input_messages([{"role": conv.ROLE_USER, "content": "hello", "prefix": True}])

    with pytest.raises(MistralConversionError, match="tool message must have tool_call_id"):
        mistral_messages_to_otel_input_messages([{"role": conv.ROLE_TOOL, "content": "result"}])

    with pytest.raises(MistralConversionError, match="tool message must contain one tool_call_response part"):
        otel_input_messages_to_mistral_messages([{"role": conv.ROLE_TOOL, "parts": []}])


def test_unknown_roles_pass_through_content_mapping() -> None:
    """Unknown roles should preserve their content mapping."""
    otel = mistral_messages_to_otel_input_messages([{"role": "developer", "content": "hello"}])
    assert otel == [{"role": "developer", "parts": [{"type": conv.TYPE_TEXT, "content": "hello"}]}]
    assert otel_input_messages_to_mistral_messages(otel) == [
        {"role": "developer", "content": [{"type": conv.TYPE_TEXT, "text": "hello"}]}
    ]
