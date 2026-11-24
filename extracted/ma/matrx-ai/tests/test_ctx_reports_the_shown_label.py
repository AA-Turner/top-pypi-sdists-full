"""The `context` tool names an object the way the manifest does — never by its key.

Conversation d1e4226e… (2026-11-12): a batch read of 11 attached PDFs came back labeled
"Resource File 0495ccdb 8c25 …" because ctx.py read ``obj.label`` raw (a title made of the
key) while the manifest renders the host's ``shown_label()`` (the file's own name from its
descriptor). The read door and the manifest must say the same name.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any
from unittest.mock import MagicMock, patch

from matrx_ai.tools.implementations.ctx import ctx_get
from matrx_ai.tools.models import ToolContext

KEY = "resource_file_0495ccdb-8c25-4845-ac0b-b8c229779932"
KEY_TITLE = "Resource File 0495ccdb 8c25 4845 Ac0b B8c229779932"
NAME = "Action of Incorporator.pdf"


def _obj(*, descriptor: Any, lazy: bool, content: str = "") -> SimpleNamespace:
    return SimpleNamespace(
        key=KEY,
        type=SimpleNamespace(value="json"),
        label=KEY_TITLE,
        shown_label=lambda: (NAME, True),
        summary_agent_id=None,
        descriptor=descriptor,
        source=SimpleNamespace(kind="file", id="0495ccdb") if lazy else None,
        is_lazy_source=lambda: lazy,
        content=content,
        content_as_str=lambda: content,
    )


async def _get(obj: Any, args: dict[str, Any], **ext: Any) -> Any:
    def _get_ext(name: str) -> Any:
        if name == "load_manifest_from_ctx":
            m = MagicMock()
            m.get.return_value = obj
            m.all.return_value = [obj]
            return lambda _app: m
        return ext[name]

    with (
        patch("matrx_ai.context.app_context.get_app_context", return_value=MagicMock(user_id="u")),
        patch("matrx_ai._ext.get_ext", side_effect=_get_ext),
        patch("matrx_ai._ext.has_ext", side_effect=lambda name: name in ext),
    ):
        return await ctx_get(
            args, ToolContext(call_id="c", user_id="u", conversation_id="conv", emitter=None)
        )


async def test_summary_of_a_described_file_carries_the_file_name() -> None:
    desc = SimpleNamespace(summary="Referenced file, 1 page.", primary_size_chars=1500)
    result = await _get(_obj(descriptor=desc, lazy=True), {"key": KEY, "mode": "summary"})
    assert result.success is True
    assert result.output.label == NAME


async def test_page_read_of_a_lazy_file_carries_the_file_name() -> None:
    async def materialize(source, *, mode, offset, chars, user_id):
        return SimpleNamespace(
            representation="raw", text="ACTION OF INCORPORATOR", offset=0, total_chars=22,
            has_more=False, next_offset=None, page_range=None,
        )

    result = await _get(
        _obj(descriptor=None, lazy=True),
        {"key": KEY, "mode": "page", "chars": 100},
        materialize_context_source=materialize,
    )
    assert result.success is True, result.error
    assert result.output.label == NAME


async def test_inline_read_carries_the_file_name() -> None:
    result = await _get(_obj(descriptor=None, lazy=False, content="whole text"), {"key": KEY})
    assert result.success is True, result.error
    assert result.output.label == NAME


async def test_an_object_without_shown_label_keeps_its_label() -> None:
    obj = _obj(descriptor=None, lazy=False, content="x")
    del obj.shown_label
    obj.label = "Notes"
    result = await _get(obj, {"key": KEY})
    assert result.output.label == "Notes"
