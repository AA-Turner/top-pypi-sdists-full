"""The kindcomp write tools append the host's preview (screenshots + findings) to a successful save —
and never anything else: no host seam, a failed save, a layer target or a knob that is off leave the
save result exactly as it was, and a preview that blows up is reported beside the save, never instead."""

from __future__ import annotations

import pytest

from matrx_ai import _ext
from matrx_ai.tools.implementations import kind_component as kc
from matrx_ai.tools.kinds.kind_components import KindComponentUpdateResult
from matrx_ai.tools.models import ToolError, ToolResult


def _saved() -> ToolResult:
    return ToolResult(
        success=True,
        output=KindComponentUpdateResult(component_id="c-1", updated_sections=["component_source"], message="Updated 1 section(s)."),
    )


@pytest.fixture
def seam(monkeypatch: pytest.MonkeyPatch):
    calls: list[str] = []
    state: dict = {"reply": None, "raises": None}

    async def preview(*, component_id: str, ctx):
        calls.append(component_id)
        if state["raises"]:
            raise state["raises"]
        return state["reply"]

    monkeypatch.setitem(_ext._registry, kc.PREVIEW_EXT_KEY, preview)
    return calls, state


@pytest.mark.asyncio
async def test_knob_on_the_save_result_carries_the_screenshots_and_findings(seam) -> None:
    calls, state = seam
    state["reply"] = {
        "kind": "image_ref_list",
        "items": [{"kind": "image_ref", "media_ref": {"file_id": "f-1"}}],
        "count": 1,
        "details": {"verdict": "fail", "findings": [{"code": "empty_render", "message": "Nothing rendered"}]},
    }
    out = await kc._with_auto_preview(_saved(), {"component_id": "c-1"}, ctx=None)
    assert calls == ["c-1"]
    assert out.success is True
    assert out.output["kind"] == "image_ref_list"
    assert out.output["details"]["findings"][0]["code"] == "empty_render"
    assert out.output["details"]["save"]["component_id"] == "c-1"


@pytest.mark.asyncio
async def test_knob_off_leaves_the_save_result_untouched(seam) -> None:
    calls, state = seam
    state["reply"] = None  # the host answers None when content_ir.shape_preview_on_save is off
    saved = _saved()
    out = await kc._with_auto_preview(saved, {"component_id": "c-1"}, ctx=None)
    assert calls == ["c-1"]
    assert out is saved


@pytest.mark.asyncio
async def test_a_preview_that_raises_is_reported_beside_the_save_never_instead(seam) -> None:
    _calls, state = seam
    state["raises"] = RuntimeError("scraper down")
    out = await kc._with_auto_preview(_saved(), {"component_id": "c-1"}, ctx=None)
    assert out.success is True
    assert out.output["save"]["component_id"] == "c-1"
    assert "scraper down" in out.output["preview"]["findings"][0]["message"]


@pytest.mark.asyncio
async def test_failed_saves_and_layer_targets_are_never_previewed(seam) -> None:
    calls, _state = seam
    failed = ToolResult(success=False, error=ToolError(error_type="validation", message="refused"))
    assert await kc._with_auto_preview(failed, {"component_id": "c-1"}, ctx=None) is failed
    saved = _saved()
    assert await kc._with_auto_preview(saved, {"component_id": "c-1", "target": "mine"}, ctx=None) is saved
    assert calls == []


@pytest.mark.asyncio
async def test_no_host_seam_means_no_preview(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delitem(_ext._registry, kc.PREVIEW_EXT_KEY, raising=False)
    saved = _saved()
    assert await kc._with_auto_preview(saved, {"component_id": "c-1"}, ctx=None) is saved
