"""Every attached entity reaches the model with its source identity: kind + name + id.

Real test PB-05 (full run 2026-10-18 08:07Z, conversation 66273ee6…): an attached table row
arrived as a bare ``id: … | gate: Gate 3 | …`` line and a task as an anonymous ``<task>``
block, so the model could only cite them as "pasted in message" — the table's name and the
task's title were lost as SOURCES, while the page kept its url/title. The law: every
structured attachment block opens with ``<attachment kind=… name=… id=…>`` so the model can
name what it cites. Sibling of ``test_attachment_every_kind_arrives.py`` (files).
"""

from __future__ import annotations

import re
from types import SimpleNamespace

import pytest

from matrx_ai.config.structured_input_config import (
    ListInputContent,
    NotesInputContent,
    TableInputContent,
    TaskInputContent,
)

ROW_ID = "d1a2fd40-0a7f-4e5a-840d-f2b5df794875"
TABLE_ID = "5b0c7a1e-2f61-4d3b-9a0e-3c8f1d2e4a77"
LIST_ID = "8e2d4c6a-1b3f-4a5e-9c7d-0f1e2d3c4b5a"
ITEM_ID = "3a4b5c6d-7e8f-4a1b-8c2d-9e0f1a2b3c4d"
TASK_ID = "244bd30d-27c2-4929-9821-7237bf371892"
NOTE_ID = "c208c61b-0cc2-4b78-a8f4-f19d29604795"


@pytest.fixture
def host(monkeypatch):
    """A signed-in request and a bookmark resolver answering like the reference orchestrator."""
    from matrx_connect.context import app_context

    from matrx_ai import _ext

    ctx = SimpleNamespace(user_id="87a6e699-3622-4869-8843-d0867456c0dd", metadata={})
    monkeypatch.setattr(app_context, "try_get_app_context", lambda: ctx)

    async def resolve_bookmarks(bookmarks, *, user_id):
        out = []
        for bm in bookmarks:
            if bm.get("type") == "table_row":
                out.append(f"id: {bm['row_id']} | gate: Gate 3 | origin: Lodi")
            elif bm.get("type") == "list_item":
                out.append("Gate 3: north apron")
        return out

    monkeypatch.setitem(_ext._registry, _ext._BOOKMARK_RESOLVER_KEY, resolve_bookmarks)
    return ctx


def _opening(text: str) -> dict[str, str]:
    m = re.match(r'\s*<attachment ([^>]*)>', text)
    assert m, f"block does not open with its source identity:\n{text[:300]}"
    return dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))


async def test_table_row_names_its_table(host):
    block = TableInputContent(
        bookmarks=[{"type": "table_row", "table_id": TABLE_ID, "row_id": ROW_ID, "table_name": "Dock gate assignments"}]
    )
    await block.resolve()
    text = block.to_anthropic()["text"]
    ident = _opening(text)
    assert ident["kind"] == "table_row"
    assert ident["name"] == "Dock gate assignments"
    assert ident["id"] == ROW_ID and ident["table_id"] == TABLE_ID
    assert "gate: Gate 3" in text


async def test_list_item_names_its_list(host):
    block = ListInputContent(
        bookmarks=[{"type": "list_item", "list_id": LIST_ID, "item_id": ITEM_ID, "list_name": "Yard aprons"}]
    )
    await block.resolve()
    ident = _opening(block.to_anthropic()["text"])
    assert ident["kind"] == "list_item" and ident["name"] == "Yard aprons" and ident["id"] == ITEM_ID


async def test_task_names_its_title(host):
    block = TaskInputContent(
        task_ids=[{"mode": "snapshot", "id": TASK_ID, "title": "Re-probe Lodi pallets", "description": "Re-probe every Lodi pallet."}]
    )
    await block.resolve()
    text = block.to_anthropic()["text"]
    ident = _opening(text)
    assert ident == {"kind": "task", "name": "Re-probe Lodi pallets", "id": TASK_ID}
    assert "Re-probe every Lodi pallet." in text


async def test_note_names_its_label(host):
    block = NotesInputContent(
        note_ids=[{"mode": "snapshot", "id": NOTE_ID, "label": "Alder Creek dock memo", "content": "The cold-room key is held by Imelda Rask."}]
    )
    await block.resolve()
    ident = _opening(block.to_anthropic()["text"])
    assert ident == {"kind": "note", "name": "Alder Creek dock memo", "id": NOTE_ID}


async def test_every_bookmarked_item_keeps_its_own_identity(host):
    """Two rows in one block: each opens with its own identity, none merged or dropped."""
    other = "aaaaaaaa-0a7f-4e5a-840d-f2b5df794875"
    block = TableInputContent(
        bookmarks=[
            {"type": "table_row", "table_id": TABLE_ID, "row_id": ROW_ID, "table_name": "Dock gate assignments"},
            {"type": "table_row", "table_id": TABLE_ID, "row_id": other, "table_name": "Dock gate assignments"},
        ]
    )
    await block.resolve()
    text = block.to_anthropic()["text"]
    assert text.count('<attachment kind="table_row"') == 2
    assert ROW_ID in text and other in text


# ── names the composer left out are resolved server-side, as the person, in ONE batch ──

AGENT_ID = "3d9d94fc-2867-4477-93b7-e7ac6be6a01e"
PROJECT_ID = "6f1e2d3c-4b5a-4968-8776-655443322110"


@pytest.fixture
def names(host, monkeypatch):
    """A host name resolver that records every call (to prove one batch per attachment set)."""
    from matrx_ai import _ext

    calls: list[list[tuple[str, str]]] = []
    known = {
        ("table", TABLE_ID): "Dock gate assignments",
        ("agent", AGENT_ID): "Alder Creek Receiving Desk",
        ("project", PROJECT_ID): "Lodi intake",
    }

    async def resolve_source_names(pairs, *, user_id):
        calls.append(list(pairs))
        assert user_id == host.user_id, "names are read as the person"
        return {p: known[p] for p in pairs if p in known}

    monkeypatch.setitem(_ext._registry, "source_name_resolver", resolve_source_names)
    host.calls = calls
    return host


def _stored(ctx) -> list[dict]:
    return list((ctx.metadata.get("request_snapshot_metadata") or {}).get("media_notices") or [])


async def test_a_nameless_row_gets_its_table_name_from_the_server(names):
    other = "aaaaaaaa-0a7f-4e5a-840d-f2b5df794875"
    block = TableInputContent(
        bookmarks=[
            {"type": "table_row", "table_id": TABLE_ID, "row_id": ROW_ID},
            {"type": "table_row", "table_id": TABLE_ID, "row_id": other},
        ]
    )
    await block.resolve()
    text = block.to_anthropic()["text"]
    assert text.count('name="Dock gate assignments"') == 2
    assert names.calls == [[("table", TABLE_ID)]], "one batched read for the whole set"


@pytest.mark.parametrize(
    "factory,kind,ident,name",
    [
        (lambda: __import__("matrx_ai.config.structured_input_config", fromlist=["x"]).AgentInputContent(agent_ids=[AGENT_ID]), "agent", AGENT_ID, "Alder Creek Receiving Desk"),
        (lambda: __import__("matrx_ai.config.structured_input_config", fromlist=["x"]).ProjectInputContent(project_ids=[PROJECT_ID]), "project", PROJECT_ID, "Lodi intake"),
    ],
    ids=["agent", "project"],
)
async def test_a_record_reference_names_its_record(names, factory, kind, ident, name):
    block = factory()
    await block.resolve()
    text = block.to_anthropic()["text"]
    assert _opening(text) == {"kind": kind, "name": name, "id": ident}
    assert "```matrx" in text, "the reference fence itself is kept for the host to resolve"


async def test_a_refused_name_keeps_kind_and_id_and_says_so(names):
    unknown = "bbbbbbbb-2867-4477-93b7-e7ac6be6a01e"
    from matrx_ai.config.structured_input_config import AgentInputContent

    block = AgentInputContent(agent_ids=[unknown])
    await block.resolve()
    ident = _opening(block.to_anthropic()["text"])
    assert ident["kind"] == "agent" and ident["id"] == unknown
    assert ident.get("name", "") == "" and ident.get("name_unavailable"), "never a silent empty name"
    (notice,) = _stored(names)
    assert unknown in notice["system_message"]


async def test_no_resolver_on_the_host_is_a_notice_not_a_blank(host):
    from matrx_ai.config.structured_input_config import AgentInputContent

    block = AgentInputContent(agent_ids=[AGENT_ID])
    await block.resolve()
    ident = _opening(block.to_anthropic()["text"])
    assert ident.get("name_unavailable") and _stored(host)


async def test_a_nameless_task_is_named_by_the_server(names, monkeypatch):
    from matrx_ai import _ext

    async def resolve_source_names(pairs, *, user_id):
        return {("task", TASK_ID): "Re-probe Lodi pallets"} if ("task", TASK_ID) in pairs else {}

    monkeypatch.setitem(_ext._registry, "source_name_resolver", resolve_source_names)
    block = TaskInputContent(task_ids=[{"mode": "snapshot", "id": TASK_ID, "description": "Re-probe every Lodi pallet."}])
    await block.resolve()
    assert _opening(block.to_anthropic()["text"])["name"] == "Re-probe Lodi pallets"


# ── every MEDIA block (image, audio, video, document) names its file on every provider ──
# PB-05 defect 54 (live build 62046bc5): the photo arrived as a bare image part, so the model
# cited "whiteboard image (no file name)" instead of IMG_2291.jpg. Providers have no title on an
# image part, so the identity rides a SEPARATE text part right before it — never the person's text.

import base64 as _b64

from matrx_ai.config import TextContent as _Text
from matrx_ai.config import UnifiedMessage as _Msg
from matrx_ai.config.media_config import DocumentContent as _Doc
from matrx_ai.config.media_config import ImageContent as _Img

IMG_ID = "4e01f58b-704a-4ac1-86f5-11b32c5cbf92"
PDF_ID = "fd6656e3-a078-4c92-9544-5f987161ab47"
PERSON = "The Lodi Orchards Cooperative delivery is at the door. Receiving line, please."


def _media_message() -> _Msg:
    return _Msg(
        role="user",
        content=[
            _Text(text=PERSON),
            _Img(base64_data=_b64.b64encode(b"\xff\xd8\xff\xe0jpeg").decode(), mime_type="image/jpeg",
                 file_id=IMG_ID, metadata={"file_name": "IMG_2291.jpg"}),
            _Doc(base64_data=_b64.b64encode(b"%PDF-1.4 x").decode(), mime_type="application/pdf",
                 file_id=PDF_ID, metadata={"file_name": "inbound-handling-procedures.pdf"}),
        ],
    )


def _wire_parts(provider: str) -> list[dict]:
    msg = _media_message()
    if provider == "anthropic":
        return msg.to_anthropic_blocks()
    if provider == "google":
        return msg.to_google_content()["parts"]
    items = msg.to_openai_items_modified()
    items = items if isinstance(items, list) else [items]
    return [p for it in items for p in (it.get("content") or [it])]


def _text_of(part: dict) -> str | None:
    if part.get("type") in ("text", "input_text"):
        return part.get("text")
    if "text" in part and len(part) == 1:
        return part["text"]
    return None


def _is_media(part: dict) -> bool:
    return part.get("type") in ("image", "document", "input_image", "input_file") or "inlineData" in part


@pytest.mark.parametrize("provider", ["anthropic", "openai", "google"])
def test_every_media_block_is_preceded_by_its_file_identity(provider):
    parts = _wire_parts(provider)
    media_at = [i for i, p in enumerate(parts) if _is_media(p)]
    assert len(media_at) == 2, parts
    for i, (name, fid) in zip(media_at, [("IMG_2291.jpg", IMG_ID), ("inbound-handling-procedures.pdf", PDF_ID)]):
        label = _text_of(parts[i - 1]) if i > 0 else None
        assert label and f'name="{name}"' in label and f'id="{fid}"' in label, (
            f"{provider}: media part {i} has no file identity right before it: {parts[i - 1] if i else None}"
        )
    person = [t for t in (_text_of(p) for p in parts) if t and PERSON in t]
    assert person == [PERSON], f"{provider}: the person's text was changed: {person}"


async def test_a_nameless_image_is_named_from_its_file_id_once(names, monkeypatch):
    from matrx_ai import _ext
    from matrx_ai.processing.media_fallback import preprocess_unsupported_media
    from matrx_ai.config import MessageList

    calls = []

    async def resolve_source_names(pairs, *, user_id):
        calls.append(list(pairs))
        return {("file", IMG_ID): "IMG_2291.jpg"}

    monkeypatch.setitem(_ext._registry, "source_name_resolver", resolve_source_names)
    img = _Img(base64_data="eA==", mime_type="image/jpeg", file_id=IMG_ID)
    ml = MessageList(_messages=[_Msg(role="user", content=[_Text(text=PERSON), img])])
    await preprocess_unsupported_media(ml, "anthropic_chat", model_name="claude-haiku-5-5", model_supports_vision=True)
    assert img.metadata.get("file_name") == "IMG_2291.jpg"
    assert calls == [[("file", IMG_ID)]]
