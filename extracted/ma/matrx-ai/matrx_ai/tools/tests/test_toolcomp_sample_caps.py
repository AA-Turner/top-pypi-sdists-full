from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.tools.implementations import tool_component


class _SampleModel:
    @classmethod
    async def get_or_none(cls, **_kwargs):
        events = [{"chunk": "x" * 8_000} for _ in range(14)]
        values = {
            "arguments": {"prompt": "a" * 8_000},
            "is_success": True,
            "raw_stream_events": events,
            "final_payload": {"result": "z" * 20_000},
            "admin_comments": "n" * 4_000,
        }
        return SimpleNamespace(_fields=values, **values)


@pytest.mark.asyncio
async def test_full_sample_events_are_paged_and_field_bounded(monkeypatch) -> None:
    monkeypatch.setattr(tool_component, "get_db_model", lambda _name: _SampleModel)

    result = await tool_component.toolcomp_get_sample_detail(
        {
            "sample_id": "00000000-0000-0000-0000-000000000001",
            "full_events": True,
            "event_offset": 10,
            "event_limit": 10,
        },
        SimpleNamespace(),
    )

    assert result.success is True
    assert result.output_self_capped is True
    page = result.output.raw_stream_events
    assert page["total_events"] == 14
    assert page["returned_events"] == 4
    assert page["has_more_events"] is False
    assert page["next_event_offset"] is None
    assert len(page["events"]) == 4
    assert page["events"][0]["truncated"] is True
    assert result.output.arguments["truncated"] is True
    assert result.output.final_payload["truncated"] is True
    assert len(result.output.admin_comments) == 2_000
