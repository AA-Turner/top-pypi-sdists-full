"""Regression test for tool-call usage detail pairing (2026-07-01).

Pins the mixed-batch misalignment defect: tool_call_details used to be built by
zipping the raw model calls positionally against content_results — but
content_results contains COMPLETED calls only (client-delegated calls are
excluded because they have no result yet), so any delegated call in the middle
of a batch shifted every subsequent detail onto the wrong call. Details must
come from each content result itself.

Also pins failure enrichment (2026-07-10): failed entries carry arguments,
structured error, agent-facing error string, and a tool-definition snapshot.
"""

from __future__ import annotations

from matrx_ai.orchestrator.executor import _tool_call_details_from_content


def test_mixed_delegated_batch_attributes_correctly():
    # Model issued three calls: [server_a, DELEGATED, server_b].
    # content_results holds only the two completed ones.
    content_results = [
        {"call_id": "c1", "tool_use_id": "c1", "name": "server_a", "is_error": False},
        {"call_id": "c3", "tool_use_id": "c3", "name": "server_b", "is_error": True},
    ]
    details = _tool_call_details_from_content(content_results)

    assert details[0] == {
        "name": "server_a",
        "id": "c1",
        "call_id": "c1",
        "success": True,
    }
    assert details[1]["name"] == "server_b"
    assert details[1]["call_id"] == "c3"
    assert details[1]["success"] is False
    assert "arguments" in details[1]
    assert "error" in details[1]
    assert "agent_error" in details[1]


def test_falls_back_to_tool_use_id():
    details = _tool_call_details_from_content(
        [{"tool_use_id": "tu-9", "name": "t", "is_error": False}]
    )
    assert details[0]["call_id"] == "tu-9"
    assert details[0]["id"] == "tu-9"


def test_empty_batch():
    assert _tool_call_details_from_content([]) == []


def test_failure_enrichment_includes_args_error_and_agent_message(monkeypatch):
    from matrx_ai.orchestrator import executor as ex

    monkeypatch.setattr(
        ex,
        "_tool_definition_snapshot",
        lambda name: {
            "name": name,
            "description": "Get context by key",
            "parameters": {"key": {"type": "string"}},
        },
    )

    content_results = [
        {
            "call_id": "toolu_fail",
            "tool_use_id": "toolu_fail",
            "name": "context",
            "is_error": True,
            "content": "TOOL ERROR [not_found]: No context objects are available.",
            "error": {
                "error_type": "not_found",
                "message": "No context objects are available.",
            },
        }
    ]
    raw_calls = [
        {
            "name": "context",
            "call_id": "toolu_fail",
            "arguments": {"action": "get", "key": "attached_document_abc"},
        }
    ]
    details = _tool_call_details_from_content(content_results, raw_calls=raw_calls)
    assert len(details) == 1
    d = details[0]
    assert d["success"] is False
    assert d["arguments"] == {"action": "get", "key": "attached_document_abc"}
    assert d["error"] == {
        "error_type": "not_found",
        "message": "No context objects are available.",
    }
    assert d["agent_error"] == ("TOOL ERROR [not_found]: No context objects are available.")
    assert d["definition"] == {
        "name": "context",
        "description": "Get context by key",
        "parameters": {"key": {"type": "string"}},
    }


def test_success_entries_stay_sparse():
    details = _tool_call_details_from_content(
        [
            {
                "call_id": "ok1",
                "name": "context",
                "is_error": False,
                "content": '{"ok": true}',
            }
        ],
        raw_calls=[{"call_id": "ok1", "name": "context", "arguments": {"action": "list"}}],
    )
    assert details == [{"name": "context", "id": "ok1", "call_id": "ok1", "success": True}]
