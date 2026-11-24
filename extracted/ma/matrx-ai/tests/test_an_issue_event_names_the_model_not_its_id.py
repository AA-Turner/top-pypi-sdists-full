"""An ops issue event records the model's NAME, never the catalog row's id.

Live 2026-11-19: recovered provider failures were filed with ``model`` =
``9f6c69bc-…`` (openai/gpt-oss-20b) and ``b32f2079-…`` (gemini-3.8-flash) because the
executor passes ``config.model``, which holds the catalog id when a client sent
``ai_model_id``. ``capture_issue`` is the one writer, so it names the model through the
shared naming door; a ref the catalog cannot name is kept as given.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.catalog.manager import ai_catalog_manager
from matrx_ai.ops import issue_capture, issue_registry

MODEL_ID = "9f6c69bc-768f-4232-a30b-12b78bc9557d"


async def _capture(monkeypatch: pytest.MonkeyPatch, model: str) -> dict[str, Any]:
    created: list[dict[str, Any]] = []
    detached: list[Any] = []

    class _OpsIssueEvent:
        @classmethod
        async def create(cls, **payload: Any) -> None:
            created.append(payload)

    async def _get_issue_class(_key: str) -> dict[str, Any]:
        return {"id": "issue-class-id", "is_active": True}

    monkeypatch.setattr(issue_capture, "get_model", lambda _name: _OpsIssueEvent)
    monkeypatch.setattr(issue_registry, "get_issue_class", _get_issue_class)
    monkeypatch.setattr("matrx_utils.detached_task", lambda coro, *, name: detached.append(coro))
    await issue_capture.capture_issue(
        "groq.structured_output_invalid",
        error_type="structured_output_invalid",
        provider="groq",
        model=model,
        organization_id="organization-id",
        was_recovered=True,
    )
    await detached.pop()
    assert len(created) == 1
    return created[0]


@pytest.mark.asyncio
async def test_a_catalog_id_is_recorded_as_the_model_name(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        ai_catalog_manager,
        "canonical_model_name",
        lambda ref: "openai/gpt-oss-20b" if ref == MODEL_ID else None,
    )
    row = await _capture(monkeypatch, MODEL_ID)
    assert row["model"] == "openai/gpt-oss-20b"


@pytest.mark.asyncio
async def test_a_ref_the_catalog_cannot_name_is_kept(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(ai_catalog_manager, "canonical_model_name", lambda ref: None)
    monkeypatch.setattr("matrx_ai.catalog.host_catalog.get_runtime_model", lambda ref: None)
    row = await _capture(monkeypatch, "some-unlisted-model")
    assert row["model"] == "some-unlisted-model"
