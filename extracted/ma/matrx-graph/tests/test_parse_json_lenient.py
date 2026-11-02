"""data.parse_json `lenient`: reads an AI's reply through the host's LLM-JSON funnel, and says
so in the run log whenever it had to repair anything. Off, the step stays exact json.loads."""

from __future__ import annotations

import json
import re
from collections.abc import Iterator
from typing import Any

import pytest

from matrx_graph import (
    Definition,
    LlmJsonExtraction,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    configure_llm_json_extractor,
    register_builtin_nodes,
    run_log,
)
from matrx_graph.run_log import RunLogEntry
from tests._fixtures import make_app_context

LABEL = "parse_json.repaired"


def _fence_reader(text: str, schema: dict | None) -> LlmJsonExtraction:
    """A stand-in funnel: every ```json fence is a candidate; the schema's required keys filter."""
    blocks = [json.loads(b) for b in re.findall(r"```json\s*(.*?)```", text, re.S)]
    required = (schema or {}).get("required", [])
    fits = [b for b in blocks if isinstance(b, dict) and all(k in b for k in required)]
    if not fits:
        try:
            fits = [json.loads(text)]
        except json.JSONDecodeError:
            return LlmJsonExtraction(ok=False, reason="no valid JSON found in response")
    return LlmJsonExtraction(ok=True, value=fits[0], candidates=len(fits))


class _Recorder:
    def __init__(self) -> None:
        self.rows: list[dict[str, Any]] = []

    async def __call__(self, **kw: Any) -> RunLogEntry:
        self.rows.append(kw)
        return RunLogEntry(
            recorded=True, entry_id=str(len(self.rows)), label=kw["label"], needs_review=kw["needs_review"]
        )

    def repairs(self) -> list[dict[str, Any]]:
        return [r for r in self.rows if r["label"] == LABEL]


@pytest.fixture
def recorder() -> Iterator[_Recorder]:
    rec = _Recorder()
    run_log.configure_run_log_writer(rec)
    configure_llm_json_extractor(_fence_reader)
    try:
        yield rec
    finally:
        run_log.configure_run_log_writer(None)
        configure_llm_json_extractor(None)


async def _run(text: str, config: dict | None):
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    data: dict = {"inputs": {"text": text}}
    if config is not None:
        data["config"] = config
    defn = Definition.model_validate(
        {"nodes": [{"id": "n", "type": "data.parse_json", "position": {"x": 0, "y": 0}, "data": data}], "edges": []}
    )
    graph = compile_graph(defn, registry=registry)
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=registry)
    return await scheduler.run(run_id="t-parse-lenient", inputs={"text": text})


REPLY = 'Here are your variants:\n```json\n{"variants": ["a", "b"]}\n```\nHope that helps.'


async def test_strict_by_default_refuses_a_fenced_reply(recorder: _Recorder):
    result = await _run(REPLY, None)
    assert result.status is RunStatus.ERRORED
    assert "parse_failed" in (result.error or "")


async def test_lenient_reads_the_fenced_reply_and_says_it_repaired(recorder: _Recorder):
    result = await _run(REPLY, {"lenient": True})
    assert result.status is RunStatus.COMPLETED
    assert result.last_outputs["n"]["value"] == {"variants": ["a", "b"]}
    assert len(recorder.repairs()) == 1


async def test_lenient_on_clean_json_is_silent(recorder: _Recorder):
    result = await _run('{"variants": []}', {"lenient": True})
    assert result.status is RunStatus.COMPLETED
    assert result.last_outputs["n"]["value"] == {"variants": []}
    assert recorder.repairs() == []


async def test_the_schema_picks_the_block_that_fits_and_names_the_choice(recorder: _Recorder):
    two = '```json\n{"note": 1}\n```\n```json\n{"variants": ["x"]}\n```\n```json\n{"variants": ["y"]}\n```'
    result = await _run(two, {"lenient": True, "schema_definition": {"type": "object", "required": ["variants"]}})
    assert result.last_outputs["n"]["value"] == {"variants": ["x"]}
    [row] = recorder.repairs()
    assert "2 JSON blocks" in row["message"]


async def test_lenient_without_a_host_funnel_fails_loudly(recorder: _Recorder):
    configure_llm_json_extractor(None)
    result = await _run(REPLY, {"lenient": True})
    assert result.status is RunStatus.ERRORED
    assert "parse_unavailable" in (result.error or "")


async def test_nothing_to_read_is_a_parse_failure(recorder: _Recorder):
    result = await _run("no json here at all", {"lenient": True})
    assert result.status is RunStatus.ERRORED
    assert "parse_failed" in (result.error or "")
