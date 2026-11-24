"""A free-tier refusal fails its stage but is never filed as an incident.

Live 2026-11-16 21:09-21:12 UTC: a free account's podcast filed every refused video and voice stage as
``agent_run_stage_failed`` ("veo-3.1-fast-generate-preview needs a paid plan. Upgrade to use it. Not run.").
The ceiling worked as designed; the person saw the sentence with its upgrade door. A real stage failure,
or a refusal mixed with a real failure, is still filed.
"""

from __future__ import annotations

import asyncio
from typing import Any

import pytest

from matrx_ai.agent_runners import _checkpoint
from matrx_ai.providers.free_tier_models import FreeTierModelRefusedError, is_free_tier_refusal

OLD = "veo-3.1-fast-generate-preview needs a paid plan. Upgrade to use it. Not run."
NEW = "This needs a paid plan. Upgrade to use it. Not run."


@pytest.fixture
def captured(monkeypatch) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    async def fake_capture(exc: BaseException, *, kind: str, **fields: Any) -> None:
        rows.append({"kind": kind, **fields})

    import matrx_connect.streaming.error_capture as ec

    monkeypatch.setattr(ec, "capture_error", fake_capture)
    return rows


@pytest.mark.parametrize(
    "error",
    [
        OLD,
        NEW,
        "This needs a paid plan. Sign up free to use it. Not run.",
        f"{OLD} (fallback model also failed: {OLD})",
        {"message": NEW},
        {"error": "free_tier_model_refused"},
    ],
)
def test_a_refusal_is_not_filed(captured, error) -> None:
    asyncio.run(_checkpoint._capture_stage_failure("run", "podcast", "u", "video_0", error=error))
    assert captured == []


def test_a_raised_refusal_is_not_filed(captured) -> None:
    exc = FreeTierModelRefusedError(model_name="veo", tier="free", user_id="u")
    asyncio.run(_checkpoint._capture_stage_failure("run", "podcast", "u", "video_0", exc=exc))
    assert captured == []


@pytest.mark.parametrize(
    "error",
    [
        "agent returned a non-URL output (not a rendered asset): 'oops'",
        f"{OLD} (fallback model also failed: RuntimeError: provider 500)",
        "needs a paid plan",
    ],
)
def test_a_real_failure_is_still_filed(captured, error) -> None:
    asyncio.run(_checkpoint._capture_stage_failure("run", "podcast", "u", "video_0", error=error))
    assert [row["kind"] for row in captured] == ["agent_run_stage_failed"]


def test_classifier() -> None:
    assert is_free_tier_refusal(NEW)
    assert not is_free_tier_refusal("")
    assert not is_free_tier_refusal(None)
    assert not is_free_tier_refusal(RuntimeError("boom"))
