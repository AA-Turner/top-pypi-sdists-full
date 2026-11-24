"""A kindcomp save handed back with its automatic preview is judged by the SAVE, not the envelope.

system_error 2026-11-01..02: ~650 rows a day of ``tool_output_contract_drift`` +
``tool_result_kind_missing`` for kindcomp_create_component / kindcomp_patch_code. The save was a
valid ``kind_component_create_result``; ``_with_auto_preview`` wrapped it in an ``image_ref_list``
so the model sees screenshots, and the executor judged the wrapper. RED before
``typed_result_inside_preview_envelope`` existed (ImportError) and before the executor used it.
"""

from __future__ import annotations

import pytest

from matrx_ai.tools.executor import typed_result_inside_preview_envelope
from matrx_ai.tools.implementations import kind_component
from matrx_ai.tools.kinds import result_kind_slug
from matrx_ai.tools.kinds.kind_components import KindComponentCreateResult
from matrx_ai.tools.models import ToolResult


def _save_result() -> ToolResult:
    return ToolResult(
        success=True,
        tool_name="kindcomp_create_component",
        output=KindComponentCreateResult(component_id="ff66ff66-0000-4000-8000-000000000000", kind="flashcard_set"),
    )


@pytest.mark.parametrize(
    "preview",
    [
        {"kind": "image_ref_list", "items": [], "count": 0, "details": {"findings": []}},
        {"verdict": "unknown", "findings": [{"code": "preview_unavailable"}]},
    ],
)
async def test_the_envelope_the_preview_makes_yields_the_declared_save(monkeypatch, preview) -> None:
    async def fake_preview(*, component_id: str, ctx) -> dict:
        return dict(preview)

    monkeypatch.setattr("matrx_ai._ext.has_ext", lambda name: name == kind_component.PREVIEW_EXT_KEY)
    monkeypatch.setattr("matrx_ai._ext.get_ext", lambda name: fake_preview)

    wrapped = await kind_component._with_auto_preview(_save_result(), {}, ctx=None)  # type: ignore[arg-type]
    assert not isinstance(wrapped.output, KindComponentCreateResult), "the preview must have wrapped the save"

    save = typed_result_inside_preview_envelope(wrapped.output)
    assert save is not None
    assert save.get("__kind") == result_kind_slug("kindcomp_create_component")
    assert save["component_id"] == "ff66ff66-0000-4000-8000-000000000000"


def test_a_plain_result_is_not_an_envelope() -> None:
    assert typed_result_inside_preview_envelope({"kind": "image_ref_list", "items": []}) is None
    assert typed_result_inside_preview_envelope({"save": "text", "preview": {}}) is None
    assert typed_result_inside_preview_envelope({"save": {}, "preview": {}, "extra": 1}) is None
    assert typed_result_inside_preview_envelope("text") is None
