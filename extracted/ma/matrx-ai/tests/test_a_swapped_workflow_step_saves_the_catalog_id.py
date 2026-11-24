"""A workflow agent step that was swapped to another model saves the CATALOG id, as the code engine does.

Live (2026-11-20, research report flip, lane X1): workflow run 68c8c791 saved ``rs_synthesis.model_id =
'claude-sonnet-5-5'`` where the code engine saved ``3f1c9a52-…`` (same model). The free-tier swap
(``swap_model_this_turn_only``) sets ``config.model`` to the stand-in's NAME; ``run_model_id`` saw the usage's
name and the config's name resolve to the same id and kept "the configured form" — the name. The code engine's
``agent.config`` still held the configured id, so its reading differed.

Driven through the real step normalizer, the real swap function and a real compiled catalog (``load_from_rows``,
the seam ``reload()`` feeds) — no stub of ``resolve_model_ref``. Red proof: ~/code/temp/research-r2/red-proof.txt.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.catalog import manager as catalog_module
from matrx_ai.catalog.manager import AiCatalogManager
from matrx_ai.config.unified_config import swap_model_this_turn_only
from matrx_ai.config.usage_config import TokenUsage
from matrx_ai.graph_nodes.shared import normalize_completed_result

OPUS_ID = "bc43581f-c7a6-4fd5-aa6a-8267074f480e"  # the live rows (ai.model_definition, read 2026-11-20)
SONNET_ID = "3f1c9a52-7b4e-4d2a-9c61-5e8a0b2d7f15"


@pytest.fixture(autouse=True)
def _catalog(monkeypatch) -> AiCatalogManager:
    catalog = AiCatalogManager()
    catalog.load_from_rows(
        endpoints=[], apis=[], offerings=[], settings=[], providers={}, aliases=[],
        models=[
            {"id": OPUS_ID, "name": "claude-opus-5-5", "common_name": "Claude Opus 5.5", "is_deprecated": False},
            {"id": SONNET_ID, "name": "claude-sonnet-5-5", "common_name": "Claude Sonnet 5.5", "is_deprecated": False},
        ],
    )
    monkeypatch.setattr(catalog_module, "ai_catalog_manager", catalog)
    return catalog


def _completed(model: str, answered_by: str) -> SimpleNamespace:
    config = SimpleNamespace(model=model, messages=[], response_format=None)
    usage = TokenUsage.aggregate_by_model([TokenUsage(matrx_model_name=answered_by, input_tokens=10, output_tokens=5)])
    assistant = SimpleNamespace(role="assistant", content="the report")
    return SimpleNamespace(
        metadata={"status": "complete"},
        request=SimpleNamespace(conversation_id="c1", request_id="r1", config=config, usage_history=[]),
        final_response=SimpleNamespace(messages=[assistant], finish_reason="stop"),
        total_usage=usage,
        timing_stats={},
        tool_call_stats={},
    ), config


def _model_id(completed: SimpleNamespace) -> str | None:
    return normalize_completed_result(completed).result.metadata["model_id"]


def test_a_step_swapped_to_another_model_saves_that_models_catalog_id() -> None:
    completed, config = _completed(OPUS_ID, "claude-sonnet-5-5")
    swap_model_this_turn_only(config, "claude-sonnet-5-5", swap_reason="free_tier", swapped_from="claude-opus-5-5")
    assert config.model == "claude-sonnet-5-5"  # the swap leaves a NAME on the config
    result_model_id = _model_id(completed)
    assert result_model_id == SONNET_ID


def test_an_unswapped_step_saves_the_catalog_id_too() -> None:
    completed, _ = _completed(OPUS_ID, "claude-opus-5-5")
    assert _model_id(completed) == OPUS_ID


def test_a_config_holding_a_name_with_no_usage_still_saves_the_id() -> None:
    completed, _ = _completed("claude-sonnet-5-5", "claude-sonnet-5-5")
    completed.total_usage = None
    assert _model_id(completed) == SONNET_ID
