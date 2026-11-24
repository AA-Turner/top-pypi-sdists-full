"""text.template renders a record/list placeholder as JSON text, never Python repr."""

from __future__ import annotations

import json

import pytest

from matrx_graph.nodes.text.manipulate import TemplateExecutor, TemplateInput


@pytest.mark.asyncio
async def test_record_and_list_placeholders_render_as_json_not_repr() -> None:
    values = {"Title": "First", "Done": True, "Owner": None, "Tags": ["a", "b"]}
    res = await TemplateExecutor().execute(
        None, TemplateInput(template="Record: {{values}} / {{values.Tags}} / {{values.Title}} / {{values.Owner}}", variables={"values": values}), None  # type: ignore[arg-type]
    )
    text = res.result.text
    assert text == f'Record: {json.dumps(values, ensure_ascii=False)} / ["a", "b"] / First / '
    assert "'" not in text and "None" not in text and "True" not in text
