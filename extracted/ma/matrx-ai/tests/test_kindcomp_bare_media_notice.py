"""A kind-component save that writes bare <img>/<video>/<audio>/<iframe> gets ONE line on its tool
result (never a refusal): the compiler converts them to the kit at render, and the author should
write the kit piece. Literal data: images are allowed by the rulebook and never counted."""

from __future__ import annotations

from contextlib import asynccontextmanager
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

from matrx_utils.source_guard import stable_source

import pytest

from matrx_ai import _ext
from matrx_ai.tools.implementations import kind_component as kc
from matrx_ai.tools.implementations import kind_layer
from matrx_ai.tools.implementations.kind_shared import bare_media_notices, bare_media_tag_count
from matrx_ai.tools.kinds.kind_components import KindComponentUpdateResult
from matrx_ai.tools.models import ToolContext, ToolResult

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
    for fn in (kc._kindcomp_update_code_save, kc._kindcomp_patch_code_save, kind_layer.layer_create):
        assert "model_notices=component_save_notices(" in stable_source(fn), fn.__name__


@pytest.mark.asyncio
async def test_creating_a_shared_component_tells_the_model(monkeypatch: pytest.MonkeyPatch) -> None:
    """The create door joins the notice to its default-replacement lines: both reach the model."""
    kind = SimpleNamespace(id=uuid4(), kind="post_idea", organization_id=str(uuid4()))
    incumbent = SimpleNamespace(id=uuid4(), source="db", component_key="old_card")

    class FakeKindComponent:
        @classmethod
        def filter(cls, **_filters):
            return SimpleNamespace(all=AsyncMock(return_value=[]))

        update_where = AsyncMock(return_value=[])
        create_item = AsyncMock(return_value=SimpleNamespace(id=uuid4(), semver="1.0.0", version=1))

    monkeypatch.setattr(kc, "_refuse_broken_source", AsyncMock(return_value=(None, True)))
    monkeypatch.setattr(kc, "resolve_kind", AsyncMock(return_value=(kind, None)))
    monkeypatch.setattr(kc, "ensure_can_edit_kind", AsyncMock(return_value=None))
    monkeypatch.setattr(kc, "get_db_model", lambda _name: FakeKindComponent)
    monkeypatch.setattr(kc, "_live_defaults", AsyncMock(return_value=[incumbent]))

    result = await kc._kindcomp_create_component_save(
        {"kind": "post_idea", "component_key": "post_idea_card", "component_source": BARE},
        ToolContext(call_id=str(uuid4()), tool_name="kindcomp_create_component", user_id=str(uuid4())),
    )

    assert result.success is True, result.error
    assert result.model_notices == [kc._replaced_default_line(incumbent), *bare_media_notices(BARE)]


@pytest.mark.asyncio
async def test_creating_a_layer_tells_the_model(monkeypatch: pytest.MonkeyPatch) -> None:
    """A target=mine/organization create is a write tool too: it answers with the same notice."""

    @asynccontextmanager
    async def fake_as_the_person():
        yield

    async def no_rows(_slug, _audience):
        return []

    audience = SimpleNamespace(
        label="your own view",
        target="mine",
        organization_id=uuid4(),
        user_id=str(uuid4()),
        fields=lambda: {"user_id": "u"},
    )
    Layer = SimpleNamespace(create_item=AsyncMock(return_value=SimpleNamespace(id=uuid4(), semver="1.0.0")))
    monkeypatch.setattr(kind_layer, "audience_for", lambda _args, _ctx: (audience, None))
    monkeypatch.setattr(kind_layer, "list_layer_rows", no_rows)
    monkeypatch.setattr(kind_layer, "get_db_model", lambda _name: Layer)
    monkeypatch.setattr(kind_layer, "as_the_person", fake_as_the_person)
    monkeypatch.setattr(kind_layer, "_kind_registered_anywhere", AsyncMock(return_value=True))

    result = await kind_layer.layer_create(
        {"kind": "post_idea", "component_key": "post_idea_card", "component_source": BARE},
        ToolContext(call_id=str(uuid4()), tool_name="kindcomp_create_component"),
        compile_checked=True,
    )

    assert result.success is True, result.error
    assert result.model_notices == bare_media_notices(BARE)


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
