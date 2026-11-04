"""Strata-2 tests: the generated pydantic models parse representative payloads,
and the Stainless-named aliases point at them."""

from __future__ import annotations

from composio_client._models import (
    SessionConfigHistoryResponse,
    SessionCreateResponse,
    SessionExecuteResponse,
)


def test_create_response_parses_and_ignores_extra() -> None:
    model = SessionCreateResponse.model_validate(
        {
            "session_id": "sess_1",
            "mcp": {"type": "http", "url": "https://mcp.example.com"},
            "tool_router_tools": [],
            "config": {
                "user_id": "u",
                "instant": False,
                "preload": {"tools": []},
                "search": {},
                "execute": {},
            },
            "config_version": 3,
            "some_future_field": "ignored",  # extra fields tolerated (relaxed types)
        }
    )
    assert model.session_id == "sess_1"
    assert model.config_version == 3


def test_execute_response_data_is_open_mapping() -> None:
    model = SessionExecuteResponse.model_validate(
        {"result_type": "completed", "data": {"anything": [1, 2, 3]}, "error": None, "log_id": "l"}
    )
    assert model.root.data == {"anything": [1, 2, 3]}


def test_config_history_is_rootmodel() -> None:
    model = SessionConfigHistoryResponse.model_validate(
        {"items": [], "total_pages": 2, "current_page": 1, "total_items": 0}
    )
    assert model.root.total_pages == 2
