"""A kind-component save that writes bare <img>/<video>/<audio>/<iframe> gets ONE line on its tool
result (never a refusal): the compiler converts them to the kit at render, and the author should
write the kit piece. Literal data: images are allowed by the rulebook and never counted."""

from __future__ import annotations

import inspect

import pytest

from matrx_ai import _ext
from matrx_ai.tools.implementations import kind_component as kc
from matrx_ai.tools.implementations.kind_shared import bare_media_notices, bare_media_tag_count
from matrx_ai.tools.kinds.kind_components import KindComponentUpdateResult
from matrx_ai.tools.models import ToolResult

BARE = """export default function C({ data }) {
  return <div>
    <img src={data.photo} className="h-64 object-cover" alt="x" />
    <video controls><source src={data.clip} /></video>
    <audio src={data.song} />
    <iframe src="https://www.youtube.com/embed/abc" title="t"></iframe>
    <img src="data:image/png;base64,AAAA" alt="dot" />
    <svg viewBox="0 0 1 1"><image href={data.u} /></svg>
  </div>;
}"""


def test_counts_bare_media_but_not_data_images_or_svg_image() -> None:
    assert bare_media_tag_count(BARE) == 4
    assert bare_media_tag_count('<img src={`data:image/svg+xml;utf8,${x}`} />') == 0
    assert bare_media_tag_count("<KindImage image={x} alt='a' /> <imgs /> <images />") == 0


def test_notice_is_one_line_naming_the_kit_and_absent_when_clean() -> None:
    (line,) = bare_media_notices(BARE)
    assert line.startswith("4 bare media tags are converted to the kit automatically at render")
    assert "KindImage/KindVideo/KindAudio/KindEmbed" in line
    assert bare_media_notices("<img src={u} />")[0].startswith("1 bare media tag is converted")
    assert bare_media_notices("<KindImage image={u} />") == []
    assert bare_media_notices(None) == []


def test_every_write_tool_attaches_the_notice() -> None:
    for fn in (kc._kindcomp_create_component_save, kc._kindcomp_update_code_save, kc._kindcomp_patch_code_save):
        assert "model_notices=bare_media_notices(" in inspect.getsource(fn), fn.__name__


@pytest.mark.asyncio
async def test_the_automatic_preview_keeps_the_notice(monkeypatch: pytest.MonkeyPatch) -> None:
    async def preview(*, component_id: str, ctx):
        return {"verdict": "ok", "findings": []}

    monkeypatch.setitem(_ext._registry, kc.PREVIEW_EXT_KEY, preview)
    saved = ToolResult(
        success=True,
        model_notices=bare_media_notices(BARE),
        output=KindComponentUpdateResult(component_id="c-1", updated_sections=["component_source"], message="ok"),
    )
    out = await kc._with_auto_preview(saved, {}, ctx=None)  # type: ignore[arg-type]
    assert out.model_notices == bare_media_notices(BARE)
    assert out.output["preview"]["verdict"] == "ok"
