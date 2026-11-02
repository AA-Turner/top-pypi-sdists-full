"""text.case — case + spacing on one text or a list, run through the real scheduler."""

from __future__ import annotations

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.nodes import BUILTIN_VALUES_ARE

from tests._fixtures import make_app_context


async def _run(inputs: dict, config: dict) -> dict:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    defn = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "n",
                    "type": "text.case",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": config, "inputs": inputs},
                }
            ],
            "edges": [],
        }
    )
    graph = compile_graph(defn, registry=registry)
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=registry)
    result = await scheduler.run(run_id="t-text-case", inputs=inputs)
    assert result.status is RunStatus.COMPLETED, result
    return result.last_outputs["n"]


async def test_list_of_email_addresses_lower_cased_and_trimmed_in_order():
    out = await _run(
        {"text": ["  Jane.Doe@Example.COM ", None, "ops@example.com"]},
        {"case": "lower"},
    )
    assert out["text"] == ["jane.doe@example.com", None, "ops@example.com"]
    assert out["changed"] == 1


async def test_title_case_keeps_hyphen_and_apostrophe_words_sane():
    out = await _run({"text": "  mary-jane   O'NEIL\tdon't "}, {"case": "title"})
    assert out["text"] == "Mary-Jane O'neil Don't"
    assert out["changed"] == 1


async def test_keep_case_only_tidies_spaces_and_none_stays_none():
    out = await _run({"text": "Acme   Widgets\n Inc"}, {})
    assert out["text"] == "Acme Widgets Inc"
    none_out = await _run({"text": None}, {"case": "upper"})
    assert (none_out["text"], none_out["changed"]) == (None, 0)
    assert none_out["__kind"] == "text_case_result"


async def test_upper_and_casefold():
    assert (await _run({"text": "tag-a"}, {"case": "upper", "trim": False}))["text"] == "TAG-A"
    assert (await _run({"text": "Straße"}, {"case": "casefold"}))["text"] == "strasse"


def test_text_case_declares_its_values_deterministic():
    assert BUILTIN_VALUES_ARE.get("text.case") == "deterministic"
